#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import config
import QyDb, pprint, time

if __name__ == '__main__':
    db = QyDb.QyDb(**config.CONF_MYSQL)
    try:
        db.connect(True)
    except Exception as e:
        print e
        print 'error connect to databases'
        exit()

    id = db.findCol(sql="select max(id) as id from game_buylist_back", col='id')
    if not id:
        id = 0

    print 'BEGION:'
    print '%s id: %d' % (time.strftime('%Y-%m-%d %H:%M:%S'), id)

    while True:
        try:
            db.connect(True)
        except Exception as e:
            print e
            print '%s error connection to databases' % (time.strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(5)
            continue

        rs = db.findAll('game_buylist', "id>%d" % id, limit=100)
        if rs:
            id = rs[-1]['id']
            db.insert('game_buylist_back', rs)
            print '%s id: %d' % (time.strftime('%Y-%m-%d %H:%M:%S'), id)
        else:
            print '%s no new data,at:%s' % (time.strftime('%Y-%m-%d %H:%M:%S'),id)
            time.sleep(1)
