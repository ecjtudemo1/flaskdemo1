import csv
import pymysql
import sys
from datetime import datetime

input_file = sys.argv[1]
input_files = sys.argv[2]
con = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='UMR123..',
    db='flask_demo3',
    charset='utf8'
)
c = con.cursor()
files_reader = csv.reader(open(input_file, 'r', newline=''))
files_readers = csv.reader(open(input_files, 'r', newline=''))
header = next(files_reader)#第一行为表头名，不写入数据库中
headers = next(files_readers)
for row in files_reader:
    data = []
    for col in range(len(header)):
        if col < 4:
           data.append(str(row[col]).lstrip('$')\
           .replace(',', '').strip())
        else:#在列大于4列的时候，变成日期列
           a_date = datetime.date(datetime.strptime(\
               str(row[col]), '%m/%d/%Y'))
           # %Y: year is 2015; %y: year is 15
           a_date = a_date.strftime('%Y-%m-%d')
           data.append(a_date)
    c.execute("""INSERT INTO huoyuliang VALUES (%s, %s, %s);""", data)
for row in files_readers:
    datas = []
    for col in range(len(headers)):
        if col < 4:
           datas.append(str(row[col]).lstrip('$')\
           .replace(',', '').strip())
        else:#在列大于4列的时候，变成日期列
           b_date = datetime.date(datetime.strptime(\
               str(row[col]), '%m/%d/%Y'))
           # %Y: year is 2015; %y: year is 15
           b_date = b_date.strftime('%Y-%m-%d')
           datas.append(b_date)
    c.execute("""INSERT INTO daily_monitor VALUES (%s, %s, %s);""", datas)
con.commit()
print("")