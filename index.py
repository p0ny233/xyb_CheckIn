# -*- coding: utf8 -*-
import requests
import json
import hashlib
import sys
import codecs
import random
import time
import os

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

mode1 = 1

mode2 = 2


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
    def handler_Notice(cls, secKey, note=None, UA=None) -> None:
        """
        :param secKey: 巴法云密钥
        :param note: msg content
        :return: None
        """
        if not secKey:
            raise Exception("Make sure user conf is Corrected")

        header = {
            "user-agent": UA
        }

        url = 'http://api.bemfa.com/api/wechat/v1/weget.php?type=2&uid=' + secKey + '&device=校友邦打卡&msg={}'.format(
            note)
        requests.get(url=url, headers=header)

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
            "cookie": "",
            "charset": "utf-8",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "content-type": "application/x-www-form-urlencoded"

        }

        self.s.headers.update()

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
        """
        模式一：
            1. 手机先切换成 按照之前正常打卡时的网络环境
            2. 浏览器网址：https://ip38.com/
            3. 将 您的本机IP地址：xxx.xxx.xxx.xx，中的 xxx.xxx.xxx.xx  写入 UserInfo.json 文件中的 clientIP 字段

        模式二：百度搜索  目标地区的IP如：广州IP，任意 选，然后在 写入 UserInfo.json 文件中的 clientIP 字段
        :return: IP
        """
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
        GetLocationInfo_resp = App.handler_request(self.s, "get", "https://restapi.amap.com/v3/geocode/regeo",
                                                   params)

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

    def handler_checkIn_(self) -> tuple:
        """
        :return: (bool, String)
        """
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
            Plan_detail_resp = App.handler_request(self.s, "post", App.urls["GetPlan_detail"],
                                                   {"traineeId": self.traineeId})

            YYMMDD = dict(Plan_detail_resp["data"]).get("clockInfo").get("date").replace(".", "-")
            HHMMSS = dict(Plan_detail_resp["data"]).get("clockInfo").get("inTime").replace(".", ":")
            date = YYMMDD + " " + HHMMSS
            note = "于 " + date + " 签到成功"
            signInture = (True, note, date, 1)
        else:
            note = "签到失败"
            signInture = (False, note, None, 0)
            # with open("user_info.json", encoding="utf-8") as fp:
            #     info = json.load(fp)
            #     info["users"]["signInture"] == 0
        return signInture

    def GetPlan_detail(self) -> tuple:
        """
        获取 打卡 状态
        :return:
        """
        note = "获取打卡状态失败"
        Inture = None
        writeable = None
        Plan_detail_resp = App.handler_request(self.s, "post", App.urls["GetPlan_detail"],
                                               {"traineeId": self.traineeId})
        if Plan_detail_resp["code"] == "200" and Plan_detail_resp["msg"] == "操作成功":
            if dict(Plan_detail_resp["data"]).get("clockInfo").get("inAddress") == "" or dict(
                    Plan_detail_resp["data"]).get("clockInfo").get("inTime") == "":
                Inture, note, date, writeable = self.handler_checkIn_()
            else:
                """已经打过卡"""
                Inture = True
                date = dict(Plan_detail_resp["data"]).get("clockInfo").get("date").replace(".", "-")
                inTime = dict(Plan_detail_resp["data"]).get("clockInfo").get("inTime").replace(".", ":")
                date = date + " " + inTime
                note = "重复签到？ 在" + date + " 时 已经签到"

            if self.sign and self.userInfo["bemfa"] != "":
                App.handler_Notice(self.userInfo["bemfa"], note, self.s.headers["User-Agent"])
                print(note, self.sign)
                print("CheckIn Flag > " + str(Inture))
                print("\nnote Flag > " + note)

        else:
            if self.sign and self.userInfo["bemfa"] != "":
                App.handler_Notice(self.userInfo["bemfa"], note, self.s.headers["User-Agent"])

            raise Exception("Get Detail Msg Error !\n")

        return (Inture, date, writeable)

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
            if self.sign and self.userInfo["bemfa"] != "":
                App.handler_Notice(self.userInfo["bemfa"], content, self.s.headers["User-Agent"])
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


