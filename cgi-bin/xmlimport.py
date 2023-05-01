import cgi
from xml.etree import ElementTree as ET
from creatin_db import cur, BASE_DIR, con
import os
if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type:text/html\r\n\r\n")
    print('''
        <script type="text/javascript">
            window.location.href = "/";
        </script>''')

form = cgi.FieldStorage()
path = BASE_DIR + '\\import\\' + form.getvalue('import')

tree = ET.parse(path)
root = tree.getroot()
table_name = root.find('table').text.strip()

columns = dict()
for row in cur.execute(f'PRAGMA table_info({table_name})'):
    columns[row[0]] = [row[1], row[2]]

data = [[None]*(len(columns)-1) for i in range(len(root.findall('.//row')))]
for i in range(1, len(columns)):
    j = 0
    for elem in root.iter(columns[i][0]):
        data[j][i-1] = elem.text
        j += 1

data = [tuple(l) for l in data]

params = '(' + columns[1][0]
for i in range(2, len(columns)):
    params += ',' + columns[i][0]
params += ')'

values = '(?'
for i in range(2, len(columns)):
    values += ',?'
values += ')'

cur.executemany(f'insert into {table_name}{params} values {values}', data)
con.commit()

print("Content-type:text/html\r\n\r\n")
print("<head><meta charset=\"utf-8\"></head>")
print('<script type="text/javascript">'
      '{'
      'window.location.href = "/";\n'
      'alert("Данные были успешно импортированы в таблицу %s из xml фaйл");'
      '}'
      '</script>' % table_name)

