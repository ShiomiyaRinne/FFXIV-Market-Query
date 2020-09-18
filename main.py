import requests
import json
import os
import pyperclip
from wox import Wox,WoxAPI
class Main(Wox):
    def query(self,key):
        results=[]
        key=key.split(' ')
        servers={
            '1':"LuXingNiao",'2':"MoGuLi",'3':"MaoXiaoPang",
            # 'hyh':"HongYuHai",'lnxy':"LaNuoXiYa",'cxwz':"ChenXiWangZuo",'yzhy':"YuZhouHeYin",
            # 'wxxr':"WoXianXiRan",'syzd':"ShenYiZhiDi",'hyqd':"HuanYingQunDao",'myc':"MengYaChi",
            # 'byx':"BaiYinXiang",'bjhx':"BaiJinHuanXiang",'sqh':"ShenQuanHen",'cft':"ChaoFengTing",
            # 'lrzq':"LvRenZhanQiao",'fxzj':"FuXiaoZhiJian",'lcsd':"Longchaoshendian",'mybj':"MengYuBaoJing",
            # 'zszq':"ZiShuiZhanQiao",'yx':"YanXia",'jyzy':"JingYuZhuangYuan",'mdn':"MoDuNa",
            # 'hmcw':"HaiMaoChaWu",'rfhw':"RouFengHaiWan",'hpy':"HuPoYuan"
        }
        worlds={
            'HongYuHai':"红玉海",
            'LaNuoXiYa':"拉诺西亚",
            'ChenXiWangZuo':"晨曦王座",
            'YuZhouHeYin':"宇宙和音",
            'WoXianXiRan':"沃仙曦染",
            'ShenYiZhiDi':"神意之地",
            'HuanYingQunDao':"幻影群岛",
            'MengYaChi':"萌芽池",

            'BaiYinXiang':"白银乡",
            'BaiJinHuanXiang':"白金幻象",
            'ShenQuanHen':"神拳痕",
            'ChaoFengTing':"潮风亭",
            'LvRenZhanQiao':"旅人栈桥",
            'FuXiaoZhiJian':"拂晓之间",
            'Longchaoshendian':"龙巢神殿",
            'MengYuBaoJing':"梦羽宝境",

            'ZiShuiZhanQiao':"紫水栈桥",
            'YanXia':"延夏",
            'JingYuZhuangYuan':"静语庄园",
            'MoDuNa':"摩杜纳",
            'HaiMaoChaWu':"海猫茶屋",
            'RouFengHaiWan':"柔风海湾",
            'HuPoYuan':"琥珀原"
        }
        if key[0]=='s':
            c1='https://cafemaker.wakingsands.com/search?columns=ID%2CUrlType%2CIcon%2CName%2CItemKind.Name&string={}'.format(key[1])
            items=json.loads(requests.get(c1).text)["Results"]
            for item in items:
                if item["UrlType"]=="Item":
                    itemID=item["ID"]
                    itemIcon='https://cafemaker.wakingsands.com/{}'.format(item["Icon"])
                    if not os.path.exists('ItemIcon/{}.png'.format(itemID)):
                        with open('ItemIcon/{}.png'.format(itemID),'wb') as f:
                            f.write(requests.get(itemIcon).content)
                    results.append({
                        "Title":"{}".format(item["Name"]),
                        "SubTitle":"{}".format(item["ItemKind"]["Name"]),
                        "IcoPath":"ItemIcon/{}.png".format(itemID),
                        "JsonRPCAction":{
                            "method":"Wox.ChangeQuery",
                            "parameters":["item q {} 1".format(item["Name"]),False],
                            "dontHideAfterAction":True
                        }
                    })
            return results
        if key[0]=='q':
            data=self.universalis(servers[key[2]],key[1])
            for item in data:
                results.append({
                    "Title": "{} x {} = {}".format(item["pricePerUnit"],item["quantity"],item["total"]),
                    "SubTitle": "{}({})".format(item["retainerName"],worlds[item["worldName"]]),
                    "IcoPath":"Images/hq.png"if item["hq"] else "Images/nq.png"
                })
            return results

    def universalis(self,server,itemName):
        c='https://cafemaker.wakingsands.com/search?string={}'.format(itemName)
        itemID=json.loads(requests.get(c).text)["Results"][0]["ID"]
        api='https://universalis.app/api/{}/{}'.format(server,itemID)
        recv=requests.get(api)
        if recv.text=='Not Found':
            return False
        return json.loads(recv.text)["listings"]


if __name__ == "__main__":
    Main()