#coding:utf-8

import unittest
from ScrapydTools import ScrapydToolsLocal

class TestToolManger(unittest.TestCase):
    
    # def test_get_server(self):
    #     """ 测试是否能获取服务器信息 """
    #     t = ScrapydToolsLocal()
    #     self.assertEqual(t.get_server("local"), "http://127.0.0.1:6800/")

    # def test_server_list(self):
    #     """ 测试是否能获取服务器列表 """
    #     t = ScrapydToolsLocal()
    #     self.assertIsInstance(t.server_list(), list)
    #     self.assertNotEqual(len(t.server_list()), 0)

    # def test_get_project(self):
    #     """ 测试是否能获取项目信息 """
    #     t = ScrapydToolsLocal()
    #     print(t.get_project("tutorial"))
    #     # self.assertEqual(t.get_project("local"), "http://127.0.0.1:6800/")

    # def test_project_list(self):
    #     """ 测试是否能获取项目列表 """
    #     t = ScrapydToolsLocal()
    #     print(t.project_list())
    #     self.assertIsInstance(t.project_list(), list)
    #     self.assertNotEqual(len(t.project_list()), 0)

    def test_connect_sqlite(self):
        """ 数据库测试 """
        t = ScrapydToolsLocal()

        result = t.connect_sqlite( action="insert", name="LOCAL", address="http://127.0.0.1:6800/")
        print("插入‘local’ " + str(result) + " 数据类型： " + str(type(result)))
        self.assertIn(result, [None, "EXIST"])

        result = t.connect_sqlite( action="get", name="LOCAL")
        print("获取‘LOCAL’ " + str(result) + " 数据类型： " + str(type(result)))
        self.assertIsInstance(result, str)

        result = t.connect_sqlite(action="get_all")
        print("获取所有 " + str(result)+ " 数据类型： " + str(type(result)))
        self.assertIsInstance(result, list)

        result =  t.connect_sqlite(action="del", name="LOCAL2")
        print("删除‘local2’ " + str(result) + " 数据类型： " + str(type(result)))
        self.assertEqual(result, None)
        


        
if __name__ == '__main__':
    unittest.main()