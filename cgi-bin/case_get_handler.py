from creatin_db import con, cur

defs = dict()
jud = dict()
for row in cur.execute('select id_def, fullname from defendants'):
    defs[row[0]] = row[1]
for row in cur.execute('select id_judge, fullname from judges'):
    jud[row[0]] = row[1]
print("""
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Дела</title>
</head>
<body>
<h2>Для добавления данных в таблицу введите данные в форму</h2>
<form action=\"post_handler.py\" method="post">
	<label>Подсудимый</label><br>
	<select name="id_def">
		<option value="null">--Выберите подсудимого--</option>""")
for k in defs.keys():
    print(f'<option value="{k}">{k}. {defs[k]}</option>')
print("""</select><br>
	<label>Судья</label><br>
	<select name="id_judge">
		<option value="null">--Выберите судью--</option>""")
for k in jud.keys():
    print(f'<option value="{k}">{k}. {jud[k]}</option>')
print("""
	</select><br>
	<label>Дата принятия дела</label><br>
	<input type="datetime-local" name="start_date"><br>
	<label>Дата закрытия дела</label><br>
	<input type="datetime-local" name="end_date"><br>
	<label>Подсудимый виновен?</label><br>
	<input type="radio" name="guilty" id="r1" value="true"> Да  
	<input type="radio" name="guilty" id="r2" value="false"> Нет    
	<input type="radio" name="guilty" id="r3" value="null">Не определено    <br>
	<label>Основная нформация по делу</label><br>
    <textarea name="info"></textarea><br>
    <label>Дело закрыто</label><br>
	<input type="radio" name="closed" id="r1" value="true"> Да  
	<input type="radio" name="closed" id="r2" value="false"> Нет    
	<input type="radio" name="closed" id="r3" value="null">Не определено    <br>
	<input name="table" value="cases" hidden>
	<input type="submit" name="submit">
</form><br>
<button type="button" onclick="home()">Вернуться в главное меню</button><br>
<form action="table_view.py" method="post">
    <input name="table" hidden value="cases">
    <input type="submit" name="submit" value="Вывести содержимое таблицы">
</form>
<form action="xmlexport.py" method="post">
    <input name="table" hidden value="cases">
    <input type="submit" name="submit" value="Экспорт таблицы в xml">
</form>
<script type="text/javascript">
	function home(){
		window.location.href = "/";
	}
</script>
</body>
</html>""")
