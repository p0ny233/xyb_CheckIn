# -*- coding: utf8 -*-
# Author：p0ny
# Date ：2022-04-04 23:46
# Tool ：PyCharm
import requests
import json
import hashlib
import sys
import codecs
import random
import time
import os
import platform

mode1 = 1

mode2 = 2

DEBUG = True

# if print request log
REQ_DEBUG = False


class App():
    common = list()

    urls = {
        "getIp": "https://xcx.xybsyw.com/behavior/Duration!getIp.action",
        # "getOpenId": "https://xcx.xybsyw.com/common/getOpenId.action",
        "GetIsUnionId": "https://xcx.xybsyw.com/common/GetIsUnionId.action",
        "getCityId": "https://xcx.xybsyw.com/common/loadLocation!getCityId.action",
        "Duration": "https://app.xybsyw.com/behavior/Duration.action",  # 心跳
        # "verify": "https://xcx.xybsyw.com/sphere/sphereInfo!verify.action",
        "get_traineeId": "https://xcx.xybsyw.com/student/clock/GetPlan!getDefault.action",
        "GetPlan_detail": "https://xcx.xybsyw.com/student/clock/GetPlan!detail.action",
        "login": "https://xcx.xybsyw.com/login/login.action",
        # "checkAccount": "https://xcx.xybsyw.com/login/checkAccount.action",
        # "checkIn": "https://xcx.xybsyw.com/student/clock/Post.action",
        "checkIn": "https://xcx.xybsyw.com/student/clock/Post!autoClock.action",
        "getIpAddr": "https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=ipv4&co=&resource_id=5809&t=" + str(
            int(time.time() * 1000)) + "&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu",
        "getProjectList": "https://xcx.xybsyw.com/student/progress/ProjectList.action",
        "LoadProjects": "https://xcx.xybsyw.com/student/practiceplan/independent/LoadProjects.action",
        "LoadSummaryPostById": "https://xcx.xybsyw.com/student/practiceplan/independent/LoadSummaryPostById.action",
        "saveEpidemicSituation": "https://xcx.xybsyw.com/student/clock/saveEpidemicSituation.action",
        "LoadAccountInfo": "https://xcx.xybsyw.com/account/LoadAccountInfo.action",
    }

    @classmethod
    def App_Log(cls, *args) -> None:
        """
        :param msg: dest msg
        :return: None
        """
        for param in args:
            if type(param) is dict or type(param) is bool:
                param = json.dumps(param, indent=4, ensure_ascii="utf-8")
            if "秒" in param:
                print("\rxyb_TAG \t" + param, end="", flush=True)
                return None
            if r"\u" in param:
                print("xyb_TAG \t" + param.encode("utf-8").decode("unicode_escape"), flush=True)
                return None

            print("xyb_TAG \t" + param, flush=True)

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

        RESP = None

        if req_method == "get":
            if REQ_DEBUG:
                App.App_Log(url, reqObj.headers, data)

            RESP = reqObj.get(url, params=data).json()
            if REQ_DEBUG:
                # App.App_Log(url, reqObj.headers, data)
                App.App_Log(RESP)
            return RESP

        if req_method == "post":
            if REQ_DEBUG:
                App.App_Log(url, reqObj.headers, data)

            RESP = reqObj.post(url, data=data).json()
            if REQ_DEBUG:
                # App.App_Log(url, reqObj.headers, data)
                App.App_Log(RESP)
            return RESP

    @classmethod
    def getIpAddr(cls, ip: None) -> str:
        headers = {
            "User_Agenet": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            "Host": App.urls.get("getIpAddr").split("/")[2]
        }
        rep = requests.get(App.urls.get("getIpAddr").replace("ipv4", ip), headers=headers)
        return json.loads(rep.text[20:-1:]).get("data")[0].get("location")

    @classmethod
    def print_user_base_info(cls, _, userInfo: dict, mode: str) -> None:
        try:
            App.App_Log(
                ("+" * 30) + "\t正在进行第 【" + str(_ + 1) + "】 位用户 " + ("有" if mode == "r+" else "无") + "状态打卡\t" + (
                        "+" * 30))
            App.App_Log("用户: " + userInfo["user"] + "  running...")
            App.App_Log("该用户基本配置信息如下：")
            App.App_Log("\t用户IP: " + userInfo["clientIP"])
            App.App_Log("\t用户IP归属地: " + App.getIpAddr(userInfo["clientIP"]))
            App.App_Log("\t用户打卡网络环境: " + userInfo["netType"])
            App.App_Log("\t用户是否开启巴法云通知: " + ("是" if userInfo["CheckInNotice"] else "否"))
            App.App_Log("\t用户巴法云通知是否正常: " + str("是" if len(userInfo["bemfa"]) == 32 else "否") + "\t 该字段仅供参考")

        except KeyError:
            raise Exception("user_info.json 用户配置信息文件有误, 请检查...")

    def __init__(self, userInfo=None, phoneInfo=None, sign=False):
        """
        :param userInfo: 个人信息、以及位置信息
        :param phoneInfo: 移动设备型号相关信息
        :param sign: 开启 巴法云 标志
        """

        #
        # if str(userInfo["addressLocation"]) == "":
        #     try:
        #         raise Addr("必须先手动提取 目标地址的经纬度信息，访问 https://api.map.baidu.com/lbsapi/getpoint/index.html 进行提取经纬度信息")
        #     except Addr as e:
        #         print(e.value)
        # 已经更新 为 自动提取 经纬度信息

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

        self.s.headers["User-Agent"] = "Mozilla/5.0 (Linux; " + self.system + "; " + self.model + " Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3195 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/8710 MicroMessenger/8.0.16.2040(0x2800153F) Process/appbrand0 WeChat/arm64 Weixin NetType/" + self.netType + " Language/zh_CN ABI/arm64 MiniProgramEnv/android"
    def AutoGetCheckInLocation(self) -> None:
        """
        修复 手动获取签到坐标位置不精确 问题
        :return:
        """
        getProjectList_resp = App.handler_request(self.s, "post", App.urls["getProjectList"], data={})
        if getProjectList_resp["code"] != "200" or getProjectList_resp["msg"] != "获取列表成功":
            raise Exception("Auto Get Location Is Failed")
        else:
            self.planId = getProjectList_resp["data"][0]["planId"]
            self.projectId = getProjectList_resp["data"][0]["projectList"][0]["projectId"]
            # if DEBUG:
            #     App.App_Log("self.planId : " + str(self.planId),"self.projectId : " + str(self.projectId))
            if not self.planId:
                raise Exception("get planId is failed...")

            getSummaryId_resp = App.handler_request(self.s, "post", App.urls["LoadProjects"],
                                                    data={"planId": self.planId})
            if getSummaryId_resp["code"] != "200" and getSummaryId_resp["msg"] != "获取列表成功":
                raise Exception("get SummaryId is failed...")
            self.summaryId = getSummaryId_resp["data"][0]["summaryId"]

            if not self.summaryId:
                raise Exception("summaryId is none! ")
            AutoGetCheckInLocation_resp = App.handler_request(self.s, "post", App.urls["LoadSummaryPostById"],
                                                              data={"summaryPostId": self.summaryId})
            if AutoGetCheckInLocation_resp["code"] != "200" and AutoGetCheckInLocation_resp["msg"] != "获取列表成功":
                raise Exception("Get lng and Get lat is error ! ")
            # 经度
            self.longitude = str(AutoGetCheckInLocation_resp["data"]["longitude"]) + "00"
            # 纬度
            self.latitude = str(AutoGetCheckInLocation_resp["data"]["latitude"]) + "00"
            # 街道
            self.street = AutoGetCheckInLocation_resp["data"]["street"]
            if DEBUG:
                App.App_Log("\t用户打卡签到经纬度: " + self.longitude + ", " + self.latitude)
                App.App_Log("\t用户打卡签到地址: " + self.street)

            return None

    def getIp(self):
        """
        模式一：
            1. 手机先切换成 按照之前正常打卡时的网络环境
            2. 浏览器网址：https://cip.cc.com/
            3. 将 您的本机IP地址：xxx.xxx.xxx.xx，中的 xxx.xxx.xxx.xx  写入 user_info.json 文件中的 clientIP 字段

        模式二：百度搜索  目标地区的IP如：广州IP，任意 选，然后在 写入 user_info.json 文件中的 clientIP 字段
        :return: IP
        """
        getIp_resp = App.handler_request(self.s, "post", App.urls["getIp"], {})

        if getIp_resp["code"] == "200" and getIp_resp["msg"] == "success" and getIp_resp["data"]["ip"] != "":
            pass
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
            pass
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
            pass
        else:
            raise Exception("Protocol is Failed !\n")

    def GetAdcode(self) -> None:
        """
        :return: 坐标信息
        """
        params = {
            "key": "c222383ff12d31b556c3ad6145bb95f4",
            "location": str(self.longitude) + "," + str(self.latitude),
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
            self.adcode = GetLocationInfo_resp["regeocode"]["addressComponent"]["adcode"]
            self.city = GetLocationInfo_resp["regeocode"]["addressComponent"]["city"]
            self.province = GetLocationInfo_resp["regeocode"]["addressComponent"]["province"]
            self.country = GetLocationInfo_resp["regeocode"]["addressComponent"]["country"]

    def getTraineeId(self) -> str:
        """
        :return: traineeId
        """
        getTraineeId_resp = App.handler_request(self.s, "post", App.urls["get_traineeId"], {})
        if getTraineeId_resp["code"] == "200" and getTraineeId_resp["msg"] == "操作成功":
            self.traineeId = str(getTraineeId_resp["data"]["clockVo"]["traineeId"])

            # App.App_Log("self.traineeId >> \t" + self.traineeId)
        else:
            raise Exception("获取实习任务ID失败")

    def Duration(self):
        data = {
            "fromType": "",
            "urlParamsStr": "",
            "app": "wx_student",
            "appVersion": "1.5.75",
            "userId": self.userId,
            "deviceToken": self.openId,
            "userName": self.userInfo["username"],
            "country": self.country,
            "province": self.province,
            "city": self.city,
            "deviceModel": "MI MAX 2",
            "operatingSystem": "android",
            "operatingSystemVersion": "7.1.1",
            "screenHeight": "699",
            "screenWidth": "393",
            "eventTime": str(time.time()),
            "pageId": "27",
            "pageName": "成长-签到",
            "preferName": "机会",
            "stayTime": "none",
            "eventType": "click",
            "eventName": "clickSignEvent",
            "clientIP": self.userInfo["clientIP"],
            "reportSrc": "2",
            "login": "1",
            "netType": "WIFI",
            "itemID": "none",
            "itemType": "其他",
        }

        App.handler_request(self.s, "post", App.urls["Duration"], data=data)

    def saveEpidemicSituation(self):

        data = {
            "healthCodeStatus": "",
            "locationRiskLevel": "0",
            "healthCodeImg": "",
        }

        App.handler_request(self.s, "post", App.urls["saveEpidemicSituation"], data=data)

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
        self.checkIn_info["adcode"] = self.adcode
        self.checkIn_info["lat"] = str(self.latitude)
        self.checkIn_info["lng"] = str(self.longitude)
        self.checkIn_info["address"] = self.street
        self.checkIn_info["deviceName"] = self.model
        self.checkIn_info["punchInStatus"] = "1"
        self.checkIn_info["clockStatus"] = "2"
        self.checkIn_info["imgUrl"] = ""
        self.checkIn_info["reason"] = ""

        self.saveEpidemicSituation()

        # self.s.headers["v"] = "1.7.14"

        self.Duration()

        checkIn_resp = App.handler_request(self.s, "post", App.urls["checkIn"], data=self.checkIn_info)
        if checkIn_resp["code"] == "200" and checkIn_resp["msg"] == "操作成功" and checkIn_resp["data"]["successCount"] == 1:
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

                # App.App_Log("CheckIn Flag > " + str(Inture))
                # App.App_Log("note Flag > " + note)

        else:
            if self.sign and self.userInfo["bemfa"] != "":
                App.handler_Notice(self.userInfo["bemfa"], note, self.s.headers["User-Agent"])

            raise Exception("Get Detail Msg Error !\n")
        if DEBUG:
            App.App_Log(note)
            App.App_Log("+" * 102)
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

    def GetUserName(self):
        """
        协议流程
        :return:
        """
        GetUserName_RESP = App.handler_request(self.s,"post", App.urls["LoadAccountInfo"],data={})
        if GetUserName_RESP["code"] == "200" and GetUserName_RESP["msg"] == "操作成功":
            self.userInfo["username"] = GetUserName_RESP["data"]["loginer"]

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
    if DEBUG:
        App.App_Log("用户配置文件 user_info.json 是否拥有可写权限 >> \t 否")

    with open(UserConfPath, mode, encoding="utf-8") as fp:
        info = json.load(fp)
        if len(info) < 1:
            raise Exception("null")
        # App.common = copy.deepcopy(info["users"])
        App.common = info["users"]
        if len(App.common) > 0:
            for _, userInfo in enumerate(App.common):
                if DEBUG:
                    App.print_user_base_info(_, userInfo, mode)
                if userInfo["phoneInfo"]["model"] and userInfo["phoneInfo"]["brand"] and \
                        userInfo["phoneInfo"][
                            "platform"]:
                    app = App(userInfo, info["phoneInfo"], userInfo["CheckInNotice"])
                else:
                    app = App(userInfo, phoneInfo=None, sign=userInfo["CheckInNotice"])

                app.getIp()
                app.Login()
                app.GetUserName()
                app.AutoGetCheckInLocation()
                app.GetAdcode()
                app.getTraineeId()
                return app.GetPlan_detail()[0]


def StatCheckIn(UserConfPath, mode="r+") -> bool:
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
    if DEBUG:
        App.App_Log("用户配置文件 user_info.json 是否拥有可写权限 >> \t" + "是")

    fix_count = 0
    with open(UserConfPath, mode, encoding="utf-8") as fp:
        info = json.load(fp)
        if len(info) < 2:
            raise Exception("null")
        # App.common = copy.deepcopy(info["users"])
        App.common = info.get("users")
        if len(App.common) > 0:
            for _, userInfo in enumerate(App.common):
                if DEBUG:
                    App.print_user_base_info(_, userInfo, mode)
                if userInfo["phoneInfo"]["model"] == "" and userInfo["phoneInfo"]["brand"] == "" and \
                        userInfo["phoneInfo"][
                            "platform"] == "":
                    app = App(userInfo, info["phoneInfo"], userInfo["CheckInNotice"])
                else:
                    app = App(userInfo, phoneInfo=None, sign=userInfo["CheckInNotice"])
                app.getIp()
                app.Login()
                app.GetUserName()
                app.AutoGetCheckInLocation()
                app.GetAdcode()
                app.getTraineeId()
                signInflag, date, writeable = app.GetPlan_detail()
                # (bool, "2022")
                if writeable:
                    fix_count += 1
                    info.get("users")[_]["signInture"] = date

            if fix_count > 0:
                fp.seek(0, 0)
                fp.truncate()
                fp.write(json.dumps(info))

            return signInflag

        else:
            print("No User")


# 腾讯云函数专用
def main_handler(event=None, context=None):
    random_sec = random.randint(10, 400)
    if event:
        """
        云函数
        """
        pass
    else:
        """
        不在云函数的Linux
        """
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

        random_sec = 2
    App.App_Log("是否打印  日志信息    ：" + str("是" if DEBUG else "否"))
    App.App_Log("是否打印 请求日志信息 ：" + str("是" if REQ_DEBUG else "否"))
    if event:
        print("倒计时{}秒！".format(random_sec), end="", flush=True)
        time.sleep(random_sec)
    else:
        for sec in range(random_sec, 0, -1):
            if sec == 1:
                print("\r倒计时1秒！", end="\n", flush=True)
                continue
            print("\r倒计时{}秒！".format(sec), end="", flush=True)
            time.sleep(1)

    # print(os.path.dirname(__file__))  # F:/DeskTop/xyb_CheckIn
    # UserConfPath = os.getcwd() + "/user_info.json"  # 'F:\\DeskTop\\xyb_CheckIn/user_info.json'
    """
    文件目录树：
        /usr/local/var/functions/ap-guangzhou/lam-kc9v6vzg
            | - helloworld-1648240471
                | - src
                    | - index,py
                    | - user_info.json
    
    使用 os.getcwd()
        弊端：
            如果：在 src 路径下 执行 python3 index.py , 
                    那么 os.getcwd() 
                    回显 /usr/local/var/functions/ap-guangzhou/lam-kc9v6vzg/helloworld-1648240471/src
            如果：在 ap-guangzhou 路径下 执行 python3 ./lam-kc9v6vzg/helloworld-1648240471/srcindex.py  
                    那么 os.getcwd() 
                    回显 /usr/local/var/functions/ap-guangzhou/
            此时 若使用 os.getcwd() 方式进行 获取 user_info.json 文件就会提示找不到
            
        推荐使用 os.path.dirname(os.path.realpath(__file__))  来拼凑路径
    """
    UserConfPath = os.path.dirname(
        os.path.realpath(__file__)) + "/user_info.json"  # 'F:\\DeskTop\\xyb_CheckIn/user_info.json'
    # print(UserConfPath)

    if not os.path.exists(UserConfPath):
        App.App_Log("【user_info.json】 Is not exists")
        return False

    OS_Name = platform.system()
    App.App_Log("运行平台: " + OS_Name)

    if SelectCheckInMode(UserConfPath) == mode1:
        """
        no status mode1
        """
        return NoStatCheckIn(UserConfPath, "r")

    elif SelectCheckInMode(UserConfPath) == mode2:
        """
        Remember last inTime
        """
        return StatCheckIn(UserConfPath, "r+")


# 支持 win/Linux 终端 进行本地测试，支持直接copy本代码 到云函数进行部署，
# 无需更改代码，只需要在 user_info.json 中填入个人相关信息即可
if __name__ == '__main__':
    main_handler()
