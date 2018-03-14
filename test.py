#!/usr/bin/env python3
#coding:utf-8

import unittest
from ScrapydTools import ScrapydTools

"""
单元测试待补全
"""

__author__ == "chenyansu"

class TestToolManger(unittest.TestCase):
    
    def test_get_project_spider(self):
        """ 测试是否能获取项目信息 """
        t = ScrapydTools()
        print(t.get_project_spider("tutorial"))
        # self.assertEqual(t.get_project("local"), "http://127.0.0.1:6800/")

    def test_get_project_list(self):
        """ 测试是否能获取项目列表 """
        t = ScrapydTools()
        result = t.get_project_list()
        print(result)

    def test_server_manager(self):
        """ 数据库测试 """
        t = ScrapydTools()

        result = t.server_manager( action="server_add", name="LOCAL", address="http://127.0.0.1:6800/")
        print("插入‘local’ " + str(result) + " 数据类型： " + str(type(result)))
        self.assertIn(result, [None, "EXIST"])

        result = t.server_manager( action="server_select", name="LOCAL")
        print("获取‘LOCAL’ " + str(result) + " 数据类型： " + str(type(result)))
        self.assertIsInstance(result, str)

        result = t.server_manager(action="server_list")
        print("获取所有 " + str(result)+ " 数据类型： " + str(type(result)))
        self.assertIsInstance(result, list)

        result =  t.server_manager(action="server_del", name="LOCAL3")
        print("删除‘local2’ " + str(result) + " 数据类型： " + str(type(result)))
        self.assertEqual(result, None)
        


        
if __name__ == '__main__':
    unittest.main()