#!/usr/bin/env python -B

import sqlite3, config, time
from twisted.enterprise import adbapi 

pool = adbapi.ConnectionPool("sqlite3", config.db_file)
pool.start()

def setup():
    for datatype in config.datatype_mapping:
        create_table(datatype)

def create_table(datatype):
    cmd = "CREATE TABLE IF NOT EXISTS %s (UID int, Timestamp double precision, Measurement double precision)" % datatype
    return pool.runQuery(cmd)

def add(d):   
    datatype = config.datatype_mapping[d['DataType']]
    cmd = "INSERT INTO %s VALUES (%i, %f, %f)" % (datatype, d['UID'], d['Timestamp'], d['Measurement'])
    return pool.runQuery(cmd)

def all(datatype):
    cmd = "SELECT * FROM %s" % datatype
    return pool.runQuery(cmd)

def last(datatype, n):
    cmd = "SELECT * FROM %s ORDER BY Timestamp DESC LIMIT %i" % (datatype, n)
    return pool.runQuery(cmd)
