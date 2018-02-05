#! /bin/sh

export PATH=$PATH:/usr/local/bin

export PYTHONPATH=$PYTHONPATH:/var/www/site/smart_screen/

log_dir=/var/log/run/uwsgi

mkdir -p ${log_dir}

cd /var/www/site/

uwsgi --reload uwsgi_ss.pid 2>&1 | cronolog ${log_dir}/reload-%Y-%m-%d.log &