import pymysql
import config
import hashlib

def get_id_user(name):

	connector = pymysql.connect(
		host = config.host,
		user = config.user,
		passwd = config.passwd,
		db = config.db,
		charset = config.charset,
		cursorclass = pymysql.cursors.DictCursor
	)

	with connector.cursor() as cursor:
		sql = 'select id, name, bikou from userinfo where name = "%s";'% (name)
		cursor.execute(sql)
		sql_result = cursor.fetchall()

		json_response = { "id_user" : sql_result }					
		return json_response

def get_id_user_pass(name):

	connector = pymysql.connect(
		host = config.host,
		user = config.user,
		passwd = config.passwd,
		db = config.db,
		charset = config.charset,
		cursorclass = pymysql.cursors.DictCursor
	)

	with connector.cursor() as cursor:
		sql = 'select pass from userinfo where name = "%s";'% (name)
		cursor.execute(sql)
		sql_result = cursor.fetchall()

		json_response = { "user_pass" : sql_result }				
		return json_response

def post_user(user):

	connector = pymysql.connect(
		host = config.host,
		user = config.user,
		passwd = config.passwd,
		db = config.db,
		charset = config.charset,
		cursorclass = pymysql.cursors.DictCursor
	)

	with connector.cursor() as cursor:

		#パスワードのハッシュ値を保存
		passhash = hashlib.sha256(user.password.encode()).hexdigest()

		sql = 'insert into userinfo(name, bikou, pass) values(%s, %s, %s);'
		cursor.execute(sql, (user.name, user.bikou, passhash))
		connector.commit()
		
		sql = 'select id from userinfo order by id desc limit 1;'
		sql_result = cursor.fetchall()
		json_response = { "user_pass" : sql_result }				
		return json_response

