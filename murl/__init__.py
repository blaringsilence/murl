#!/usr/bin/env python3


class Murl(object):
    def __init__(self, name):
        self.name = name

    def whois(self, name):
        if name != self.name:
            print(name + ' who?')
        else:
            print('Yes.')

    def whodat(self, name):
        if name == self.name:
            print('Oh no!')
        else:
            print('Hey stranger.')
