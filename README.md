```json
{

    "users":[
      {
        "user": "账号也就是手机号", 
        "pwd": "密码",
        "netType": "WIFI或者流量（按照之前正常打卡时的网络环境）",
        "clientIP": "切换成常用的网络环境然后访问  https://ip38.com/ ",
        "addressLocation": "实习地址的经纬度信息 https://api.map.baidu.com/lbsapi/getpoint/index.html",
        "addressName": "xxxx园xxxx栋",
        "phoneInfo": {
            "model": "MI MAX 2",  // 可选（可留空）
            "brand": "Xiaomi",    // 可选（可留空）
            "platform": "android",  // 可选（可留空），若 以上可选项都是空，那么移动设备信息默认使用 phoneInfo对象中的信息 
            "system": "Android 7.1.1"  // 可选（可留空），要填写就按实际情况
        },
        "bemfa":"巴法云密钥",
        "CheckInNotice": true,  // 是否开启 巴法云通知，true为 开启，false 为关闭
        "signInture": 0  // 此字段值无需改动
        // 打卡时间点，该字段记录第一次打卡的时间点，是否改变取决于 user_info.json 文件是否 可写
      }
    ],
  "phoneInfo": {
            "model": "MI MAX 2",
            "brand": "Xiaomi",
            "platform": "android",
            "system": "Android 7.1.1"
        }
}
````


#### 如下例子

```json
{
    "bemfa":"f5d361a74585...45856",  // 巴法云密钥
    "users":[
      {
        "user": "13800138000",  // 账号
        "pwd": "123456",
        "netType": "WIFI",
        "clientIP": "192.168.1.1",
        "addressLocation": "116.404147,39.914949",  // 北京天安门入口 经纬度
        "addressName": "xxx港xxx栋",  // 最好模拟位置然后抓包对比
        "phoneInfo": {
            "model": "",
            "brand": "",
            "platform": "",
            "system": ""
        },
        "bemfa":"f5d361a74585...45856" // 巴法云密钥
        "CheckInNotice": true,  // 开启 巴法云通知
        "signInture": "2022-03-28 09:01:33"
      }
    ],
  "phoneInfo": {
            "model": "MI MAX 2",
            "brand": "Xiaomi",
            "platform": "android",
            "system": "Android 7.1.1"
        }
}
```

#### 注意：开启 巴法云通知，要将 巴法云密钥 填到 user_info.json 文件中的 bemfa 的字段中，否则 巴法云通知 还是在 关闭状态
