#! /bin/sh

export PATH=$PATH:/usr/local/bin

export PYTHONPATH=$PYTHONPATH:/var/www/site/smart_screen

log_dir=/var/log/run/drilling

mkdir -p ${log_dir}

cd /var/www/site/smart_screen/drilling

python init.py 2>&1 | cronolog ${log_dir}/init_ss_data-%Y-%m-%d.log &