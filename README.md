```json
{

    "users":[
      {
        "user": "账号也就是手机号",   // 必填
        "pwd": "密码",  // 必填
        "netType": "WIFI或者流量（按照之前正常打卡时的网络环境）",  // 必填
        "clientIP": "切换成常用的网络环境然后访问  https://cip.cc/ ",  // 必填
        "addressLocation": "实习地址的经纬度信息 https://api.map.baidu.com/lbsapi/getpoint/index.html",  // 当前版本必填，下一个发布版 自动获取签到地址
        "addressName": "xxxx园xxxx栋",  // 当前版本必填，下一个发布版 自动获取签到地址
        "phoneInfo": {
            "model": "MI MAX 2",  // 可选（可留空）
            "brand": "Xiaomi",    // 可选（可留空）
            "platform": "android",  // 可选（可留空），若 以上可选项都是空，那么移动设备信息默认使用 phoneInfo对象中的信息 
            "system": "Android 7.1.1"  // 可选（可留空），要填写就按实际情况
        },
        "bemfa":"巴法云密钥", // 可选（可留空）
        "CheckInNotice": true, // 可选（可留空） // 是否开启 巴法云通知，true为 开启，false 为关闭
        "signInture": 0  // 此字段值无需改动
        // 打卡时间点，该字段记录第一次打卡的时间点，是否改变取决于 user_info.json 文件是否拥有 可写权限
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
        "signInture": 0
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
