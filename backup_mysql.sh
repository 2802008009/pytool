#!/usr/bin/env bash

echo "======start备份并压缩=========="

dump_path="/home/mysql_backup/$(date +"%Y%m%d")"
if [ ! -d $dump_path ]; then
  mkdir $dump_path
fi

filename="$(date +"%Y%m%d-%H%M")"
/usr/local/mysql/bin/mysqldump --host=localhost -uroot -pwin13168win opel| gzip > $dump_path/$filename.sql.gz

echo "======end==========="

ls $dump_path

echo "======del删除10天前的备份=============="

find /home/mysql_backup -mtime +10 -exec rm -rf {} \;

echo "=======end================"