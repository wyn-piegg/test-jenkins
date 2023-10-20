import xlrd
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
        # 通过文件名获得工作表,获取工作表1
        if (isinstance(sheetNameOrIndex, str)):
            table = data.sheet_by_name(sheetNameOrIndex)
        elif (isinstance(sheetNameOrIndex, int)):
            table = data.sheet_by_index(sheetNameOrIndex)
        else:
            print("表名或表索引错误")
            return ""
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
        datas=[]
        for i in range(0,1):
            for j in range(startCols, endCols):
                class_hero=table.cell(i, j).value
                class_hero=class_hero.split("[")[0] # 提取分割后的前半部分 去掉字符串后面不需要的部分
                datas.append(class_hero)
        # 取出来的值有空值就删除这个空的值
        while '' in datas:
            datas.remove('')
        for d in datas:
            a="        "+"self."+d+"=0"
            z=open(r'hero.py',"a+")
            print(a, file=z)
            z.close()
if __name__ == '__main__':
    rex = readExcel()
    rex.read_xlrd('hero.xls', "Sheet1",)







































