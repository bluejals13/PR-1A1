#!/bin/bash

source /opt/db-backup/.env

echo "[INFO] 청소 시작"

find $BACKUP_DIR -type f -name "*.gz" -mtime +7 -delete

echo "[INFO] 청소 완료" >> /opt/db-backup/logs/backup.log