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

        self.out_msg     = 'NOK: no up-to-date s3sync found'
        self.out_status  = 2

        self.__logs      = [
                'syslog',
                'messages',
                'syslog.1',
                'messages.1',
                ]

        self.__find_log()

    def __print(self, string, level=1):
        if self.__debug >= level:
            print string

    def __matching(self, matchers, iteration):
      now  = datetime.now()
      year = now.year
      if matchers:
          self.__print('Matcher found for %s' % iteration)
          for m in matchers:
              date_str = '%i %s %s %s' % (year, m.group('month'), m.group('day').zfill(2), m.group('time'))
              try:
                last = datetime.strptime(date_str, '%Y %b %d %H:%M:%S')
              except ValueError:
                last = datetime.strptime(date_str, '%Y %m %d %H:%M:%S')
              self.__print('Found: %s' % last)
              if last.date() == now.date() or now.hour < self.__threshold and last.date() == (now - timedelta(days=1)).date():
                  self.__print('Threshold is met')
                  self.out_msg = 'OK: last s3 pull %s' % last
                  self.out_status  = 0
      else:
        self.__print('No matcher found for %s' % iteration)


    def __find_log(self):
        reg1 = re.compile('(?P<month>[A-z]{3})\s+(?P<day>[0-9]{1,2}) (?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}) \w+ %s: success' % self.__title)
        reg2 = re.compile('(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})T(?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}).+ %s: success' % self.__title)
        now  = datetime.now()
        year = now.year
        for log in self.__logs:
            self.__print('Testing %s' % os.path.join('/var/log', log))
            f = open(os.path.join('/var/log', log), 'r').read()
	    matchers1 = reg1.finditer(f)
            self.__matching(matchers1, '1')
            matchers2 = reg2.finditer(f)
            self.__matching(matchers2, '2')




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check if s3sync is successful')
    parser.add_argument('--debug', '-d', help='Set verbosity level', default=0, type=int)
    parser.add_argument('--threshold', '-t', help='Delay after which we expect the sync to be finished, in hours.', default='4', type=int)
    parser.add_argument('--log-title', '-T', help='Log title, as passed to logger with -t option', default='s3sync-duplicity', type=str)

    args = parser.parse_args()
    check = checker(args)
    print check.out_msg
    sys.exit(check.out_status)
