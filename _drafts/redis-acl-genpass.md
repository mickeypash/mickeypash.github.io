# Using Redis to generate secure passwords

![redis-takeway]

So it's May 12th 2020 and RedisLabs is hosting [RedisConf 2020 Takeaway](https://redislabs.com/blog/redisconf-2020-takeaway-is-almost-here/) a virtual version of their annual conference, this of course is due to the ongoing situation with COVID-19. They built an impressive intreactive experience and announced many cool products, including but not limited to [RedisAI](https://oss.redislabs.com/redisai/), [ReadisGears](https://oss.redislabs.com/redisgears/), [Active-Active Data Replication with Redis Streams](https://events.redislabs.com/sessions/active-active-data-replication-redis-streams-redis-modules/).

One of the major announcements was the earlier release of [Redis 6.0.0 GA](https://raw.githubusercontent.com/antirez/redis/6.0/00-RELEASENOTES). The one change that stood out to me was the was [`ACL GENPASS`](https://redis.io/commands/acl-genpass) which now uses `HMAC-SHA256`


```bash
> ACL GENPASS
"dd721260bfe1b3d9601e7fbab36de6d04e2e67b0ef1c53de59d45950db0dd3cc"

> ACL GENPASS 32
"355ef3dd"

> ACL GENPASS 5
"90"
```

[RFC2104 - HMAC](https://tools.ietf.org/html/rfc2104)
[RFC4231 - HMAC-SHA-224](https://tools.ietf.org/html/rfc4231)


https://github.com/antirez/redis-doc/blob/c0853c162defc400e3fba311dbde2622a29653a4/commands/acl-genpass.md 2 days ago
acl genpass

HMAC-SHA256(seed || c)

/dev/urandom

acl.c
```cpp
 else if (!strcasecmp(sub,"genpass") && (c->argc == 2 || c->argc == 3)) {
    #define GENPASS_MAX_BITS 4096
    char pass[GENPASS_MAX_BITS/8*2]; /* Hex representation. */
    long bits = 256; /* By default generate 256 bits passwords. */

    if (c->argc == 3 && getLongFromObjectOrReply(c,c->argv[2],&bits,NULL)
        != C_OK) return;

    if (bits <= 0 || bits > GENPASS_MAX_BITS) {
        addReplyErrorFormat(c,
            "ACL GENPASS argument must be the number of "
            "bits for the output password, a positive number "
            "up to %d",GENPASS_MAX_BITS);
        return;
    }

    long chars = (bits+3)/4; /* Round to number of characters to emit. */
    getRandomHexChars(pass,chars);
    addReplyBulkCBuffer(c,pass,chars);
```

utils.c
```cpp
/* Generate the Redis "Run ID", a SHA1-sized random number that identifies a
 * given execution of Redis, so that if you are talking with an instance
 * having run_id == A, and you reconnect and it has run_id == B, you can be
 * sure that it is either a different instance or it was restarted. */
void getRandomHexChars(char *p, size_t len) {
    char *charset = "0123456789abcdef";
    size_t j;

    getRandomBytes((unsigned char*)p,len);
    for (j = 0; j < len; j++) p[j] = charset[p[j] & 0x0F];
}
```

utils.c
```cpp
/* Get random bytes, attempts to get an initial seed from /dev/urandom and
 * the uses a one way hash function in counter mode to generate a random
 * stream. However if /dev/urandom is not available, a weaker seed is used.
 *
 * This function is not thread safe, since the state is global. */
void getRandomBytes(unsigned char *p, size_t len) {
    /* Global state. */
    static int seed_initialized = 0;
    static unsigned char seed[64]; /* 512 bit internal block size. */
    static uint64_t counter = 0; /* The counter we hash with the seed. */

    if (!seed_initialized) {
        /* Initialize a seed and use SHA1 in counter mode, where we hash
         * the same seed with a progressive counter. For the goals of this
         * function we just need non-colliding strings, there are no
         * cryptographic security needs. */
        FILE *fp = fopen("/dev/urandom","r");
        if (fp == NULL || fread(seed,sizeof(seed),1,fp) != 1) {
            /* Revert to a weaker seed, and in this case reseed again
             * at every call.*/
            for (unsigned int j = 0; j < sizeof(seed); j++) {
                struct timeval tv;
                gettimeofday(&tv,NULL);
                pid_t pid = getpid();
                seed[j] = tv.tv_sec ^ tv.tv_usec ^ pid ^ (long)fp;
            }
        } else {
            seed_initialized = 1;
        }
        if (fp) fclose(fp);
    }

    while(len) {
        /* This implements SHA256-HMAC. */
        unsigned char digest[SHA256_BLOCK_SIZE];
        unsigned char kxor[64];
        unsigned int copylen =
            len > SHA256_BLOCK_SIZE ? SHA256_BLOCK_SIZE : len;

        /* IKEY: key xored with 0x36. */
        memcpy(kxor,seed,sizeof(kxor));
        for (unsigned int i = 0; i < sizeof(kxor); i++) kxor[i] ^= 0x36;

        /* Obtain HASH(IKEY||MESSAGE). */
        SHA256_CTX ctx;
        sha256_init(&ctx);
        sha256_update(&ctx,kxor,sizeof(kxor));
        sha256_update(&ctx,(unsigned char*)&counter,sizeof(counter));
        sha256_final(&ctx,digest);

        /* OKEY: key xored with 0x5c. */
        memcpy(kxor,seed,sizeof(kxor));
        for (unsigned int i = 0; i < sizeof(kxor); i++) kxor[i] ^= 0x5C;

        /* Obtain HASH(OKEY || HASH(IKEY||MESSAGE)). */
        sha256_init(&ctx);
        sha256_update(&ctx,kxor,sizeof(kxor));
        sha256_update(&ctx,digest,SHA256_BLOCK_SIZE);
        sha256_final(&ctx,digest);

        /* Increment the counter for the next iteration. */
        counter++;

        memcpy(p,digest,copylen);
        len -= copylen;
        p += copylen;
    }
}
```