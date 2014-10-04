Connection
==========

Connection is a set of tools that I use on my site [Parallel Transport](https://kartikprabhu.com/) to talk to the rest of the Web. It only includes a basic tool for sending webmentions and a microformats parser — though I plan to add a webmention receiver and some tools for POSSEing.

Installation
------------

To install Connection you'd need to clone this repository through git and install its dependencies using the following commands:

```
git clone https://github.com/kartikprabhu/connection.git
cd connection
pip install -r requirements/standard.txt
```

This will install Connection with its dependencies from pypi. If you want to use the latest development versions of [mf2py](https://github.com/kartikprabhu/mf2py), [ronkyuu](https://github.com/bear/ronkyuu) and [mf2util](https://github.com/kylewm/mf2util) replace the last command by:

```
pip install -r requirements/dev.txt
```


