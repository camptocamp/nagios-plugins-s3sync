nagios-plugin-s3sync
==================

Overview
--------

Simple checker for the last S3 sync you made

Usage
-----

* Install python-boto3
* create a cron job for your sync as bellow
* configure this plugin in your nagios

Cronjob
-------

```Bash
(aws s3 sync s3://BUCKETNAME /srv/duplicity-s3/ --delete 2>&1 && echo 'success') | logger -t s3sync-duplicity
```

License
-------

Copyright (c) Camptocamp 2016 All rights reserved.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
