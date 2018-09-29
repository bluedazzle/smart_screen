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


## **总总览**

```
POST /api/v1/overview/
```

### **Parameters**


### **Return**

成功
```
{
    "body":{
        "fuel":[
            {
                "amount":13910.97,
                "cls_name":"汽油"
            },
            {
                "amount":1267.32,
                "cls_name":"柴油"
            }
        ],
        "card":[
            {
                "total":48992.43,
                "cls_name":"汽油"
            },
            {
                "total":7494.42,
                "cls_name":"柴油"
            },
            {
                "total":1021.5,
                "cls_name":"非油"
            }
        ],
        "unit":{
            "amount_unit":"升",
            "total_unit":"元"
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



## **当日油品销售预测**

```
GET /fuel/predict
```

### **Parameters**


### **Return**

成功
```
{
    "body":{
        "fuel_predict_list":[
            {
                "predict_str":"低峰期",
                "is_peak":false,
                "average":0.0625,
                "predict_list":[
                    {
                        "amount":0,
                        "hour":0
                    },
                    {
                        "amount":0,
                        "hour":1
                    },
                    {
                        "amount":0,
                        "hour":2
                    },
                    {
                        "amount":0,
                        "hour":3
                    },
                    {
                        "amount":0,
                        "hour":4
                    },
                    {
                        "amount":0,
                        "hour":5
                    },
                    {
                        "amount":0,
                        "hour":6
                    },
                    {
                        "amount":0,
                        "hour":7
                    },
                    {
                        "amount":0,
                        "hour":8
                    },
                    {
                        "amount":0,
                        "hour":9
                    },
                    {
                        "amount":0,
                        "hour":10
                    },
                    {
                        "amount":0,
                        "hour":11
                    },
                    {
                        "amount":0,
                        "hour":12
                    },
                    {
                        "amount":0,
                        "hour":13
                    },
                    {
                        "amount":0,
                        "hour":14
                    },
                    {
                        "amount":1,
                        "hour":15
                    },
                    {
                        "amount":0,
                        "hour":16
                    },
                    {
                        "amount":0,
                        "hour":17
                    },
                    {
                        "amount":0,
                        "hour":18
                    },
                    {
                        "amount":0,
                        "hour":19
                    },
                    {
                        "amount":0,
                        "hour":20
                    },
                    {
                        "amount":0,
                        "hour":21
                    },
                    {
                        "amount":0,
                        "hour":22
                    },
                    {
                        "amount":0,
                        "hour":23
                    }
                ],
                "fuel_name":"-20号 车用柴油(Ⅴ)"
            },
            {
                "predict_str":"低峰期",
                "is_peak":false,
                "average":1.4583333333333333,
                "predict_list":[
                    {
                        "amount":0,
                        "hour":0
                    },
                    {
                        "amount":0,
                        "hour":1
                    },
                    {
                        "amount":0,
                        "hour":2
                    },
                    {
                        "amount":0,
                        "hour":3
                    },
                    {
                        "amount":0,
                        "hour":4
                    },
                    {
                        "amount":0,
                        "hour":5
                    },
                    {
                        "amount":1,
                        "hour":6
                    },
                    {
                        "amount":2,
                        "hour":7
                    },
                    {
                        "amount":2,
                        "hour":8
                    },
                    {
                        "amount":4,
                        "hour":9
                    },
                    {
                        "amount":2,
                        "hour":10
                    },
                    {
                        "amount":5,
                        "hour":11
                    },
                    {
                        "amount":3,
                        "hour":12
                    },
                    {
                        "amount":1,
                        "hour":13
                    },
                    {
                        "amount":0,
                        "hour":14
                    },
                    {
                        "amount":0,
                        "hour":15
                    },
                    {
                        "amount":1,
                        "hour":16
                    },
                    {
                        "amount":1,
                        "hour":17
                    },
                    {
                        "amount":2,
                        "hour":18
                    },
                    {
                        "amount":1,
                        "hour":19
                    },
                    {
                        "amount":2,
                        "hour":20
                    },
                    {
                        "amount":2,
                        "hour":21
                    },
                    {
                        "amount":0,
                        "hour":22
                    },
                    {
                        "amount":1,
                        "hour":23
                    }
                ],
                "fuel_name":"0号 车用柴油(Ⅴ)"
            },
            {
                "predict_str":"高峰期",
                "is_peak":true,
                "average":13.604166666666666,
                "predict_list":[
                    {
                        "amount":1,
                        "hour":0
                    },
                    {
                        "amount":0,
                        "hour":1
                    },
                    {
                        "amount":5,
                        "hour":2
                    },
                    {
                        "amount":1,
                        "hour":3
                    },
                    {
                        "amount":0,
                        "hour":4
                    },
                    {
                        "amount":2,
                        "hour":5
                    },
                    {
                        "amount":5,
                        "hour":6
                    },
                    {
                        "amount":24,
                        "hour":7
                    },
                    {
                        "amount":16,
                        "hour":8
                    },
                    {
                        "amount":28,
                        "hour":9
                    },
                    {
                        "amount":12,
                        "hour":10
                    },
                    {
                        "amount":19,
                        "hour":11
                    },
                    {
                        "amount":14,
                        "hour":12
                    },
                    {
                        "amount":29,
                        "hour":13
                    },
                    {
                        "amount":16,
                        "hour":14
                    },
                    {
                        "amount":30,
                        "hour":15
                    },
                    {
                        "amount":20,
                        "hour":16
                    },
                    {
                        "amount":19,
                        "hour":17
                    },
                    {
                        "amount":19,
                        "hour":18
                    },
                    {
                        "amount":15,
                        "hour":19
                    },
                    {
                        "amount":13,
                        "hour":20
                    },
                    {
                        "amount":18,
                        "hour":21
                    },
                    {
                        "amount":9,
                        "hour":22
                    },
                    {
                        "amount":6,
                        "hour":23
                    }
                ],
                "fuel_name":"92号 车用汽油(Ⅴ)"
            },
            {
                "predict_str":"高峰期",
                "is_peak":true,
                "average":3.25,
                "predict_list":[
                    {
                        "amount":0,
                        "hour":0
                    },
                    {
                        "amount":0,
                        "hour":1
                    },
                    {
                        "amount":0,
                        "hour":2
                    },
                    {
                        "amount":0,
                        "hour":3
                    },
                    {
                        "amount":0,
                        "hour":4
                    },
                    {
                        "amount":0,
                        "hour":5
                    },
                    {
                        "amount":0,
                        "hour":6
                    },
                    {
                        "amount":2,
                        "hour":7
                    },
                    {
                        "amount":2,
                        "hour":8
                    },
                    {
                        "amount":13,
                        "hour":9
                    },
                    {
                        "amount":3,
                        "hour":10
                    },
                    {
                        "amount":2,
                        "hour":11
                    },
                    {
                        "amount":3,
                        "hour":12
                    },
                    {
                        "amount":5,
                        "hour":13
                    },
                    {
                        "amount":5,
                        "hour":14
                    },
                    {
                        "amount":13,
                        "hour":15
                    },
                    {
                        "amount":8,
                        "hour":16
                    },
                    {
                        "amount":6,
                        "hour":17
                    },
                    {
                        "amount":2,
                        "hour":18
                    },
                    {
                        "amount":4,
                        "hour":19
                    },
                    {
                        "amount":4,
                        "hour":20
                    },
                    {
                        "amount":2,
                        "hour":21
                    },
                    {
                        "amount":0,
                        "hour":22
                    },
                    {
                        "amount":0,
                        "hour":23
                    }
                ],
                "fuel_name":"95号 车用汽油(Ⅴ)"
            }
        ],
        "start_time":"2017-04-23 00:00:00",
        "end_time":"2017-04-23 23:59:59"
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
* type(_Optional_|string)-环比类型

|type 取值|含义|
| --------------  | :---: |
|month|月环比|
|week|周环比|
|day|日环比|

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


## **油品月环比**

```
GET /fuel/month/sequential
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


## **油品计划**

```
GET /fuel/plan
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
        "object_list":[
            {
                "sell":302.880269000007,
                "fuel_type":"汽油",
                "plan":1000,
                "month":1
            },
            {
                "sell":101.16626,
                "fuel_type":"柴油",
                "plan":1000,
                "month":1
            },
            {
                "sell":98.5780079999999,
                "fuel_type":"柴油",
                "plan":1000,
                "month":2
            },
            {
                "sell":281.439814999984,
                "fuel_type":"汽油",
                "plan":1000,
                "month":2
            },
            {
                "sell":354.58253299997995,
                "fuel_type":"汽油",
                "plan":1000,
                "month":3
            },
            {
                "sell":212.988713,
                "fuel_type":"柴油",
                "plan":1000,
                "month":3
            },
            {
                "sell":347.592158999994,
                "fuel_type":"汽油",
                "plan":2000,
                "month":4
            },
            {
                "sell":194.91588000000002,
                "fuel_type":"柴油",
                "plan":2000,
                "month":4
            }
        ],
        "page_obj":{

        },
        "end_time":"2017-10-22 00:00:00"
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
* type(_Optional_|string)-同比类型


|type 取值|含义|
| --------------  | :---: |
|year|年同比|
|month|月同比|
|custom|自定义同比|

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


## **非油分类销售统计**

```
GET /goods/sell/classification
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
        "object_list":[
            {
                "total_income":57,
                "amount":11,
                "cls_name":"饼干/糕点"
            },
            {
                "total_income":673,
                "amount":32,
                "cls_name":"零食"
            },
            {
                "total_income":611.5,
                "amount":58,
                "cls_name":"糖果"
            },
            {
                "total_income":46,
                "amount":8,
                "cls_name":"速食"
            },
            {
                "total_income":1485,
                "amount":126,
                "cls_name":"包装饮料"
            },
            {
                "total_income":26,
                "amount":2,
                "cls_name":"面包"
            },
            {
                "total_income":287,
                "amount":6,
                "cls_name":"汽车用品"
            },
            {
                "total_income":4596,
                "amount":60,
                "cls_name":"香烟"
            },
            {
                "total_income":100,
                "amount":1,
                "cls_name":"润滑油"
            },
            {
                "total_income":186.8,
                "amount":4,
                "cls_name":"清洁用品"
            },
            {
                "total_income":29,
                "amount":3,
                "cls_name":"酒类"
            },
            {
                "total_income":316.5,
                "amount":9,
                "cls_name":"家庭食品"
            },
            {
                "total_income":2.5,
                "amount":4,
                "cls_name":"日用品"
            },
            {
                "total_income":430.5,
                "amount":15,
                "cls_name":"个人护理用品"
            },
            {
                "total_income":281,
                "amount":13,
                "cls_name":"奶类"
            }
        ],
        "end_time":"2017-02-10 00:00:00"
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


## **非油销售排行**

```
GET /goods/sell/rank
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
        "object_list":[
            {
                "data":[
                    {
                        "amount":43,
                        "name":"红牛 维生素功能饮料（原味型） 250ml",
                        "income":810
                    },
                    {
                        "amount":22,
                        "name":"百事可乐 汽水 600ML",
                        "income":115.5
                    },
                    {
                        "amount":18,
                        "name":"农夫山泉 茶Π蜜桃乌龙茶 500ML",
                        "income":126.5
                    },
                    {
                        "amount":13,
                        "name":"脉动 维生素饮料荔枝口味 600ML",
                        "income":81
                    },
                    {
                        "amount":12,
                        "name":"农夫山泉 茶Π柚子绿茶 500ML",
                        "income":88
                    },
                    {
                        "amount":11,
                        "name":"农夫山泉 茶Π柠檬红茶 500ML",
                        "income":82.5
                    },
                    {
                        "amount":10,
                        "name":"康师傅 茉莉蜜茶 550ml",
                        "income":42
                    },
                    {
                        "amount":10,
                        "name":"露露 露露 480ML",
                        "income":84
                    },
                    {
                        "amount":10,
                        "name":"农夫山泉 天然水（24瓶1箱） 380ML",
                        "income":64.5
                    },
                    {
                        "amount":9,
                        "name":"尖叫 (纤维)功能饮料 550ML",
                        "income":45
                    },
                    {
                        "amount":9,
                        "name":"农夫山泉 果味水葡萄 530ML",
                        "income":52
                    },
                    {
                        "amount":9,
                        "name":"健力宝 银标橙蜜味 560ml",
                        "income":49
                    },
                    {
                        "amount":9,
                        "name":"农夫山泉 茶Π西柚茉莉花茶 500ML",
                        "income":55
                    },
                    {
                        "amount":8,
                        "name":"红牛 维生素功能饮料（牛磺酸强化型） 250m",
                        "income":80
                    },
                    {
                        "amount":8,
                        "name":"康师傅 蜂蜜茉莉绿茶 550ML",
                        "income":42
                    },
                    {
                        "amount":8,
                        "name":"屈臣氏 香草味苏打水 330ML",
                        "income":192.5
                    },
                    {
                        "amount":8,
                        "name":"农夫山泉 东方树叶绿茶 500ML",
                        "income":40
                    },
                    {
                        "amount":7,
                        "name":"雀巢 咖啡(香滑即饮) 180ML",
                        "income":48
                    },
                    {
                        "amount":7,
                        "name":"康师傅 鲜果橙 450ML",
                        "income":36
                    },
                    {
                        "amount":7,
                        "name":"恒大 冰泉长白山天然矿泉水 500ML",
                        "income":22.5
                    },
                    {
                        "amount":7,
                        "name":"康师傅 包装饮用水 550ml",
                        "income":33
                    },
                    {
                        "amount":7,
                        "name":"农夫山泉 饮用天然水 550ML",
                        "income":22
                    },
                    {
                        "amount":6,
                        "name":"农夫山泉 东方树叶茉莉花茶 500ML",
                        "income":28
                    },
                    {
                        "amount":6,
                        "name":"冰峰 汽水 330ML",
                        "income":21
                    },
                    {
                        "amount":5,
                        "name":"农夫山泉 果味水柚子 530ML",
                        "income":28
                    },
                    {
                        "amount":5,
                        "name":"露露 杏仁露 240ML",
                        "income":132
                    },
                    {
                        "amount":5,
                        "name":"昆仑山 天然雪山矿泉水 510ML",
                        "income":30
                    },
                    {
                        "amount":5,
                        "name":"康师傅 茉莉清茶 550ml",
                        "income":21
                    },
                    {
                        "amount":5,
                        "name":"统一 小茗同学茉莉萃茶 480ML",
                        "income":30
                    },
                    {
                        "amount":5,
                        "name":"农夫山泉 天然矿泉水 535ML",
                        "income":28
                    },
                    {
                        "amount":4,
                        "name":"尖叫 (活性肽)功能饮料 550ML",
                        "income":22.5
                    },
                    {
                        "amount":4,
                        "name":"果倍爽 橙汁 330ML",
                        "income":36
                    },
                    {
                        "amount":4,
                        "name":"脉动 维生素饮料水蜜桃口味 600ML",
                        "income":31.5
                    },
                    {
                        "amount":4,
                        "name":"脉动 维生素饮料青柠口味 600ML",
                        "income":18
                    },
                    {
                        "amount":4,
                        "name":"屈臣氏 苏打水 330ML",
                        "income":55
                    },
                    {
                        "amount":4,
                        "name":"加多宝 金罐凉茶 310ML",
                        "income":136
                    },
                    {
                        "amount":3,
                        "name":"果倍爽 樱桃复合果汁 330ML",
                        "income":30
                    },
                    {
                        "amount":3,
                        "name":"统一 小茗同学青柠红茶 480ML",
                        "income":22
                    },
                    {
                        "amount":3,
                        "name":"特丽娜 水蜜桃果肉饮料 240ML",
                        "income":28
                    },
                    {
                        "amount":2,
                        "name":"怪兽 维生素果味饮料 280ML",
                        "income":30
                    },
                    {
                        "amount":2,
                        "name":"统一 海之言柠檬味 500ML",
                        "income":9
                    },
                    {
                        "amount":2,
                        "name":"农夫山泉 水溶C100柠檬汁 445ML",
                        "income":15
                    },
                    {
                        "amount":2,
                        "name":"怡宝 纯净水 555ML （24瓶每箱）",
                        "income":10
                    },
                    {
                        "amount":2,
                        "name":"可口可乐 汽水 330ml",
                        "income":62.5
                    },
                    {
                        "amount":2,
                        "name":"昆仑山 天然雪山矿泉水 350ML",
                        "income":112.5
                    },
                    {
                        "amount":2,
                        "name":"统一 小茗同学溜溜哒茶 480ML",
                        "income":12
                    },
                    {
                        "amount":2,
                        "name":"农夫山泉 饮用天然水 750ML",
                        "income":5
                    },
                    {
                        "amount":2,
                        "name":"昆仑好客 青藏冰川天然矿泉水 420ml",
                        "income":8
                    },
                    {
                        "amount":1,
                        "name":"统一 海之言水蜜桃味 500ML",
                        "income":4.5
                    },
                    {
                        "amount":1,
                        "name":"果倍爽 梨汁 200ML",
                        "income":9
                    }
                ],
                "cls_name":"包装饮料"
            },
            {
                "data":[
                    {
                        "amount":75,
                        "name":"芙蓉王 (硬) 20支",
                        "income":8200
                    },
                    {
                        "amount":57,
                        "name":"兰州 硬盒香烟(包) 11MG",
                        "income":2610
                    },
                    {
                        "amount":19,
                        "name":"利群 (新版) 20支",
                        "income":1736
                    },
                    {
                        "amount":14,
                        "name":"云烟 12mg",
                        "income":620
                    },
                    {
                        "amount":12,
                        "name":"云烟 (软珍品) 20支",
                        "income":1863
                    },
                    {
                        "amount":12,
                        "name":"中华 (软) 20支",
                        "income":3990
                    },
                    {
                        "amount":9,
                        "name":"红塔山 经典100 20支",
                        "income":140
                    },
                    {
                        "amount":7,
                        "name":"黄鹤楼 软蓝(包) 12mg",
                        "income":228
                    },
                    {
                        "amount":7,
                        "name":"兰州 (16支吉祥) 20支",
                        "income":580
                    },
                    {
                        "amount":6,
                        "name":"兰州 (硬吉祥) 11MG",
                        "income":750
                    },
                    {
                        "amount":4,
                        "name":"苏烟 (软金砂) 20支",
                        "income":1104
                    },
                    {
                        "amount":4,
                        "name":"中华 (硬) 20支",
                        "income":1530
                    },
                    {
                        "amount":4,
                        "name":"芙蓉王 (软蓝) 20支",
                        "income":420
                    },
                    {
                        "amount":4,
                        "name":"延安 硬醇和 10MG",
                        "income":70
                    },
                    {
                        "amount":3,
                        "name":"红旗渠 (银河之光) 20支",
                        "income":275
                    },
                    {
                        "amount":3,
                        "name":"兰州 (桥) 硬盒香烟(包) 6MG",
                        "income":252
                    },
                    {
                        "amount":3,
                        "name":"泰山 (宏图) 20支",
                        "income":341
                    },
                    {
                        "amount":3,
                        "name":"南京 (特醇) 条",
                        "income":360
                    },
                    {
                        "amount":3,
                        "name":"芙蓉王 软黄 8MG",
                        "income":160
                    },
                    {
                        "amount":3,
                        "name":"芙蓉王 (蓝) 20支",
                        "income":770
                    },
                    {
                        "amount":2,
                        "name":"黄鹤楼 (大彩)硬盒 12MG",
                        "income":330
                    },
                    {
                        "amount":2,
                        "name":"黄鹤楼天下名楼8MG",
                        "income":32
                    },
                    {
                        "amount":2,
                        "name":"玉溪 (软) 20支",
                        "income":92
                    },
                    {
                        "amount":1,
                        "name":"红塔山 (经典1956) 20支",
                        "income":7.5
                    },
                    {
                        "amount":1,
                        "name":"云烟 (大紫) 8MG",
                        "income":14
                    },
                    {
                        "amount":1,
                        "name":"娇子 娇子 蓝色(包)13MG 13MG",
                        "income":13
                    },
                    {
                        "amount":1,
                        "name":"南京 金陵十二钗 0.6MG",
                        "income":66
                    },
                    {
                        "amount":1,
                        "name":"云烟 (印象)香烟",
                        "income":65
                    },
                    {
                        "amount":1,
                        "name":"苏烟 五星红杉树 20支",
                        "income":22
                    },
                    {
                        "amount":1,
                        "name":"兰州 经典硬",
                        "income":30
                    },
                    {
                        "amount":1,
                        "name":"泰山 拂光细支 25支 6MG",
                        "income":80
                    },
                    {
                        "amount":1,
                        "name":"云烟 细支祥瑞 10MG",
                        "income":230
                    },
                    {
                        "amount":1,
                        "name":"大熊猫 (硬时代) 20支",
                        "income":85
                    },
                    {
                        "amount":1,
                        "name":"玉溪 (硬) 20支",
                        "income":230
                    }
                ],
                "cls_name":"香烟"
            },
            {
                "data":[
                    {
                        "amount":55,
                        "name":"箭牌 真知棒果汁什锦108支罐装 10.5G",
                        "income":47.5
                    },
                    {
                        "amount":17,
                        "name":"箭牌 绿箭 五片装",
                        "income":28.5
                    },
                    {
                        "amount":7,
                        "name":"酷滋 无糖薄荷糖荔枝味 21g",
                        "income":77
                    },
                    {
                        "amount":6,
                        "name":"士力架 花生夹心巧克力 51G",
                        "income":67.5
                    },
                    {
                        "amount":6,
                        "name":"酷兹 压片薄荷糖 野莓味 21G",
                        "income":66
                    },
                    {
                        "amount":5,
                        "name":"益达 西瓜 五片装",
                        "income":17.5
                    },
                    {
                        "amount":5,
                        "name":"酷滋 无糖薄荷糖水蜜桃味 21g",
                        "income":55
                    },
                    {
                        "amount":5,
                        "name":"费列罗 榛果威化巧克力16粒装 200g",
                        "income":468
                    },
                    {
                        "amount":4,
                        "name":"绿箭 无糖黑加仑薄荷口味 35粒",
                        "income":60
                    },
                    {
                        "amount":4,
                        "name":"德芙 丝滑牛奶巧克力 80G",
                        "income":60
                    },
                    {
                        "amount":4,
                        "name":"箭牌 薄荷糖铁盒装35粒留兰香 23.8g",
                        "income":42
                    },
                    {
                        "amount":4,
                        "name":"益达 清爽草莓木糖醇 56G",
                        "income":60
                    },
                    {
                        "amount":4,
                        "name":"脆香米 脆米心牛奶巧克力 24G",
                        "income":14
                    },
                    {
                        "amount":4,
                        "name":"德芙 M&M牛奶 40G",
                        "income":27.5
                    },
                    {
                        "amount":4,
                        "name":"酷兹 咀嚼薄荷糖柠檬味 52G",
                        "income":52
                    },
                    {
                        "amount":4,
                        "name":"好时 牛奶巧克力排块 23G",
                        "income":18
                    },
                    {
                        "amount":3,
                        "name":"德芙 黑巧克力 43G",
                        "income":110.5
                    },
                    {
                        "amount":3,
                        "name":"5 酷酸草莓味 12片",
                        "income":24
                    },
                    {
                        "amount":3,
                        "name":"德芙 榛仁、巴旦木及葡萄干巧克力 43G",
                        "income":102
                    },
                    {
                        "amount":3,
                        "name":"M&M'S 迷你筒装巧克力 30.6G",
                        "income":30
                    },
                    {
                        "amount":3,
                        "name":"德芙 草莓曲奇白巧克力 42G",
                        "income":108
                    },
                    {
                        "amount":3,
                        "name":"益达 青桔汽水味12片装 32G",
                        "income":24
                    },
                    {
                        "amount":3,
                        "name":"酷滋 无糖薄荷糖柠檬味 21g",
                        "income":33
                    },
                    {
                        "amount":2,
                        "name":"益达 木糖醇香橙薄荷瓶装 40粒",
                        "income":24
                    },
                    {
                        "amount":2,
                        "name":"好时 曲奇奶香巧克力排块 23G",
                        "income":13.5
                    },
                    {
                        "amount":2,
                        "name":"德芙 抹茶曲奇白巧克力 42G",
                        "income":18
                    },
                    {
                        "amount":2,
                        "name":"费列罗 榛果威化巧克力 8粒心型装",
                        "income":120
                    },
                    {
                        "amount":2,
                        "name":"好丽友 木糖醇花香混合味 101G",
                        "income":34
                    },
                    {
                        "amount":2,
                        "name":"雅客 益牙木糖醇蓝莓味 56G",
                        "income":22
                    },
                    {
                        "amount":2,
                        "name":"酷滋 咀嚼薄荷糖水蜜桃味 52g",
                        "income":26
                    },
                    {
                        "amount":1,
                        "name":"德芙 柠檬曲奇白巧克力 42G",
                        "income":18
                    },
                    {
                        "amount":1,
                        "name":"酷兹 咀嚼薄荷糖绿豆沙味 52G",
                        "income":13
                    },
                    {
                        "amount":1,
                        "name":"益达 无糖口香糖热带水果味12片装 12G",
                        "income":6
                    },
                    {
                        "amount":1,
                        "name":"益达 木糖醇香浓蜜瓜瓶装 40粒",
                        "income":12
                    },
                    {
                        "amount":1,
                        "name":"德芙 榛子巧克力 43G",
                        "income":8.5
                    },
                    {
                        "amount":1,
                        "name":"彩虹糖 原味迷你桶装 30G",
                        "income":5
                    },
                    {
                        "amount":1,
                        "name":"益达 木糖醇无糖口香糖清爽西瓜味40粒瓶装",
                        "income":12
                    }
                ],
                "cls_name":"糖果"
            },
            {
                "data":[
                    {
                        "amount":9,
                        "name":"上好佳 鲜虾条特惠装 110G",
                        "income":58.5
                    },
                    {
                        "amount":7,
                        "name":"广文 麻辣锅巴 110G",
                        "income":32
                    },
                    {
                        "amount":7,
                        "name":"金丝猴 麦丽素 80g",
                        "income":42
                    },
                    {
                        "amount":5,
                        "name":"喜之郎 黄桃果肉果冻 200G",
                        "income":31.5
                    },
                    {
                        "amount":5,
                        "name":"NATUNA乳酪圈 60G",
                        "income":37.5
                    },
                    {
                        "amount":5,
                        "name":"NATUNA香脆虾条 60G",
                        "income":45
                    },
                    {
                        "amount":4,
                        "name":"金鸽 多味葵花子 160G",
                        "income":30
                    },
                    {
                        "amount":4,
                        "name":"米老头 时尚法式簿饼(香橙) 150G",
                        "income":22
                    },
                    {
                        "amount":3,
                        "name":"好丽友 呀土豆蜂蜜黄油味 40G",
                        "income":12
                    },
                    {
                        "amount":3,
                        "name":"有友 泡凤爪 100G",
                        "income":24
                    },
                    {
                        "amount":3,
                        "name":"热烈 易拉罐焦糖爆米花 150G",
                        "income":45
                    },
                    {
                        "amount":3,
                        "name":"东宝 有机落花生 200G",
                        "income":27
                    },
                    {
                        "amount":3,
                        "name":"佳宝 山楂片水蜜桃纸包装 165G",
                        "income":30
                    },
                    {
                        "amount":3,
                        "name":"米老头 青稞米棒花生味 150g",
                        "income":18
                    },
                    {
                        "amount":2,
                        "name":"米老头 蛋黄煎饼原味 150G",
                        "income":14
                    },
                    {
                        "amount":2,
                        "name":"劲仔 劲仔鱼（麻辣） 12G",
                        "income":9
                    },
                    {
                        "amount":2,
                        "name":"米老头 满嘴香青稞米棒（芝麻味） 150G",
                        "income":12
                    },
                    {
                        "amount":1,
                        "name":"可可西里 藏牦牛肉干咖喱味 210G",
                        "income":220
                    },
                    {
                        "amount":1,
                        "name":"小王子 紫薯雪饼 84G",
                        "income":4
                    },
                    {
                        "amount":1,
                        "name":"可可西里 藏牦牛肉干五香味 210G",
                        "income":220
                    },
                    {
                        "amount":1,
                        "name":"可可西里 藏牦牛肉干 果糖 麻辣味 150G",
                        "income":48
                    },
                    {
                        "amount":1,
                        "name":"三江雪 黑玫瑰葡萄干(瓶) 210G",
                        "income":25
                    },
                    {
                        "amount":1,
                        "name":"劲仔 劲仔鱼（糖醋） 12G",
                        "income":30
                    },
                    {
                        "amount":1,
                        "name":"可可西里 手撕牦牛肉 香辣味 150G",
                        "income":234
                    },
                    {
                        "amount":1,
                        "name":"小王子 薯片原味 108G",
                        "income":7
                    }
                ],
                "cls_name":"零食"
            },
            {
                "data":[
                    {
                        "amount":13,
                        "name":"金锣 王中王 70g",
                        "income":82.5
                    },
                    {
                        "amount":9,
                        "name":"康师傅香辣牛肉面109g/桶",
                        "income":70
                    },
                    {
                        "amount":7,
                        "name":"龙涎香 香卤蛋 35G",
                        "income":34.5
                    },
                    {
                        "amount":6,
                        "name":"康师傅油泼辣子酸汤面122g/桶",
                        "income":40
                    },
                    {
                        "amount":6,
                        "name":"康师傅 油辣子麻辣牛肉桶面 111G",
                        "income":55
                    },
                    {
                        "amount":4,
                        "name":"康师傅香菇炖鸡面101g/桶",
                        "income":25
                    },
                    {
                        "amount":2,
                        "name":"有友 山椒竹笋 120G",
                        "income":9
                    },
                    {
                        "amount":2,
                        "name":"康师傅 红烧牛肉桶面 108G",
                        "income":15
                    },
                    {
                        "amount":1,
                        "name":"巧面馆 方便面老坛酸菜牛肉味 135g",
                        "income":8
                    }
                ],
                "cls_name":"速食"
            }
        ],
        "end_time":"2017-02-10 00:00:00"
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


## **非油客单价**

```
GET /goods/guest/unit_price
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
        "object_list":[
            {
                "amount":1485,
                "month":1,
                "income":51998.7
            },
            {
                "amount":172,
                "month":2,
                "income":5958
            }
        ],
        "end_time":"2017-02-10 00:00:00"
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


## **油非转换率**

```
GET /goods/guest/conversion
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
        "object_list":[
            {
                "fuel_total":13024,
                "conversion":0.11402027027027027,
                "goods_total":1485,
                "month":1
            },
            {
                "fuel_total":2888,
                "conversion":0.1038781163434903,
                "goods_total":300,
                "month":2
            }
        ],
        "end_time":"2017-02-10 00:00:00"
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


## **吨油非油分析**

```
GET /goods/fuel/compare
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "start_time":"2017-02-01 00:00:00",
        "object_list":[
            {
                "conversion":2.0425040555052747,
                "goods_total_income":18,
                "day":1,
                "fuel_total_amount":8.812712
            },
            {
                "conversion":161.00016550141828,
                "goods_total_income":2003,
                "day":2,
                "fuel_total_amount":12.440980999999999
            },
            {
                "conversion":163.89821815429045,
                "goods_total_income":1635.5,
                "day":3,
                "fuel_total_amount":9.97875400000001
            },
            {
                "conversion":119.29655589198931,
                "goods_total_income":1306,
                "day":4,
                "fuel_total_amount":10.947508
            },
            {
                "conversion":162.1663787780796,
                "goods_total_income":1858.5,
                "day":5,
                "fuel_total_amount":11.460452
            },
            {
                "conversion":71.65241486235583,
                "goods_total_income":936.5,
                "day":6,
                "fuel_total_amount":13.070041
            },
            {
                "conversion":88.47625504142297,
                "goods_total_income":1039.5,
                "day":7,
                "fuel_total_amount":11.748915
            },
            {
                "conversion":49.6022887337129,
                "goods_total_income":430.5,
                "day":8,
                "fuel_total_amount":8.679035
            },
            {
                "conversion":45.87219697168516,
                "goods_total_income":624,
                "day":9,
                "fuel_total_amount":13.603011
            }
        ],
        "end_time":"2017-02-10 00:00:00"
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


## **商品品效**

```
GET /goods/product/effect
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
        "object_list":[
            {
                "item_num":6381,
                "month":1,
                "product_effect":8.14898918664786,
                "income":51998.7
            },
            {
                "item_num":6381,
                "month":2,
                "product_effect":1.5438802695502272,
                "income":9851.5
            }
        ],
        "end_time":"2017-02-10 00:00:00"
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


## **商品搜索**

```
GET /goods/search/item/
```

### **Parameters**

* search(_Required_|string)-搜索条件

### **Return**

成功
```
{
    "body":{
        "goodsinventory_list":[
            {
                "barcode":"70219191",
                "name":"乐虎 牛磺酸强化型功能饮料瓶装 380ML"
            },
            {
                "barcode":"70259656",
                "name":"绿箭 脆皮软心薄荷柠檬薄荷味 80G"
            },
            {
                "barcode":"70241119",
                "name":"圣湖 浓缩酸牛奶 180G"
            },
            {
                "barcode":"70000579",
                "name":"红牛 维生素功能饮料（原味型） 250ml"
            },
            {
                "barcode":"70000590",
                "name":"麒麟 午后奶茶原味 500ml"
            },
            {
                "barcode":"70001159",
                "name":"红牛 维生素功能饮料（牛磺酸强化型） 250m"
            },
            {
                "barcode":"70004310",
                "name":"德芙 丝滑牛奶巧克力 80G"
            },
            {
                "barcode":"70004421",
                "name":"雀巢 威化奶香 20G*24"
            },
            {
                "barcode":"70010148",
                "name":"红牛 高级鞋油"
            },
            {
                "barcode":"70038093",
                "name":"南孚 耐能电池2粒装(黑耐) R20P"
            }
        ],
        "page_obj":{
            "current":1,
            "next":2,
            "total":4,
            "page_range":[
                {
                    "page":1
                },
                {
                    "page":2
                },
                {
                    "page":3
                },
                {
                    "page":4
                }
            ],
            "previous":null
        },
        "is_paginated":true
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


## **非油总览**

```
GET /goods/overview
```

### **Parameters**

### **Return**

成功
```
{
    "body":{
        "oil_goods_conversion":"14.15%", # 油非转化率
        "ton_oil_goods":147.22849189858246, # 吨油非油收入
        "average":36.258620689655174, # 客单价
        "amount":58, # 订单数
        "product_effect":0.32957216737188527, # 商品品效
        "total":2103 # 销售收入
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


## **商品环比**

```
GET /goods/sequential
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间
* type(_Optional_|string)-环比类型

|type 取值|含义|
| --------------  | :---: |
|month|月环比|
|week|周环比|
|day|日环比|

### **Return**

成功
```
{
    "body":{
        "current_data":{
            "start_time":"2016-12-26 00:00:00",
            "object_list":[
                {
                    "cls_id":2002,
                    "amount":21,
                    "cls_name":"包装饮料",
                    "income":171.5
                },
                {
                    "cls_id":2007,
                    "amount":4,
                    "cls_name":"零食",
                    "income":454
                },
                {
                    "cls_id":2019,
                    "amount":1,
                    "cls_name":"汽车用品",
                    "income":100
                },
                {
                    "cls_id":2001,
                    "amount":6,
                    "cls_name":"香烟",
                    "income":369
                },
                {
                    "cls_id":2006,
                    "amount":10,
                    "cls_name":"糖果",
                    "income":237
                },
                {
                    "cls_id":2013,
                    "amount":2,
                    "cls_name":"日用品",
                    "income":1.5
                }
            ],
            "end_time":"2017-01-01 23:59:59"
        },
        "last_data":{
            "start_time":"2016-12-19 00:00:00",
            "object_list":[

            ],
            "end_time":"2016-12-25 23:59:59"
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


## **商品同比**

```
GET /goods/compare
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间
* type(_Optional_|string)-同比类型


|type 取值|含义|
| --------------  | :---: |
|year|年同比|
|month|月同比|
|custom|自定义同比|

### **Return**

成功
```
{
    "body":{
        "current_data":{
            "start_time":"2017-01-01 00:00:00",
            "object_list":[
                {
                    "cls_id":2010,
                    "amount":93,
                    "cls_name":"饼干/糕点",
                    "income":699.5
                },
                {
                    "cls_id":2006,
                    "amount":539,
                    "cls_name":"糖果",
                    "income":5023.5
                },
                {
                    "cls_id":2012,
                    "amount":131,
                    "cls_name":"速食",
                    "income":927.5
                },
                {
                    "cls_id":2002,
                    "amount":1201,
                    "cls_name":"包装饮料",
                    "income":12012.1
                },
                {
                    "cls_id":2011,
                    "amount":54,
                    "cls_name":"面包",
                    "income":702
                },
                {
                    "cls_id":2019,
                    "amount":68,
                    "cls_name":"汽车用品",
                    "income":2634
                },
                {
                    "cls_id":2001,
                    "amount":782,
                    "cls_name":"香烟",
                    "income":62559
                },
                {
                    "cls_id":2020,
                    "amount":8,
                    "cls_name":"润滑油",
                    "income":821
                },
                {
                    "cls_id":2014,
                    "amount":26,
                    "cls_name":"清洁用品",
                    "income":946.6
                },
                {
                    "cls_id":2005,
                    "amount":69,
                    "cls_name":"酒类",
                    "income":10449
                },
                {
                    "cls_id":2008,
                    "amount":127,
                    "cls_name":"家庭食品",
                    "income":5172
                },
                {
                    "cls_id":2013,
                    "amount":18,
                    "cls_name":"日用品",
                    "income":417
                },
                {
                    "cls_id":2015,
                    "amount":78,
                    "cls_name":"个人护理用品",
                    "income":2228.5
                },
                {
                    "cls_id":2004,
                    "amount":85,
                    "cls_name":"奶类",
                    "income":2582.9
                },
                {
                    "cls_id":2016,
                    "amount":1,
                    "cls_name":"药品/计生/保健",
                    "income":68
                },
                {
                    "cls_id":2007,
                    "amount":221,
                    "cls_name":"零食",
                    "income":2524.5
                }
            ],
            "end_time":"2017-12-31 23:59:59"
        },
        "last_data":{
            "start_time":"2016-01-01 00:00:00",
            "object_list":[
                {
                    "cls_id":2002,
                    "amount":4,
                    "cls_name":"包装饮料",
                    "income":20.5
                },
                {
                    "cls_id":2006,
                    "amount":1,
                    "cls_name":"糖果",
                    "income":3.5
                },
                {
                    "cls_id":2001,
                    "amount":1,
                    "cls_name":"香烟",
                    "income":18
                }
            ],
            "end_time":"2016-12-31 23:59:59"
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


## **搜索环比**

```
GET /goods/search/sequential
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间
* search(_Required_|string)-搜索条件

### **Return**

成功
```
{
    "body":{
        "current_data":{
            "start_time":"2017-01-30 00:00:00",
            "object_list":[
                {
                    "amount":4,
                    "name":"云烟 12mg",
                    "income":220
                }
            ],
            "end_time":"2017-02-05 23:59:59"
        },
        "last_data":{
            "start_time":"2017-01-23 00:00:00",
            "object_list":[
                {
                    "amount":7,
                    "name":"云烟 12mg",
                    "income":280
                }
            ],
            "end_time":"2017-01-29 23:59:59"
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


## **搜索月环比**

```
GET /goods/search/month/sequential
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间
* search(_Required_|string)-搜索条件

### **Return**

成功
```
{
    "body":{
        "current_data":{
            "start_time":"2017-01-30 00:00:00",
            "object_list":[
                {
                    "amount":4,
                    "name":"云烟 12mg",
                    "income":220
                }
            ],
            "end_time":"2017-02-05 23:59:59"
        },
        "last_data":{
            "start_time":"2017-01-23 00:00:00",
            "object_list":[
                {
                    "amount":7,
                    "name":"云烟 12mg",
                    "income":280
                }
            ],
            "end_time":"2017-01-29 23:59:59"
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


## **搜索同比**

```
GET /goods/search/compare
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间
* search(_Required_|string)-搜索条件

### **Return**

成功
```
{
    "body":{
        "current_data":{
            "start_time":"2017-01-01 00:00:00",
            "object_list":[
                {
                    "amount":181,
                    "name":"云烟 12mg",
                    "income":6170
                }
            ],
            "end_time":"2017-12-31 23:59:59"
        },
        "last_data":{
            "start_time":"2016-01-01 00:00:00",
            "object_list":[

            ],
            "end_time":"2016-12-31 23:59:59"
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


## **获取日结时间**

```
GET /tool/daytime
```

### **Parameters**


### **Return**

成功
```
{
    "body":{
        "start_time":"2017-10-18 16:05:37",
        "end_time":"2017-10-19 16:05:37"
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



## **滞销商品**

```
GET /goods/unsold
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间
* unsold_day(_Optional_|integer)-未动销天数，不填默认从最长时间返回结果

### **Return**

成功
```
{
    "body":{
        "goodsinventory_list":[
            {
                "third_cls_id":20010301,
                "second_cls_id":200103,
                "last_sell_time":"2017-09-19 20:17:00",
                "hash":"e51a141ef64137ec6a148cb934f9142c",
                "name":"云烟 神秘花园 5MG",
                "barcode":"70240614",
                "original_create_time":"2017-12-17 23:30:24",
                "amount":65,
                "belong_id":1,
                "itemcode":"70240614",
                "create_time":"2017-12-17 23:30:24",
                "modify_time":"2017-12-17 23:37:49",
                "cls_id":2001,
                "id":4624,
                "unit":"包",
                "unsold_day":99
            },
            {
                "third_cls_id":20050201,
                "second_cls_id":200502,
                "last_sell_time":"2017-09-20 20:25:00",
                "hash":"42b04d448ea2ec8ed89e8e2aaf4f41f4",
                "name":"青海湖 青稞酒（精品装） 500ML",
                "barcode":"70259956",
                "original_create_time":"2017-12-17 23:30:31",
                "amount":6,
                "belong_id":1,
                "itemcode":"70259956",
                "create_time":"2017-12-17 23:30:31",
                "modify_time":"2017-12-17 23:37:53",
                "cls_id":2005,
                "id":5531,
                "unit":"瓶",
                "unsold_day":98
            },
            {
                "third_cls_id":20050201,
                "second_cls_id":200502,
                "last_sell_time":"2017-09-22 03:29:00",
                "hash":"f78b10cb962a65035cc513a18b6f2428",
                "name":"互助 神仙酿 45度 500ML",
                "barcode":"70187875",
                "original_create_time":"2017-12-17 23:30:14",
                "amount":34,
                "belong_id":1,
                "itemcode":"70187875",
                "create_time":"2017-12-17 23:30:14",
                "modify_time":"2017-12-17 23:37:43",
                "cls_id":2005,
                "id":3471,
                "unit":"瓶",
                "unsold_day":96
            },
            {
                "third_cls_id":20020601,
                "second_cls_id":200206,
                "last_sell_time":"2017-09-26 08:30:00",
                "hash":"d1e8ec507d14b06f7369831b81bed52e",
                "name":"碱法 苹果味苏打汽水 500ML",
                "barcode":"70247386",
                "original_create_time":"2017-12-17 23:30:26",
                "amount":70,
                "belong_id":1,
                "itemcode":"70247386",
                "create_time":"2017-12-17 23:30:26",
                "modify_time":"2017-12-17 23:37:50",
                "cls_id":2002,
                "id":4915,
                "unit":"瓶",
                "unsold_day":92
            },
            {
                "third_cls_id":20060202,
                "second_cls_id":200602,
                "last_sell_time":"2017-09-26 12:51:00",
                "hash":"a00756f6566c588dbfb5b607bbd2b39a",
                "name":"箭牌 “5”无糖口香糖12片装激酷薄荷味 32G",
                "barcode":"70206419",
                "original_create_time":"2017-12-17 23:30:16",
                "amount":0,
                "belong_id":1,
                "itemcode":"70206419",
                "create_time":"2017-12-17 23:30:16",
                "modify_time":"2017-12-17 23:37:44",
                "cls_id":2006,
                "id":3706,
                "unit":"每个",
                "unsold_day":92
            },
            {
                "third_cls_id":20080701,
                "second_cls_id":200807,
                "last_sell_time":"2017-09-26 13:47:00",
                "hash":"c535c7e5cd72d2fa8788e66cf1036971",
                "name":"雪峰 三炮台 500G/盒",
                "barcode":"70090682",
                "original_create_time":"2017-12-17 23:30:11",
                "amount":0,
                "belong_id":1,
                "itemcode":"70090682",
                "create_time":"2017-12-17 23:30:11",
                "modify_time":"2017-12-17 23:37:39",
                "cls_id":2008,
                "id":2699,
                "unit":"包",
                "unsold_day":92
            },
            {
                "third_cls_id":20080501,
                "second_cls_id":200805,
                "last_sell_time":"2017-09-27 11:28:00",
                "hash":"bac716d5250c2489db18fcd83ff9acae",
                "name":"西北骄 雪域奶茶咸味 360G",
                "barcode":"70254664",
                "original_create_time":"2017-12-17 23:30:28",
                "amount":8,
                "belong_id":1,
                "itemcode":"70254664",
                "create_time":"2017-12-17 23:30:28",
                "modify_time":"2017-12-17 23:37:51",
                "cls_id":2008,
                "id":5142,
                "unit":"包",
                "unsold_day":91
            },
            {
                "third_cls_id":20110502,
                "second_cls_id":201105,
                "last_sell_time":"2017-09-27 15:25:00",
                "hash":"60d019c930a119befaaab14c10055450",
                "name":"唇动 白色经典柠檬味涂饰蛋糕 180G",
                "barcode":"70262018",
                "original_create_time":"2017-12-17 23:30:32",
                "amount":14,
                "belong_id":1,
                "itemcode":"70262018",
                "create_time":"2017-12-17 23:30:32",
                "modify_time":"2017-12-17 23:37:53",
                "cls_id":2011,
                "id":5598,
                "unit":"包",
                "unsold_day":91
            },
            {
                "third_cls_id":20080207,
                "second_cls_id":200802,
                "last_sell_time":"2017-09-28 18:12:00",
                "hash":"25f455c8e23086a0ebbea8eb1352d798",
                "name":"福临门 非转基因纯香菜籽油 5L",
                "barcode":"70254446",
                "original_create_time":"2017-12-17 23:30:28",
                "amount":0,
                "belong_id":1,
                "itemcode":"70254446",
                "create_time":"2017-12-17 23:30:28",
                "modify_time":"2017-12-17 23:37:51",
                "cls_id":2008,
                "id":5130,
                "unit":"桶",
                "unsold_day":90
            },
            {
                "third_cls_id":20020301,
                "second_cls_id":200203,
                "last_sell_time":"2017-09-29 12:51:00",
                "hash":"7391f5d98c959553be6775dde7c302de",
                "name":"雀巢 咖啡香浓(听) 180ML",
                "barcode":"70214355",
                "original_create_time":"2017-12-17 23:30:17",
                "amount":96,
                "belong_id":1,
                "itemcode":"70214355",
                "create_time":"2017-12-17 23:30:17",
                "modify_time":"2017-12-17 23:37:44",
                "cls_id":2002,
                "id":3785,
                "unit":"罐",
                "unsold_day":89
            },
            {
                "third_cls_id":20020602,
                "second_cls_id":200206,
                "last_sell_time":"2017-09-29 15:21:00",
                "hash":"fb5afcdda74241e0a645d0dce8e77fdb",
                "name":"农夫 农夫山泉天然饮用水4升装 4升/桶",
                "barcode":"70240287",
                "original_create_time":"2017-12-17 23:30:23",
                "amount":37,
                "belong_id":1,
                "itemcode":"70240287",
                "create_time":"2017-12-17 23:30:23",
                "modify_time":"2017-12-17 23:37:49",
                "cls_id":2002,
                "id":4613,
                "unit":"桶",
                "unsold_day":89
            },
            {
                "third_cls_id":20080804,
                "second_cls_id":200808,
                "last_sell_time":"2017-09-30 16:27:00",
                "hash":"f7efd555e40095e1e18328b800d5e83e",
                "name":"徽珍 帝女花（大皇菊） 9G",
                "barcode":"70263622",
                "original_create_time":"2017-12-17 23:30:33",
                "amount":1,
                "belong_id":1,
                "itemcode":"70263622",
                "create_time":"2017-12-17 23:30:33",
                "modify_time":"2017-12-17 23:37:54",
                "cls_id":2008,
                "id":5703,
                "unit":"包",
                "unsold_day":88
            },
            {
                "third_cls_id":20080504,
                "second_cls_id":200805,
                "last_sell_time":"2017-09-30 16:27:00",
                "hash":"15727a0ffd1711be33385713bcdc95f2",
                "name":"中粮 特制茯砖纸包 350G",
                "barcode":"70274803",
                "original_create_time":"2017-12-17 23:30:37",
                "amount":8,
                "belong_id":1,
                "itemcode":"70274803",
                "create_time":"2017-12-17 23:30:37",
                "modify_time":"2017-12-17 23:37:56",
                "cls_id":2008,
                "id":6190,
                "unit":"包",
                "unsold_day":88
            },
            {
                "third_cls_id":20080504,
                "second_cls_id":200805,
                "last_sell_time":"2017-09-30 16:27:00",
                "hash":"bcfa26e720b62f832e5413c01f5e1633",
                "name":"黟山好客 皇菊小礼盒 2G",
                "barcode":"70273252",
                "original_create_time":"2017-12-17 23:30:36",
                "amount":5,
                "belong_id":1,
                "itemcode":"70273252",
                "create_time":"2017-12-17 23:30:36",
                "modify_time":"2017-12-17 23:37:56",
                "cls_id":2008,
                "id":6131,
                "unit":"包",
                "unsold_day":88
            },
            {
                "third_cls_id":20080804,
                "second_cls_id":200808,
                "last_sell_time":"2017-09-30 16:27:00",
                "hash":"8372aef423ea29049eff21c9e884a51e",
                "name":"雪峰 柴达木枸杞 250G",
                "barcode":"70172114",
                "original_create_time":"2017-12-17 23:30:14",
                "amount":2,
                "belong_id":1,
                "itemcode":"70172114",
                "create_time":"2017-12-17 23:30:14",
                "modify_time":"2017-12-17 23:37:42",
                "cls_id":2008,
                "id":3271,
                "unit":"包",
                "unsold_day":88
            },
            {
                "third_cls_id":20070301,
                "second_cls_id":200703,
                "last_sell_time":"2017-10-01 12:23:00",
                "hash":"7b41fce2b4ac18caa1be07cc49a68b31",
                "name":"佳宝 九制杨梅 65g",
                "barcode":"70049212",
                "original_create_time":"2017-12-17 23:30:06",
                "amount":0,
                "belong_id":1,
                "itemcode":"70049212",
                "create_time":"2017-12-17 23:30:06",
                "modify_time":"2017-12-17 23:37:37",
                "cls_id":2007,
                "id":2036,
                "unit":"包",
                "unsold_day":87
            },
            {
                "third_cls_id":20130404,
                "second_cls_id":201304,
                "last_sell_time":"2017-10-01 19:11:00",
                "hash":"0579a0972ee7b99aa4a86589897b66cd",
                "name":"匡迪 真空保温杯 2L",
                "barcode":"70242291",
                "original_create_time":"2017-12-17 23:30:24",
                "amount":11,
                "belong_id":1,
                "itemcode":"70242291",
                "create_time":"2017-12-17 23:30:24",
                "modify_time":"2017-12-17 23:37:49",
                "cls_id":2013,
                "id":4702,
                "unit":"每个",
                "unsold_day":87
            },
            {
                "third_cls_id":20080504,
                "second_cls_id":200805,
                "last_sell_time":"2017-10-01 20:41:00",
                "hash":"23e29f89bbfe5c138e5105c663f3e64d",
                "name":"三江雪 熬茶(青稞味) 100G",
                "barcode":"70151300",
                "original_create_time":"2017-12-17 23:30:13",
                "amount":0,
                "belong_id":1,
                "itemcode":"70151300",
                "create_time":"2017-12-17 23:30:13",
                "modify_time":"2017-12-17 23:37:41",
                "cls_id":2008,
                "id":3077,
                "unit":"包",
                "unsold_day":87
            },
            {
                "third_cls_id":20150409,
                "second_cls_id":201504,
                "last_sell_time":"2017-10-02 22:39:00",
                "hash":"28be793b63fd94bf2a5fd25d7c30ee54",
                "name":"隆力奇 蛇油护手霜套装 50G*2+30G",
                "barcode":"70096814",
                "original_create_time":"2017-12-17 23:30:11",
                "amount":4,
                "belong_id":1,
                "itemcode":"70096814",
                "create_time":"2017-12-17 23:30:11",
                "modify_time":"2017-12-17 23:37:40",
                "cls_id":2015,
                "id":2742,
                "unit":"包",
                "unsold_day":86
            },
            {
                "third_cls_id":20080505,
                "second_cls_id":200805,
                "last_sell_time":"2017-10-02 22:39:00",
                "hash":"68004b03c8b46b06463dbbf6b24f8064",
                "name":"香飘飘奶茶香芋味80g",
                "barcode":"70001680",
                "original_create_time":"2017-12-17 23:29:59",
                "amount":4,
                "belong_id":1,
                "itemcode":"70001680",
                "create_time":"2017-12-17 23:29:59",
                "modify_time":"2017-12-17 23:37:31",
                "cls_id":2008,
                "id":880,
                "unit":"每个",
                "unsold_day":86
            },
            {
                "third_cls_id":20150101,
                "second_cls_id":201501,
                "last_sell_time":"2017-10-02 22:39:00",
                "hash":"2cc4531262c63e5ea9bdc30c19b685db",
                "name":"丝蕴 深层修护洗护套装 750ML+500ML",
                "barcode":"70268603",
                "original_create_time":"2017-12-17 23:30:34",
                "amount":17,
                "belong_id":1,
                "itemcode":"70268603",
                "create_time":"2017-12-17 23:30:34",
                "modify_time":"2017-12-17 23:37:55",
                "cls_id":2015,
                "id":5928,
                "unit":"包",
                "unsold_day":86
            },
            {
                "third_cls_id":20150703,
                "second_cls_id":201507,
                "last_sell_time":"2017-10-03 10:38:00",
                "hash":"e023ee4dd7beb876a482fca5cec48d66",
                "name":"清怡 CR009CS薄荷软抽 150抽",
                "barcode":"70029861",
                "original_create_time":"2017-12-17 23:30:04",
                "amount":12,
                "belong_id":1,
                "itemcode":"70029861",
                "create_time":"2017-12-17 23:30:04",
                "modify_time":"2017-12-17 23:37:35",
                "cls_id":2015,
                "id":1775,
                "unit":"包",
                "unsold_day":85
            },
            {
                "third_cls_id":20070401,
                "second_cls_id":200704,
                "last_sell_time":"2017-10-03 19:16:00",
                "hash":"a86abd30a80204d5582ef1b544bd361b",
                "name":"西北娇 糖果牛肉干 150克",
                "barcode":"70094449",
                "original_create_time":"2017-12-17 23:30:11",
                "amount":7,
                "belong_id":1,
                "itemcode":"70094449",
                "create_time":"2017-12-17 23:30:11",
                "modify_time":"2017-12-17 23:37:40",
                "cls_id":2007,
                "id":2727,
                "unit":"包",
                "unsold_day":85
            },
            {
                "third_cls_id":20130701,
                "second_cls_id":201307,
                "last_sell_time":"2017-10-03 19:16:00",
                "hash":"b245fbcd61c9bfa21193126b0fc3c361",
                "name":"红心 吹风机系列 RH3108",
                "barcode":"70218559",
                "original_create_time":"2017-12-17 23:30:18",
                "amount":4,
                "belong_id":1,
                "itemcode":"70218559",
                "create_time":"2017-12-17 23:30:18",
                "modify_time":"2017-12-17 23:37:45",
                "cls_id":2013,
                "id":3926,
                "unit":"每个",
                "unsold_day":85
            },
            {
                "third_cls_id":20190501,
                "second_cls_id":201905,
                "last_sell_time":"2017-10-03 19:16:00",
                "hash":"8cb9f16dce1824643dfc60533bf5a6b6",
                "name":"多奇 太阳挡CD袋 1*1",
                "barcode":"70183148",
                "original_create_time":"2017-12-17 23:30:14",
                "amount":2,
                "belong_id":1,
                "itemcode":"70183148",
                "create_time":"2017-12-17 23:30:14",
                "modify_time":"2017-12-17 23:37:43",
                "cls_id":2019,
                "id":3417,
                "unit":"每个",
                "unsold_day":85
            },
            {
                "third_cls_id":20080701,
                "second_cls_id":200807,
                "last_sell_time":"2017-10-04 16:28:00",
                "hash":"1e7be71ec0ce4a8d6cd799132b34b60d",
                "name":"顶麦 苏式无蔗糖月饼 60G",
                "barcode":"70137985",
                "original_create_time":"2017-12-17 23:30:12",
                "amount":14,
                "belong_id":1,
                "itemcode":"70137985",
                "create_time":"2017-12-17 23:30:12",
                "modify_time":"2017-12-17 23:37:41",
                "cls_id":2008,
                "id":2981,
                "unit":"每个",
                "unsold_day":84
            },
            {
                "third_cls_id":20080504,
                "second_cls_id":200805,
                "last_sell_time":"2017-10-04 19:55:00",
                "hash":"b6d3515caa4b84623b25be895ecf6794",
                "name":"中茶 软装特级花茶 100G",
                "barcode":"70247457",
                "original_create_time":"2017-12-17 23:30:26",
                "amount":0,
                "belong_id":1,
                "itemcode":"70247457",
                "create_time":"2017-12-17 23:30:26",
                "modify_time":"2017-12-17 23:37:51",
                "cls_id":2008,
                "id":4931,
                "unit":"包",
                "unsold_day":84
            },
            {
                "third_cls_id":20020601,
                "second_cls_id":200206,
                "last_sell_time":"2017-10-04 23:19:00",
                "hash":"79d7963b71d6618e3d0d338b601f1788",
                "name":"碱法 柠檬味饮苏打汽水PET 500ML",
                "barcode":"70258670",
                "original_create_time":"2017-12-17 23:30:30",
                "amount":70,
                "belong_id":1,
                "itemcode":"70258670",
                "create_time":"2017-12-17 23:30:30",
                "modify_time":"2017-12-17 23:37:52",
                "cls_id":2002,
                "id":5307,
                "unit":"瓶",
                "unsold_day":84
            },
            {
                "third_cls_id":20020401,
                "second_cls_id":200204,
                "last_sell_time":"2017-10-05 10:05:00",
                "hash":"fc4de95ccd2365ea806057c28d1cecc7",
                "name":"如一 石榴果汁 300ML",
                "barcode":"70259343",
                "original_create_time":"2017-12-17 23:30:31",
                "amount":18,
                "belong_id":1,
                "itemcode":"70259343",
                "create_time":"2017-12-17 23:30:31",
                "modify_time":"2017-12-17 23:37:53",
                "cls_id":2002,
                "id":5469,
                "unit":"瓶",
                "unsold_day":83
            },
            {
                "third_cls_id":20020601,
                "second_cls_id":200206,
                "last_sell_time":"2017-10-05 10:39:00",
                "hash":"c158d6d5736a1b73ef94c8b3bf210937",
                "name":"经口葡萄糖 补水液 450ML",
                "barcode":"70276944",
                "original_create_time":"2017-12-17 23:30:37",
                "amount":150,
                "belong_id":1,
                "itemcode":"70276944",
                "create_time":"2017-12-17 23:30:37",
                "modify_time":"2017-12-17 23:37:56",
                "cls_id":2002,
                "id":6218,
                "unit":"瓶",
                "unsold_day":83
            },
            {
                "third_cls_id":20190102,
                "second_cls_id":201901,
                "last_sell_time":"2017-10-05 15:16:00",
                "hash":"98eeb391e2f0c7f1c2ca4d66715d4770",
                "name":"昆仑之星玻璃养护液-10℃高效型 1.75kg/桶",
                "barcode":"456947",
                "original_create_time":"2017-12-17 23:29:58",
                "amount":0,
                "belong_id":1,
                "itemcode":"456947",
                "create_time":"2017-12-17 23:29:58",
                "modify_time":"2017-12-17 23:37:30",
                "cls_id":2019,
                "id":657,
                "unit":"桶",
                "unsold_day":83
            },
            {
                "third_cls_id":20070401,
                "second_cls_id":200704,
                "last_sell_time":"2017-10-06 07:35:00",
                "hash":"527d96f9f377dc3191bcef0677ee8076",
                "name":"可可西里 藏牦牛肉干 五香味(新品) 150G",
                "barcode":"70058694",
                "original_create_time":"2017-12-17 23:30:08",
                "amount":13,
                "belong_id":1,
                "itemcode":"70058694",
                "create_time":"2017-12-17 23:30:08",
                "modify_time":"2017-12-17 23:37:37",
                "cls_id":2007,
                "id":2181,
                "unit":"包",
                "unsold_day":82
            },
            {
                "third_cls_id":20130501,
                "second_cls_id":201305,
                "last_sell_time":"2017-10-06 10:41:00",
                "hash":"07caad85b5e72e2b59f5d0f3df29df5b",
                "name":"小熊 煮蛋器 ZDQ-219",
                "barcode":"70218583",
                "original_create_time":"2017-12-17 23:30:18",
                "amount":0,
                "belong_id":1,
                "itemcode":"70218583",
                "create_time":"2017-12-17 23:30:18",
                "modify_time":"2017-12-17 23:37:45",
                "cls_id":2013,
                "id":3932,
                "unit":"每个",
                "unsold_day":82
            },
            {
                "third_cls_id":20070402,
                "second_cls_id":200704,
                "last_sell_time":"2017-10-07 13:06:00",
                "hash":"4243d4d3063bfde7406d69f634997c18",
                "name":"全航 麻辣猪蹄 1",
                "barcode":"70268540",
                "original_create_time":"2017-12-17 23:30:34",
                "amount":17,
                "belong_id":1,
                "itemcode":"70268540",
                "create_time":"2017-12-17 23:30:34",
                "modify_time":"2017-12-17 23:37:55",
                "cls_id":2007,
                "id":5920,
                "unit":"包",
                "unsold_day":81
            },
            {
                "third_cls_id":20070101,
                "second_cls_id":200701,
                "last_sell_time":"2017-10-07 13:06:00",
                "hash":"1f985cc0ab261641df142cc0703a26e9",
                "name":"口水娃 虾片 35G",
                "barcode":"70263904",
                "original_create_time":"2017-12-17 23:30:33",
                "amount":84,
                "belong_id":1,
                "itemcode":"70263904",
                "create_time":"2017-12-17 23:30:33",
                "modify_time":"2017-12-17 23:37:54",
                "cls_id":2007,
                "id":5706,
                "unit":"包",
                "unsold_day":81
            },
            {
                "third_cls_id":20150602,
                "second_cls_id":201506,
                "last_sell_time":"2017-10-07 15:44:00",
                "hash":"38aff16ac70306d21b13efa6bde9ed20",
                "name":"威露士 洗手液 525G",
                "barcode":"70079260",
                "original_create_time":"2017-12-17 23:30:10",
                "amount":8,
                "belong_id":1,
                "itemcode":"70079260",
                "create_time":"2017-12-17 23:30:10",
                "modify_time":"2017-12-17 23:37:39",
                "cls_id":2015,
                "id":2627,
                "unit":"瓶",
                "unsold_day":81
            },
            {
                "third_cls_id":20020402,
                "second_cls_id":200204,
                "last_sell_time":"2017-10-07 16:30:00",
                "hash":"4e1f4a5347ceaf1456a2281dc1981282",
                "name":"果倍爽 橙汁 200ML",
                "barcode":"70244645",
                "original_create_time":"2017-12-17 23:30:25",
                "amount":80,
                "belong_id":1,
                "itemcode":"70244645",
                "create_time":"2017-12-17 23:30:25",
                "modify_time":"2017-12-17 23:37:50",
                "cls_id":2002,
                "id":4762,
                "unit":"包",
                "unsold_day":81
            },
            {
                "third_cls_id":20080101,
                "second_cls_id":200801,
                "last_sell_time":"2017-10-07 19:48:00",
                "hash":"7d49f59fe1400aae44dd7db9af3bec35",
                "name":"龙禹 葵花阳光精香营养米 5KG",
                "barcode":"70205729",
                "original_create_time":"2017-12-17 23:30:16",
                "amount":4,
                "belong_id":1,
                "itemcode":"70205729",
                "create_time":"2017-12-17 23:30:16",
                "modify_time":"2017-12-17 23:37:44",
                "cls_id":2008,
                "id":3700,
                "unit":"包",
                "unsold_day":81
            },
            {
                "third_cls_id":20020402,
                "second_cls_id":200204,
                "last_sell_time":"2017-10-07 22:39:00",
                "hash":"7316d64b6903779bd4d79ba90e2d4ac5",
                "name":"农夫山泉 水溶C100青柠汁饮 445ML",
                "barcode":"70238841",
                "original_create_time":"2017-12-17 23:30:23",
                "amount":34,
                "belong_id":1,
                "itemcode":"70238841",
                "create_time":"2017-12-17 23:30:23",
                "modify_time":"2017-12-17 23:37:48",
                "cls_id":2002,
                "id":4556,
                "unit":"瓶",
                "unsold_day":81
            },
            {
                "third_cls_id":20060202,
                "second_cls_id":200602,
                "last_sell_time":"2017-10-08 03:54:00",
                "hash":"ceed55b58f8ca05c458fed854582c73f",
                "name":"益达 蓝莓 五片装",
                "barcode":"70000143",
                "original_create_time":"2017-12-17 23:29:58",
                "amount":121,
                "belong_id":1,
                "itemcode":"70000143",
                "create_time":"2017-12-17 23:29:58",
                "modify_time":"2017-12-17 23:37:30",
                "cls_id":2006,
                "id":685,
                "unit":"每个",
                "unsold_day":80
            },
            {
                "third_cls_id":20201102,
                "second_cls_id":202011,
                "last_sell_time":"2017-10-08 11:35:00",
                "hash":"943c29b51fc59b0b2a73e584406c3740",
                "name":"昆仑天润KR8 5W-30汽油机油 3.5kg/桶",
                "barcode":"456545",
                "original_create_time":"2017-12-17 23:29:58",
                "amount":29,
                "belong_id":1,
                "itemcode":"456545",
                "create_time":"2017-12-17 23:29:58",
                "modify_time":"2017-12-17 23:37:30",
                "cls_id":2020,
                "id":622,
                "unit":"桶",
                "unsold_day":80
            },
            {
                "third_cls_id":20070101,
                "second_cls_id":200701,
                "last_sell_time":"2017-10-08 13:28:00",
                "hash":"042eff66a46cfac063a24a45db9939cf",
                "name":"乐事 番茄味 40G",
                "barcode":"70018170",
                "original_create_time":"2017-12-17 23:30:03",
                "amount":29,
                "belong_id":1,
                "itemcode":"70018170",
                "create_time":"2017-12-17 23:30:03",
                "modify_time":"2017-12-17 23:37:34",
                "cls_id":2007,
                "id":1478,
                "unit":"包",
                "unsold_day":80
            },
            {
                "third_cls_id":20140104,
                "second_cls_id":201401,
                "last_sell_time":"2017-10-08 13:28:00",
                "hash":"4329a0d6f24676604dbd65e76149e4c1",
                "name":"蓝月亮 袋装香薰柔顺剂（玉玲兰）500ml",
                "barcode":"70014662",
                "original_create_time":"2017-12-17 23:30:02",
                "amount":44,
                "belong_id":1,
                "itemcode":"70014662",
                "create_time":"2017-12-17 23:30:02",
                "modify_time":"2017-12-17 23:37:34",
                "cls_id":2014,
                "id":1402,
                "unit":"对",
                "unsold_day":80
            },
            {
                "third_cls_id":20070101,
                "second_cls_id":200701,
                "last_sell_time":"2017-10-08 13:28:00",
                "hash":"d32f4d91d003a4ba75963ec1d706bc3e",
                "name":"达利 可比克薯片桶装香辣味 45g",
                "barcode":"70004797",
                "original_create_time":"2017-12-17 23:30:00",
                "amount":62,
                "belong_id":1,
                "itemcode":"70004797",
                "create_time":"2017-12-17 23:30:00",
                "modify_time":"2017-12-17 23:37:32",
                "cls_id":2007,
                "id":1080,
                "unit":"包",
                "unsold_day":80
            },
            {
                "third_cls_id":20100107,
                "second_cls_id":201001,
                "last_sell_time":"2017-10-08 16:39:00",
                "hash":"71803034cd965a333015103065d368bd",
                "name":"南益 巧克力粒饼干 200G",
                "barcode":"70238499",
                "original_create_time":"2017-12-17 23:30:23",
                "amount":10,
                "belong_id":1,
                "itemcode":"70238499",
                "create_time":"2017-12-17 23:30:23",
                "modify_time":"2017-12-17 23:37:48",
                "cls_id":2010,
                "id":4554,
                "unit":"包",
                "unsold_day":80
            },
            {
                "third_cls_id":20010401,
                "second_cls_id":200104,
                "last_sell_time":"2017-10-08 19:11:00",
                "hash":"dc3f258f30c57ebb3b940f887fadfff6",
                "name":"娇子 (X) 20支",
                "barcode":"70002706",
                "original_create_time":"2017-12-17 23:30:00",
                "amount":24,
                "belong_id":1,
                "itemcode":"70002706",
                "create_time":"2017-12-17 23:30:00",
                "modify_time":"2017-12-17 23:37:31",
                "cls_id":2001,
                "id":922,
                "unit":"包",
                "unsold_day":80
            },
            {
                "third_cls_id":20080509,
                "second_cls_id":200805,
                "last_sell_time":"2017-10-09 12:17:00",
                "hash":"70e960c351a07cfa8f899e772136fb23",
                "name":"和小白 红豆多多 45G",
                "barcode":"70267337",
                "original_create_time":"2017-12-17 23:30:34",
                "amount":0,
                "belong_id":1,
                "itemcode":"70267337",
                "create_time":"2017-12-17 23:30:34",
                "modify_time":"2017-12-17 23:37:54",
                "cls_id":2008,
                "id":5816,
                "unit":"每个",
                "unsold_day":79
            },
            {
                "third_cls_id":20070401,
                "second_cls_id":200704,
                "last_sell_time":"2017-10-09 14:37:00",
                "hash":"d21c9abab2ddaa9520399d5658f5b440",
                "name":"西北骄 牛肉干(香辣) 200G",
                "barcode":"70092299",
                "original_create_time":"2017-12-17 23:30:11",
                "amount":4,
                "belong_id":1,
                "itemcode":"70092299",
                "create_time":"2017-12-17 23:30:11",
                "modify_time":"2017-12-17 23:37:40",
                "cls_id":2007,
                "id":2714,
                "unit":"包",
                "unsold_day":79
            },
            {
                "third_cls_id":20150703,
                "second_cls_id":201507,
                "last_sell_time":"2017-10-10 08:32:00",
                "hash":"4b75910fc517bf7e662e0b0d102c2956",
                "name":"昆悦 抽取式软抽面巾纸185MM×208MM 200抽",
                "barcode":"70235029",
                "original_create_time":"2017-12-17 23:30:22",
                "amount":32,
                "belong_id":1,
                "itemcode":"70235029",
                "create_time":"2017-12-17 23:30:22",
                "modify_time":"2017-12-17 23:37:48",
                "cls_id":2015,
                "id":4475,
                "unit":"包",
                "unsold_day":78
            },
            {
                "third_cls_id":20070101,
                "second_cls_id":200701,
                "last_sell_time":"2017-10-10 10:09:00",
                "hash":"c49158f2aed954db5563833aa1093720",
                "name":"口水娃 锅巴(五香味) 108G",
                "barcode":"70061449",
                "original_create_time":"2017-12-17 23:30:08",
                "amount":21,
                "belong_id":1,
                "itemcode":"70061449",
                "create_time":"2017-12-17 23:30:08",
                "modify_time":"2017-12-17 23:37:37",
                "cls_id":2007,
                "id":2242,
                "unit":"包",
                "unsold_day":78
            }
        ],
        "page_obj":{
            "current":1,
            "next":2,
            "total":3,
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
        "is_paginated":true
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


## **卡总览**

```
GET /card/overview
```

### **Parameters**

### **Return**

成功
```
{
    "body":{
        "amount":6,
        "income":8000
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


## **卡消费结构**

```
GET /card/composition
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
        "object_list":[
            {
                "card_type":"银行卡",
                "amount":3,
                "cls_name":"速食",
                "card_type_id":0
            },
            {
                "card_type":"记名卡",
                "amount":5,
                "cls_name":"奶类",
                "card_type_id":1
            },
            {
                "card_type":"银行卡",
                "amount":3604,
                "cls_name":"汽油",
                "card_type_id":0
            },
            {
                "card_type":"银行卡",
                "amount":6,
                "cls_name":"汽车用品",
                "card_type_id":0
            },
            {
                "card_type":"车队卡",
                "amount":13,
                "cls_name":"包装饮料",
                "card_type_id":2
            },
            {
                "card_type":"记名卡",
                "amount":11,
                "cls_name":"家庭食品",
                "card_type_id":1
            },
            {
                "card_type":"车队卡",
                "amount":2141,
                "cls_name":"柴油",
                "card_type_id":2
            },
            {
                "card_type":"车队卡",
                "amount":1,
                "cls_name":"零食",
                "card_type_id":2
            },
            {
                "card_type":"银行卡",
                "amount":62,
                "cls_name":"香烟",
                "card_type_id":0
            },
            {
                "card_type":"记名卡",
                "amount":16,
                "cls_name":"糖果",
                "card_type_id":1
            },
            {
                "card_type":"银行卡",
                "amount":3,
                "cls_name":"饼干/糕点",
                "card_type_id":0
            },
            {
                "card_type":"银行卡",
                "amount":1,
                "cls_name":"日用品",
                "card_type_id":0
            },
            {
                "card_type":"银行卡",
                "amount":212,
                "cls_name":"柴油",
                "card_type_id":0
            },
            {
                "card_type":"银行卡",
                "amount":6,
                "cls_name":"零食",
                "card_type_id":0
            },
            {
                "card_type":"记名卡",
                "amount":1,
                "cls_name":"面包",
                "card_type_id":1
            },
            {
                "card_type":"车队卡",
                "amount":3,
                "cls_name":"饼干/糕点",
                "card_type_id":2
            },
            {
                "card_type":"车队卡",
                "amount":13,
                "cls_name":"香烟",
                "card_type_id":2
            },
            {
                "card_type":"记名卡",
                "amount":4,
                "cls_name":"清洁用品",
                "card_type_id":1
            },
            {
                "card_type":"银行卡",
                "amount":3,
                "cls_name":"酒类",
                "card_type_id":0
            },
            {
                "card_type":"车队卡",
                "amount":5322,
                "cls_name":"汽油",
                "card_type_id":2
            },
            {
                "card_type":"记名卡",
                "amount":7,
                "cls_name":"个人护理用品",
                "card_type_id":1
            },
            {
                "card_type":"记名卡",
                "amount":23,
                "cls_name":"",
                "card_type_id":1
            },
            {
                "card_type":"车队卡",
                "amount":3,
                "cls_name":"汽车用品",
                "card_type_id":2
            },
            {
                "card_type":"银行卡",
                "amount":64,
                "cls_name":"包装饮料",
                "card_type_id":0
            },
            {
                "card_type":"车队卡",
                "amount":1,
                "cls_name":"面包",
                "card_type_id":2
            },
            {
                "card_type":"记名卡",
                "amount":1,
                "cls_name":"饼干/糕点",
                "card_type_id":1
            },
            {
                "card_type":"银行卡",
                "amount":30,
                "cls_name":"糖果",
                "card_type_id":0
            },
            {
                "card_type":"记名卡",
                "amount":7,
                "cls_name":"香烟",
                "card_type_id":1
            },
            {
                "card_type":"记名卡",
                "amount":4,
                "cls_name":"日用品",
                "card_type_id":1
            },
            {
                "card_type":"车队卡",
                "amount":1,
                "cls_name":"清洁用品",
                "card_type_id":2
            },
            {
                "card_type":"银行卡",
                "amount":5,
                "cls_name":"奶类",
                "card_type_id":0
            },
            {
                "card_type":"记名卡",
                "amount":1,
                "cls_name":"速食",
                "card_type_id":1
            },
            {
                "card_type":"记名卡",
                "amount":2640,
                "cls_name":"汽油",
                "card_type_id":1
            },
            {
                "card_type":"车队卡",
                "amount":3,
                "cls_name":"个人护理用品",
                "card_type_id":2
            },
            {
                "card_type":"车队卡",
                "amount":70,
                "cls_name":"",
                "card_type_id":2
            },
            {
                "card_type":"银行卡",
                "amount":7,
                "cls_name":"家庭食品",
                "card_type_id":0
            },
            {
                "card_type":"记名卡",
                "amount":3,
                "cls_name":"汽车用品",
                "card_type_id":1
            },
            {
                "card_type":"记名卡",
                "amount":3,
                "cls_name":"酒类",
                "card_type_id":1
            },
            {
                "card_type":"银行卡",
                "amount":6,
                "cls_name":"个人护理用品",
                "card_type_id":0
            },
            {
                "card_type":"记名卡",
                "amount":19,
                "cls_name":"包装饮料",
                "card_type_id":1
            },
            {
                "card_type":"车队卡",
                "amount":1,
                "cls_name":"家庭食品",
                "card_type_id":2
            },
            {
                "card_type":"记名卡",
                "amount":375,
                "cls_name":"柴油",
                "card_type_id":1
            },
            {
                "card_type":"记名卡",
                "amount":5,
                "cls_name":"零食",
                "card_type_id":1
            },
            {
                "card_type":"车队卡",
                "amount":10,
                "cls_name":"糖果",
                "card_type_id":2
            },
            {
                "card_type":"银行卡",
                "amount":1,
                "cls_name":"清洁用品",
                "card_type_id":0
            }
        ],
        "end_time":"2017-12-31 00:00:00"
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

## **卡销比**

```
GET /card/compare
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "start_time":"2018-01-15 00:00:00",
        "object_list":[
            {
                "total_money":20,
                "cls_name":"汽油"
            },
            {
                "total_money":20,
                "cls_name":"柴油"
            }
        ],
        "end_time":"2018-01-15 23:59:59"
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


## **卡消费排行**

```
GET /card/ranks/
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间

### **Return**

成功
```
{
    "body":{
        "start_time":"2018-02-01 00:00:00",
        "object_list":[
            {
                "card_type":2,
                "money":4413.71,
                "card_id":"9130180001320487",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":3206.99,
                "card_id":"9130180001419410",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":3051.42,
                "card_id":"9100000001515523",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":2240,
                "card_id":"9130180000983094",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":900,
                "card_id":"9130180001087919",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":900,
                "card_id":"9130220000893343",
                "bank_card_id":null
            },
            {
                "card_type":1,
                "money":801.79,
                "card_id":"9030170001030594",
                "bank_card_id":null
            },
            {
                "card_type":0,
                "money":625,
                "card_id":"0",
                "bank_card_id":"6259652800540489"
            },
            {
                "card_type":2,
                "money":603.43,
                "card_id":"9130180000198209",
                "bank_card_id":null
            },
            {
                "card_type":0,
                "money":600,
                "card_id":"0",
                "bank_card_id":"6228481948050844272"
            },
            {
                "card_type":2,
                "money":570,
                "card_id":"9130180000558311",
                "bank_card_id":null
            },
            {
                "card_type":0,
                "money":566.91,
                "card_id":"0",
                "bank_card_id":"6228481946020141969"
            },
            {
                "card_type":0,
                "money":530,
                "card_id":"0",
                "bank_card_id":"6259960228652384"
            },
            {
                "card_type":1,
                "money":515.84,
                "card_id":"9030180001331899",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":513.58,
                "card_id":"9130180000361391",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":509.69,
                "card_id":"9130180000969288",
                "bank_card_id":null
            },
            {
                "card_type":1,
                "money":506.29,
                "card_id":"9030180001625577",
                "bank_card_id":null
            },
            {
                "card_type":0,
                "money":500,
                "card_id":"0",
                "bank_card_id":"6259590000065214"
            },
            {
                "card_type":0,
                "money":500,
                "card_id":"0",
                "bank_card_id":"6214839720214899"
            },
            {
                "card_type":1,
                "money":494.62,
                "card_id":"9030180001476467",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":488,
                "card_id":"9100000001398512",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":486.64,
                "card_id":"9130180001097809",
                "bank_card_id":null
            },
            {
                "card_type":1,
                "money":485.22,
                "card_id":"9030180001567291",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":485,
                "card_id":"9130180000817632",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":476.83,
                "card_id":"9130180001418808",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":472,
                "card_id":"9130180000847551",
                "bank_card_id":null
            },
            {
                "card_type":1,
                "money":466.04,
                "card_id":"9030180001631517",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":463.4,
                "card_id":"9130180000866553",
                "bank_card_id":null
            },
            {
                "card_type":2,
                "money":460,
                "card_id":"9130180001310731",
                "bank_card_id":null
            }
        ],
        "end_time":"2018-02-01 23:59:59",
        "unit":{

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


## **卡消费数据表**

```
GET /cards
```

### **Parameters**

* start_time(_Optional_|string)-开始时间
* end_time(_Optional_|string)-结束时间
* search(_Optional_|string)-查询条件(card_id)


|card_type|说明|
| --------------  | :---: |
|0|银行卡|
|1|记名卡|
|2|车队卡|


### **Return**

成功
```
{
    "body":{
        "is_paginated":false,
        "cardrecord_list":[
            {
                "pos_id":null,
                "classification_id":100101,
                "trade_type":0,
                "classification":{
                    "name":"汽油",
                    "original_create_time":"2017-12-17 23:13:05",
                    "belong_id":null,
                    "parent_id":1001,
                    "create_time":"2017-12-09 23:01:28",
                    "modify_time":"2017-12-09 23:01:28",
                    "id":100101
                },
                "bank_unique_id":"1234",
                "original_create_time":"2018-01-15 13:32:52",
                "card_id":"",
                "belong_id":1,
                "bank_card_id":"636",
                "card_type":1,
                "create_time":"2018-01-15 13:32:52",
                "modify_time":"2018-01-15 13:32:52",
                "total":1000,
                "pump_id":0,
                "balance":10000,
                "id":3,
                "unique_id":3
            },
            {
                "pos_id":null,
                "classification_id":100102,
                "trade_type":0,
                "classification":{
                    "name":"柴油",
                    "original_create_time":"2017-12-17 23:13:05",
                    "belong_id":null,
                    "parent_id":1001,
                    "create_time":"2017-12-09 23:01:28",
                    "modify_time":"2017-12-09 23:01:28",
                    "id":100102
                },
                "bank_unique_id":null,
                "original_create_time":"2018-01-15 13:32:52",
                "card_id":"112",
                "belong_id":1,
                "bank_card_id":null,
                "card_type":2,
                "create_time":"2018-01-15 13:32:52",
                "modify_time":"2018-01-15 13:32:52",
                "total":2000,
                "pump_id":0,
                "balance":20000,
                "id":2,
                "unique_id":2
            },
            {
                "pos_id":null,
                "classification_id":100101,
                "trade_type":0,
                "classification":{
                    "name":"汽油",
                    "original_create_time":"2017-12-17 23:13:05",
                    "belong_id":null,
                    "parent_id":1001,
                    "create_time":"2017-12-09 23:01:28",
                    "modify_time":"2017-12-09 23:01:28",
                    "id":100101
                },
                "bank_unique_id":null,
                "original_create_time":"2018-01-15 13:32:52",
                "card_id":"111",
                "belong_id":1,
                "bank_card_id":null,
                "card_type":1,
                "create_time":"2018-01-15 13:32:52",
                "modify_time":"2018-01-15 13:32:52",
                "total":1000,
                "pump_id":0,
                "balance":10000,
                "id":1,
                "unique_id":1
            }
        ],
        "page_obj":{

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


## **异常卡**

```
GET /card/abnormal
```

### **Parameters**


|card_type|说明|
| --------------  | :---: |
|1|记名卡|
|2|车队卡|

|abnormal_type|说明|
| --------------  | :---: |
|1|日异常|
|2|周异常|


### **Return**

成功
```
{
    "body":{
        "abnormalrecord_list":[
            {
                "start_time":"2018-01-15 14:00:21",
                "card_id":"112",
                "belong_id":1,
                "card_type":2,
                "reason":"一周内汽柴油混刷",
                "create_time":"2018-01-15 14:00:21",
                "end_time":"2018-03-01 00:00:00",
                "abnormal_type":2,
                "id":2
            },
            {
                "start_time":"2018-01-15 14:00:21",
                "card_id":"111",
                "belong_id":1,
                "card_type":1,
                "reason":"单日汽油消费 800 元以上",
                "create_time":"2018-01-15 14:00:21",
                "end_time":"2018-03-01 00:00:00",
                "abnormal_type":1,
                "id":1
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

## **获取消息**

```
GET /messages/
```

### **Parameters**


### **Return**

成功
```
{
    "body":{
        "page_obj":{

        },
        "is_paginated":false,
        "deliveryrecord_list":[
            {
                "hash":"7d7b1d8eb0e7dc8d8f90bcb23ae02984",
                "original_create_time":"2018-01-22 23:17:25",
                "belong_id":1,
                "create_time":"2017-12-18 20:14:00",
                "modify_time":"2018-01-22 23:17:27",
                "receiver":"收货",
                "supplier":"油品供应商",
                "truck_number":"青A42168",
                "id":263
            },
            {
                "hash":"beb2c70a042718d75cffe1a488130629",
                "original_create_time":"2018-01-22 23:17:38",
                "belong_id":1,
                "create_time":"2017-12-18 20:14:00",
                "modify_time":"2018-01-22 23:17:40",
                "receiver":"收货",
                "supplier":"油品供应商",
                "truck_number":"青A42168",
                "id":262
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


## **智慧大屏登录**

```
GET /login/
```

### **Parameters**
password(_Required_|string)-密码

### **Return**

成功
```
{
    "body":{
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


# **管理后台API**

## **登录**

```
POST /api/admin/login/
```

### **Parameters**

* name(_Required_|string)-用户名
* password(_Required_|string)-密码

### **Return**

成功
```
{
    "body": {
        "account": {
            "token": "6g0cP7dJKAiHsnSkbFs9Mlvw3Zaijny2",
            "belong": {
                "name": "测试站",
                "slug": "test"
            },
            "name": "test"
        }
    },
    "status": 1,
    "msg": "success"
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

**注：管理API所有接口均需要 login 接口获得的 token 拼装在 url 里**

## **获取库存列表**

```
GET /api/admin/inventories/
```

### **Parameters**

* page(_Optional_|integer)-分页

### **Return**

成功
```
{
    "body": {
        "goodsinventory_list": [
            {
                "third_cls_id": 20020402,
                "second_cls_id": 200204,
                "last_sell_time": "2017-08-10 17:11:00",
                "cost": 0,
                "name": "康师傅 鲜果橙 450ML",
                "barcode": "70001767",
                "original_create_time": "2017-12-17 20:35:34",
                "amount": 117,
                "belong_id": 1,
                "itemcode": "70001767",
                "create_time": "2017-12-17 20:35:34",
                "modify_time": "2017-12-17 22:08:30",
                "hash": "c998243e7485d33de74ddc62513139f5",
                "cls_id": 2002,
                "id": 13655,
                "unit": "瓶"
            },
            {
                "third_cls_id": 20020202,
                "second_cls_id": 200202,
                "last_sell_time": "2017-07-03 16:28:00",
                "cost": 0,
                "name": "统一 小茗同学冰橘绿茶 480ML",
                "barcode": "70247077",
                "original_create_time": "2017-12-17 20:35:53",
                "amount": 0,
                "belong_id": 1,
                "itemcode": "70247077",
                "create_time": "2017-12-17 20:35:53",
                "modify_time": "2017-12-17 22:08:47",
                "hash": "fe79ba9418434cc61d89d2b3ef6b2987",
                "cls_id": 2002,
                "id": 17612,
                "unit": "瓶"
            },
            {
                "third_cls_id": 20010401,
                "second_cls_id": 200104,
                "last_sell_time": "2017-08-15 13:55:00",
                "cost": 0,
                "name": "兰州 (桥) 硬盒香烟(包) 6MG",
                "barcode": "70239821",
                "original_create_time": "2017-12-17 20:35:51",
                "amount": 79,
                "belong_id": 1,
                "itemcode": "70239821",
                "create_time": "2017-12-17 20:35:51",
                "modify_time": "2017-12-17 22:08:45",
                "hash": "b419aa5572c87f91edab6094323321b8",
                "cls_id": 2001,
                "id": 17349,
                "unit": "包"
            },
            {
                "third_cls_id": 20120101,
                "second_cls_id": 201201,
                "last_sell_time": "2017-07-24 20:31:00",
                "cost": 0,
                "name": "巧面馆 方便面老坛酸菜牛肉味 135g",
                "barcode": "70023877",
                "original_create_time": "2017-12-17 20:35:38",
                "amount": 0,
                "belong_id": 1,
                "itemcode": "70023877",
                "create_time": "2017-12-17 20:35:38",
                "modify_time": "2017-12-17 22:08:33",
                "hash": "030612f75d0a2ca748c6ff0351aec35e",
                "cls_id": 2012,
                "id": 14380,
                "unit": "桶"
            },
            {
                "third_cls_id": 20010401,
                "second_cls_id": 200104,
                "last_sell_time": "2017-07-31 21:49:00",
                "cost": 0,
                "name": "云烟 (印象)香烟",
                "barcode": "70015299",
                "original_create_time": "2017-12-17 20:35:37",
                "amount": 100,
                "belong_id": 1,
                "itemcode": "70015299",
                "create_time": "2017-12-17 20:35:37",
                "modify_time": "2017-12-17 22:08:32",
                "hash": "c2eb7da4a2384bfca1dd5ec1d17c1007",
                "cls_id": 2001,
                "id": 14180,
                "unit": "包"
            },
            {
                "third_cls_id": 20060303,
                "second_cls_id": 200603,
                "last_sell_time": "2017-08-18 14:06:00",
                "cost": 0,
                "name": "好时 曲奇奶香巧克力排块 23G",
                "barcode": "70256940",
                "original_create_time": "2017-12-17 20:35:55",
                "amount": 1,
                "belong_id": 1,
                "itemcode": "70256940",
                "create_time": "2017-12-17 20:35:55",
                "modify_time": "2017-12-17 22:08:50",
                "hash": "92bea126c2d46ae2f8e5ce17ea5337e2",
                "cls_id": 2006,
                "id": 18010,
                "unit": "每个"
            },
            {
                "third_cls_id": 20040301,
                "second_cls_id": 200403,
                "last_sell_time": "2017-08-20 11:18:00",
                "cost": 0,
                "name": "光明 莫斯利安 2.4KG",
                "barcode": "70188971",
                "original_create_time": "2017-12-17 20:35:46",
                "amount": 0,
                "belong_id": 1,
                "itemcode": "70188971",
                "create_time": "2017-12-17 20:35:46",
                "modify_time": "2017-12-17 22:08:41",
                "hash": "9d60a70b7a5fdc62dc0bdc353d027907",
                "cls_id": 2004,
                "id": 16248,
                "unit": "每个"
            },
            {
                "third_cls_id": 20020101,
                "second_cls_id": 200201,
                "last_sell_time": "2017-08-16 08:15:00",
                "cost": 0,
                "name": "可口可乐 汽水 330ml",
                "barcode": "70024754",
                "original_create_time": "2017-12-17 20:35:38",
                "amount": 144,
                "belong_id": 1,
                "itemcode": "70024754",
                "create_time": "2017-12-17 20:35:38",
                "modify_time": "2017-12-17 22:08:33",
                "hash": "1c86092ebdf63fd9a6d91e09d1f4eeee",
                "cls_id": 2002,
                "id": 14412,
                "unit": "罐"
            },
            {
                "third_cls_id": 20190802,
                "second_cls_id": 201908,
                "last_sell_time": "2017-05-30 07:55:00",
                "cost": 0,
                "name": "昆仑之星乙二醇型重负荷机动车发动机冷却液",
                "barcode": "405936",
                "original_create_time": "2017-12-17 20:35:32",
                "amount": 0,
                "belong_id": 1,
                "itemcode": "405936",
                "create_time": "2017-12-17 20:35:32",
                "modify_time": "2017-12-17 22:08:28",
                "hash": "700f3bee1e5c360eb8e82f8008c0f38d",
                "cls_id": 2019,
                "id": 13108,
                "unit": "桶"
            },
            {
                "third_cls_id": 20060202,
                "second_cls_id": 200602,
                "last_sell_time": "2017-04-19 13:59:00",
                "cost": 0,
                "name": "绿箭 无糖黑加仑薄荷口味 35粒",
                "barcode": "70192051",
                "original_create_time": "2017-12-17 20:35:46",
                "amount": 0,
                "belong_id": 1,
                "itemcode": "70192051",
                "create_time": "2017-12-17 20:35:46",
                "modify_time": "2017-12-17 22:08:41",
                "hash": "d2fe5b3da4cf6df75151d358ee3e4fa9",
                "cls_id": 2006,
                "id": 16307,
                "unit": "瓶"
            },
            {
                "third_cls_id": 20100103,
                "second_cls_id": 201001,
                "last_sell_time": "2017-08-15 11:19:00",
                "cost": 0,
                "name": "奥利奥 双心脆威化 87G",
                "barcode": "70035465",
                "original_create_time": "2017-12-17 20:35:39",
                "amount": 62,
                "belong_id": 1,
                "itemcode": "70035465",
                "create_time": "2017-12-17 20:35:39",
                "modify_time": "2017-12-17 22:08:34",
                "hash": "b170bc4f4f109ddcedb677351efbe413",
                "cls_id": 2010,
                "id": 14617,
                "unit": "包"
            },
            {
                "third_cls_id": 20050201,
                "second_cls_id": 200502,
                "last_sell_time": "2017-07-18 01:46:00",
                "cost": 0,
                "name": "互助 新版坛头45° 500ML*6",
                "barcode": "70195708",
                "original_create_time": "2017-12-17 20:35:47",
                "amount": 37,
                "belong_id": 1,
                "itemcode": "70195708",
                "create_time": "2017-12-17 20:35:47",
                "modify_time": "2017-12-17 22:08:41",
                "hash": "26aff337530bd78648589dddd648932d",
                "cls_id": 2005,
                "id": 16345,
                "unit": "瓶"
            },
            {
                "third_cls_id": 20120107,
                "second_cls_id": 201201,
                "last_sell_time": "2017-08-08 09:39:00",
                "cost": 0,
                "name": "龙涎香 香卤蛋 35G",
                "barcode": "70168280",
                "original_create_time": "2017-12-17 20:35:45",
                "amount": 139,
                "belong_id": 1,
                "itemcode": "70168280",
                "create_time": "2017-12-17 20:35:45",
                "modify_time": "2017-12-17 22:08:40",
                "hash": "bb90f79aaf3780428bd2bd8284d2b81b",
                "cls_id": 2012,
                "id": 15999,
                "unit": "包"
            },
            {
                "third_cls_id": 20040301,
                "second_cls_id": 200403,
                "last_sell_time": "2017-03-05 19:54:00",
                "cost": 0,
                "name": "伊利 利乐钻安幕希希腊酸奶 205G 1*12",
                "barcode": "70233690",
                "original_create_time": "2017-12-17 20:35:51",
                "amount": 0,
                "belong_id": 1,
                "itemcode": "70233690",
                "create_time": "2017-12-17 20:35:51",
                "modify_time": "2017-12-17 22:08:45",
                "hash": "a5d38c160856d9c3431bd350a3b3b909",
                "cls_id": 2004,
                "id": 17136,
                "unit": "包"
            },
            {
                "third_cls_id": 20120101,
                "second_cls_id": 201201,
                "last_sell_time": "2017-08-18 02:13:00",
                "cost": 0,
                "name": "康师傅油泼辣子酸汤面122g/桶",
                "barcode": "70061532",
                "original_create_time": "2017-12-17 20:35:40",
                "amount": 37,
                "belong_id": 1,
                "itemcode": "70061532",
                "create_time": "2017-12-17 20:35:40",
                "modify_time": "2017-12-17 22:08:36",
                "hash": "bbd8b29e2aa787e1064927b3e6cfb16b",
                "cls_id": 2012,
                "id": 15014,
                "unit": "桶"
            },
            {
                "third_cls_id": 20050201,
                "second_cls_id": 200502,
                "last_sell_time": "2017-02-03 16:01:00",
                "cost": 0,
                "name": "青海湖 青稞酒（蓝瓶） 500ml",
                "barcode": "70259958",
                "original_create_time": "2017-12-17 20:35:56",
                "amount": 2,
                "belong_id": 1,
                "itemcode": "70259958",
                "create_time": "2017-12-17 20:35:56",
                "modify_time": "2017-12-17 22:08:51",
                "hash": "a13e2e66baca53c1f399cf0c432030da",
                "cls_id": 2005,
                "id": 18298,
                "unit": "瓶"
            },
            {
                "third_cls_id": 20010401,
                "second_cls_id": 200104,
                "last_sell_time": "2017-07-25 12:54:00",
                "cost": 0,
                "name": "利群 (软长嘴)香烟 20支",
                "barcode": "70002658",
                "original_create_time": "2017-12-17 20:35:34",
                "amount": 37,
                "belong_id": 1,
                "itemcode": "70002658",
                "create_time": "2017-12-17 20:35:34",
                "modify_time": "2017-12-17 22:08:30",
                "hash": "6274fbdccd5e0ea44519a82998cb08ca",
                "cls_id": 2001,
                "id": 13683,
                "unit": "包"
            },
            {
                "third_cls_id": 20120106,
                "second_cls_id": 201201,
                "last_sell_time": "2017-08-15 10:55:00",
                "cost": 0,
                "name": "金锣 王中王 70g",
                "barcode": "70087506",
                "original_create_time": "2017-12-17 20:35:42",
                "amount": 53,
                "belong_id": 1,
                "itemcode": "70087506",
                "create_time": "2017-12-17 20:35:42",
                "modify_time": "2017-12-17 22:08:38",
                "hash": "47ac7ae382577ba47b6fd37522ded48e",
                "cls_id": 2012,
                "id": 15444,
                "unit": "每个"
            },
            {
                "third_cls_id": 20020502,
                "second_cls_id": 200205,
                "last_sell_time": "2017-08-15 10:53:00",
                "cost": 0,
                "name": "脉动 维生素饮料水蜜桃口味 600ML",
                "barcode": "70003391",
                "original_create_time": "2017-12-17 20:35:35",
                "amount": 33,
                "belong_id": 1,
                "itemcode": "70003391",
                "create_time": "2017-12-17 20:35:35",
                "modify_time": "2017-12-17 22:08:31",
                "hash": "182bee9e5beee614a7ebfce1f44ac1d3",
                "cls_id": 2002,
                "id": 13759,
                "unit": "瓶"
            },
            {
                "third_cls_id": 20150201,
                "second_cls_id": 201502,
                "last_sell_time": "2017-05-01 11:55:00",
                "cost": 0,
                "name": "OLAY 紧致滋润沐浴乳特惠装 720ML",
                "barcode": "70270322",
                "original_create_time": "2017-12-17 20:35:59",
                "amount": 13,
                "belong_id": 1,
                "itemcode": "70270322",
                "create_time": "2017-12-17 20:35:59",
                "modify_time": "2017-12-17 22:08:54",
                "hash": "34118af32fabfe523950d1d42cc2a5da",
                "cls_id": 2015,
                "id": 18813,
                "unit": "瓶"
            }
        ],
        "page_obj": {
            "current": 1,
            "next": 2,
            "total": 320,
            "page_range": [
                {
                    "page": 1
                },
                {
                    "page": 2
                },
                {
                    "page": 3
                }

            ],
            "previous": null
        },
        "is_paginated": true
    },
    "status": 1,
    "msg": "success"
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

## **更新库存信息**

```
POST /api/admin/inventorie/{iid}/
```

### **Parameters**

* iid(_Required_|integer)-库存id
* cost(_Required_|float)-库存成本价

### **Return**

成功
```
{
    "body": {
        "object": {
            "third_cls_id": 20020402,
            "second_cls_id": 200204,
            "last_sell_time": "2017-08-10 17:11:00",
            "cost": "12",
            "name": "康师傅 鲜果橙 450ML",
            "barcode": "70001767",
            "original_create_time": "2017-12-17 20:35:34",
            "amount": 117,
            "belong_id": 1,
            "itemcode": "70001767",
            "create_time": "2017-12-17 20:35:34",
            "modify_time": "2018-01-01 19:26:18",
            "hash": "c998243e7485d33de74ddc62513139f5",
            "cls_id": 2002,
            "id": 13655,
            "unit": "瓶"
        }
    },
    "status": 1,
    "msg": "success"
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

## **获取站点信息**

```
GET /api/admin/site/
```

### **Parameters**


### **Return**

成功
```
{
    "body": {
        "site": {
            "info": "",
            "name": "测试站",
            "slug": "test"
        }
    },
    "status": 1,
    "msg": "success"
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


## **更新站点信息**

```
POST /api/admin/site/
```

### **Parameters**
* content(_Required_|string)-站点介绍


### **Return**

成功
```
{
    "body": {
        "site": {
            "info": "",
            "name": "测试站",
            "slug": "test"
        }
    },
    "status": 1,
    "msg": "success"
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


## **上传图片**

```
POST /api/admin/upload/
```

### **Parameters**
* image(_Required_|file)-图片


### **Return**

成功
```
{
    "body": {
        "url": "/static/image/fe952dd9d091c50bf2635fab2f9992a6.png"
    },
    "status": 1,
    "msg": "success"
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


## **创建油品销售计划**

```
POST /api/admin/plan/
```

### **Parameters**
* fuel_type(_Required_|integer)-油品类型
* plan_type(_Required_|integer)-计划类型
* total(_Optional_|Float)-年总量
* jan(_Optional_|Float)-一月
* feb(_Optional_|Float)-二月
* mar(_Optional_|Float)-三月
* apr(_Optional_|Float)-四月
* may(_Optional_|Float)-五月
* jun(_Optional_|Float)-六月
* jul(_Optional_|Float)-七月
* aug(_Optional_|Float)-八月
* sep(_Optional_|Float)-九月
* oct(_Optional_|Float)-十月
* nov(_Optional_|Float)-十一月
* dec(_Optional_|Float)-十二月

|fuel_type|含义|
| --------------  | :---: |
|1001001|汽油|
|1001002|柴油|

|plan_type|含义|
| --------------  | :---: |
|1|年计划|
|2|月计划|


### **Return**

成功
```
{
    "body": {
    },
    "status": 1,
    "msg": "success"
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


## **油品销售计划列表**

```
GET /api/admin/plans/
```

### **Parameters**

### **Return**

成功
```
{
    "body":{
        "page_obj":{

        },
        "is_paginated":false,
        "fuelplan_list":[
            {
                "mar":1000,
                "feb":1000,
                "aug":1000,
                "sep":1000,
                "apr":1000,
                "fuel_type_id":100102,
                "jun":1000,
                "jul":1000,
                "oct":1000,
                "jan":1000,
                "may":1000,
                "belong_id":1,
                "year":2018,
                "total":12000,
                "nov":1000,
                "dec":1000,
                "id":2
            },
            {
                "mar":1000,
                "feb":1000,
                "aug":1000,
                "sep":1000,
                "apr":1000,
                "fuel_type_id":100101,
                "jun":1000,
                "jul":1000,
                "oct":1000,
                "jan":1000,
                "may":1000,
                "belong_id":1,
                "year":2018,
                "total":12000,
                "nov":1000,
                "dec":1000,
                "id":1
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


## **删除油品销售计划**

```
DELETE /api/admin/plan/{pid}
```

### **Parameters**
pid 为计划 id

### **Return**

成功
```
{
    "body": {
    },
    "status": 1,
    "msg": "success"
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

## **更新预算信息**

```
POST /api/admin/budget/
```

### **Parameters**
* members(_Required_|integer)-加油站人数
* depreciation_cost(_Required_|Float)- 折旧损耗
* salary_cost(_Required_|Float)-员工薪酬
* water_ele_cost(_Required_|Float)-水电暖费
* daily_repair(_Required_|Float)-日常维修
* oil_loss(_Required_|Float)-油品损耗
* other_cost(_Required_|Float)-其他费用
* oil_gross_profit(_Required_|Float)-成品油毛利
* oil_profit(_Required_|Float)-成品油利润
* goods_profit(_Required_|Float)-非油利润
* ton_oil_cost(_Required_|Float)-吨油费用
* ton_oil_g_profit(_Required_|Float)-吨油利润
* per_oil_amount(_Required_|Float)-人均销量
* per_profit(_Required_|Float)-人均利润
* per_goods_income(_Required_|Float)-人均非油收入
* cost_control(_Required_|String)-费用控制方向
* promote(_Required_|String)-促销效果分析
* advice(_Required_|String)-其他管理建议

### **Return**
```
{
    "body":{
        "object":{
            "daily_repair":0,
            "depreciation_cost":"8888",
            "lock":0,
            "per_profit":0,
            "month":"3",
            "salary_cost":"2828",
            "water_ele_cost":0,
            "create_time":"2018-02-02 21:50:29",
            "check":false,
            "goods_profit":0,
            "total_cost":40040,
            "pictures":"/static/image/aba3a49051155eb39f9ec294fae3f765.png,/static/image/e201248d56fa6b80ce98aa101c0f8ac2.png,/static/image/47c2a8cfaef4d7d194798caf6dc5dc84.png,/static/image/5db36e0d35b5045cfafe5a1a12e47ed6.png,/static/image/240193b230d725805ba540644e3adede.png,/static/image/7c552854e43abdb7455a2c0b051ca7ee.png,/static/image/b48001a9939f9a387221fb8fa26546d9.png",
            "per_oil_amount":0,
            "oil_loss":0,
            "id":2,
            "ton_oil_g_profit":0,
            "per_goods_income":0,
            "other_cost":"28324",
            "original_create_time":"2018-02-02 21:50:29",
            "bos_server":"10.97.223.2",
            "members":"11",
            "oil_profit":0,
            "info":"五四加油站隶属于西宁分公司城西经营部，始建于1956年12月20日，占地面积1500平方米，是青海省的第一座加油站，主要经营92#，95#，98#高标号清洁汽油。加油站现有员工16名，本站员工全为市场化员工，平均年龄29岁，是一支充满活力、凝聚力较强的青年团队。",
            "total_profit":0,
            "name":"五四加油站",
            "ton_oil_cost":0,
            "modify_time":"2018-09-29 17:10:16",
            "fuel_server":"10.97.223.1",
            "oil_gross_profit":0
        }
    },
    "status":1,
    "msg":"success"
}
```