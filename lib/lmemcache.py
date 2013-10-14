#!/usr/bin/env python
#coding=utf8
import memcache


class db_memcache:
    def __init__(self, host='127.0.0.1', debug=False):
        self.host = host
        self.debug = debug
    
    def connect(self):

        try:
            self.mc = memcache.Client([self.host], self.debug)
        except Exception as e:
            print 'connect error: host %s, %s' %(self.host, e)
    
    def set(self, key, val, timeout=36000):
        try:
            self.mc.set(key, val, timeout)
        except Exception as e:
            print 'set error: %s, %s' %(key, e)
        
    def get(self, key):
        try:
            return self.mc.get(key)
        except Exception as e:
            print 'get error: %s, %s' %(key, e)
    
    def delete(self, key):
        try:
            self.mc.delete(key)
        except Exception as e:
            print 'get error: %s, %s' %(key, e)