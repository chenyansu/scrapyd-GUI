#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json 
import sqlite3
import os
import shutil

__author__ == "chenyansu"

class ScrapydTools(object):
    """ 后端：Scrapyd API 的封装调用
        日后修改方向：函数打散，不使用类继承。
    """

    def __init__(self, baseUrl ='http://127.0.0.1:6800/'):
        self.baseUrl = baseUrl

    def get_server_status(self):
        """ 获取服务器状态 """
        r = requests.get(self.baseUrl + 'daemonstatus.json')
        print(r.text)
        return eval(r.text)

    def get_project_list(self):
        """ 获取项目列表 """
        r = requests.get(self.baseUrl + 'listprojects.json')
        print(r.text)
        return eval(r.text)

    def get_project_spider(self,project):
        """ 获取某项目的所有爬虫 """
        listspdUrl = self.baseUrl + 'listspiders.json?project=%s' % project
        r = requests.get(listspdUrl)
        print(r.text)
        return eval(r.text)

    def get_project_version(self, project):
        """ 获取某项目所有版本(重复提交项目会增加版本) """
        listspdvUrl=self.baseUrl + 'listversions.json?project=%s' % project
        r = requests.get(listspdvUrl)
        print(r.text)
        return eval(r.text)

    def get_job_list(self, project):
        """ 获取所有爬虫(各种状态) """
        listjobUrl=self.baseUrl + 'listjobs.json?project=%s' % project
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

    def stop_spider(self, project, jobid):
        """ 根据jobid停止爬虫 """
        cancelUrl = self.baseUrl + 'cancel.json'
        dictdata = {"project":project ,"job":jobid}
        r = requests.post(cancelUrl, data=dictdata)
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

    def server_manager(self, action="server_list", name=None, address=None):
        """ 
        将利用sqlite创建并使用server表，对此增删改查
        提供 server_select，server_list，server_add， server_del 方法
        """
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
        if action == "server_select":
            cursor.execute("SELECT ADDRESS FROM SERVER WHERE NAME=='%s';" %name)
            result = cursor.fetchone()[0] #<class 'str'>
        elif action == "server_list":
            cursor.execute("SELECT NAME FROM SERVER")
            result = [x[0] for x in cursor.fetchall()] #<class 'list'>
        elif action == "server_add":
            try:
                cursor.execute("INSERT INTO SERVER (NAME, ADDRESS) VALUES ('%s', '%s');" %(name, address))
                result = None #<class 'NoneType'>
            except sqlite3.IntegrityError:
                result = "EXIST" #<class 'str'>
        elif action == "server_del":
            cursor.execute("DELETE from SERVER WHERE NAME=='%s';" %name)
            result = None #<class 'NoneType'>
        else:
            result = "ILLEGAL OPERATION" #<class 'str'>

        # 关闭链接
        cursor.close()
        conn.commit()
        conn.close()

        return result

    def project_add(self, project_name, project_address):
        if os.path.exists(project_address+"scrapyd-deploy") == False:
            try:
                shutil.copy("scrapyd-deploy", project_address)
            except:
                print("没有复制权限")
        old_address = os.getcwd()
        os.chdir(project_address)
        os.system("scrapyd-deploy -p %s" %project_name)
        os.chdir(old_address)


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