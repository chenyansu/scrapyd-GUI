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
    
    """通过本地文件/数据库配置
    """

    ############### 服务器管理 ###################

    def read_server(self):
        """ 从文件中读取服务器信息 """
        with open('server_dict', 'r') as f:
            server_dict = {}
            for i in f.read().split('\n'):
                if i:
                    server_dict[i.split("|")[0]] = i.split("|")[1]
                else:
                    break
        return server_dict

    def write_server(self, name, address):
        """ 向文件中写入服务器信息 """
        with open('server_dict', 'a') as f:
            f.write(name+'|'+address+"\n")

    def get_server(self, name):
        """ 根据服务器名称获取服务器信息 """
        return self.read_server()[name]

    def server_list(self): 
        """ 服务器名称列表 """
        return [k for k in self.read_server().keys() ]

    ############### 项目管理 ###################

    def read_project(self):
        """ 从文件中读取项目信息 """
        with open('project_dict', 'r') as f:
            project_dict = {}
            for i in f.read().split('\n'):
                if i:
                    project_dict[i.split("|")[0]] = i.split("|")[1]
                else:
                    break
        return project_dict

    def write_project(self, name, address):
        """ 向文件中写入项目信息 """
        with open('project_dict', 'a') as f:
            f.write(name+'|'+address+"\n")

    def get_project(self, name):
        """ 根据服务器名称获取项目信息 """
        return self.read_project()[name]

    def project_list(self): 
        """ 项目名称列表 """
        # 应该设置为从服务读取
        # return [k for k in self.read_project().keys() ]
        pass


    ############### 数据库版本###################
    
    def connect_sqlite(self, table = "PROJECT", action="get", name=None, address=None):
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
            create_tb_cmd = """
            CREATE TABLE IF NOT EXISTS PROJECT
            (NAME TEXT PRIMARY KEY, 
            ADDRESS TEXT); 
            """
            cursor.execute(create_tb_cmd)
            print("创建数据库tool.db并生成SERVER和PROJECT表格")
        else:
            # 开启sqlite3链接
            conn = sqlite3.connect('tool.db')
            cursor = conn.cursor()

        # 通过action设定获取键值，获取所有值，插入键值，删除功能
        if action == "get":
            cursor.execute("SELECT ADDRESS FROM %s WHERE NAME=='%s';" %(table, name))
            result = cursor.fetchone()[0] #<class 'str'>
        elif action == "get_all":
            cursor.execute("SELECT ADDRESS FROM %s" %table)
            result = [x[0] for x in cursor.fetchall()] #<class 'list'>
        elif action == "insert":
            try:
                cursor.execute("INSERT INTO %s (NAME, ADDRESS) VALUES ('%s', '%s');" %(table, name, address))
                result = None #<class 'NoneType'>
            except sqlite3.IntegrityError:
                result = "EXIST" #<class 'str'>
        elif action == "del":
            cursor.execute("DELETE from %s WHERE NAME=='%s';" %(table, name))
            result = None #<class 'NoneType'>
        elif action == "check":
            cursor.execute("SELECT NAME FROM %s" %table)
            result = [x[0] for x in cursor.fetchall()] #<class 'list'>
        else:
            result = "ILLEGAL OPERATION" #<class 'str'>

        # 关闭链接
        cursor.close()
        conn.commit()
        conn.close()

        return result

def consistency_check(baseUrl):
    
    server = ScrapydToolsNet(baseUrl=baseUrl)
    local = ScrapydToolsLocal()

    server_set = set(server.get_project_list)
    local_set = set(local.connect_sqlite(table = "PROJECT", action="check"))

    if server_set == local_set
        return True
    else:
        return 
        
            


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