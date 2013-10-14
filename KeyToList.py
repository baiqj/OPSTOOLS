#!/usr/bin/env python
import sys
from lib.lredis import db_redis
from conf.config import REDIS

def main(argv):
    if len(argv) < 3:
        sys.stderr.write('Usage: %s src_keyname dst_listname       |src_key pay* open.appuid*|dst_list order_syn appuid_syn\n' %argv[0])
        return 1
    r = db_redis( host = REDIS['host'])
    r.connect()
    k = r.pool.keys(argv[1])                     # pay*   open.appuid*
    print len(k)
    r.pipeline()
    if k:
        for i in k:
            r.lpush(argv[2], i)                      # prder_syn  appuid_syn
    r.execute()
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))