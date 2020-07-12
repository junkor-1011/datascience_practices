#!/usr/bin/env sh

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

openssl req -batch -new -x509 -newkey rsa:4096 -nodes -sha256 \
  -subj /CN=example.com/O=example -days 3650 \
  -keyout ./notebook.key \
  -out ./notebook.crt
