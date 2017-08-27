#!/bin/bash
cd /home/ssl/
python acme_tiny.py --account-key ./account.key --csr ./rsa.csr --acme-dir /home/www/challenges/ > ./rsa.crt || exit
wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > intermediate.pem
cat rsa.crt intermediate.pem > chained.pem
service nginx reload
