# -*- coding: utf8 -*-
import requests
import json
import copy
import hashlib
import sys
import codecs
import random
import time

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class App():
    common = list()
    urls = {
        "getIp": "https://xcx.xybsyw.com/behavior/Duration!getIp.action",
        # "getOpenId": "https://xcx.xybsyw.com/common/getOpenId.action",
        "GetIsUnionId": "https://xcx.xybsyw.com/common/GetIsUnionId.action",
        "getCityId": "https://xcx.xybsyw.com/common/loadLocation!getCityId.action",
        # "Duration": "https://app.xybsyw.com/behavior/Duration.action",  # 心跳
        # "verify": "https://xcx.xybsyw.com/sphere/sphereInfo!verify.action",
        "get_traineeId": "https://xcx.xybsyw.com/student/clock/GetPlan!getDefault.action",
        "GetPlan_detail": "https://xcx.xybsyw.com/student/clock/GetPlan!detail.action",
        "login": "https://xcx.xybsyw.com/login/login.action",
        # "checkAccount": "https://xcx.xybsyw.com/login/checkAccount.action",
        "checkIn": "https://xcx.xybsyw.com/student/clock/Post.action",

    }

    @classmethod
    def handler_request(cls, reqObj, req_method, url, data=None) -> object:
        """
        :return: response.json()
        """
        if "xcx.xybsyw" in url:
            reqObj.headers["Host"] = "xcx.xybsyw.com"
        elif "app.xybsyw" in url:
            reqObj.headers["Host"] = "app.xybsyw.com"
        elif "restapi.amap" in url:
            reqObj.headers["Host"] = "restapi.amap.com"

        if req_method == "get":
            return reqObj.get(url, params=data).json()

        if req_method == "post":
            return reqObj.post(url, data=data).json()

    def __init__(self, userInfo=None, phoneInfo=None, sign=False):
        """
        :param userInfo: 个人信息、以及位置信息
        :param phoneInfo: 移动设备型号相关信息
        :param sign: 开启 巴法云 标志
        """
        if str(userInfo["addressLocation"]) == "":
            try:
                raise Addr("必须先手动提取 目标地址的经纬度信息，访问 https://api.map.baidu.com/lbsapi/getpoint/index.html 进行提取经纬度信息")
            except Addr as e:
                print(e.value)

        self.userInfo = userInfo
        self.s = requests.Session()
        self.openId = "ooru94oy6OWtK7Xsc2azPH2SI78A"
        self.unionId = "oHY-uwcaYNyNd9Jlj_lDOHWkvlXU"
        self.traineeId = ""
        self.userId = ""
        self.checkIn_info = dict()
        self.s.headers = {
            "Host": "",
            "Connection": "keep-alive",
            "User-Agent": "",
            "cookie": "",
            "charset": "utf-8",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "content-type": "application/x-www-form-urlencoded"

        }

        if phoneInfo is None:  # user 有 设备信息
            self.system = self.userInfo["phoneInfo"]["system"]
            self.model = self.userInfo["phoneInfo"]["model"]
            self.netType = self.userInfo["netType"]
            self.brand = self.userInfo["phoneInfo"]["brand"]
            self.platform = self.userInfo["phoneInfo"]["platform"]

        else:
            self.system = phoneInfo["system"]
            self.model = phoneInfo["model"]
            self.netType = self.userInfo["netType"]
            self.brand = phoneInfo["brand"]
            self.platform = phoneInfo["platform"]

        self.sign = sign

        self.s.headers[
            "User-Agent"] = "Mozilla/5.0 (Linux; " + self.system + "; " + self.model + " Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3195 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/8710 MicroMessenger/8.0.16.2040(0x2800103B) Process/appbrand0 WeChat/arm64 Weixin NetType/" + self.netType + " Language/zh_CN ABI/arm64 MiniProgramEnv/android"

    def getIp(self):
        getIp_resp = App.handler_request(self.s, "post", App.urls["getIp"], {})

        if getIp_resp["code"] == "200" and getIp_resp["msg"] == "success" and getIp_resp["data"]["ip"] != "":
            ...
        else:
            raise Exception("Get Real IP Error !\n")

    def GetIsUnionId(self) -> None:
        """
        协议流程
        :return: None
        """
        if self.s.headers.get("cookie") == "":

            GetIsUnionId_resp = App.handler_request(self.s, "post", App.urls["GetIsUnionId"],
                                                    {"openId": self.openId, "unionId": ""})
        else:
            GetIsUnionId_resp = App.handler_request(self.s, "post", App.urls["GetIsUnionId"],
                                                    {"openId": self.openId, "unionId": self.unionId})

        if GetIsUnionId_resp["code"] == "200" and dict(GetIsUnionId_resp["data"]).get("isUnionId") == True:
            ...
        else:
            raise Exception("Protocol is Failed !\n")

    def getCityId(self):
        """
        :return: getCityId
        """
        getCityId_resp = App.handler_request(self.s, "post", App.urls["getCityId"],
                                             {"cityName": self.checkIn_info.get("city")})
        if getCityId_resp["code"] == "200" and getCityId_resp["msg"] == "操作成功":
            # self.checkIn_info["cityId"] = getCityId_resp["data"]
            ...
        else:
            raise Exception("Protocol is Failed !\n")

    def GetAdcode(self) -> str:
        """
        :return: 坐标信息
        """
        params = {
            "key": "c222383ff12d31b556c3ad6145bb95f4",
            "location": self.userInfo["addressLocation"],
            "extensions": "all",
            "s": "rsx",
            "platform": "WXJS",
            "appname": "c222383ff12d31b556c3ad6145bb95f4",
            "sdkversion": "1.2.0",
            "logversion": "1.2.2.0"
        }
        GetLocationInfo_resp = App.handler_request(self.s, "get", "https://restapi.amap.com/v3/geocode/regeo", params)

        if GetLocationInfo_resp["info"] == "OK" and GetLocationInfo_resp["infocode"] == "10000":
            # self.checkIn_info["city"] = GetLocationInfo_resp["regeocode"]["addressComponent"]["city"]
            # self.checkIn_info["province"] = GetLocationInfo_resp["regeocode"]["addressComponent"]["province"]
            return GetLocationInfo_resp["regeocode"]["addressComponent"]["adcode"]

    def getTraineeId(self) -> str:
        """
        :return: traineeId
        """
        getTraineeId_resp = App.handler_request(self.s, "post", App.urls["get_traineeId"], {})
        if getTraineeId_resp["code"] == "200" and getTraineeId_resp["msg"] == "操作成功":
            self.traineeId = str(getTraineeId_resp["data"]["clockVo"]["traineeId"])
        else:
            raise Exception("获取实习任务ID失败")

    def handler_checkIn_(self):
        self.checkIn_info["model"] = self.model
        self.checkIn_info["brand"] = self.brand
        self.checkIn_info["platform"] = self.platform
        self.checkIn_info["system"] = self.system
        self.checkIn_info["openId"] = self.openId
        self.checkIn_info["unionId"] = self.unionId
        self.checkIn_info["traineeId"] = self.traineeId
        self.checkIn_info["adcode"] = self.GetAdcode()
        self.checkIn_info["lat"] = self.userInfo["addressLocation"].split(",")[1]
        self.checkIn_info["lng"] = self.userInfo["addressLocation"].split(",")[0]
        self.checkIn_info["address"] = self.userInfo["addressName"]
        self.checkIn_info["deviceName"] = self.model
        self.checkIn_info["punchInStatus"] = "0"
        self.checkIn_info["clockStatus"] = "2"

        checkIn_resp = App.handler_request(self.s, "post", App.urls["checkIn"], data=self.checkIn_info)
        if checkIn_resp["code"] == "200" and checkIn_resp["msg"] == "success":
            content = "签到成功"
        else:
            content = "签到失败"
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        print(content)
        if self.sign and self.userInfo["bemfa"] != "":
            requests.get(
                'http://api.bemfa.com/api/wechat/v1/weget.php?type=2&uid=' + self.userInfo[
                    "bemfa"] + '&device=校友邦打卡&msg={}'.format(
                    content), headers=headers)

        sys.exit(0)

    def GetPlan_detail(self):
        """
        获取 打卡 状态
        :return:
        """
        Plan_detail_resp = App.handler_request(self.s, "post", App.urls["GetPlan_detail"],
                                               {"traineeId": self.traineeId})

        if Plan_detail_resp["code"] == "200" and Plan_detail_resp["msg"] == "操作成功":
            if dict(Plan_detail_resp["data"]).get("clockInfo").get("inAddress") == "":
                return self.handler_checkIn_()

            else:
                """已经打卡"""
                content = "重复签到？"
                headers = {
                    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
                }
                print(content, self.sign)
                if self.sign and self.userInfo["bemfa"] != "":
                    requests.get(
                        'http://api.bemfa.com/api/wechat/v1/weget.php?type=2&uid=' + self.userInfo[
                            "bemfa"] + '&device=校友邦打卡&msg={}'.format(
                            content), headers=headers)

                sys.exit(0)

        else:
            raise Exception("Get Detail Msg Error !\n")

    def Login(self):
        m = hashlib.md5()
        m.update(self.userInfo["pwd"].encode("utf-8"))
        LoginInfo = {
            "username": self.userInfo["user"],
            "password": m.hexdigest(),
            "openId": self.openId,
            "unionId": self.unionId,
            "model": self.model,
            "brand": self.brand,
            "platfor": self.platform,
            "system ": self.system,
            "deviceId": ""
        }
        login_resp = App.handler_request(self.s, "post", App.urls["login"], LoginInfo)
        if login_resp["msg"] != "登录成功":
            content = "Login Failed !"
            headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }
            if self.sign and self.userInfo["bemfa"] != "":
                requests.get(
                    'http://api.bemfa.com/api/wechat/v1/weget.php?type=2&uid=' + self.userInfo[
                        "bemfa"] + '&device=校友邦打卡&msg={}'.format(
                        content), headers=headers)

            raise Exception("Login Failed !")

        self.s.headers["cookie"] = "JSESSIONID=" + login_resp["data"]["sessionId"]
        self.userId = login_resp["data"]["loginerId"]

    def destory(self):
        """
        完成任务自毁
        :return:
        """
        del self


