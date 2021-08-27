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

		cursor.execute('select name from userinfo where name = %s', user.name)
		result = cursor.fetchall()

		if not result:
			cursor.execute('insert into userinfo(name, bikou, pass) values(%s, %s, %s)', (user.name, user.bikou, user.password))
			connector.commit()
			sql = 'select id from userinfo order by id desc limit 1;'
			sql_result = cursor.fetchall()
			json_response = { "user_pass" : sql_result }
			return json_response
		else:
			return False

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
		cursor.execute('select pass from userinfo where name = %s', name)
		sql_result = cursor.fetchall()

		#ユーザが存在しなければFalseを返す
		if not sql_result:
			return False
		else:
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

	#ユーザが存在しなければFalseを返す
	if db_pass_hash == False:
		return False

	#パスワード照合
	if auth_user.password == db_pass_hash:
		with connector.cursor() as cursor:

			cursor.execute('select name, bikou from userinfo where name = %s', auth_user.name)
			sql_result = cursor.fetchall()
			json_response = { "user_info" : sql_result }
			return json_response
	else:
		return False


