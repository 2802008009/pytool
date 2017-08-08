#!/usr/bin/env bash

echo "======start备份并压缩=========="

dump_path="/data/backup_mysql/$(date +"%Y%m%d")"
if [ ! -d $dump_path ]; then
  mkdir $dump_path
fi

filename="$(date +"%Y%m%d-%H%M")"
/usr/local/mysql/bin/mysqldump --host=localhost -uroot -pwin13168win --lock-tables --databases opel --master-data=2| gzip > $dump_path/$filename.sql.gz

echo "======end==========="

ls $dump_path

echo "======del删除7天前的备份=============="

find /data/backup_mysql -mtime +7 -exec rm -rf {} \;

echo "=======end================"