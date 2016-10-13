#!/usr/bin/env python3
from murl import Murl, urlende

if __name__ == "__main__":
    foo = Murl('http://haha.google.com')
    foo.addQuery('hello!', 'world?&')
    print(foo)
    print(foo.getQuery('hello!'))
    foo.fragment = 'hello there sugaaaa!!!!???//'
    print(foo.domain)
