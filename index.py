import requests
import json
import copy
import hashlib

class App():
    common = list()

    @classmethod
    def handler_request(cls,reqObj, req_method, url, data=None):
        """

        :return: response
        """
        if "xcx.xybsyw" in url:
            reqObj.header["Host"] = "xcx.xybsyw.com"
        elif "app.xybsyw" in url:
            reqObj.header["Host"] = "app.xybsyw.com"
        elif "restapi.amap" in url:
            reqObj.header["Host"] = "restapi.amap.com"

        if req_method == "get":
            return reqObj.get(url, params=data).json()

        if req_method == "post":
            return reqObj.post(url, data=data).json()

    urls = {
        "getIp": "https://xcx.xybsyw.com/behavior/Duration!getIp.action",
        "getOpenId": "https://xcx.xybsyw.com/common/getOpenId.action",
        "GetIsUnionId": "https://xcx.xybsyw.com/common/GetIsUnionId.action",
        "getCityId": "https://xcx.xybsyw.com/common/loadLocation!getCityId.action",
        "Duration": "https://app.xybsyw.com/behavior/Duration.action",  # 心跳
        "verify": "https://xcx.xybsyw.com/sphere/sphereInfo!verify.action",
        "get_traineeId": "https://xcx.xybsyw.com/student/clock/GetPlan!getDefault.action",
        "GetPlan_detail": "https://xcx.xybsyw.com/student/clock/GetPlan!detail.action",
        "login": "https://xcx.xybsyw.com/login/login.action",

    }

    def __init__(self,ip,userInfo=None, phoneInfo=None):

        if userInfo["addressLocation"] == "":
            raise Exception("必须先手动提取 目标地址的经纬度信息，访问 https://api.map.baidu.com/lbsapi/getpoint/index.html")

        self.userInfo = userInfo

        self.s = requests.Session()
        self.openId = ""
        self.unionId = ""
        self.traineeId = ""

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


        if phoneInfo is None:
            self.system = self.userInfo["phoneInfo"]["system"]
            self.model = self.userInfo["phoneInfo"]["model"]
            self.netType = self.userInfo["netType"]
            self.brand = self.userInfo["brand"]
            self.platform = self.userInfo["platform"]


        else:
            self.system = phoneInfo["system"]
            self.model = phoneInfo["model"]
            self.netType = self.userInfo["netType"]
            self.brand = phoneInfo["brand"]
            self.platform = phoneInfo["platform"]

        self.s.headers["User-Agent"] = "Mozilla/5.0 (Linux; "+ self.system +"; "+ self.model +" Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3195 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/8710 MicroMessenger/8.0.16.2040(0x2800103B) Process/appbrand0 WeChat/arm64 Weixin NetType/"+ self.netType +" Language/zh_CN ABI/arm64 MiniProgramEnv/android"







    def getIp(self):
        getIp_resp = App.handler_request(self.s,"post", App.urls["getIp"], {})

        if getIp_resp["code"] == "200" and getIp_resp["msg"] == "success" and getIp_resp["data"]["ip"] != "" :
            return ip
        else:
            Exception

    def getUOid(self):
        """
        :return: (unionId, openId )
        """
        if self.openId == "":
            getUOid_resp = App.handler_request(self.s,"post", App.urls["getOpenId"],{"code":"023FOWkl2NIhS84l3Skl2pIBJh4FOWkr"})

        if getUOid_resp["code"] == "200" and dict(getUOid_resp["data"]).get("unionId") != None and dict(getUOid_resp["data"]).get("openId") != None:
            return (dict(getUOid_resp["data"]).get("unionId"), dict(getUOid_resp["data"]).get("openId"))  # (unionId, openId )

    def GetIsUnionId(self)->None:
        """
        协议流程
        :return: None
        """
        if self.s.headers.get("cookie") == "":

            GetIsUnionId_resp = App.handler_request(self.s, "post", App.urls["GetIsUnionId"], {"openId":self.openId,"unionId":""} )
        else:
            GetIsUnionId_resp = App.handler_request(self.s, "post", App.urls["GetIsUnionId"], {"openId":self.openId,"unionId": self.unionId})

        if GetIsUnionId_resp["code"] == "200" and dict(GetIsUnionId_resp["data"]).get("isUnionId") == True:
            ...
        else:
            raise Exception("Protocol is Failed !\n")

    def getCityId(self):
        """
        :return: getCityId
        """
        getCityId_resp = App.handler_request(self.s, "post", App.urls["getCityId"], {"cityName": self.checkIn_info.get("city")} )
        if getCityId_resp["code"] == "200" and getCityId_resp["msg"] == "操作成功":
            self.checkIn_info["cityId"] = getCityId_resp["data"]

        else:
            raise Exception("Protocol is Failed !\n")



    def GetLocationInfo(self):
        """
        :return: 坐标信息
        """
        params = {
            "key":"c222383ff12d31b556c3ad6145bb95f4",
            "location": self.userInfo["addressLocation"],
            "extensions":"all",
            "s":"rsx",
            "platform":"WXJS",
            "appname":"c222383ff12d31b556c3ad6145bb95f4",
            "sdkversion":"1.2.0",
            "logversion":"1.2.2.0"
        }
        GetLocationInfo_resp = App.handler_request(self.s, "get", "https://restapi.amap.com/v3/geocode/regeo", params)

        if GetLocationInfo_resp["info"] == "OK" and GetLocationInfo_resp["infocode"] == "10000":
            self.checkIn_info["city"] = GetLocationInfo_resp["regeocode"]["addressComponent"]["city"]
            self.checkIn_info["province"] = GetLocationInfo_resp["regeocode"]["addressComponent"]["province"]
            self.checkIn_info["adcode"] = GetLocationInfo_resp["regeocode"]["addressComponent"]["adcode"]




    def verify(self)->None:
        """
        协议流程
        :return: None
        """
        verify_resp = App.handler_request(self.s, "post", App.urls["verify"], {"unionId": self.unionId,"code": "SIGN_IN",})

        if verify_resp["data"] is True and verify_resp["msg"] == "success":
            ...
        else:
            raise Exception("Protocol is Failed !\n")


    def getTraineeId(self)->str:
        """
        :return: traineeId
        """
        getTraineeId_resp = App.handler_request(self.s, "post", App.urls["get_traineeId"], {})
        if getTraineeId_resp["code"] == "200" and getTraineeId_resp["msg"] == "操作成功":
            self.traineeId = str(getTraineeId_resp["data"]["clockVo"]["traineeId"])
        else:
            raise Exception("获取实习任务ID失败")

    def GetPlan_detail(self):
        """
        获取 今日是否打卡相关信息
        :return:
        """
        Plan_detail_resp = App.handler_request(self.s, "post", App.urls["GetPlan_detail"], {"traineeId": self.traineeId})

        if Plan_detail_resp["code"] == "200" and Plan_detail_resp["msg"] == "操作成功":
            if dict(Plan_detail_resp["data"]).get("clockInfo") is not None:
                """
                Plan_detail_resp["data"]).get("clockInfo") 存放 上次打卡的信息
                """



    def Login(self):
        m = hashlib.md5()
        LoginInfo = {
            "username": m.update(self.userInfo["pwd"].encode("utf-8")),
            "password": hashlib.md5(),
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
            raise Exception( "Login Failed !")

        self.s.headers["cookie"] = login_resp["data"]["sessionId"]




    def destory(self):
        """
        完成任务自毁
        :return:
        """
        del self



if __name__ == '__main__':


    with open("UserInfo.json", encoding="utf-8") as fp:
        info = json.load(fp)
        if len(info) < 1:
            raise Exception("null")
        App.common = copy.deepcopy(info["users"])



    if len(App.common) > 0:

        for userInfo in App.common:

            # 模式一：目前可方便到达实习的位置【推荐且默认】 将 mode 修改为 1 如：mode = 1
            # 模式二：目前不方便到达实习的位置  将 mode 修改为 0 如：mode = 0
            # mode = 0




            ip = ""  # 获取IP方式建议 百度搜索 目标地址的IP，如 xxx市的ip
            # ip : 实习地址的ip，保证目前人是在实习地址，注意网络环境，之前打卡是链接WIFI还是数据，如果是WIFI先链接WIFI然后浏览器访问网址 ip.sb，数据同理，获取到 拿到ip 即填写


            # 申请签到打卡地区的经纬度，通过 https://api.map.baidu.com/lbsapi/getpoint/index.html 获取经纬度
            # 如获取的 经纬度 113.398193,22.438461
            # addressLocation = tuple(113.398193,22.438461)

            if userInfo["phoneInfo"] == "":
                app = App(ip, userInfo, info["phoneInfo"])
            else:
                app = App(ip, userInfo)

            app.unionId,app.openId = app.getUOid()

