#!/usr/bin/env python
# coding=utf8

'''
author  dave
mail    ershaoye@gmail.com
date    20120517
'''

import email,smtplib,mimetypes
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
import sys

class smail:
    def __init__(self, src_addr, src_user, src_pass, dst_addr, sub):
        self.saddr = src_addr
        self.suser = src_user
        self.spwd  = src_pass
        self.daddr = dst_addr
        self.sub   = sub
        self.message            = MIMEMultipart()
        self.message['To']      = ','.join(self.daddr)
        self.message['From']    = self.saddr
        self.message['Subject'] = self.sub

    def connect(self, host, port = 25, debug = 0):
        self.smtp = host
        self.port = port
        self.debug = debug
        try:
            self.s = smtplib.SMTP(self.smtp, self.port)
            try:
                self.s.login(self.suser, self.spwd)
                self.s.set_debuglevel(self.debug)
            except Exception as e:
                print 'Login Error: %s' %e
                sys.exit(2)
        except Exception as e:
            print 'Connect Error: %s' %e
            sys.exit(1)

    def msg(self, message, type = 'plain', coding = 'utf-8'):
            self.msg = message
            self.type = type  #plain or html
            self.code = coding
            self.message.attach(MIMEText(self.msg, self.type, self.code))

    def att(self, file):
            self.ctype, self.encoding = mimetypes.guess_type(file)
            self.maintype, self.subtype = self.ctype.split('/', 1)
            try:
                self.fp = open(file, 'rb')
            except Exception as e:
                print 'Error: %s' %e
                sys.exit(3)
            self.attmsg = MIMEBase(self.maintype, self.subtype)
            self.attmsg.set_payload(self.fp.read())
            self.fp.close()
            encoders.encode_base64(self.attmsg)
            self.attmsg.add_header("Content-Disposition", "attachment", filename = file)
            self.message.attach(self.attmsg)

    def send(self):
            try:
                self.s.sendmail(self.saddr, self.daddr, self.message.as_string())
                self.s.quit()
            except Exception as e:
                print 'Error: %s' %e