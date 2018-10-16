# SmartScreen 新增看板 API


---

**host: http://zhz.chafanbao.com**

**api_version: v1**

#概要

 2. API请求格式：host + "api" + api_version + 请求地址。（eg: http://zhz.chafanbao.com/api/v1/tanks）
 3. API返回格式：`json:{"status":1,"body":{}}`status返回操作结果码,body包含返回信息，如果无返回信息，body为空。
 4. status结果码对照表：

|status结果码|状态|
| --------------  | :---: |
|0|未知错误|
|1|成功|
|2|权限不足|
|3|帐号不存在|
|4|数据错误|
|5|密码错误|
|6|已存在|
|7|不存在|
|8|已过期|
|10|验证码为空|
|11|验证码错误|


#API认证


 1. 所有请求请带参数 `token={site.slug}` 或 set cookie 用以识别站点信息; eg:http://zhz.chafanbao.com/api/v1/fuel_charge_times?token=test

## **举例(所有接口返回格式均和举例一样)**

```
GET /api/v1/fin/support/toc/
```

### **Parameters**
* target(_Required_|string)-指标选择 (month: 月度指标 year: 年度指标)
* compare(_Required_|integer)-对标对象选择 (传对标站的 id, 无对标时传 0)
* year(_Optional_|integer)-年份 (当指标为月度指标时传年份值 如： 2018)
* fuel_type(_Optional_|integer)-油品型号 (只有需要传油品的接口才需要此参数)

fuel_type 取值： （左侧为可取值，右侧为含义）
```
98: '98号 车用汽油(V)'
95: '95号 车用汽油(Ⅴ)'
92: '92号 车用汽油(Ⅴ)'
0: '0号 车用柴油(Ⅴ)'
-20: '-20号 车用柴油(Ⅴ)'
35: '35号 车用柴油(Ⅴ)'
10: '10号 车用柴油(Ⅴ)'
20: '20号 车用柴油(Ⅴ)'
```



### **Return**

### 成功

#### 月度指标
##### 无对标
```
{
    "body":{
        "compare":0,
        "target":"month",
        "start_time":"2017-01-01 00:00:00",
        "object_list":[
            {
                "last_month":0, # 上月
                "month":1, # 月份
                "current":116.285335483792, # 本月
                "hb":116.285335483792, # 环比
                "tq":116.285335483792, # 同期
                "tb":0 # 同比
            },
            {
                "last_month":116.285335483792,
                "month":2,
                "current":116.285335483792,
                "hb":0,
                "tq":116.285335483792,
                "tb":0
            }
        ],
        "last_end_time":"2016-12-31 00:00:00",
        "api_name":"吨油费用", # 接口名称
        "last_start_time":"2016-01-01 00:00:00",
        "end_time":"2017-12-31 00:00:00",
        "year":2017,
        "unit":{
            "current_unit":"元" # 显示单位
        }
    },
    "status":1,
    "msg":"success"
}
```

##### 有对标
```
{
    "body":{
        "compare":2,
        "target":"month",
        "start_time":"2017-01-01 00:00:00",
        "object_list":[
            {
                "current":116.285335483792, # 本月累计
                "yddb":0, # 月度对比
                "month":1 # 月份
            },
            {
                "current":116.285335483792,
                "yddb":0,
                "month":2
            }
        ],
        "last_end_time":"2016-12-31 00:00:00",
        "api_name":"吨油费用",
        "last_start_time":"2016-01-01 00:00:00",
        "end_time":"2017-12-31 00:00:00",
        "year":2017,
        "unit":{
            "current_unit":"元"
        }
    },
    "status":1,
    "msg":"success"
}
```

#### 年度指标
##### 无对标
```
{
    "body":{
        "compare":0,
        "target":"year",
        "start_time":"2000-01-01 00:00:00",
        "object_list":[
            {
                "current":232.570670967584, # 本年累积
                "yszj":232.570670967584, # 预算增减
                "year":2017, # 年份
                "tqzj":232.570670967584, # 同期增减
                "tq":0 # 同期累积
            }
        ],
        "last_end_time":"2018-12-31 00:00:00",
        "api_name":"吨油费用",
        "last_start_time":"2000-01-01 00:00:00",
        "end_time":"2018-12-31 00:00:00",
        "year":2017,
        "unit":{
            "current_unit":"元"
        }
    },
    "status":1,
    "msg":"success"
}
```

##### 有对标
```
{
    "body":{
        "compare":2,
        "target":"year",
        "start_time":"2000-01-01 00:00:00",
        "object_list":[
            {
                "current":232.570670967584, # 本年累积
                "nddb":0, # 年度对标
                "year":2017 # 年份
            }
        ],
        "last_end_time":"2018-12-31 00:00:00",
        "api_name":"吨油费用",
        "last_start_time":"2000-01-01 00:00:00",
        "end_time":"2018-12-31 00:00:00",
        "year":2017,
        "unit":{
            "current_unit":"元"
        }
    },
    "status":1,
    "msg":"success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}
```

# 接口

#### 收入指标
##### GET /api/v1/fin/income/osa/ 油品销售数量 （汽柴油销量均用这个接口）
##### GET /api/v1/fin/income/osm/ 油品销售收入 (汽柴油收入均用这个接口)
##### GET /api/v1/fin/income/gsm/ 非油销售收入
#### 成本指标
##### GET /api/v1/fin/cost/gsc/ 汽油销售成本
##### GET /api/v1/fin/cost/dsc/ 柴油销售成本
##### GET /api/v1/fin/cost/gdsc/ 非油销售成本
##### GET /api/v1/fin/cost/dc/ 折旧损耗
##### GET /api/v1/fin/cost/sc/ 员工薪酬
##### GET /api/v1/fin/cost/wec/ 水电暖费
##### GET /api/v1/fin/cost/ol/ 油品损溢
##### GET /api/v1/fin/cost/oc/ 其他费用
##### GET /api/v1/fin/cost/dr/ 日常维修
##### GET /api/v1/fin/cost/tc/ 费用总额
#### 利润指标

##### GET /api/v1/fin/profit/ogp/ 成品油毛利
##### GET /api/v1/fin/profit/tp/ 利润总额
##### GET /api/v1/fin/profit/op/ 成品油利润
##### GET /api/v1/fin/profit/gp/ 非油利润
#### 辅助指标

##### GET /api/v1/fin/support/togp/ 吨油毛利
##### GET /api/v1/fin/support/tggp/ 汽油毛利
##### GET /api/v1/fin/support/tdgp/ 柴油毛利
##### GET /api/v1/fin/support/toc/ 吨油费用
##### GET /api/v1/fin/support/top/ 吨油利润
##### GET /api/v1/fin/support/poa/ 人均销量
##### GET /api/v1/fin/support/pop/ 人均利润
##### GET /api/v1/fin/support/pgp/ 人均非油收入
##### GET /api/v1/fin/support/dsa/ 单站日销量
##### GET /api/v1/fin/support/dagm/ 单店日均非油收入
#### 指标运用

##### GET /api/v1/fin/use/bv/ 盈亏平衡点




## **对标站列表**

```
GET /api/v1/fin/compare/list/
```

### **Parameters**

### **Return**

### 成功

```
{
    "body":{
        "page_obj":{

        },
        "is_paginated":false,
        "site_list":[
            {
                "slug":"air",
                "id":3,
                "name":"曹家堡服务区加油站"
            },
            {
                "slug":"54",
                "id":2,
                "name":"五四加油站"
            },
            {
                "slug":"mf",
                "id":1,
                "name":"马坊加油站"
            }
        ]
    },
    "status":1,
    "msg":"success"
}
```