#!/bin/bash

set -e

ls -a
ls -l

echo -e "\n db.env -> .env 복사 \n"

if [ ! -f "db.env" ]; then
  echo "db.env 파일이 존재하지 않습니다."
  exit 1
fi

cp -f db.env .env

echo "[INFO] .env "

ls -l .env



