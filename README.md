# murl

A URI Manipulation module aimed at web use. Motivated by the [Quora challenge](https://www.quora.com/challenges#python_uri), which is why `murl` has its own implementation of some functions in `urllib` and `urlparse`.

## General Use

- Create a `Murl` object using an existing relative or absolute but valid/standard URI or without any parameters to construct the URI dynamically.
- Add/change/get URI components:
  - scheme [add/change/get]
  - host (entire string, including subdomains, etc, but not port) [add/change/get]
  - domain (only the domain without any subdomains, etc) [get]
  - auth (username/password) [add/change/get]
  - port [add/change/get]
  - path [add/change/get]
  - query string/individual key/value pairs [add/change/get]
  - fragment [add/change/get]
  
## References

- [RFC 3986 (2005)](https://tools.ietf.org/html/rfc3986)
- [Public Suffix List](https://publicsuffix.org/)
