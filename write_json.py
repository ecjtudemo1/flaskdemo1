#1、每天的不同货物的销量表；2、

import json
import pymysql
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='UMR123..',
    db='flask_demo3',
    charset='utf8'
)
cur = conn.cursor()
aa = 0
sql = "select * from huoyuliang"
cur.execute(sql)
content = cur.fetchall()
data = {}
xaxis = []
yaxis = []
for i in content:
    xaxis.append(i[1])
    yaxis.append(i[2])
data['xaxis'] = xaxis
data['yaxis'] = yaxis
with open("./data.json", "w") as f:
     json.dump(data, f)
     print("加载入文件完成...")

