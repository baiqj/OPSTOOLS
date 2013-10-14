#!/usr/bin/env python
# coding=utf8

import sys
import datetime
from conf import config
from lib.lredis import db_redis
from lib.lmysql import db_mysql


def main(argv):
    MAX = 100
    RDCONFIG = config.REDIS
    MYCONFIG = config.MYSQL
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s src_keyname dst_tablename' % argv[0])
        return 1
    if len(sys.argv) >= 4:
        database = sys.argv[3]
    else:
        database = MYCONFIG['base']

    r = db_redis(RDCONFIG['host'])
    r.connect()
    # result = r.pool.lrange('%s' % sys.argv[1], 0, -1)

    result2 = []
    result3 = []

    sql = "replace into `%s`(%s) VALUES (%s)"

    for i in range(0, MAX):
        tmp = r.lget('%s' % sys.argv[1])
        if tmp:
            result2.append(tmp)
        # else:
        #    print 'get None'

    for i in result2:
        a = r.hget(i)
        a.append(('redis_hashkey', i))
        result3.append(dict((x, y) for x, y in a))

    sql_list = []
    for i in result3:
        k = []
        v = []
        for key, val in i.items():
            k.append(key)
            v.append(val)
        k_str = ', '.join(map(lambda x: "`" + x + "`", k))
        v_str = ', '.join(map(lambda x: "'" + x + "'", v))
        #sql_list.append(sql%(k_str, v_str))
        sql_list.append(sql % (sys.argv[2], k_str, v_str))
    if sql_list:
        try:
            m = db_mysql(host=MYCONFIG['host'], user=MYCONFIG[
                             'user'], passwd=MYCONFIG['pass'], db=database)
            m.connect()
            for i in sql_list:
                print datetime.datetime.now(), '\t', i, '\n'
                m.execute(i)
            m.commit()
            m.__del__()
        except Exception as e:
            print 'Error %s' % e
    else:
        print 'The SQL_List is Null.'

if __name__ == '__main__':
    sys.exit(main(sys.argv))
