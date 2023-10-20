# from openpyxl import load_workbook
#
# from openpyxl.worksheet.worksheet import Worksheet
#
#
# class ExcelHandler():
#
#
#     def __init__(self, file):
#
#
#         self.file = file
#
#
#     def open_sheet(self, name) -> Worksheet:
#
#
#         # 表示此函数的返回值，是一个这样的类型，函数注解
#
#         wb = load_workbook(self.file)  # 通过属性传递
#
#         sheet = wb[name]
#
#         return sheet
#
#
#     def header(self, sheet_name):
#
#
#         '''获取表头'''
#
#         sheet = self.open_sheet(sheet_name)
#
#         headers = []
#
#         for i in sheet[1]:
#
#             headers.append(i.value)
#
#             return headers
#
#
#     def read(self, sheet_name):
#
#
#         '''读取所有数据'''
#
#         sheet = self.open_sheet(sheet_name)
#
#         rows = list(sheet.rows)  # 得到所有的数据，包括表头
#
#         data = []  # 存取所有行的数据
#
#         for row in rows[1:]:
#
#             row_data = []  # 存取一行的数据
#
#             for cell in row:  # 取出单元格
#
#                 row_data.append(cell.value)  # 把单元格的值存在一行的数据中
#
#                 # 列表转字典，要和header zip
#
#                 data_dict = dict(zip(self.header(sheet_name), row_data))
#
#                 data.append(data_dict)  # 把一行的值存在放所有行的数据中
#
#                 print(data)
#
#                 return data
#
#
#     @staticmethod
#     def write(file, sheet_name, row, column, data):
#         wb = load_workbook(file)
#
#         sheet = wb[sheet_name]  # 获取表单
#
#         cell = sheet.cell(row, column)  # 获取单个单元格
#
#         cell.value = data  # 写入值
#
#         wb.save(file)  # 保存
#
#         wb.close()
#
# if __name__ == '__main__':
#
#     excel = ExcelHandler(r'D:\cases.xlsx')
#
#     sheet = excel.read('Sheet1')
# !/usr/bin/python
# coding=utf-8

__author__ = 'adengou'
__version__ = '0.1.0'
__update__ = '2020.3.17'

import json

import xlrd

'''
           xlrd用法
----------------------------------------------
table = data.sheets()[0]          #通过索引顺序获取

table = data.sheet_by_index(sheet_indx)) #通过索引顺序获取

table = data.sheet_by_name(sheet_name)#通过名称获取

以上三个函数都会返回一个xlrd.sheet.Sheet()对象

names = data.sheet_names()    #返回book中所有工作表的名字

data.sheet_loaded(sheet_name or indx)   # 检查某个sheet是否导入完毕
-----------------------------------------------
nrows = table.nrows  #获取该sheet中的有效行数

table.row(rowx)  #返回由该行中所有的单元格对象组成的列表

table.row_slice(rowx)  #返回由该列中所有的单元格对象组成的列表

table.row_types(rowx, start_colx=0, end_colx=None)    #返回由该行中所有单元格的数据类型组成的列表

table.row_values(rowx, start_colx=0, end_colx=None)   #返回由该行中所有单元格的数据组成的列表

table.row_len(rowx) #返回该列的有效单元格长度
---------------------------------------------
ncols = tablencols = table.ncols   #获取列表的有效列数

table.col(colx, start_rowx=0, end_rowx=None)  #返回由该列中所有的单元格对象组成的列表

table.col_slice(colx, start_rowx=0, end_rowx=None)  #返回由该列中所有的单元格对象组成的列表

table.col_types(colx, start_rowx=0, end_rowx=None)    #返回由该列中所有单元格的数据类型组成的列表

table.col_values(colx, start_rowx=0, end_rowx=None)   #返回由该列中所有单元格的数据组成的列表
------------------------------------------------
table.cell(rowx,colx)   #返回单元格对象

table.cell_type(rowx,colx)    #返回单元格中的数据类型

table.cell_value(rowx,colx)   #返回单元格中的数据

table.cell_xf_index(rowx, colx)   # 暂时还没有搞懂

'''


###构建类
class readExcel:
    ####初始化变量
    def __init__(self):
        self.list = []

        ####析构函数

    def __del__(self):

        self.list = None

    def read_xlrd(self, hero, sheetNameOrIndex, startRows=0, startCols=0, endRows=0, endCols=0):
        # 读取Excle文件，excelFile为文件名，
        # sheetNameOrIndex为工作表名或者工作表索引号
        # startRows开始行号（下标从0开始）
        # startCols开始列号（下标从0开始）
        # endRows结束行号（默认为0，读取整个行）
        # endCols结束列号，(默认为0，读取整列)

        # 打开文件
        data = xlrd.open_workbook(hero)
        # 查看工作表
        # data.sheet_names()
        # print("sheets:" + str(data.sheet_names()))

        # 通过文件名获得工作表,获取工作表1
        # sheetType =isinstance(sheetNameOrIndex,str)
        # sheetType=type(sheetNameOrIndex)
        # print(sheetType)
        if (isinstance(sheetNameOrIndex, str)):
            table = data.sheet_by_name(sheetNameOrIndex)
        elif (isinstance(sheetNameOrIndex, int)):
            table = data.sheet_by_index(sheetNameOrIndex)
        else:
            print("表名或表索引错误")
            return ""
        # print(table)
        # 打印data.sheet_names()可发现，返回的值为一个列表，
        # 通过对列表索引操作获得工作表1
        # table = data.sheet_by_index(0)

        # 获取行数和列数
        # 行数：table.nrows
        # 列数：table.ncols
        # print("总行数：" + str(table.nrows))
        # print("总列数：" + str(table.ncols))

        # 获取整行的值 和整列的值，返回的结果为数组
        # 整行值：table.row_values(start,end)

       # table.row_values(start, end)
        # 整列值：table.col_values(start,end)
        # 参数 start 为从第几个开始打印，
        # end为打印到那个位置结束，默认为none
        # print("整行值：" + str(table.row_values(0)))
        # print("整列值：" + str(table.col_values(1)))

        # 获取某个单元格的值，例如获取B3单元格值
        # cel_B3 = table.cell(3,2).value

        # table.cell(3, 2)
        # print("第三行第二列的值：" + cel_B3)

        if (endRows == 0):
            endRows = table.nrows
        if (endCols == 0):
            endCols = table.ncols
        s = "class HeroBase:""\n"+"    def __init__(self):"
        f = open(r'hero.py', "a+")
        f.seek(0)  # 定位
# 先清空后写入代码如下
        # # 写txt文件追加
        # def writetxt_a(txt, path):
        #     with codecs.open(path, 'a', 'utf-8') as w:
        #         w.seek(0)  # 定位
        #         w.truncate()  # 清空文件
        #         w.write(txt)
        f.truncate()
        print(s, file=f)
        f.close()
        # print("class HeroBase:""\n", "   def __init__(self):")
        datas=[]
        for i in range(1,2):
            for j in range(startCols, endCols):
                class_hero=table.cell(i, j).value
                datas.append(class_hero)
        for d in datas:
            a="        "+"self."+d+"=0"
            z=open(r'hero.py',"a+")
            print(a, file=z)
            z.close()
            # print("      ","self.",d,"=0",sep="")


if __name__ == '__main__':
    rex = readExcel()
    rex.read_xlrd('hero.xls', "Sheet1",)







































