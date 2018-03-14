#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Ui_main_window import *
from ScrapydTools import ScrapydTools
import sys
import os
import requests

__author__ == "chenyansu"

class Run(ScrapydTools):
    """
    后端与UI结合
    可以使用qt设计师随意更改ui样式,但是不能更改相关组件名称。
    """

    def __init__(self):
        # ScrapydTools.__init__(self, baseUrl=baseUrl)
        super().__init__()
        self.s_r_counter = 0
        self.message = "" # 显示在主窗口的信息
        self.pending_number = 0
        self.running_number = 0
        self.finished_number = 0
        self.open_ui()
        self.Ui_register()
        self.close_ui()

    def open_ui(self):
        """ 打开Ui绘制 """
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def close_ui(self):
        """ 关闭Ui绘制 """
        sys.exit(self.app.exec_())

    def Ui_register(self):
        """ 交互式Ui注册 """
        self.show_message() # 注册显示器
        self.refresh_button_func()
        self.button_register() # 注册按钮
        self.combobox_register()

    def show_message(self):
        """ 注册显示器 """
        self.ui.show_message_textBrowser.setText(self.message)
        self.ui.pending_lcdNumber.display(self.pending_number)
        self.ui.running_lcdNumber.display(self.running_number)
        self.ui.finished_lcdNumber.display(self.finished_number)

    def button_register(self):
        """ 按钮注册 """
        self.ui.refresh_pushButton.clicked.connect(self.refresh_button_func) #刷新按钮
        self.ui.server_add_pushButton.clicked.connect(self.server_add_button_func) #添加服务器
        self.ui.start_spider_pushButton.clicked.connect(self.start_spider_button_func)
        self.ui.kill_spider_pushButton.clicked.connect(self.kill_spider_button_func)
        self.ui.s_r_spider_pushButton.clicked.connect(self.s_r_spider_button_func)
        self.ui.project_add_pushButton.clicked.connect(self.project_add_button_func)
        self.ui.del_project_pushButton.clicked.connect(self.del_project_button_func)
        self.ui.server_del_pushButton.clicked.connect(self.server_del_button_func)

    def combobox_register(self):
        """ 下拉框注册 """
        self.show_server_in_combobox()
        self.show_project_in_combobox()
        self.show_spider_in_combobox()
        self.show_running_in_combobox()


    def fetch_server_list(self):
        """ 获取服务器名称列表 """
        self.server_list = self.server_manager(action="server_list")
        print(self.server_list)
        return self.server_list

    def fetch_server(self):
        """ 获取所有 服务器-地址"""
        server_list = self.server_manager(action="server_list")
        self.server_dict = {} # 字典{server:address}
        for server_name in server_list:
            self.server_dict[server_name] = self.server_manager(action="server_select", name=server_name)
        print(self.server_dict)
        return self.server_dict
    
    def fetch_project(self):
        """ 获取所有 服务器-项目 """
        self.project_dict = {} # 字典{server:project(list)}
        for server_name,address in self.server_dict.items():
            self.project_dict[server_name] = eval(requests.get(address + 'listprojects.json').text)["projects"]
        print(self.project_dict)
        return self.project_dict

    def fetch_spider(self):
        """ 获取所有 服务器-项目-spider """
        self.project_spider_dict = {} #嵌套字典{server:[{project:spider}, {}], }
        for server_name,address in self.server_dict.items():
            project_list = self.project_dict[server_name]
            self.project_spider_dict[server_name] = {}
            for project in project_list:
                spider = eval(requests.get(address+'listspiders.json?project=%s' % project).text)["spiders"]
                self.project_spider_dict[server_name][project] = spider
        print(self.project_spider_dict)
        return self.project_spider_dict

    def fetch_running(self):
        """ 获取所有 服务器-项目-runningspider """
        self.project_running_dict = {} #嵌套字典{server:[{project:running_spider}, {}], }
        self.running_pid = {}
        self.running_number = 0 # 借道使用，免得重复获取，lcd显示器需要的数据
        self.pending_number = 0 # 借道使用，免得重复获取，lcd显示器需要的数据
        self.finished_number = 0 # 借道使用，免得重复获取，lcd显示器需要的数据
        for server_name,address in self.server_dict.items():
            project_list = self.project_dict[server_name]
            self.project_running_dict[server_name] = {}
            for project in project_list:
                # running = eval(requests.get(address+'listjobs.json?project=%s' % project).text)["running"]
                jobs = eval(requests.get(address+'listjobs.json?project=%s' % project).text)
                running = jobs["running"]
                self.running_number += len(jobs["running"]) # 借道使用，免得重复获取，lcd显示器需要的数据
                self.pending_number += len(jobs["pending"]) # 借道使用，免得重复获取，lcd显示器需要的数据
                self.finished_number += len(jobs["finished"]) # 借道使用，免得重复获取，lcd显示器需要的数据
                if running:
                    spider = running["spider"]
                    pid = running["pid"]
                    self.running_pid["spider"] = pid
                    self.project_running_dict[server_name] = {project:spider}
                    print(self.self.running_pid)
                    print(self.project_running_dict)

    def server_on_activated(self, text):
        """ 项目值的变化让project下拉框改变 """
        self.server_set()
        self.ui.project_name_comboBox.clear()
        self.ui.project_name_comboBox.addItems(self.project_dict[text])
    
    def project_on_activated(self, text):
        """ 项目值的变化让spider下拉框和running下拉框改变 """
        self.ui.spider_name_comboBox.clear()
        self.ui.running_spider_comboBox.clear()
        server = self.ui.server_select_comboBox.currentText()
        self.ui.spider_name_comboBox.addItems(self.project_spider_dict[server][text])
        try:
            self.ui.running_spider_comboBox.addItems(self.project_running_dict[server][text])
        except:
            self.ui.running_spider_comboBox.addItem("None")
        
    
    def show_server_in_combobox(self):
        """ 服务器下拉框,从数据库拉取 """
        self.ui.server_select_comboBox.clear()
        self.ui.server_select_comboBox.addItems(self.server_list)
        self.ui.server_select_comboBox.activated[str].connect(self.server_on_activated)

    def show_project_in_combobox(self):
        """ 项目下拉框 """
        self.ui.project_name_comboBox.clear()
        self.server_set()
        server_name = self.ui.server_select_comboBox.currentText()
        self.ui.project_name_comboBox.addItems(self.project_dict[server_name])
        # self.ui.project_name_comboBox.addItems(self.get_project_list()["projects"])
        self.ui.project_name_comboBox.activated[str].connect(self.project_on_activated)

    def show_spider_in_combobox(self):
        """ 爬虫下拉框 """
        self.ui.spider_name_comboBox.clear()
        server = self.ui.server_select_comboBox.currentText()
        project = self.ui.project_name_comboBox.currentText()
        self.ui.spider_name_comboBox.addItems(self.project_spider_dict[server][project])
        # self.ui.spider_name_comboBox.addItems(self.get_project_spider(project)["spiders"])

    def show_running_in_combobox(self):
        """ 获取运行中的爬虫名称 """
        self.ui.running_spider_comboBox.clear()
        server = self.ui.server_select_comboBox.currentText()
        project = self.ui.project_name_comboBox.currentText()
        try:
            self.ui.running_spider_comboBox.addItems(self.project_running_dict[server][project])
        except:
            pass

    def start_spider_button_func(self):
        """ 启动爬虫 """
        project = self.ui.project_name_comboBox.currentText()
        spider = self.ui.spider_name_comboBox.currentText() 
        self.start_spider(spider=spider, project=project)
        self.show_running_in_combobox()
        self.message+="\n 开始爬虫: %s \n"%spider 
        self.show_message()

    def s_r_spider_button_func(self):
        """ 暂停/恢复 本地爬虫(根据kill制作，不可操作远程服务器)"""
        project = self.ui.project_name_comboBox.currentText()
        running_spider = self.ui.running_spider_comboBox.currentText()
        running_spider_pid = self.running_pid[running_spider]
        if self.s_r_counter % 2 == 0:
            self.ui.s_r_spider_pushButton.setText("恢复爬虫")
            os.system("kill -STOP {}".format(running_spider_pid))
            self.message+="\n 暂停爬虫: {}".format(running_spider) + "本功能根据kill -stop制作，仅限于本地爬虫"
            self.s_r_counter += 1
        else:
            self.ui.s_r_spider_pushButton.setText("暂停爬虫")
            os.system("kill -CONT {}".format(running_spider_pid))
            self.message+="\n 恢复爬虫: {}".format(running_spider) + "本功能根据kill -conf制作，仅限于本地爬虫"
            self.s_r_counter += 1
        self.show_message()
        self.show_running_in_combobox()

    def kill_spider_button_func(self):
        """ 杀死爬虫 """
        project = self.ui.project_name_comboBox.currentText()
        running_spider = self.ui.running_spider_comboBox.currentText()
        # running_spider_pid = self.running_job_dict[running_spider]
        running_spider_pid = self.running_pid[running_spider]
        os.system("kill -9 {}".format(running_spider_pid))
        self.message+="\n 杀死爬虫: {}".format(running_spider) + "本功能根据kill -9制作，仅限于本地爬虫"
        self.show_message()
        self.show_running_in_combobox()

    def refresh_button_func(self):
        """ 刷新 """
        # self.message = ""
        self.show_message()
        self.fetch_server()
        self.fetch_server_list()
        self.fetch_project()
        self.fetch_spider()
        self.fetch_running()
        self.combobox_register()
    
    def server_add_button_func(self):
        """ 服务器添加按钮的背后逻辑 """
        server_name = self.ui.server_name_lineEdit.text()
        server_address = self.ui.server_address_lineEdit.text()
        result = str(self.server_manager(action="server_add", 
                                                name=server_name, 
                                                address=server_address))
        self.message+='\n'+'添加服务器'+server_name+" 地址为： "+server_address
        self.show_message()

    def project_add_button_func(self):
        """ 添加项目按钮的函数 """
        project_name = self.ui.project_name_lineEdit.text()
        project_address =self.ui.project_address_lineEdit.text()
        self.project_add(project_name=project_name, project_address=project_address)
        self.message+='\n'+'添加项目'+project_name+" 路径为： "+project_address
        self.show_message()

    def del_project_button_func(self):
        """ 删除项目按钮的函数 """
        project_name = self.ui.project_name_comboBox.currentText()
        self.del_project(project=project_name)
        self.message+='\n'+'删除项目'+project_name
        self.show_message()

    def server_set(self):
        """ 设置服务器 """
        server_name = self.ui.server_select_comboBox.currentText()
        self.baseUrl = self.server_manager(action="server_select", name=server_name)
        return server_name

    def server_del_button_func(self):
        """ 删除服务器按钮的函数 """
        server_name = self.ui.server_select_comboBox.currentText()
        self.server_manager(action="server_del", name=server_name)
        self.refresh_button_func() 
    
if __name__ == "__main__":
    a = Run()


    
