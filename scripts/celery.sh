#! /bin/sh

export PATH=$PATH:/usr/local/bin

export PYTHONPATH=$PYTHONPATH:/var/www/site/smart_screen/

log_dir=/var/log/run/celery

mkdir -p ${log_dir}

cd /var/www/site/smart_screen/

celery -A drilling.tasks worker -l info -B 2>&1 | cronolog ${log_dir}/celery-%Y-%m-%d.log &
