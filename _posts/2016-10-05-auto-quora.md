---
layout: post
title: Automated my Quora answer
---

[Answer can be found here.](https://www.quora.com/Why-do-all-bootstrap-websites-look-the-same-and-how-can-you-be-different/answer/Mickey-Pash)

**Disclaimer** I generally think this is not advisable as this just reduces the quality of what has the potential to be a very good learning resource.

Code I used is simple.
It uses the BeautifulSoup Python library to extract all the headings from the article and generate markdown links.
Time was of the essence as there is a relationship between the *length* of your answer and the *time to answer*.

{% highlight python %}
from bs4 import BeautifulSoup
import urllib2

url= 'https://colorlib.com/wp/free-css3-frameworks/'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), "html.parser")

css_frameworks = soup.findAll("h2")

for framework in css_frameworks:

    try:
        name = framework.a.text
        url = framework.a.get('href')
        print('[{}]({})'.format(name, url))
    except:
        pass
{% endhighlight %}