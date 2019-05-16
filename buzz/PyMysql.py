import pymysql


db = pymysql.connect(host='localhost',user='root',password='zgh19970701',port=3306,db='spiders')
cursor = db.cursor()


cursor.execute('create table if not exists students (id varchar(255) not null, name varchar(255) not null,age int not null,primary key (id))')

db.close()
