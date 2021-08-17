# encoding: utf-8
"""
@file: readSQLFile.py
@time: 2021/8/5 13:43
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import re
from ast import literal_eval


class ReadSQLFile:
    def __init__(self, sqlFilePath, sqlHader=('INSERT', 'SET', 'DROP', 'CREATE', 'DELETE', 'UPDATE', 'SELECT')):
        self.sqlFilePath = sqlFilePath
        self.sqlHader = sqlHader
        self.sqlList = []
        self.read_SQL_file(sqlHader)

    def read_SQL_file(self, sqlHader):
        sqlStr = ''
        with open(self.sqlFilePath, 'r+', encoding='utf-8', errors="ignore") as fo:
            while True:
                text_line = fo.readline()
                if text_line:
                    if text_line.startswith(sqlHader):
                        if text_line.replace('\n', '').endswith(';'):
                            self.sqlList.append(text_line.replace('\n', ''))
                        else:
                            sqlStr = text_line
                    elif sqlStr.startswith(sqlHader):
                        sqlStr += text_line
                        if text_line.replace('\n', '').endswith(';'):
                            self.sqlList.append(sqlStr.replace('\n', ''))
                            sqlStr = ''
                else:
                    break

    def get_SQL_List(self):
        return self.sqlList

    def get_SQL_columns(self):
        if 'CREATE' in self.sqlHader:
            for row in self.sqlList:
                if row.startswith('CREATE'):
                    # 移除块注释
                    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", row)
                    # 移除整行注释
                    lines = [line for line in q.splitlines() if not re.match(r"^\s*(--|#)", line)]
                    # 移除行尾注释
                    q = " ".join([re.split("--|#", line)[0] for line in lines])
                    q = re.sub(r"(.*?)\(", "", q, count=1)
                    q = re.sub(r" COMMENT '(.*?)',", ",", q)
                    q = re.sub(r" DEFAULT '(.*?)',|DEFAULT NULL,", ',', q)
                    q = re.sub(r" PRIMARY KEY (.*$)| UNIQUE KEY (.*$)", '', q)
                    return re.findall(r"`(.*?)`", q)
        elif 'INSERT' in self.sqlHader:
            for row in self.sqlList:
                if row.startswith('INSERT'):
                    # 待验证
                    q = re.sub(r" VALUES (.*$)", "", row)
                    q = re.search(r"\((.*?)\)", q)
                    return re.findall(r"`(.*?)`", str(q))

    def get_SQL_data(self):
        tupleDatas = []
        if 'INSERT' in self.sqlHader:
            for da in self.sqlList:
                if da.startswith('INSERT') and da.endswith(');'):
                    q = re.sub(r"(.*?)VALUES \(", "", da, count=1).rstrip(');')
                    for v in q.split('),('):
                        if v.startswith('('):
                            v = v[1:]
                        elif v.endswith(')'):
                            v = v[:-1]
                        if "'NULL'" not in v:
                            v = v.replace('NULL', "'NULL'").replace('null', "'NULL'").replace("''NULL''", "'NULL'")
                        checks = literal_eval('(' + v + ')')
                        tupleDatas.append(list(checks))
        return tupleDatas

    def get_SQL_dict(self):
        data_dict = []
        column = self.get_SQL_columns()
        for da in self.get_SQL_data():
            data_dict.append(dict(zip(column, da)))
