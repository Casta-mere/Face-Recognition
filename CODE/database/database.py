import pymysql

# change the following to your own database

# local
host = 'localhost'
user = 'root'
password = ''

# server


class my_sql():

    def __init__(self, database_name):
        self.database_name = database_name

    def execute_sql(self, sql):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
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

    def add_new_entry(self, table_name, item):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        values = ""
        for i in item:
            if(type(i) == str):
                values += f'"{i}",'
            else:
                values += f'{i},'
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

    def update_table_entry(self, id, timee):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        sql = f'update entry set timee="{timee}",bool = 0 where id ="{id}" and bool = 1;'
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

    def delete_table_entry(self, table_name, id):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        sql = f'delete from {table_name} where id ="{id}"'
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

    def get_attributes(self, table_name, attribute):  # attribute is a list
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
        return data

    def get_all_data_by_sepecific_attribute_value(self, table_name, attr_name, attr_value):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            f'select * from {table_name} where {attr_name}="{attr_value}"')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

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
        return data

    def get_newest_data(self, table_name, id):
        conn = pymysql.connect(host=host, user=user, password=password,
                               database=self.database_name, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            f'select * from {table_name} where id={id} order by date desc,times desc limit 1')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data


def reset():
    tabname_info = "info"
    column_info = []
    column_info.append(['id', 'int(11)'])
    column_info.append(['name', 'varchar(255)'])
    column_info.append(['email', 'varchar(255)'])

    info1 = [1, '王旭刚', '2287245796@qq.com']
    info2 = [2, '韦杨婧', '981193371@qq.com']
    info3 = [3, '刘俊伟', '1917871807@qq.com']

    tabname_entry = "entry"
    column_entry = []
    column_entry.append(['id', 'int(11)'])
    column_entry.append(['name', 'varchar(255)'])
    column_entry.append(['date', 'date'])
    column_entry.append(['times', 'time'])
    column_entry.append(['timee', 'time'])
    column_entry.append(['bool', 'boolean'])

    entry1 = [1, '王旭刚', '2020-01-01', '08:00:00', '09:00:00', False]
    entry2 = [2, '韦杨婧', '2020-01-01', '08:00:00', '09:00:00', False]
    entry3 = [3, '刘俊伟', '2020-01-01', '08:00:00', '09:00:00', False]

    db = my_sql("facerecognition")

    db.Create_Database()
    db.Create_table(tabname_info, column_info)
    db.add_new_entry(tabname_info, info1)
    db.add_new_entry(tabname_info, info2)
    db.add_new_entry(tabname_info, info3)

    db.Create_table(tabname_entry, column_entry)
    db.add_new_entry(tabname_entry, entry1)
    db.add_new_entry(tabname_entry, entry2)
    db.add_new_entry(tabname_entry, entry3)


def showlist(L):
    for i in L:
        for j in i:
            print(j, end=" ")
        print()


if __name__ == "__main__":
    reset()
    # db=my_sql("facerecognition")

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
