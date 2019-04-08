# SmartScreen

##快速构建开发环境

###依赖
	
* PostgreSQL [https://hub.docker.com/_/postgres](https://hub.docker.com/_/postgres)
* python2.7 [	https://hub.docker.com/_/python](https://hub.docker.com/_/python)
* redis [https://hub.docker.com/_/redis](https://hub.docker.com/_/redis)


###手动构建

####-postgresqsl

```
docker run --name sprucesmart_db -e POSTGRES_PASSWORD=123456qq -e POSTGRES_DB=ss_produce -e POSTGRES_USER=postgres -p 5432:5432 -d postgres
```

####-redis
```
```
	
####-backend server

```
cd {{code dir}}
	
docker build -t smart_screen ./

docker run -itd --name smart_screen_backend -p 8000:8000 -v {{code dir}}:/code --link sprucesmart_db:db_host smart_screen
```

####初始化数据表

```
#bash
docker exec -it smart_screen bash

python manage.py makemigrations
python manage.py migrate

python manage.py shell

#python-shell

from sqlalchemy.engine import create_engine
from core.util import conf
from drilling.models import Base
engine = create_engine('postgresql+psycopg2://'+conf.smart_screen_user+':'+conf.smart_screen_password+'@'+conf.smart_screen_host+':'+conf.smart_screen_port+'/'+conf.smart_screen_name)
Base.metadata.create_all(engine)
```

