#!/bin/sh
# py脚本里需要pip安装库，安装pip的命令apt install python3-pip
echo "0 2-23/3 * * * /usr/bin/python3 /usr/share/nginx/html/RSS/thepaperRSS.py >/dev/null" >> /var/spool/cron/crontabs/${USER}
echo "0 2-23/3 * * * /usr/bin/python3 /usr/share/nginx/html/RSS/reutersRSS.py >/dev/null" >> /var/spool/cron/crontabs/${USER}
echo "0 2-23/3 * * * /usr/bin/python3 /usr/share/nginx/html/RSS/jwviewRSS.py >/dev/null" >> /var/spool/cron/crontabs/${USER}
