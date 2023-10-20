# from openpyxl import load_workbook
# from openpyxl.worksheet.worksheet import Worksheet
#
#
# class ExcelHandler():
#     def __init__(self, file):
#         self.file = file
#
#     def open_sheet(self,name): #-> Worksheet :<br>  # 表示此函数的返回值，是一个这样的类型，函数注解
#         wb = load_workbook(self.file)  # 通过属性传递
#         sheet = wb[name]
#         return sheet
#
#
# def header(self, sheet_name):
#     '''获取表头'''
#     sheet = self.open_sheet(sheet_name)
#     headers = []
#     for i in sheet[1]:
#         headers.append(i.value)
#     return headers
#
#
# def read(self, sheet_name):
#     '''读取所有数据'''
#     sheet = self.open_sheet(sheet_name)
#     rows = list(sheet.rows)  # 得到所有的数据，包括表头
#
#     data = []  # 存取所有行的数据
#     for row in rows[1:]:
#         row_data = []  # 存取一行的数据
#         for cell in row:  # 取出单元格
#             row_data.append(cell.value)  # 把单元格的值存在一行的数据中
#             # 列表转字典，要和header zip
#             data_dict = dict(zip(self.header(sheet_name), row_data))
#
#         data.append(data_dict)  # 把一行的值存在放所有行的数据中
#         print(data)
#     return data
#
#
# @staticmethod
# def write(file, sheet_name, row, column, data):
#     wb = load_workbook(file)
#     sheet = wb[sheet_name]  # 获取表单
#     cell = sheet.cell(row, column)  # 获取单个单元格
#     cell.value = data  # 写入值
#     wb.save(file)  # 保存
#     wb.close()
#
#
# if __name__ == '__main__':
#     excel = ExcelHandler(r'D:')
#     sheet = excel.read('Sheet')


class ConvertBean:
    def __init__(self, HeroName, parameters):
        self.HeroName = HeroName
        self.parameters = parameters
    def convert(self):
        classStr = "class {0}:\n    def __init__(self,{1}):\n{2}\n\n{3}\n{4}"
        propertyStr = "@property"
        setterStr = ".setter"
        initParms = []
        initParmsAss = []
        initParmsGetter = []
        initParmsSetter = []
        size = len(self.parameters)
        for i in range(size):
            parm = self.parameters[i]
            initParms.append(parm)
            initParmsAss.append("        self." + parm + " = " + parm)
            initParmsGetter.append(
                "    " + propertyStr + "\n    def " + parm + "(self):\n        return self." + parm + "\n")
            initParmsSetter.append(
                "    @" + parm + setterStr + "\n    def " + parm + "(self, " + parm + "):\n        self." + parm + " = " + parm + "\n")
        __initParmsForInitParms = ",".join(initParms)  # 填充构造函数参数
        __initParmsForAssignment = "\n".join(initParmsAss)  # 参数赋值
        __initParmsForGetter = "\n".join(initParmsGetter)  # 生成getter
        __initParmsForSetter = "\n".join(initParmsSetter)  # 生成setter

        print(classStr.format(self.HeroName, __initParmsForInitParms, __initParmsForAssignment, __initParmsForGetter,
                              __initParmsForSetter))
bean = ConvertBean("Hero", ["hid", "type", "subType","quality","level","levelMax","attack","speed","itemId","target","activate"])
bean.convert()
# self.hid = 0
# # 英雄类别
# self.type = 0
# # 英雄类型
# self.subType = 0
# # 品质
# self.quality = 0
# # 初始等级
# self.level = 0
# # 最大等级
# self.levelMax = 0
# # 英雄攻击
# self.attack = 0
# # 英雄攻速
# self.speed = 0
# # 英雄道具
# self.itemId = 0
# # 目标
# self.target = 0
# # 激活数量
# self.activate = 0













































