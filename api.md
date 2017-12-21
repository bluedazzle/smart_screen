# SmartScreen API


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


#油库
## **获取油罐信息**
```
GET /tanks
```
### **Parameters**

### **Return**
成功
```
{
    "body":{
        "fueltank_list":[
            {
                "name":"第T004号油罐",
                "temperature":17.21,
                "max_value":35000,
                "min_value":1000,
                "original_create_time":"2017-10-19 00:30:03",
                "belong_id":1,
                "grade_id":102,
                "current":null,
                "create_time":"2017-12-06 01:28:17",
                "modify_time":"2017-12-06 01:28:15",
                "water_stick":0,
                "id":11,
                "tank_id":4
            },
            {
                "name":"第T001号油罐",
                "temperature":17.21,
                "max_value":35000,
                "min_value":1000,
                "original_create_time":"2017-10-19 00:30:02",
                "belong_id":1,
                "grade_id":77,
                "current":null,
                "create_time":"2017-12-06 01:28:13",
                "modify_time":"2017-12-06 01:28:12",
                "water_stick":0,
                "id":8,
                "tank_id":1
            },
            {
                "name":"第T002号油罐",
                "temperature":17.21,
                "max_value":35000,
                "min_value":1000,
                "original_create_time":"2017-10-19 00:30:02",
                "belong_id":1,
                "grade_id":77,
                "current":null,
                "create_time":"2017-12-06 01:28:14",
                "modify_time":"2017-12-06 01:28:13",
                "water_stick":0,
                "id":9,
                "tank_id":2
            },
            {
                "name":"第T003号油罐",
                "temperature":17.21,
                "max_value":35000,
                "min_value":1000,
                "original_create_time":"2017-10-19 00:30:02",
                "belong_id":1,
                "grade_id":101,
                "current":null,
                "create_time":"2017-12-06 01:28:15",
                "modify_time":"2017-12-06 01:28:14",
                "water_stick":0,
                "id":10,
                "tank_id":3
            }
        ],
        "page_obj":{

        },
        "is_paginated":false
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

## **获取卸入量及损耗数据**
```
GET /fuel_inventories
```
### **Parameters**

### **Return**
|record_type|含义|
| --------------  | :---: |
|1|卸前计量|
|2|卸后计量|
|3|日结班结|

成功
```
{
    "body":{
        "page_obj":{
            "current":1,
            "next":2,
            "total":198,
            "page_range":[
                {
                    "page":1
                },
                {
                    "page":2
                },
                {
                    "page":3
                }
            ],
            "previous":null
        },
        "is_paginated":true,
        "inventoryrecord_list":[
            {
                "receive_amount":0,
                "shift_control_id":2693,
                "water_altitude":0,
                "fuel_volum":17212,
                "record_type":3,
                "create_time":"2017-12-18 20:51:38",
                "tanker_out_amount":0,
                "hash":"9daa0179d14d0d6c0a001df04c1b5098",
                "id":1258,
                "tank_id":8,
                "vcf20":0,
                "tanker_act_out_amount":3175.91999999993,
                "altitude":0,
                "loss_amount":3.91999999992549,
                "fuel_standard_volum":17212,
                "experiment_density":850,
                "experiment_temperature":20,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-25 09:21:05",
                "belong_id":1,
                "fuel_name":"第T001号油罐",
                "fuel_temperature":20,
                "tank_out_amount":3172,
                "standard_density":850,
                "modify_time":"2017-12-18 20:51:38",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2694,
                "water_altitude":0,
                "fuel_volum":12443,
                "record_type":3,
                "create_time":"2017-12-18 20:51:38",
                "tanker_out_amount":0,
                "hash":"039c1f34ea27bcc4f079cfe0830ae5c6",
                "id":1259,
                "tank_id":8,
                "vcf20":0,
                "tanker_act_out_amount":4779.27000000002,
                "altitude":0,
                "loss_amount":10.2700000000186,
                "fuel_standard_volum":12443,
                "experiment_density":850,
                "experiment_temperature":20,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-25 16:18:55",
                "belong_id":1,
                "fuel_name":"第T001号油罐",
                "fuel_temperature":20,
                "tank_out_amount":4769,
                "standard_density":850,
                "modify_time":"2017-12-18 20:51:38",
                "standard_temperature":0
            },
            {
                "receive_amount":20391.686,
                "shift_control_id":2695,
                "water_altitude":0,
                "fuel_volum":31082,
                "record_type":2,
                "create_time":"2017-12-18 20:51:38",
                "tanker_out_amount":0,
                "hash":"783f4a4e9b4ee85ce48750f9fc834ee5",
                "id":1261,
                "tank_id":8,
                "vcf20":0,
                "tanker_act_out_amount":0,
                "altitude":0,
                "loss_amount":139.504000000001,
                "fuel_standard_volum":30951.456,
                "experiment_density":850,
                "experiment_temperature":20,
                "send_amount":20252.182,
                "back_tank_amount":0,
                "original_create_time":"2017-04-25 21:18:50",
                "belong_id":1,
                "fuel_name":"第T001号油罐",
                "fuel_temperature":25,
                "tank_out_amount":0,
                "standard_density":850,
                "modify_time":"2017-12-18 20:51:38",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2695,
                "water_altitude":0,
                "fuel_volum":10811,
                "record_type":1,
                "create_time":"2017-12-18 20:51:38",
                "tanker_out_amount":0,
                "hash":"88aa3f51aaf461ddf0fe889adf6809c6",
                "id":1260,
                "tank_id":8,
                "vcf20":0,
                "tanker_act_out_amount":0,
                "altitude":0,
                "loss_amount":0,
                "fuel_standard_volum":10870.46,
                "experiment_density":850,
                "experiment_temperature":20,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-25 21:17:14",
                "belong_id":1,
                "fuel_name":"第T001号油罐",
                "fuel_temperature":13.4,
                "tank_out_amount":0,
                "standard_density":850,
                "modify_time":"2017-12-18 20:51:38",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2689,
                "water_altitude":0,
                "fuel_volum":7300,
                "record_type":3,
                "create_time":"2017-12-18 20:51:36",
                "tanker_out_amount":0,
                "hash":"a394771794dddaace9cdeea15dfaa619",
                "id":1246,
                "tank_id":8,
                "vcf20":0,
                "tanker_act_out_amount":5857.06000000006,
                "altitude":700,
                "loss_amount":13157.0600000001,
                "fuel_standard_volum":7300,
                "experiment_density":850,
                "experiment_temperature":20,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-23 09:22:00",
                "belong_id":1,
                "fuel_name":"第T001号油罐",
                "fuel_temperature":20,
                "tank_out_amount":-7300,
                "standard_density":850,
                "modify_time":"2017-12-18 20:51:36",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2690,
                "water_altitude":0,
                "fuel_volum":3676,
                "record_type":3,
                "create_time":"2017-12-18 20:51:36",
                "tanker_out_amount":0,
                "hash":"4d5da5ba43b81f3ea0857abf37316287",
                "id":1247,
                "tank_id":8,
                "vcf20":0,
                "tanker_act_out_amount":3626.45999999996,
                "altitude":0,
                "loss_amount":2.45999999996275,
                "fuel_standard_volum":3676,
                "experiment_density":850,
                "experiment_temperature":20,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-23 16:07:23",
                "belong_id":1,
                "fuel_name":"第T001号油罐",
                "fuel_temperature":20,
                "tank_out_amount":3624,
                "standard_density":850,
                "modify_time":"2017-12-18 20:51:36",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2689,
                "water_altitude":0,
                "fuel_volum":978,
                "record_type":3,
                "create_time":"2017-12-18 20:51:36",
                "tanker_out_amount":0,
                "hash":"373faed3a922fcaad1b75a64cedc8265",
                "id":1248,
                "tank_id":9,
                "vcf20":0,
                "tanker_act_out_amount":30.1699999999837,
                "altitude":0,
                "loss_amount":1008.16999999998,
                "fuel_standard_volum":978,
                "experiment_density":850,
                "experiment_temperature":8.4,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-23 09:22:00",
                "belong_id":1,
                "fuel_name":"第T002号油罐",
                "fuel_temperature":20,
                "tank_out_amount":-978,
                "standard_density":842,
                "modify_time":"2017-12-18 20:51:36",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2690,
                "water_altitude":0,
                "fuel_volum":561,
                "record_type":3,
                "create_time":"2017-12-18 20:51:36",
                "tanker_out_amount":0,
                "hash":"dfa301bc6d2b2e98478d58b824680839",
                "id":1249,
                "tank_id":9,
                "vcf20":0,
                "tanker_act_out_amount":27.1500000000233,
                "altitude":0,
                "loss_amount":-384.351999999977,
                "fuel_standard_volum":566.498,
                "experiment_density":850,
                "experiment_temperature":8.4,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-23 16:07:23",
                "belong_id":1,
                "fuel_name":"第T002号油罐",
                "fuel_temperature":8.4,
                "tank_out_amount":411.502,
                "standard_density":842,
                "modify_time":"2017-12-18 20:51:36",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2689,
                "water_altitude":0,
                "fuel_volum":19130.135,
                "record_type":3,
                "create_time":"2017-12-18 20:51:36",
                "tanker_out_amount":0,
                "hash":"9ab13250cc135a9eaf7e33321cf5703d",
                "id":1250,
                "tank_id":10,
                "vcf20":0,
                "tanker_act_out_amount":2154.35000000009,
                "altitude":1381.354,
                "loss_amount":21478.6560000001,
                "fuel_standard_volum":19324.306,
                "experiment_density":770,
                "experiment_temperature":20,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-23 09:22:00",
                "belong_id":1,
                "fuel_name":"第T003号油罐",
                "fuel_temperature":10.92,
                "tank_out_amount":-19324.306,
                "standard_density":770,
                "modify_time":"2017-12-18 20:51:36",
                "standard_temperature":0
            },
            {
                "receive_amount":0,
                "shift_control_id":2690,
                "water_altitude":0,
                "fuel_volum":17474.26,
                "record_type":3,
                "create_time":"2017-12-18 20:51:36",
                "tanker_out_amount":0,
                "hash":"9fe97b4b2f67318e872603b32d8aa012",
                "id":1251,
                "tank_id":10,
                "vcf20":0,
                "tanker_act_out_amount":1659.75,
                "altitude":1287.997,
                "loss_amount":-15.5540000000001,
                "fuel_standard_volum":17649.002,
                "experiment_density":770,
                "experiment_temperature":20,
                "send_amount":0,
                "back_tank_amount":0,
                "original_create_time":"2017-04-23 16:07:23",
                "belong_id":1,
                "fuel_name":"第T003号油罐",
                "fuel_temperature":11,
                "tank_out_amount":1675.304,
                "standard_density":770,
                "modify_time":"2017-12-18 20:51:36",
                "standard_temperature":0
            }
        ]
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

## **卸油次数**
```
GET /fuel/charge_times
```
### **Parameters**
* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "fuel_charges_times":[
            {
                "fuel_name":"第T003号油罐",
                "times":33
            },
            {
                "fuel_name":"第T002号油罐",
                "times":8
            },
            {
                "fuel_name":"第T004号油罐",
                "times":91
            },
            {
                "fuel_name":"第T001号油罐",
                "times":30
            }
        ]
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

## **提枪次数**
```
GET /fuel/tanker_times
```
### **Parameters**
* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "tanker_sell_times":[
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":3,
                "times":2708
            },
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":6,
                "times":1584
            },
            {
                "fuel_name":"95号 车用汽油(Ⅴ)",
                "tanker_id":1,
                "times":5930
            },
            {
                "fuel_name":"0号 车用柴油(Ⅴ)",
                "tanker_id":9,
                "times":1631
            },
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":5,
                "times":6519
            },
            {
                "fuel_name":"97号 车用汽油(Ⅳ)",
                "tanker_id":2,
                "times":24
            },
            {
                "fuel_name":"-20号 车用柴油(Ⅴ)",
                "tanker_id":7,
                "times":755
            },
            {
                "fuel_name":"95号 车用汽油(Ⅴ)",
                "tanker_id":2,
                "times":2122
            },
            {
                "fuel_name":"-20号 车用柴油(Ⅴ)",
                "tanker_id":8,
                "times":750
            },
            {
                "fuel_name":"97号 车用汽油(Ⅳ)",
                "tanker_id":1,
                "times":212
            },
            {
                "fuel_name":"0号 车用柴油(Ⅴ)",
                "tanker_id":10,
                "times":580
            },
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":4,
                "times":19695
            }
        ],
        "start_time":"2017-01-01 00:00:00",
        "end_time":"2017-08-08 23:59:59"
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

