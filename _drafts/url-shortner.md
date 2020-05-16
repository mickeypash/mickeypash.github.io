# Building a simple URL shortner

1. Grab a domain, preferrable memorable and short (I went for this [`mickeys.link`](https://mickeys.link) which is **cheap** and somewhat memorable)
2. Create a [new Github repository](https://github.com/new). Would could name it anything. I chose to name it the same as my short link domain `mickeys.link`.
3. Add a single `_redirects` file. This is a [Netlify feautre](https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file). The file sturcture is simple:
    ```
    /lk                https://www.linkedin.com/in/mickeypash/
    /short             http://some-extremely-long-url-that-you-probably-cant-remember.dig.baz.foo.xyz


    /*                 <your-website>
    ```
4. Visit [Netlify](https://app.netlify.com/), do the usual account set up.
5. Create a new site by clicking on [New site from Git](https://app.netlify.com/start)
6. Select the repository from the list. If it's empty simply configure the access to Github.



Note: redirects engine will process the first matching rule it [finds](https://docs.netlify.com/routing/redirects/#rule-processing-order)]
