#!/bin/bash

cd /opt/ops/RedisToMySQL

python HashToMySQL.py order_syn orders db_j_pay &>> log/`date +%Y%m%d`_hashtomysql.log