## **提枪次数**
```
GET /fuel/tanker_times
```
### **Parameters**
* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "tanker_sell_times":[
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":3,
                "times":2708
            },
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":6,
                "times":1584
            },
            {
                "fuel_name":"95号 车用汽油(Ⅴ)",
                "tanker_id":1,
                "times":5930
            },
            {
                "fuel_name":"0号 车用柴油(Ⅴ)",
                "tanker_id":9,
                "times":1631
            },
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":5,
                "times":6519
            },
            {
                "fuel_name":"97号 车用汽油(Ⅳ)",
                "tanker_id":2,
                "times":24
            },
            {
                "fuel_name":"-20号 车用柴油(Ⅴ)",
                "tanker_id":7,
                "times":755
            },
            {
                "fuel_name":"95号 车用汽油(Ⅴ)",
                "tanker_id":2,
                "times":2122
            },
            {
                "fuel_name":"-20号 车用柴油(Ⅴ)",
                "tanker_id":8,
                "times":750
            },
            {
                "fuel_name":"97号 车用汽油(Ⅳ)",
                "tanker_id":1,
                "times":212
            },
            {
                "fuel_name":"0号 车用柴油(Ⅴ)",
                "tanker_id":10,
                "times":580
            },
            {
                "fuel_name":"92号 车用汽油(Ⅴ)",
                "tanker_id":4,
                "times":19695
            }
        ],
        "start_time":"2017-01-01 00:00:00",
        "end_time":"2017-08-08 23:59:59"
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

