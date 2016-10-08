#!/usr/bin/env python3
from murl import Murl

if __name__ == "__main__":
	name = input('Who dis? ')
	foo = Murl('Bearl')
	foo.whois(name)
	other = input('And who dat? ')
	foo.whodat(other)