class Addr(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# 本地测试专用
# if __name__ == '__main__':


# 腾讯云函数专用
def main_handler(event, context):
    time.sleep(random.randint(10, 400))

    # *************************  根据意愿 手动修改 ***************************
    # 是否开启 巴法云 通知
    # sign = True 表示 开启 巴法云 通知
    # sign = False 表示 关闭 巴法云 通知
    # 默认关闭 巴法云 通知
    sign = True  # 开启巴法云，需要将 巴法云密钥  作为 user_info.json 文件中的 bemfa 的字段值 填入
    # sign = False # 关闭
    # ***********************************************************************

    with open("user_info.json", encoding="utf-8") as fp:
        info = json.load(fp)
        if len(info) < 1:
            raise Exception("null")
        App.common = copy.deepcopy(info["users"])

    if len(App.common) > 0:

        for userInfo in App.common:

            if userInfo["phoneInfo"]["model"] == "" and userInfo["phoneInfo"]["brand"] == "" and userInfo["phoneInfo"][
                "platform"] == "":
                app = App(userInfo, info["phoneInfo"], sign)
            else:
                app = App(userInfo, phoneInfo=None, sign=sign)
            app.getIp()
            app.Login()
            app.getTraineeId()
            app.GetPlan_detail()
            app.destory()
