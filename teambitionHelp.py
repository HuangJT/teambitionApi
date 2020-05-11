# -*- coding: UTF-8 -*-
import requests
import json
import pymysql
from pymysql import cursors
import time
import urllib
import codecs
from datetime import datetime, date, timedelta
# pip install PyJWT
import jwt

import sys
# reload(sys)
# sys.setdefaultencoding('utf8') 

from settings  import SETTINGS


class TeambitionHelp:

    __tbAppId = "" # api token
    __tbSecrect = "" 
    __accessToken = "" 


    def __init__(self):
        self.__tbAppId = SETTINGS["TB_APP_ID"]
        self.__tbSecrect = SETTINGS["TB_APP_SECRECT"]


        expire_time = int(time.time() + 3600)  # 1 小时后超时
        encoded = jwt.encode({'_appId': self.__tbAppId, 'exp': expire_time}, self.__tbSecrect, algorithm='HS256')
        # print(encoded)
        encoded_str = str(encoded, encoding='utf-8')
        # print(encoded_str)

        self.__accessToken = encoded_str

    def __getAuthHeaders(self):
        return {'Authorization': 'Bearer '+ self.__accessToken,'X-Tenant-Id':SETTINGS['TB_ORG_ID'],'X-Tenant-Type':'organization'}
        



    def logf(self,content):
        logContent =   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  + " " + content + "\n"    
        logFile = codecs.open(SETTINGS['LOG_FILE'], 'a', encoding='utf-8')
        logFile.write(logContent)
        print(logContent)
        logFile.close()
    
    def getOrgInfo(self):
        res = requests.get(SETTINGS["URL_TB_GET_ORG_INFO"] + "?orgId="+ SETTINGS["TB_ORG_ID"],headers=self.__getAuthHeaders())    
        print(res.content.decode("utf-8"))
        # resJson = json.loads(res.content.decode("utf-8"))      

    def getTaskGroup(self,groupId):
        res = requests.get(SETTINGS["URL_TB_GET_TASK_GROUP"] + "?projectId="+ groupId,headers=self.__getAuthHeaders())    
        print(res.content.decode("utf-8"))
        resJson = json.loads(res.content.decode("utf-8"))
        return resJson.get("result")

    def getTaskList(self,taskListId):
        res = requests.get(SETTINGS["URL_TB_GET_TASK_LIST"] + "?tasklistId="+ taskListId,headers=self.__getAuthHeaders())    
        print(res.content.decode("utf-8"))
        resJson = json.loads(res.content.decode("utf-8"))
        return resJson.get("result")

    def getTasksByTql(self,tql):
        res = requests.post(SETTINGS["URL_TB_GET_TASK_TQL"] ,json={"tql":tql},headers=self.__getAuthHeaders())    
        print(res.content.decode("utf-8"))
        resJson = json.loads(res.content.decode("utf-8"))
        return resJson.get("result")





def main():


    teambitionHelp = TeambitionHelp()
    # groupList = teambitionHelp.getTaskGroup(SETTINGS["TB_PROJECT_ID_DEVELOP"])

    # for group in groupList:
    #     print(group.get("name"))
    #     # print(group.get("tasklistIds"))
    #     for taskListId in group.get("tasklistIds"):
    #         print(teambitionHelp.getTaskList(taskListId))

    tasks = teambitionHelp.getTasksByTql("projectId=" + SETTINGS["TB_PROJECT_ID_DEVELOP"] + " AND id = 5e78xxxxxxx7880 " )
    for task in tasks:
        print(task)
        print("\n")
    



if __name__ == '__main__':
    main()    