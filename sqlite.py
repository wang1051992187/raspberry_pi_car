import sqlite3

class sqllite(object):
    def __init__(self):
        self.db = 'raspberry.db'

    def cursor(self,type, sql):
        conn = sqlite3.connect('raspberry.db')
        cursor = conn.cursor()
        cursor.execute(sql)
        if type == 3:
            values = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        if type == 3:
            return values

    def create_table(self,sql):
        self.cursor(1,sql)

    def insert(self,sql):
        self.cursor(2,sql)

    def select(self,sql):
        values = self.cursor(3,sql)
        return values


if __name__ == '__main__':
    lite = sqllite()
    create_sql = "DROP TABLE IF EXISTS tb_location"
    lite.create_table(create_sql)

    create_sql = "create table tb_location(id integer primary key,jingdu varchar(30),weidu varchar(30),create_time varchar(50))"
    lite.create_table(create_sql)

    jingdu = '32.434343'
    weidu  = '64.434242'
    insert_sql = "insert into tb_location(jingdu, weidu) values (\'"+ jingdu+"\', \'"+ weidu+"\')"
    lite.insert(insert_sql)

    select_sql = "select * from tb_location"
    values = lite.select(select_sql)
    print(values)


