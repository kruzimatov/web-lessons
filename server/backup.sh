#!/bin/sh
# Daily copy of the database, kept 14 days. Cron: 30 2 * * * /var/www/web-lessons/app/server/backup.sh
set -e
dir=/home/ubuntu/backups/web-lessons
mkdir -p "$dir"
python3 -c "import sqlite3, sys; sqlite3.connect(sys.argv[1]).backup(sqlite3.connect(sys.argv[2]))" \
  /var/www/web-lessons/data/lessons.db "$dir/lessons-$(date +%F).db"
find "$dir" -name 'lessons-*.db' -mtime +14 -delete