def SelectCheckInMode(userconfpath):
    """
    mode1: no status CheckIn
    mode2: Remember last inTime
    :return: mode1 or mode2
    """
    return mode2 if os.access(userconfpath, os.W_OK) else mode1


def NoStatCheckIn(UserConfPath, mode) -> bool:
    """
    :param UserConfPath: user conf json path
    :param mode: Read-Only
    :return:
    """
    with open(UserConfPath, mode, encoding="utf-8") as fp:
        info = json.load(fp)
        if len(info) < 1:
            raise Exception("null")
        # App.common = copy.deepcopy(info["users"])
        App.common = info["users"]
        if len(App.common) > 0:
            for _, userInfo in enumerate(App.common):

                if userInfo["phoneInfo"]["model"] == "" and userInfo["phoneInfo"]["brand"] == "" and \
                        userInfo["phoneInfo"][
                            "platform"] == "":
                    app = App(userInfo, info["phoneInfo"], userInfo["CheckInNotice"])
                else:
                    app = App(userInfo, phoneInfo=None, sign=userInfo["CheckInNotice"])

                app.getIp()
                app.Login()
                app.getTraineeId()
                return app.GetPlan_detail()[0]


def StatCheckIn(UserConfPath, mode="r+", uname="win32") -> bool:
    """
    :param UserConfPath: user conf json path
    :param mode: Read And Write
    :param uname: OS system name
    :return:
    """
    # if uname.startswith("win32"):
    #     _,TempFilePath = tempfile.mkstemp(prefix="xyb_check_", suffix=".json")
    # elif uname.startswith("Linux"):
    #     TempFilePath = "./." + UserConfPath
    #     cmd_args = ["cp","-r","-f",UserConfPath,TempFilePath]
    #     subprocess.call(cmd_args,shell=False)
    fix_count = 0
    with open(UserConfPath, mode, encoding="utf-8") as fp:
        info = json.load(fp)
        if len(info) < 2:
            raise Exception("null")
        # App.common = copy.deepcopy(info["users"])
        App.common = info.get("users")
        if len(App.common) > 0:
            for _, userInfo in enumerate(App.common):
                timestamp = int(time.mktime(time.strptime(info.get("users")[_]["signInture"], "%Y-%m-%d %H:%M:%S")))

                print(info.get("users")[_]["signInture"] + " >>>>>>  " + timestamp)
                if not int(time.time()) - timestamp > 86300:
                    continue
                if userInfo["phoneInfo"]["model"] == "" and userInfo["phoneInfo"]["brand"] == "" and \
                        userInfo["phoneInfo"][
                            "platform"] == "":
                    app = App(userInfo, info["phoneInfo"], userInfo["CheckInNotice"])
                else:
                    app = App(userInfo, phoneInfo=None, sign=userInfo["CheckInNotice"])
                app.getIp()
                app.Login()
                app.getTraineeId()
                signInflag, date, writeable = app.GetPlan_detail()
                # (bool, "2022")
                if writeable:
                    fix_count += 1
                    info.get("users")[_]["signInture"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date))

            if fix_count > 0:
                fp.seek(0, 0)
                fp.truncate()
                fp.write(json.dumps(info))

            return signInflag

        else:
            print("No User")


# 腾讯云函数专用
def main_handler(event=None, context=None):
    time.sleep(random.randint(10, 400))

    # print(os.path.dirname(__file__))  # F:/DeskTop/xyb_CheckIn

    UserConfPath = os.getcwd() + "/user_info.json"  # 'F:\\DeskTop\\xyb_CheckIn/user_info.json'

    if not os.path.exists(UserConfPath):
        print("User JSON FIle Is not exists")
        return False

    if SelectCheckInMode(UserConfPath) == mode1:
        """
        no status mode1
        """
        return NoStatCheckIn(UserConfPath, "r")

    elif SelectCheckInMode(UserConfPath) == mode2:
        """
        Remember last inTime
        """
        StatCheckIn(UserConfPath, "r+", "win32")


# 本地测试专用 放开 以下注释 可在 win以及Linux终端上进行测试
if __name__ == '__main__':
    main_handler()
