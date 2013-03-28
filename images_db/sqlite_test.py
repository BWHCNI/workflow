#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('test.db')

with con:
    
    cur = con.cursor()    
    #cur.execute("CREATE TABLE t1( a INTEGER PRIMARY KEY, b INTEGER );")
    cur.execute("INSERT INTO t1 VALUES(NULL,123);")
    cur.execute("INSERT INTO t1 VALUES(NULL,456);")
    cur.execute("INSERT INTO t1 VALUES(NULL,789);")

    #cur.execute("CREATE TABLE Cars(id INTEGER PRIMARY KEY, Name TEXT, Price INT)")
    #cur.execute("INSERT INTO Cars(id, Name, Price) VALUES(1,'Audi',52642)")
    cur.execute("INSERT INTO Cars(Name, Price) VALUES('Mercedes',57127)")
    cur.execute("INSERT INTO Cars(Name, Price) VALUES('Mercedes',57127)")
    cur.execute("INSERT INTO Cars(Name, Price) VALUES('Mercedes',57127)")


