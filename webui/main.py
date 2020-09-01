#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

from bottle import get, run, static_file, template
from pprint import pformat, pprint

@get("/static/<sfile>")
def get_sfile(sfile):
    return static_file(sfile, root="static")

@get("/")
@get("/index")
def mainpage():
    return template("templates/index.html")

def main():
    run(host="0.0.0.0", port=42133)

if __name__ == '__main__':
    exit(main())
