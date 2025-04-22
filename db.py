import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12774664",
        password="hz555pnMdl",
        database="sql12774664",
        port=3306
    )
