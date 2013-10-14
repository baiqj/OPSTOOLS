#!/usr/bin/env python
#coding=utf8

import sys
import datetime
from conf import config
from lib import rd
from lib import mdb

def main(argv):
    MAX = 100
    RDCONFIG=config.REDIS
    MYCONFIG=config.MYSQL
    
    r = rd.db_redis(RDCONFIG['host'])
    r.connect()
    results = r.pool.keys('user.uuid*')
    
    sql="insert into db_j_user.user_uuid(`hash_key`,`name`) VALUES('%s','%s')"
    sql_list1 = []    
    sql_list2 = []
    
    for i in results:
        key=[]
        key = r.pool.hkeys(i)
        if len(key) >= 2:
            for k in key:
                sql_list1.append(sql %(i, k))
        elif len(key)<=1:
            sql_list2.append(sql %(i,key[0]))
    
    m = mdb.db_mysql(host = MYCONFIG['host'], user = 'ops', passwd = MYCONFIG['pass'], db = 'db_j_user')
    m.connect()
    for i in sql_list1:
        m.execute(i)
    for i in sql_list2:
        m.execute(i)
    m.commit()
    m.__del__()

if __name__ == '__main__':
    sys.exit(main())