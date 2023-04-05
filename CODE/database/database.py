import pymysql

# change the following to your own database

# local
host='localhost'
user='root'
password=''

# server

class my_sql():
    def __init__(self,database_name):
        self.database_name=database_name

    def execute_sql(self,sql):
        conn=pymysql.connect(host=host,user=user,password=password,database=self.database_name,charset='utf8')
        cursor=conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()

    def Create_Database(self):
        conn = pymysql.connect(host=host, user=user,
                               password=password, charset='utf8')

        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS %s" % self.database_name)
        cursor.execute("CREATE DATABASE %s" % self.database_name)
        cursor.close()
        conn.close()

    def Drop_Database(self):
        conn = pymysql.connect(host=host, user=user,
                               password=password, charset='utf8')

        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS %s" % self.database_name)
        cursor.close()
        conn.close()

    def Drop_table(self, table_name):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
        cursor.close()
        conn.close()

    def Create_table(self, table_name, columns):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        self.Drop_table(table_name)
        cursor.execute("CREATE TABLE %s (%s)" %
                       (table_name, self.translate(columns)))
        cursor.close()
        conn.close()

    def translate(self, column_list):
        column = ''
        for i in column_list:
            column += i[0]+' '+i[1]+','
        return column[:-1]

    def Update_table(self, table_name, item):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        values = ""
        for i in item:
            if(type(i) == str):values += f'"{i}",'
            else:values += f'{i},'
        sql = f'insert into `{table_name}` values({values[:-1]});'
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            with open("err.txt", "a", encoding="utf-8")as f:
                f.write(sql+"\n")
            print("error")
        cursor.close()
        conn.close()

    def get_all_data(self, table_name):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(f'select * from {table_name}')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data    
    
    def get_attributes(self, table_name, attribute): # attribute is a list
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        values = ""
        for i in attribute:
            values += f'{i},'
        cursor.execute(f'select {values[:-1]} from {table_name}')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return list(data)

    def get_all_data_by_sepecific_attribute_value(self, table_name, attr_name, attr_value):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            f'select * from {table_name} where {attr_name}="{attr_value}"')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return list(data)

    def get_attributes_by_sepecific_attribute_value(self, table_name, attr_name, attr_value, attribute):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        values = ""
        for i in attribute:
            values += f'{i},'
        cursor.execute(
            f'select {values[:-1]} from {table_name} where {attr_name}="{attr_value}"')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return list(data)


def reset():
    tabname="info"
    column=[]
    column.append(['id','int(11)'])
    column.append(['name','varchar(255)'])
    column.append(['date','date'])
    column.append(['times','time'])
    column.append(['timee','time'])
    column.append(['bool','boolean'])

    info1=[1,'zhangsan','2020-01-01','08:00:00','09:00:00',False]
    info2=[2,'lisi','2020-01-01','08:00:00','09:00:00',False]

    db=my_sql("facerecognition")
    db.Create_table(tabname,column)
    db.Update_table(tabname,info1)
    db.Update_table(tabname,info2)

if __name__=="__main__":
    # reset()
    db=my_sql("facerecognition")
    l=list(db.get_all_data("info"))
    for i in l:
        for j in i:
            print(j,type(j))
        print()