## **油品消费类型**

```
GET /fuel/payments
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "start_time":"2017-01-01 00:00:00",
        "payments":[
            {
                "payment_type":"支付宝",
                "times":278
            },
            {
                "payment_type":"IC 卡",
                "times":11629
            },
            {
                "payment_type":"离线自用油卡",
                "times":2
            },
            {
                "payment_type":"现金",
                "times":23634
            },
            {
                "payment_type":"其他",
                "times":1905
            },
            {
                "payment_type":"银联卡",
                "times":4486
            },
            {
                "payment_type":"微信",
                "times":576
            }
        ],
        "end_time":"2017-10-09 23:59:59"
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



## **油品环比**

```
GET /fuel/sequential
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "current_data":{
            "start_time":"2017-03-01 00:00:00",
            "end_time":"2017-03-07 23:59:59",
            "contrast":[
                {
                    "fuel_type":"汽油",
                    "times":2607
                },
                {
                    "fuel_type":"柴油",
                    "times":285
                }
            ]
        },
        "last_data":{
            "start_time":"2017-02-20 00:00:00",
            "end_time":"2017-02-26 23:59:59",
            "contrast":[
                {
                    "fuel_type":"汽油",
                    "times":2521
                },
                {
                    "fuel_type":"柴油",
                    "times":194
                }
            ]
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

## **油品结构**

```
GET /fuel/composition
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "start_time":"2017-03-01 00:00:00",
        "summary":[
            {
                "fuel_type":"汽油",
                "amount":358
            },
            {
                "fuel_type":"柴油",
                "amount":43
            }
        ],
        "end_time":"2017-03-01 23:59:59",
        "detail":[
            {
                "fuel_type":"-20号 车用柴油(Ⅴ)",
                "amount":23
            },
            {
                "fuel_type":"0号 车用柴油(Ⅴ)",
                "amount":20
            },
            {
                "fuel_type":"92号 车用汽油(Ⅴ)",
                "amount":281
            },
            {
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "amount":77
            }
        ]
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

## **油品同比**

```
GET /fuel/compare
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "current_data":{
            "start_time":"2017-03-01 00:00:00",
            "end_time":"2017-03-07 23:59:59",
            "contrast":[
                {
                    "fuel_type":"汽油",
                    "times":2607
                },
                {
                    "fuel_type":"柴油",
                    "times":285
                }
            ]
        },
        "last_data":{
            "start_time":"2017-02-20 00:00:00",
            "end_time":"2017-02-26 23:59:59",
            "contrast":[
                {
                    "fuel_type":"汽油",
                    "times":2521
                },
                {
                    "fuel_type":"柴油",
                    "times":194
                }
            ]
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

## **油品销售对比数据**

```
GET /fuel/detail
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "start_time":"2017-03-01 00:00:00",
        "object_list":[
            {
                "amount":19,
                "total_price":2421,
                "fuel_type":"92号 车用汽油(Ⅴ)",
                "hour":19,
                "sales":373.57
            },
            {
                "amount":5,
                "total_price":1093.33,
                "fuel_type":"92号 车用汽油(Ⅴ)",
                "hour":20,
                "sales":170.1
            },
            {
                "amount":25,
                "total_price":5008.2,
                "fuel_type":"92号 车用汽油(Ⅴ)",
                "hour":21,
                "sales":772.855
            },
            {
                "amount":3,
                "total_price":450,
                "fuel_type":"92号 车用汽油(Ⅴ)",
                "hour":22,
                "sales":69.44
            },
            {
                "amount":3,
                "total_price":554.72,
                "fuel_type":"92号 车用汽油(Ⅴ)",
                "hour":23,
                "sales":86.15
            },
            {
                "amount":3,
                "total_price":955.83,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":0,
                "sales":139.45
            },
            {
                "amount":2,
                "total_price":484.19,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":7,
                "sales":70.07
            },
            {
                "amount":1,
                "total_price":30,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":8,
                "sales":4.317
            },
            {
                "amount":9,
                "total_price":1645.68,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":9,
                "sales":237.43
            },
            {
                "amount":4,
                "total_price":1357,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":10,
                "sales":195.72
            },
            {
                "amount":6,
                "total_price":2040.04,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":11,
                "sales":293.53
            },
            {
                "amount":3,
                "total_price":979.82,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":12,
                "sales":143.46
            },
            {
                "amount":3,
                "total_price":785.25,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":13,
                "sales":113.34
            },
            {
                "amount":8,
                "total_price":1896.35,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":14,
                "sales":272.87
            },
            {
                "amount":9,
                "total_price":3306.22,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":15,
                "sales":479.6
            },
            {
                "amount":5,
                "total_price":1520.68,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":16,
                "sales":220.903
            },
            {
                "amount":4,
                "total_price":949.9,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":17,
                "sales":137.39
            },
            {
                "amount":1,
                "total_price":350,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":18,
                "sales":50.72
            },
            {
                "amount":4,
                "total_price":1382.86,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":19,
                "sales":200.11
            },
            {
                "amount":4,
                "total_price":1019.02,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":20,
                "sales":148.17
            },
            {
                "amount":9,
                "total_price":2847,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":21,
                "sales":412.325
            },
            {
                "amount":1,
                "total_price":150,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":22,
                "sales":21.58
            },
            {
                "amount":1,
                "total_price":100,
                "fuel_type":"95号 车用汽油(Ⅴ)",
                "hour":23,
                "sales":14.39
            }
        ],
        "end_time":"2017-03-01 23:59:59"
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

## **非油消费类型**

```
GET /goods/payments
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "start_time":"2017-03-01 00:00:00",
        "object_list":[
            {
                "amount":17,
                "payment_type":"支付宝",
                "cls_name":[
                    {
                        "name":"包装饮料"
                    },
                    {
                        "name":"糖果"
                    },
                    {
                        "name":"家庭食品"
                    },
                    {
                        "name":"饼干/糕点"
                    }
                ]
            },
            {
                "amount":31,
                "payment_type":"积分消费",
                "cls_name":[
                    {
                        "name":"香烟"
                    },
                    {
                        "name":"包装饮料"
                    },
                    {
                        "name":"奶类"
                    },
                    {
                        "name":"糖果"
                    },
                    {
                        "name":"零食"
                    },
                    {
                        "name":"家庭食品"
                    },
                    {
                        "name":"饼干/糕点"
                    },
                    {
                        "name":"日用品"
                    },
                    {
                        "name":"清洁用品"
                    },
                    {
                        "name":"个人护理用品"
                    },
                    {
                        "name":"汽车用品"
                    }
                ]
            },
            {
                "amount":41,
                "payment_type":"IC 卡",
                "cls_name":[
                    {
                        "name":"香烟"
                    },
                    {
                        "name":"包装饮料"
                    },
                    {
                        "name":"奶类"
                    },
                    {
                        "name":"糖果"
                    },
                    {
                        "name":"零食"
                    },
                    {
                        "name":"家庭食品"
                    },
                    {
                        "name":"饼干/糕点"
                    },
                    {
                        "name":"面包"
                    },
                    {
                        "name":"清洁用品"
                    },
                    {
                        "name":"个人护理用品"
                    },
                    {
                        "name":"汽车用品"
                    }
                ]
            },
            {
                "amount":1273,
                "payment_type":"现金",
                "cls_name":[
                    {
                        "name":"香烟"
                    },
                    {
                        "name":"包装饮料"
                    },
                    {
                        "name":"奶类"
                    },
                    {
                        "name":"酒类"
                    },
                    {
                        "name":"糖果"
                    },
                    {
                        "name":"零食"
                    },
                    {
                        "name":"家庭食品"
                    },
                    {
                        "name":"饼干/糕点"
                    },
                    {
                        "name":"面包"
                    },
                    {
                        "name":"速食"
                    },
                    {
                        "name":"日用品"
                    },
                    {
                        "name":"清洁用品"
                    },
                    {
                        "name":"个人护理用品"
                    },
                    {
                        "name":"药品/计生/保健"
                    },
                    {
                        "name":"汽车用品"
                    },
                    {
                        "name":"润滑油"
                    }
                ]
            },
            {
                "amount":1,
                "payment_type":"其他",
                "cls_name":[
                    {
                        "name":"包装饮料"
                    }
                ]
            },
            {
                "amount":62,
                "payment_type":"微信",
                "cls_name":[
                    {
                        "name":"香烟"
                    },
                    {
                        "name":"包装饮料"
                    },
                    {
                        "name":"奶类"
                    },
                    {
                        "name":"酒类"
                    },
                    {
                        "name":"糖果"
                    },
                    {
                        "name":"零食"
                    },
                    {
                        "name":"家庭食品"
                    },
                    {
                        "name":"饼干/糕点"
                    },
                    {
                        "name":"面包"
                    },
                    {
                        "name":"速食"
                    },
                    {
                        "name":"个人护理用品"
                    },
                    {
                        "name":"汽车用品"
                    }
                ]
            },
            {
                "amount":93,
                "payment_type":"银联卡",
                "cls_name":[
                    {
                        "name":"香烟"
                    },
                    {
                        "name":"包装饮料"
                    },
                    {
                        "name":"奶类"
                    },
                    {
                        "name":"糖果"
                    },
                    {
                        "name":"零食"
                    },
                    {
                        "name":"家庭食品"
                    },
                    {
                        "name":"饼干/糕点"
                    },
                    {
                        "name":"速食"
                    },
                    {
                        "name":"清洁用品"
                    },
                    {
                        "name":"个人护理用品"
                    }
                ]
            }
        ],
        "end_time":"2017-04-01 23:59:59"
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