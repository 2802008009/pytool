#!/usr/bin/python
# -*- coding: utf-8 -*-

import commands
import os
import subprocess
import sys
import time


def update_system():
    try:
        popen = subprocess.Popen(['yum', 'update', '-y'], stdout=subprocess.PIPE)
        while True:
            next_line = popen.stdout.readline()
            if next_line == '' and popen.poll() != None:
                break
            sys.stdout.write(next_line)

        print time.strftime('%Y-%m-%d %H:%M:%S'), ' update sucess'
    except Exception as e:
        print 'th-error:update,', e
        exit()


def optimize_system():
    try:
        (status, output) = commands.getstatusoutput("ulimit -u 65535")
        print output
        fn = '/etc/sysctl.conf'
        back = '/etc/sysctl.conf.back'
        if not os.path.exists(back):
            commands.getstatusoutput("cp -a %s %s" % (fn, back))

        commands.getstatusoutput("cat %s > %s" % (back, fn))
        commands.getstatusoutput("echo 'net.ipv4.tcp_tw_reuse = 1'>> %s" % (fn))
        commands.getstatusoutput("echo 'net.ipv4.tcp_tw_recycle = 1'>> %s" % (fn))
        commands.getstatusoutput("sysctl -p")

        print time.strftime('%Y-%m-%d %H:%M:%S'), ' optimize system sucess'
    except Exception as e:
        print 'th-error:optimize system,', e
        exit()


def set_nginx_repo():
    try:
        t = '''
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/6/$basearch/
gpgcheck=0
enabled=1
'''
        fn = '/etc/yum.repos.d/nginx.repo'
        (status, output) = commands.getstatusoutput("echo >%s" % fn)
        print output

        fp = open(fn, 'w')
        fp.truncate()
        fp.write(t)
        fp.close()
        print time.strftime('%Y-%m-%d %H:%M:%S'), ' set repo sucess'
    except Exception as e:
        print 'th-error:set repo,', e
        exit()


def install_nginx():
    try:
        popen = subprocess.Popen(['yum', 'install', '-y', 'nginx'], stdout=subprocess.PIPE)
        while True:
            next_line = popen.stdout.readline()
            if next_line == '' and popen.poll() != None:
                break
            sys.stdout.write(next_line)

        print time.strftime('%Y-%m-%d %H:%M:%S'), ' install nginx sucess'
    except Exception as e:
        print 'th-error:install nginx,', e
        exit()


# backup nginx.conf
def backup_nginx_conf():
    try:
        fn = '/etc/nginx/nginx.conf'
        (status, output) = commands.getstatusoutput("mv %s %s.back" % (fn, fn))
        print output
        print time.strftime('%Y-%m-%d %H:%M:%S'), ' backup nginx.conf sucess'
    except Exception as e:
        print 'th-error:backup nginx.conf,', e
        exit()


# update nginx.conf
def update_nginx_conf():
    try:
        conf = '''
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

worker_rlimit_nofile 51200;


events {
    use epoll;
    worker_connections 51200;
    multi_accept on;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  off;
    sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	server_tokens off;
    keepalive_timeout  120;


    include /etc/nginx/conf.d/*.conf;
    include /dev/shm/thgame/*.conf;
}        
'''
        fn = '/etc/nginx/nginx.conf'
        (status, output) = commands.getstatusoutput("echo >%s" % (fn))
        print output

        fp = open(fn, 'w')
        fp.truncate()
        fp.write(conf)
        fp.close()
        print time.strftime('%Y-%m-%d %H:%M:%S'), ' update nginx.conf sucess'
    except Exception as e:
        print 'th-error:update nginx.conf,', e
        exit()


# set proxy.conf
def set_proxy_conf():
    try:
        conf = '''
proxy_connect_timeout 300s;
proxy_send_timeout 900;
proxy_read_timeout 900;
proxy_buffer_size 32k;
proxy_buffers 4 64k;
proxy_busy_buffers_size 128k;
proxy_redirect off;
proxy_hide_header Vary;
proxy_set_header Accept-Encoding '';
proxy_set_header Referer $http_referer;
proxy_set_header Cookie $http_cookie;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
'''
        fn = '/etc/nginx/proxy.conf'
        (status, output) = commands.getstatusoutput("echo >%s" % fn)
        print output

        fp = open(fn, 'a')
        fp.truncate()
        fp.write(conf)
        fp.close()
        print time.strftime('%Y-%m-%d %H:%M:%S'), ' set proxy.conf sucess'
    except Exception as e:
        print 'th-error:set proxy.conf,', e
        exit()


