import pymysql
import config
import hashlib

#ユーザ登録
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

		sql = 'insert into userinfo(name, bikou, pass) values(%s, %s, %s);'
		cursor.execute(sql, (user.name, user.bikou, user.password))
		connector.commit()
		
		sql = 'select id from userinfo order by id desc limit 1;'
		sql_result = cursor.fetchall()
		json_response = { "user_pass" : sql_result }				
		return json_response

#ユーザのパスワードハッシュ取得
def get_user_hash(name):

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
		user_pass_hash = sql_result[0]["pass"]		
		return user_pass_hash

#ユーザ情報取得
def get_user_info(auth_user):

	connector = pymysql.connect(
		host = config.host,
		user = config.user,
		passwd = config.passwd,
		db = config.db,
		charset = config.charset,
		cursorclass = pymysql.cursors.DictCursor
	)

	db_pass_hash = get_user_hash(auth_user.name)
	
	#パスワード照合
	if auth_user.password == db_pass_hash:
		with connector.cursor() as cursor:

			sql = 'select name, bikou from userinfo where name = "%s";'% (auth_user.name)
			cursor.execute(sql)
			sql_result = cursor.fetchall()
			json_response = { "user_info" : sql_result }				
			return json_response
	else:
		json_response = { "user_pass" : "not authorized" }
		return json_response


