#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import config
import threading
import QyDb, pprint, time


class BackupWorker(threading.Thread):
    def __init__(self, tbname, idname):
        threading.Thread.__init__(self)
        self.tbname = tbname
        self.idname = idname

    def run(self):  # 定义每个线程要运行的函数
        db = QyDb.QyDb(**config.CONF_MYSQL)
        db2 = QyDb.QyDb(**config.CONF_MYSQL_BACKUP)
        try:
            db.connect(True)
            db2.connect(True)
        except Exception as e:
            print e
            print 'error connect to databases'
            return

        rs = db2.find(self.tbname, order='%s desc' % self.idname)
        id = 0
        if rs:
            id = int(rs[self.idname])

        print 'start %s:' % self.tbname
        print '%s %s id: %d' % (time.strftime('%m-%d %H:%M:%S'), self.tbname, id)

        while True:
            db.reconnect()
            rs = db.findAll(self.tbname, "%s>%d" % (self.idname, id), limit=1000)
            if rs:
                id = rs[-1][self.idname]
                db2.reconnect()
                db2.insert(self.tbname, rs)
                print '%s %s id: %d' % (time.strftime('%m-%d %H:%M:%S'), self.tbname, id)
            else:
                print '%s %s no new,at:%s' % (time.strftime('%m-%d %H:%M:%S'), self.tbname, id)
                time.sleep(1)


def main():
    threads = []
    tbnames = {'user_bank_log': 'id', 'user': 'userid', 'k_user': 'uid', 'game_buylist': 'id'}

    for tbname in tbnames:
        t = BackupWorker(tbname, tbnames[tbname])
        t.setDaemon(True)
        threads.append(t)
        t.start()

    while True:
        print 'while %s' % (time.strftime('%m-%d %H:%M:%S'))
        time.sleep(10)


if __name__ == '__main__':
    print 'start to work %s' % (time.strftime('%m-%d %H:%M:%S'))
    main()
    print 'end to work %s' % (time.strftime('%m-%d %H:%M:%S'))
