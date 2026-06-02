# mysql 일때, 사용법

## 도커 컨테이너 mysqldump 생성 계정 db | gzip 써서 경로 에
```bash
docker exec -i 154f9eda1ceb mysqldump -u root -ppassword eventdb | gzip > ~/mysql.sql.gz
```

## 파일 확인
```bash
ls ~/mysql.sql.gz
ls -lh ~/mysql.sql.gz
gzip -t ~/mysql.sql.gz
```
 
### 압축 해제 | 도커 컨테이너 계정 db 
```bash
gunzip -c ~/mysql.sql.gz | docker exec -i 154f9eda1ceb mysql -u root -ppassword userdb
```
### 실 db 내부에서 확인
```bash
docker exec -it 154f9eda1ceb mysql -u root -p
```
### db 확인
```bash
show databases;
```
### db 사용 후 tables 확인 및 스키마
```bash
use userdb;
show tables;
desc users;
select * from users;
exit
```
### 백업 파일 정리 및 삭제
```bash
ls ~/mysql.sql.gz
rm ~/mysql.sql.gz
```



