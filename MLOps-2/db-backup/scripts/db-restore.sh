#!/bin/bash

source /opt/db-backup/.env

FILE=$1

if [ -z "$FILE" ]; then
  echo "사용: restore.sh /path/to/file.sql.gz"
  exit 1
fi

echo "[INFO] Restoring from $FILE"

gunzip < $FILE | docker exec -i $MYSQL_CONTAINER \
mysql -u $MYSQL_USER -p"$MYSQL_PASSWORD" $MYSQL_DB

echo "[INFO] 롤백 완료"
