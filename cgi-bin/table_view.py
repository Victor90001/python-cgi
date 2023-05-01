import cgi
from creatin_db import con, cur
import os
form = cgi.FieldStorage()
table_name = form.getvalue('table')
if os.environ['REQUEST_METHOD'] == 'GET' or table_name is None:
    print("Content-type:text/html\r\n\r\n")
    print('''
        <script type="text/javascript">
            window.location.href = "/";
        </script>''')
table = [[]]
for row in cur.execute(f'PRAGMA table_info({table_name})'):
    table[0].append(row[1])
for row in cur.execute(f'select * from {table_name}'):
    table.append(row)

print("Content-type:text/html\r\n\r\n")
print("""
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Содержимое таблицы %s</title>
</head>
<body>""" % table_name)
print(f'<h2>Содержимое таблицы {table_name}</h2>')
print('<table>')
for i in range(len(table)):
    print('<tr>')
    for j in range(len(table[i])):
        if i == 0:
            print(f'<th>{table[i][j]}</th>')
        else:
            print(f'<td>{table[i][j]}</td>')
    print('</tr>')
print('</table>')
print("""<button type="button" onclick="home()">Вернуться в главное меню</button>   
<button type="button" onclick="history.back()">Назад</button>
<form action="xmlexport.py" method="post">
    <input name="table" hidden value="%s">
    <input type="submit" name="submit" value="Экспорт таблицы в xml">
</form>
<script type="text/javascript">
	function home(){
		window.location.href = "/";
	}
</script>
</body>
</html>""" % table_name)
