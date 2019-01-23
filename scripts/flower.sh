#! /bin/sh

export PATH=$PATH:/usr/local/bin

export PYTHONPATH=$PYTHONPATH:/var/www/site/smart_screen/

log_dir=/var/log/run/celery

mkdir -p ${log_dir}

cd /var/www/site/

celery --app=smart_screen.drilling.tasks flower --port=5555 2>&1 | cronolog ${log_dir}/flower-%Y-%m-%d.log &