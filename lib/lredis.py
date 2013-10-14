#!/usr/bin/env python
#coding=utf8

import redis
import cPickle as pickle

class db_redis:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.base = db
    
    def connect(self):
        try:
            RPOOL = redis.ConnectionPool(host=self.host, port=self.port, db=self.base)
            try:
                self.pool = redis.Redis(connection_pool=RPOOL)
            except Exception as e:               
                print 'connection Error: host %s, instance %s, %s' %(self.host, self.base, e)
                exit(1)
        except Exception as e:
            print 'pool Error: host %s, instance %s, %s' %(self.host, self.base, e)
            exit(1)
    
    def lget(self, key):
        try:
            keyname = self.pool.lpop(key)
            return keyname
        except Exception as e:
            print 'Error: instance %s, get keys error %s' %(key, e)
            

    def hget(self, key):
        try:
            return zip(self.pool.hkeys(key), self.pool.hvals(key))
        except Exception as e:
            print 'Error: instance %s, get keys error %s' %(key, e)
    
    def pipeline(self):
        try:
            self.pipe = self.pool.pipeline()
        except Exception as e:
            print 'Error: %s' %e
            
    def lpush(self, key, string):
        try:
            self.pipe.lpush(key, string)
        except Exception as e:
            print 'Error: %s' %e
 
    def execute(self):
        try:
            self.pipe.execute()
        except Exception as e:
            print 'Error: %s' %e   