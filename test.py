#!/usr/bin/env python3
from murl import Murl, urlende

if __name__ == "__main__":
    foo = Murl('https://12.1.222.2?this=that&this=those')
    foo.addQuery('hello!', 'world?+&')
    print(foo)
    print(foo.getQuery('hello!'))
    print(foo.getQuery('this'))
    print(foo.domain)
    foo.fragment = 'hello there sugaaaa!!!!???//'
    print(foo.domain)
