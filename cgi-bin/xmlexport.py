import cgi
from xml.etree import ElementTree as ET
from xml.dom import minidom
from creatin_db import cur, BASE_DIR
import os
if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type:text/html\r\n\r\n")
    print('''
        <script type="text/javascript">
            window.location.href = "/";
        </script>''')
export = cgi.FieldStorage()
table_name = export.getvalue('table')
columns = dict()
for row in cur.execute(f'PRAGMA table_info({table_name})'):
    columns[row[0]] = row[1]
root = ET.Element('data')
tree = ET.ElementTree(root)
table = ET.Element('table')
table.text = table_name
root.append(table)
c = 1
for row in cur.execute(f'SELECT * from {table_name}'):
    r = ET.Element('row')
    r.text = str(c)
    table.append(r)
    for i in range(len(row)):
        a = ET.Element(columns[i])
        a.text = str(row[i])
        r.append(a)
    c += 1
file = f'{BASE_DIR}/export/{table_name}_export.xml'
# tree.write(file, encoding='utf-8')
t = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
with open(file, 'w') as f:
    f.write(t)

print("Content-type:text/html\r\n\r\n")
print("<head><meta charset=\"utf-8\"></head>")
print('<script type="text/javascript">'
      '{'
      'window.location.href = "/";'
      'alert("Таблица %s была экспортирована в xml фaйл");'
      '}'
      '</script>' % table_name)
