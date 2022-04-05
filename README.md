### 使用教程

>
> 使用过程中，需要改动的内容都在 `user_info.json` 文件中

```json
{

    "users":[
      {
        "user": "账号也就是手机号",   // 必填
        "pwd": "密码",  // 必填
        "netType": "WIFI",
        "clientIP": "切换成常用的网络环境然后访问  https://cip.cc/ ",  // 必填
        "phoneInfo": {
            "model": "",  // 可选（可留空）
            "brand": "",    // 可选（可留空）
            "platform": "",  // 可选（可留空），若 以上可选项都是空，那么移动设备信息默认使用 下面的phoneInfo对象中的信息 
            "system": ""  // 可选（可留空）
            // 这里的phoneInfo 中的四个字段 要填写就按自己手机的实际情况填写
        },
        "bemfa":"巴法云密钥", // 可选（可留空，双引号不可去掉）
        "CheckInNotice": false, // 可选（可留空） // 是否开启 巴法云通知，true为 开启，false 为关闭
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

#### 如下对以上各个字段的解释

> 1. user：用户的账号，也就是用手机号
> 2. pwd ：用户的密码
> 3. netType：打卡时使用的是 `WIFI`，无需修改
>
> 4. clientIP：在签到时候使用的是哪个IP。
>
>    - 获取 clientIP 方式：
>
>       a. 按照之前签到时使用的网络环境`4G` / `5G` / `WIFI`，切换成对应的网络环境后。
>
>       b. 浏览器访问：`http://cip.cc/`
>
>       c. 访问该网站 返回 的页面中 `IP	: 10.29.16.16`
>
>       d. 将 `10.29.16.16` 作为 `ClientIP` 字段的值 填入
>
>       e. 如：`"clientIP": "10.29.16.16",`
>
> 5. phoneInfo 里面的内容，是可选项，留空就可以。
>
> 6. bemfa：主要用于在微信上通知是否完成相对应的任务情况`失败` / `成功`。巴法云私钥【记得绑定微信】
> 
>    - 秘钥获取方式
>  
>      `https://cloud.bemfa.com/user/index.html?c=2`
> 
> 7. CheckInNotice：用于 `开启` / `关闭` 巴法云通知
>
>    - 关闭
>      
>      代码执行完毕，没有通知到手机微信上
> 
>   - 开启
> 
>     代码执行完毕，会有通知发送到手机微信上【注意前提是微信关联了巴法云，同时 巴法云秘钥 已经 填到 `bemfa` 字段中】 
> 
> 8. signInture：标记 当天的 第一次签到 时间，注：重复签到 不会更新内容
>
>     `signInture` 字段值会不会改变 取决于 运行代码时，`user_info.json` 文件是否拥有 `可写权限`，若有 `可写权限`，内容会被更新，反之
> 
> 9. 最后一个 phoneInfo，不推荐修改，这是最基础的设备信息。
> 
> 
> 字段总结：至少修改
>




#### 如下例子

```json
{
    "users":[
      {
        "user": "13800138000",
        "pwd": "123456",
        "netType": "WIFI",
        "clientIP": "10.29.16.16",
        "phoneInfo": {
            "model": "",
            "brand": "",
            "platform": "",
            "system": ""
        },
        "bemfa":"",
        "CheckInNotice": true,
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

**注意：开启 巴法云通知，要将 `巴法云密钥` 填到 `user_info.json` 文件中的 `bemfa`的字段中，同时`CheckInNotice` 字段的值是 `true` ,若前面条件没有同时成立，那么 巴法云通知 还是在 关闭状态**

### 配置文件修改好之后

1. 可以在云函数中的 `终端` 或者 `部署测试`

2. 可以在装有`Python`的 Windows环境下测试

3. 可以在装有`Python`的 Linux环境下测试