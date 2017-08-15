#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import config
import QyDb, pprint, time

if __name__ == '__main__':
    db = QyDb.QyDb(**config.CONF_MYSQL)
    db_backup = QyDb.QyDb(**config.CONF_MYSQL_BACKUP)
    try:
        db.connect(True)
        db_backup.connect(True)
    except Exception as e:
        print e
        print 'error connect to databases'
        exit()

    id = db_backup.findCol(sql="select max(id) as id from game_buylist", col='id')
    if not id:
        id = 0

    print 'BEGION:'
    print '%s id: %d' % (time.strftime('%Y-%m-%d %H:%M:%S'), id)

    while True:
        try:
            db.connect(True)
        except Exception as e:
            print e
            print 'db1 %s error connection to databases' % (time.strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(5)
            continue

        rs = db.findAll('game_buylist', "id>%d" % id, limit=1000)
        if rs:
            try:
                db_backup.connect(True)
            except Exception as e:
                print e
                print 'db2 %s error connection to databases' % (time.strftime('%Y-%m-%d %H:%M:%S'))
                time.sleep(5)
                continue

            id = rs[-1]['id']
            db_backup.insert('game_buylist', rs)
            print '%s id: %d' % (time.strftime('%Y-%m-%d %H:%M:%S'), id)
        else:
            print '%s no new data,at:%s' % (time.strftime('%Y-%m-%d %H:%M:%S'),id)
            time.sleep(1)
