import pymysql

import sys
sys.path.append(sys.path[0]+'/..')
from Log import log

# change the following to your own database

# local
host = 'localhost'
user = 'root'
password = ''

# server


class my_sql():

    def __init__(self, database_name):
        self.database_name = database_name
        self.log=log.classlog("database")

    # self-test when booting
    def boot_selftest(self):

        # check if user name and password are correct
        try:
            conn = pymysql.connect(host=host, user=user,
                                   password=password, charset='utf8')
        except:
            return False, "FAIL : Wrong user name or password for Database!"
        cursor = conn.cursor()

        # check if database exists, if not create one
        try:
            sql = f"SELECT * FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = '{self.database_name}'"
            cursor.execute(sql)
            cursor.close()
        except:
            print("ALERT : Database not found, creating new database...")
            self.Create_Database()

        self.conn=pymysql.connect(host=host, user=user,passwd=password, db=self.database_name, charset='utf8')
        self.cursor=self.conn.cursor()

        return True, "SUCCESS : Database connected!"

    def execute_sql(self, sql):

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            self.log.log("SUCCESS : "+sql)
            return self.cursor.fetchall()
        except Exception as e:
            self.log.log("ERROR : "+str(e))
            self.log.log("ERROR : "+sql)
            self.conn.rollback()
            print("ERROR : Check your sql syntax!")


    def Create_Database(self):
        conn = pymysql.connect(host=host, user=user,
                               password=password, charset='utf8')

        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS %s" % self.database_name)
        cursor.execute("CREATE DATABASE %s" % self.database_name)
        cursor.close()
        conn.close()
        self.conn=pymysql.connect(host=host, user=user,passwd=password, db=self.database_name, charset='utf8')
        self.cursor=self.conn.cursor()

    def Drop_Database(self):
        conn = pymysql.connect(host=host, user=user,
                               password=password, charset='utf8')

        cursor = conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS %s" % self.database_name)
        cursor.close()
        conn.close()
        
    def Drop_table(self, table_name):
        sql="DROP TABLE IF EXISTS %s" % table_name
        self.execute_sql(sql)

    def Create_table(self, table_name, columns):
        self.Drop_table(table_name)
        sql="CREATE TABLE %s (%s)" % (table_name, self.translate(columns))
        self.execute_sql(sql)

    def translate(self, column_list):
        column = ''
        for i in column_list:
            column += i[0]+' '+i[1]+','
        return column[:-1]

    # add new entry to table "table_name"
    def add_new_entry(self, table_name, item):

        values = ""
        for i in item:
            if(type(i) == str):
                values += f'"{i}",'
            else:
                values += f'{i},'
        sql = f'insert into `{table_name}` values({values[:-1]});'
        self.execute_sql(sql)

    def update_table(self, table_name, item_find, item_change):
        find=str.join(" and ",[f"{i[0]}='{i[1]}'" for i in item_find])
        change=str.join(",",[f"{i[0]}='{i[1]}'" for i in item_change])
        sql=f"update {table_name} set {change} where {find};"
        self.execute_sql(sql)

    def delete_table(self,table_name,item):
        find=str.join(" and ",[f"{i[0]}='{i[1]}'" for i in item])
        sql=f"delete from {table_name} where {find};"
        self.execute_sql(sql)

    def update_table_entry(self, id, timee):
        item_find=[["id",id],["bool",1]]
        item_change=[["timee",timee],["bool",0]]
        self.update_table("entry",item_find,item_change)

    def delete_table_entry(self, table_name, id):
        item=[["id",id]]
        self.delete_table(table_name,item)

    def get_all_data(self, table_name):
        sql=f'select * from {table_name}'
        return self.execute_sql(sql)

    def get_attributes(self, table_name, attribute):  # attribute is a list
        sql=f'select {",".join(attribute)} from {table_name}'
        return self.execute_sql(sql)

    def get_all_data_by_sepecific_attribute_value(self, table_name, attr_name, attr_value):
        sql=f'select * from {table_name} where {attr_name}="{attr_value}"'
        return self.execute_sql(sql)

    def get_attributes_by_sepecific_attribute_value(self, table_name, attr_name, attr_value, attribute):
        sql=f'select {",".join(attribute)} from {table_name} where {attr_name}="{attr_value}"'
        return self.execute_sql(sql)

    def get_newest_data(self, table_name, id):
        sql=f'select * from {table_name} where id={id} order by date desc, times desc limit 1'
        return self.execute_sql(sql)


