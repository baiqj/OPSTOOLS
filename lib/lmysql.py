#!/usr/bin/env python

#Author: dave
#mail:   ershaoye@gmail.com
#date:   20120815
#
#

import os
import datetime
from sys import exit
import MySQLdb as mdb
from DBUtils.PooledDB import PooledDB


class db_mysql:
    def  __init__(self, host = 'localhost', user = 'dbuser', passwd = 'dbpass', port = 3306, db=None, charset='utf8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = db
        self.charset = charset
        self.numbers = 50

    def connect(self):
        try:
            self.conn = mdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port, charset=self.charset)
            try:
                self.curs = self.conn.cursor()
            except Exception as e:
                print 'Error: host %s, instance %s, user %s, %s' %(self.host, self.db, self.user, e)
                exit(1)
        except Exception as e:
            print 'Error: host %s, instance %s, user %s, %s' %(self.host, self.db, self.user, e)
            exit(1)

    def poolconnect(self):
        try:
            self.pool= PooledDB(creator=MySQLdb, maxusage=self.numbers, host=self.host, user=self.user, passwd=self.passwd,db=self.db)
            try:
                self.pooconn = self.pool.connection()
                self.curs = self.pooconn.cursor()
            except Exception as e:
                print 'Error: host %s, instance %s, user %s, %s' %(self.host, self.db, self.user, e)
                exit(1)
        except Exception as e:
            print 'Error: host %s, instance %s, user %s, %s' %(self.host, self.db, self.user, e)
            exit(1)

    def execute(self, sql):
        try:
            return self.curs.execute(sql)
        except Exception as e:
            print 'Error: %s' %e
            exit(2)

    def commit(self):
        self.conn.commit()

    def show(self):
        try:
            self.results = self.curs.fetchall()
            return self.results
        except Exception as e:
            print 'Errpr: %s' %e
            exit(3)

    def timestr(timeformat = '%Y%m%d%H%M%S'):
        return datetime.datetime.now().strftime(timeformat)

    def result2excel(self, sheet = 'sheet1', file = timestr() + '.xls'):
        self.sheet = sheet
        self.file = file
        import xlwt
        wb = xlwt.Workbook()
        ws0 = wb.add_sheet(self.sheet)
        # set background for the header row
        BkgPat = xlwt.Pattern()
        BkgPat.pattern = xlwt.Pattern.SOLID_PATTERN
        BkgPat.pattern_fore_colour = 22
        # bold fonts for the header row
        font = xlwt.Font()
        font.name = 'SimSun'    #songti
        font.bold = True
        # non-bold fonts for the body
        font0 = xlwt.Font()
        font0.name = 'SimSun'
        font0.bold = False
        # style and write field lables
        style = xlwt.XFStyle()
        style.font = font
        style.pattern = BkgPat
        style0 = xlwt.XFStyle()
        style0.font = font0

        row_number = 0
        col_number = 0
        for header in self.curs.description:
                try:
                    ws0.write(row_number, col_number, str(header[0]).decode('utf8'), style)
                    col_number += 1
                except Exception as e:
                    print 'Error: %s' %e
        row_number = 1
        for row in self.results:
            col_number=0
            for item in row:
#               print item
                try:
                    ws0.write(row_number, col_number, str(item).decode('utf8'), style0)
                    col_number += 1
                except Exception as e:
                    print 'Error: %s' %e
            row_number += 1
        wb.save(file)


    def __del__(self):
        try:
            self.curs.close()
        except:
            pass
        try:
            self.conn.close()
        except:
            pass