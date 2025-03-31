from dotenv import dotenv_values

config = dotenv_values(".env")

BD_AUTHORIZATION = config.get('BD_AUTHORIZATION')
MYSQL_USER = config.get('MYSQL_USER')
MYSQL_PASSWORD = config.get('MYSQL_PASSWORD')
MYSQL_HOST = config.get('MYSQL_HOST')
MYSQL_PORT =config.get('MYSQL_PORT')
MYSQL_DB = config.get('MYSQL_DB')
TOKEN = config.get('TOKEN')
CHAT_ID = config.get('CHAT_ID')