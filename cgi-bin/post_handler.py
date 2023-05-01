from creatin_db import con, cur
import cgi
import os
if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type:text/html\r\n\r\n")
    print('''
        <script type="text/javascript">
            window.location.href = "/";
        </script>''')
form = cgi.FieldStorage()

table_name = form.getvalue('table')
post = {k: form.getvalue(k) for k in form
        if not k == 'submit' or k == 'table'}
post_keys = list(post.keys())

params = '('+post_keys[0]
for i in range(1, len(post)-1):
    params += ','+post_keys[i]
params += ')'

values = '(?'
for i in range(1, len(post)-1):
    values += ',?'
values += ')'
cur.execute(f'insert into {table_name}{params} values {values}', (post[k] for k in post_keys))
con.commit()
print("Content-type:text/html\r\n\r\n")
print('<script type="text/javascript">'
      '{'
      'window.location.href = "/";'
      '}'
      '</script>')
