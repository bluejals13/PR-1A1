#!/bin/bash

set -e

source /opt/db-backup/.env

DATE=$(date +%Y%m%d_%H%M%S)
FILE="$BACKUP_DIR/backup_$DATE.sql.gz"

mkdir -p $BACKUP_DIR

echo "[INFO] db 백업 시작: $DATE"

docker exec $MYSQL_CONTAINER \
mysqldump -u $MYSQL_USER -p"$MYSQL_PASSWORD" $MYSQL_DB \
| gzip > $FILE

echo "[INFO] 백업 완료 파일: $FILE" >> /opt/db-backup/logs/backup.log