# stop selinux
def stop_selinux():
    try:
        (status, output) = commands.getstatusoutput("setenforce 0")
        print output
        print time.strftime('%Y-%m-%d %H:%M:%S'), ' stop selinux sucess'
    except Exception as e:
        print 'th-error:stop selinux,', e
        exit()


# open iptables 80
def set_iptables():
    try:
        conf = '''
# Firewall configuration written by system-config-firewall
# Manual customization of this file is not recommended.
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 443 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT
'''
        fn = '/etc/sysconfig/iptables'
        (status, output) = commands.getstatusoutput("cp -a %s %s%s" % (fn, fn, time.strftime('%Y%m%d_%H%M%S')))
        print output

        (status, output) = commands.getstatusoutput("echo >%s" % fn)
        print output

        fp = open(fn, 'w')
        fp.truncate()
        fp.write(conf)
        fp.close()

        (status, output) = commands.getstatusoutput("service iptables restart")
        print output

        print time.strftime('%Y-%m-%d %H:%M:%S'), ' set iptables sucess'
    except Exception as e:
        print 'th-error:set iptables,', e
        exit()


# down load conf
def down_load_conf():
    pass


# start nginx
def start_nginx():
    try:
        (status, output) = commands.getstatusoutput("ps -ef|grep -i [n]ginx|awk '{print $2}'")
        print output

        output = output.strip().split("\n")
        output = ' '.join(output)
        (status, output) = commands.getstatusoutput("kill -9 %s" % output)
        print output

        (status, output) = commands.getstatusoutput("service nginx restart")
        print output

        (status, output) = commands.getstatusoutput("pgrep nginx")
        print output
        output = output.strip().split("\n")
        if len(output) < 1:
            raise Exception('nginx service not start')

        (status, output) = commands.getstatusoutput('netstat -tulnp|grep -i ":80"|grep -i "nginx"')
        print output
        output = output.strip().split("\n")
        if len(output) < 1:
            raise Exception('nginx service not start')

        print time.strftime('%Y-%m-%d %H:%M:%S'), ' start nginx sucess'
    except Exception as e:
        print 'th-error:start nginx,', e
        exit()


# clear log
def clear_log():
    try:
        (status, output) = commands.getstatusoutput("history -c")
        print output

        t = "anaconda.syslog anaconda.xlog btmp cron dmesg dmesg.old lastlog maillog messages secure spooler tallylog wtmp" \
            .split(" ")
        for i in t:
            fn = '/var/log/%s' % i
            if os.path.exists(fn):
                (status, output) = commands.getstatusoutput("echo > %s" % fn)
            (status, output) = commands.getstatusoutput("rm -rf %s*" % fn)

        (status, output) = commands.getstatusoutput("echo > /var/log/wtmp")
        (status, output) = commands.getstatusoutput("echo > /var/log/btmp")
        (status, output) = commands.getstatusoutput("echo > /var/log/lastlog")
        (status, output) = commands.getstatusoutput("rm -rf /var/log/*.log")
        (status, output) = commands.getstatusoutput("rm -rf /var/log/audit/*.log")
        (status, output) = commands.getstatusoutput("rm -rf /var/log/nginx/*.log")
        (status, output) = commands.getstatusoutput("echo > ~/.bash_history")
        (status, output) = commands.getstatusoutput("history -c")

        (status, output) = commands.getstatusoutput("ps axjf|grep [n]ginx")
        print output

        print time.strftime('%Y-%m-%d %H:%M:%S'), ' clear log sucess'
    except Exception as e:
        print 'th-error:clear log,', e
        exit()


if __name__ == '__main__':
    update_system()
    optimize_system()
    set_nginx_repo()
    install_nginx()
    backup_nginx_conf()
    update_nginx_conf()
    set_proxy_conf()
    stop_selinux()
    set_iptables()
    down_load_conf()
    start_nginx()
    clear_log()

    print 'th-success'
