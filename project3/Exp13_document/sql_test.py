import sqlite3

# 连接到数据库（如果不存在则创建）
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 创建用户表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
password TEXT NOT NULL
)
''')
conn.commit()

# 插入示例用户数据
cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('user1', 'password123'))
conn.commit()

# 查询示例用户
cursor.execute('SELECT * FROM users WHERE username=? AND password=?', ('user1', 'password123'))
user = cursor.fetchone()
if user:
    print(f'Logged in as {user[1]}')
else:
    print('Invalid credentials')

# 关闭连接
cursor.close()
conn.close()
