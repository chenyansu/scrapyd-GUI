# -*- coding: utf-8 -*-

import requests
import json 
import sqlite3
import os

class ScrapydToolsNet(object):
    """ 向服务器发送请求
    """

    def __init__(self, baseUrl ='http://127.0.0.1:6800/'):
        self.baseUrl = baseUrl
        self.daemUrl = self.baseUrl + 'daemonstatus.json'
        self.listproUrl = self.baseUrl + 'listprojects.json'
        self.listspdUrl = self.baseUrl + 'listspiders.json?project=%s'
        self.listspdvUrl= self.baseUrl + 'listversions.json?project=%s'
        self.listjobUrl = self.baseUrl + 'listjobs.json?project=%s'
        self.delspdvUrl = self.baseUrl + 'delversion.json'

    def get_server_status(self):
        """ 获取服务器状态 """
        r = requests.get(self.daemUrl)
        print(r.text)
        return eval(r.text)

    def get_project_list(self):
        """ 获取项目列表 """
        r = requests.get(self.listproUrl)
        print(r.text)
        return eval(r.text)

    def get_project_spider(self,project):
        """ 获取某项目的所有爬虫 """
        listspdUrl = self.listspdUrl % project
        r = requests.get(listspdUrl)
        print(r.text)
        return eval(r.text)

    def get_project_spider_version(self, project):
        """ 获取某项目所有版本(重复提交项目会增加版本) """
        listspdvUrl=self.listspdvUrl % project
        r = requests.get(listspdvUrl)
        print(r.text)
        return eval(r.text)

    def get_job_list(self, project):
        """ 获取所有爬虫(各种状态) """
        listjobUrl=self.listjobUrl % project
        r=requests.get(listjobUrl)
        print(r.text)
        return eval(r.text)

    def start_spider(self, project, spider):
        """ 开始爬虫，返回jobid """
        schUrl = self.baseUrl + 'schedule.json'
        dictdata ={ "project":project,"spider":spider}
        r= requests.post(schUrl, data= dictdata)
        print(r.text)
        return eval(r.text)

    def del_project_by_version(self, project, version):
        """ 根据版本删除项目"""
        delverUrl = self.baseUrl + 'delversion.json'
        dictdata={"project":project ,"version": version }
        r = requests.post(delverUrl, data= dictdata)
        print(r.text)
        return eval(r.text)

    def del_project(self, project):
        """ 删除项目 """
        delProUrl = self.baseUrl + 'delproject.json'
        dictdata = {"project":project}
        r = requests.post(delProUrl, data= dictdata)
        print(r.text)
        return eval(r.text)


class ScrapydToolsLocal(object):
    
    """通过本地文件/数据库配置服务器
    """
    
    ############### 数据库版本###################
    
    def connect_sqlite(self, action="get_all", name=None, address=None):
        """ 将创建并使用两张表，一个project, 一个server，对此增删改查"""

        # 数据库自检
        if os.path.exists("tool.db") == False:
            conn = sqlite3.connect('tool.db')
            cursor = conn.cursor()
            # 如果表不存在则创建表
            create_tb_cmd = """
            CREATE TABLE IF NOT EXISTS SERVER 
            (NAME TEXT PRIMARY KEY, 
            ADDRESS TEXT); 
            """
            cursor.execute(create_tb_cmd)
            print("创建数据库tool.db并生成SERVER表")
        else:
            # 开启sqlite3链接
            conn = sqlite3.connect('tool.db')
            cursor = conn.cursor()

        # 通过action设定获取键值，获取所有值，插入键值，删除功能
        if action == "get":
            cursor.execute("SELECT ADDRESS FROM SERVER WHERE NAME=='%s';" %name)
            result = cursor.fetchone()[0] #<class 'str'>
        elif action == "get_all":
            cursor.execute("SELECT ADDRESS FROM SERVER")
            result = [x[0] for x in cursor.fetchall()] #<class 'list'>
        elif action == "insert":
            try:
                cursor.execute("INSERT INTO SERVER (NAME, ADDRESS) VALUES ('%s', '%s');" %(name, address))
                result = None #<class 'NoneType'>
            except sqlite3.IntegrityError:
                result = "EXIST" #<class 'str'>
        elif action == "del":
            cursor.execute("DELETE from SERVER WHERE NAME=='%s';" %name)
            result = None #<class 'NoneType'>
        else:
            result = "ILLEGAL OPERATION" #<class 'str'>

        # 关闭链接
        cursor.close()
        conn.commit()
        conn.close()

        return result


if __name__ == "__main__":
    st = ScrapydToolsNet()
    # st.get_server_status()
    # st.get_project_list()
    # st.get_project_spider("tutorial")
    # st.get_project_spider_version("tutorial")
    # st.get_job_list("tutorial")
    # st.start_spider(project = "tutorial", spider="author")
    # st.del_project_by_version(project="tutorial",version="1520788750" ) 
    # st.del_project("tutorial")