def reset():
    tabname_info = "info"
    column_info = []
    column_info.append(['id', 'varchar(255)'])
    column_info.append(['name', 'varchar(255)'])
    column_info.append(['email', 'varchar(255)'])

    info1 = ["2020329621074", '王旭刚', '2287245796@qq.com']
    info2 = ["2020329621199", '韦杨婧', '981193371@qq.com']
    info3 = ["2020329621229", '刘俊伟', '1917871807@qq.com']

    tabname_entry = "entry"
    column_entry = []
    column_entry.append(['id', 'varchar(255)'])
    column_entry.append(['name', 'varchar(255)'])
    column_entry.append(['date', 'date'])
    column_entry.append(['times', 'time'])
    column_entry.append(['timee', 'time'])
    column_entry.append(['bool', 'boolean'])

    entry1 = ["2020329621074", '王旭刚', '2020-01-01', '08:00:00', '09:00:00', False]
    entry2 = ["2020329621199", '韦杨婧', '2020-01-01', '08:00:00', '09:00:00', False]
    entry3 = ["2020329621229", '刘俊伟', '2020-01-01', '08:00:00', '09:00:00', False]

    table_device = "device"
    colunm_device = []
    colunm_device.append(['id', 'int(11)'])
    colunm_device.append(['name', 'varchar(255)'])
    colunm_device.append(['tpye', 'tinyint(1)'])
    
    # 0: in, 1: out, 2: in&out
    device1 = [1, '10-409前门外', 0]
    device3 = [2, '10-409前门内', 1]
    device2 = [3, '10-409后门', 2]

    db = my_sql("facerecognition")
    print(db.boot_selftest())

    db.Create_Database()
    db.Create_table(tabname_info, column_info)
    db.add_new_entry(tabname_info, info1)
    db.add_new_entry(tabname_info, info2)
    db.add_new_entry(tabname_info, info3)

    db.Create_table(tabname_entry, column_entry)
    db.add_new_entry(tabname_entry, entry1)
    db.add_new_entry(tabname_entry, entry2)
    db.add_new_entry(tabname_entry, entry3)

    db.Create_table(table_device, colunm_device)
    db.add_new_entry(table_device, device1)
    db.add_new_entry(table_device, device2)
    db.add_new_entry(table_device, device3)


def showlist(L):
    for i in L:
        for j in i:
            print(j, end=" ")
        print()


if __name__ == "__main__":
    reset()
    # db=my_sql("facerecognition")
    # db.boot_selftest()
    # print(db.execute_sql("select * from info"))
    # find=[["id","1"],["name","王旭刚"]]
    # change=[["name","王旭刚"],["timee","18:00:00"]]
    # db.update_table("entry",find,change)

    # print(db.get_newest_data("entry",2))
    # showlist(db.get_newest_data("entry",3))
    # info=entry2=[3,'ljw','2022-01-01','08:00:00','',True]
    # db.add_entry("entry",info)

    # l=list(db.get_all_data_by_sepecific_attribute_value("entry",'id',1))
    # showlist(l)
    # db.update_entry(1,"18:00:00")
    # l=list(db.get_all_data_by_sepecific_attribute_value("entry",'id',1))
    # showlist(l)
    # l=list(db.get_all_data("info"))
    # showlist(l)
