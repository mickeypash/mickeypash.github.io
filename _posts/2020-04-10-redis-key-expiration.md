---
layout: post
title: Redis Key Expiration
excerpt: There are only two hard things in Computer Science: cache invalidation and naming things.
---

![redis]({{ site.baseurl }}/images/redis.png)

Not too long ago I was tasked with looking into a performance issue with an internal service using Redis.
At the time I had no exposure to it after some time I identified that the issue might be related to issues with key expiration. As part of my investigation I found this great talk by [@antirez](https://twitter.com/antirez), the creator of Redis, on [The Evolution of Redis Key Expiration Algorithms](https://www.youtube.com/watch?v=SyQTG0hXPxY). This is a short post about my learnings, with links to relevant points in the C code.

## Intro
Let's start with the basics, Redis stands for Remote Dictionary Server, as the name suggests it is a distributed, in-memory key-value database. It uses a hash table, called `dict` as it's core data structure, where values can be stored as a linked list.
One of the many features it provides is [EXPIRE](https://redis.io/commands/expire), which sets a timeout for a given key. In other words it allows users to specify how long the keys shoul exist for before being delete. 

In order to make this happen Redis needs to store the expiration information with a `key`. 

The obvious approach is to have the existing data structure support expiry for each `key`. However, this adds unnecessary memory overhead, if only a small subset of keys are set to expire. 

The alternative solution is to have a second hash-table that stores the [expiry information](https://github.com/antirez/redis/blob/b73d87f5e59ae68a2b901fe5a158d6e22840214c/src/server.c#L2747). The image below attempts to illustrate this.

![redis]({{ site.baseurl }}/images/redis-key-expire.png)


The time at which a key will expire is set at a unix timestamp.
To further conserve space, Redis reuses the pointer for the `key` from the primary `dict`, in terms of the expiry, the author also tries to optimize by storing a unix timestamp as a pointer.
To conserve space it gets stored as a pointer.

This means that if there are no `expires`, the expiration hastable is empty.
- The keys are shared so there is no waisted memory
- The expiration information gets stored in place of the pointer for the value object in the hashtable

How to evict keys:
1. Passive expiration
- If Redis receives the command `GET('foo')`
- Down the call chain it calls [`lookUpKey`](https://github.com/antirez/redis/blob/30724986659c6845e9e48b601e36aa4f4bca3d30/src/db.c#L55)
- This in turn calls `expireIfNeeded` which ensures that if the time has passed the key expires
- It returns a [`NULL` to the caller if has expired](https://github.com/antirez/redis/blob/30724986659c6845e9e48b601e36aa4f4bca3d30/src/db.c#L278)


2. Active expiration

In the second approach we apply random sampling to the `expires` table.
We sample 10 times per second and test 20 random keys. If the expire time is less than the current timestamp i can evict the key.

However as the number of keys to be expired becomes smaller we are simply burning CPU.

The less keys are expired the more CPU we burn.

After we find less than given percentage of keys that are expired we stop the expire cycle. In the case of Redis this is [25%](https://github.com/antirez/redis/blob/b73d87f5e59ae68a2b901fe5a158d6e22840214c/src/expire.c#L119)

When Twitter upgraded from v2.8 (quite an old version) to v6.0 they noticed a regression.
In their case where 25% of keys that were expired was not an acceptable default.
That's why an [`effort` configuration was introduced](https://github.com/antirez/redis/commit/84b01f63dbe28d5541e09313d35deacf4344ab16)


New approach


[Using a Radix tree](https://en.wikipedia.org/wiki/Radix_tree)

Some people have a usecase where they want to use Redis as a timer.
What they would do is listen to the Keyspace notification for [`expired` events](https://github.com/antirez/redis/blob/b73d87f5e59ae68a2b901fe5a158d6e22840214c/src/expire.c#L65)



Redis docs:

Specifically this is what Redis does 10 times per second:

1. Test 20 random keys from the set of keys with an associated expire.
2. Delete all the keys found expired.
3. If more than 25% of keys were expired, start again from step 1.

However imagine you have a million keys that are "forgotten" by the application code.
That means they won't be accessed therefore never expired if we only relied on this approach.


To check for an `expire` he checks the "expire hashtable" for a an entry with that key



[KeyDB - Rethinking the Redis Key EXPIRE](https://docs.keydb.dev/blog/2019/10/21/blog-post/)

[CubeDrone Endiannes](https://www.youtube.com/watch?v=LGH3ND0kP4Q)


https://redis.io/commands/expire

https://github.com/antirez/redis/blob/b73d87f5e59ae68a2b901fe5a158d6e22840214c/src/expire.c#L123