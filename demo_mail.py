#!/usr/local/python2.7.2/bin/python
# coding=utf8

from lib.lsmail import smail
from conf.config import MAIL
import sys
config = MAIL

def main(argv):
    if len(argv) < 2:
        sys.stderr.write('Usage: %s mail_messages\n' %argv[0])
        return 1
    mail = smail(src_addr=config['mailfm'], src_user=config['mailfm'], src_pass=config['passwd'], dst_addr=config['toadds'], sub=argv[1])
    mail.connect('mail.9719.com')
    mail.msg(argv[1])
    #mail.att('results/20120515103222_各省pv统计.xls')
    mail.send()#!/usr/bin/env python
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))