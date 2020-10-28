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
            recvListings=self.cafemaker(key[1])
            for item in recvListings:
                itemID,itemType,itemIconPath,itemKindName,itemName=self.itemSolve(item)
                if itemType=="Item":
                    itemIconUrl='https://cafemaker.wakingsands.com/{}'.format(itemIconPath)
                    if not os.path.exists('ItemIcon/{}.png'.format(itemID)):
                        with open('ItemIcon/{}.png'.format(itemID),'wb') as f:
                            f.write(requests.get(itemIconUrl).content)

                    results.append({
                        "Title":"{}".format(itemName),
                        "SubTitle":"{}".format(itemKindName),
                        "IcoPath":"ItemIcon/{}.png".format(itemID),
                        "JsonRPCAction":{
                            "method":"Wox.ChangeQuery",
                            "parameters":["item q {} 1 ({})".format(itemID,itemName),False],
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

    def universalis(self,server,itemID):
        api='https://universalis.app/api/{}/{}'.format(server,itemID)
        recv=requests.get(api)
        if recv.text=='Not Found':
            return False
        return json.loads(recv.text)["listings"]

    def cafemaker(self,queryName):
        u='https://cafemaker.wakingsands.com/search?columns=ID%2CUrlType%2CIcon%2CName%2CItemKind.Name&string={}'.format(queryName)
        return json.loads(requests.get(u).text)["Results"]

    def itemSolve(self,item):
        return item["ID"],item["UrlType"],item["Icon"],item["ItemKind"]["Name"],item["Name"]



if __name__ == "__main__":
    Main()
