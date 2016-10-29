#!/usr/bin/env python3
from mrf_murl import Murl

if __name__ == "__main__":
    foo = Murl('https://test.me?this=that')
    # Entire assembled URI
    # ---------------------
    print(foo) # or str(foo)


    # Scheme
    # ------
    ## Get
    scheme = foo.scheme # returns a string, e.g. 'https'
    ## Set
    foo.scheme = 'http'


    # Authority
    # ---------
    ## Host
    ## ====
    ### Get
    host = foo.host
    ### Set
    foo.host = 'google.com'

    ## Authentication (username/password)
    ## ==================================
    ### Get (Either together or individually)
    auth = foo.auth # returns a dict with the keys 'username' and 'password'
    username = foo.username # returns a string
    password = foo.password # returns a string
    ### Set (Either together or individually)
    foo.auth = dict(username='scott', password='tiger')
    foo.username = 'scott'
    foo.password = 'tiger'

    ## Port
    ## ====
    ### Get
    port = foo.port # returns an int
    ### Set
    foo.port = 25

    # Path
    # ----
    ## Get
    path = foo.path # returns string
    ## Set
    foo.path = 'more.html' # does not have to start with /. 
    # If / is required and not present, it will be added to the assembled URI.

    # Query
    # -----
    ## Get
    querystring = foo.queryString
    singleQuery = foo.getQuery('this') # returns the value of the query, decoded
    ## Set
    foo.addQuery('this', 'those') # will add key=value pair even if key exists
    foo.changeQuery('this', 'not') # will delete all prev key values & add this val
    foo.removeQuery('this') # will remove all values for this key
    # see docs to change/remove one key=value pair even if key has mult values

    # Fragment
    # --------
    ## Get
    fragment = foo.fragment # returns a string
    ## Set
    foo.fragment = 'hello'

    print(foo) # http://google.com


