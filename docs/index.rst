.. murl documentation master file, created by
   sphinx-quickstart on Fri Oct 28 14:00:36 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

murl
====

.. toctree::
   :maxdepth: 2

.. _intro:

Introduction
------------
About
~~~~~
murl is a URI manipulation module aimed at web use. Motivated by the **Python URI Quora challenge** (see note), which is why it has its own implementations of functions already available in `urllib`_ and similar components of the Python Standard Library.

The idea is to parse an existing URI into a Murl object and manipulate its components flexibly according to the standards mentioned in `RFC 3986`_ and other relevant documentation (details on that in the rules below), or alternatively, create an empty Murl object and add/change components on the fly.

`Logo Credit`_

.. note:: As of sometime between October 13th and October 29th, 2016, this challenge was removed. There's a copy of the prompt, however, `in my blog post`_.

Rules
~~~~~
General URI syntax:
::
	scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]

- Scheme must start with a letter, followed by letters, digits, +, ., or -, and then a colon.
- Authority part which has an optional username/password, a host, and an optional port has to start with // and end with the end of the URI, a /, a ?, or a #.
- Path must begin with / whenever there's an authority present. Can begin with / if not, but never //.
- Query must begin with ? and is a string of key=value pairs delimetered by & or ; usually.
- Keys in Query can be duplicates and indicate multiple values for the same thing.
- Fragment must begin with # and span until the end of the URI.
- All unsafe characters and unreserved characters in any given URI component must be percent-encoded in % HEXDEG HEXDIG format.
- Domains (without subdomains, etc) must consist of one segment that (might start with and) ends with a . plus a public suffix, where a public suffix may have a number of dot-delimeterd segments and a wide range of lengths itself (see `Public Suffix list`_).

Installation
~~~~~~~~~~~~~
1. Get the package:
::
	$ pip install mrf-murl

2. Import it in your program/script:
::
	from mrf_murl import Murl


General Use
~~~~~~~~~~~
1. Create a Murl object using an existing relative or absolute valid URI
::
	foo = Murl('https://test.me?this=that')
or without any parameters for an empty object where you create componenets on the fly:
::
	bar = Murl()

2. Add/change/get URI components using the object's parameters.

Below is a quick/non-comprehensive example (note that values that don't exist will return None, or raise an error. See comprehensive docs):
::
	# Entire assembled URI
	# ---------------------
	print(foo) # or use str(foo)

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
	foo.path = '/more.html' # does not have to start with /. 
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

	print(foo) # http://scott:tiger@google.com:25/more.html#hello


.. _docs:

Docs
----
.. automodule:: mrf_murl
	:members:

.. automodule:: mrf_murl.urlsec
	:members:

.. automodule:: mrf_murl.urlende
	:members:







.. _urllib: https://docs.python.org/3/library/urllib.html
.. _RFC 3986: https://tools.ietf.org/html/rfc3986
.. _Public Suffix list: https://publicsuffix.org/
.. _Logo Credit: http://www.flaticon.com/authors/freepik
.. _in my blog post: http://blog.maarouf.me/post/151745263197/murl-init



