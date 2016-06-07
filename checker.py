#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
import argparse
import os
import re
import sys

class checker:
    def __init__(self, args):
        self.__threshold = args.threshold
        self.__debug     = args.debug
        self.__title     = args.log_title

        self.__out_msg   = 'OK: Last s3 sync %s'
        self.out_msg     = ''
        self.out_status  = 0

        self.__logs      = ['syslog', 'syslog.1']

        self.__find_log()

    def __print(self, string, level=1):
        if self.__debug >= level:
            print string

    def __find_log(self):
        reg = re.compile('(?P<month>[A-z]{3})\s+(?P<day>[0-9]{1,2}) (?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}) \w+ %s: success' % self.__title)
        year = datetime.now().year
        for log in self.__logs:
            self.__print('Testing %s' % os.path.join('/var/log', log))
            f = open(os.path.join('/var/log', log), 'r').read()
            m = reg.search(f)
            if m:
                date_str = '%i %s %s %s' % (year, m.group('month'), m.group('day').zfill(2), m.group('time'))
                last = datetime.strptime(date_str, '%Y %b %d %H:%M:%S')
                self.__print('Found: %s' % last)
                if datetime.now() - timedelta(hours = self.__threshold) < last:
                    self.__print('Threshold is met')
                    self.out_msg = self.__out_msg % last



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check if s3sync is successful')
    parser.add_argument('--debug', '-d', help='Set verbosity level', default=0, type=int)
    parser.add_argument('--threshold', '-t', help='Delay after which we expect the sync to be finished, in hours.', default='4', type=int)
    parser.add_argument('--log-title', '-T', help='Log title, as passed to logger with -t option', default='s3sync-duplicity', type=str)

    args = parser.parse_args()
    check = checker(args)
    print check.out_msg
    sys.exit(check.out_status)
