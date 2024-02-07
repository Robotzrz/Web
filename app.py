from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import datetime as dt

items = mysql.connector.connect(
  host="localhost",
  user="root",
  password="14916",
  database="items"
)

items_cur = items.cursor()

people = mysql.connector.connect(
  host="localhost",
  user="root",
  password="14916",
  database="people"
)
people_cur = people.cursor()


admin_blank = "INSERT INTO admins (id, name, password) VALUES (%s, %s, %s)"

user_blank = "INSERT INTO users (id, name, password, gifts, fields) VALUES (%s, %s, %s, %s, %s)"

gift_blank = "INSERT INTO gifts (id, name, description) VALUES (%s, %s, %s)"

field_blank = "INSERT INTO fields (id, name, size, board) VALUES (%s, %s, %s, %s)"


def check_user(username, password):                                           # функция возвращает число: 
    people_cur.execute(f"SELECT password FROM users WHERE name='{username}'") # 0 - имени нет в базе;
    a = people_cur.fetchall()                                                 # 1 - имя есть в базе, но пароль неверен;
    if len(a) == 0:                                                           # 2 - имя и пароль верны
        return 0
    elif len(a) == 1:
        if a[0][0] == password:
            return 2
        else:
            return 1
    else:
        print("ЕСТЬ ПОЛЬЗОВАТЕЛИ С ОДИНАКОВЫМИ ИМЕНАМИ!")
        raise(OverflowError)
    
    
def check_admin(username, password):                                           # функция возвращает число: 
    people_cur.execute(f"SELECT password FROM admins WHERE name='{username}'") # 0 - имени нет в базе;
    a = people_cur.fetchall()                                                  # 1 - имя есть в базе, но пароль неверен;
    if len(a) == 0:                                                            # 2 - имя и пароль верны
        return 0
    elif len(a) == 1:
        if a[0][0] == password:
            return 2
        else:
            return 1
    else:
        print("ЕСТЬ АДМИНЫ С ОДИНАКОВЫМИ ИМЕНАМИ!")
        raise(OverflowError)    


def create_user(name, password):                   # функция возвращает число:  
    result = check_user(name, password)            # 0 - имя уже есть в базе;
    if result == 0:                                # 1 - пользователь успешно создан
        people_cur.execute("SELECT id FROM users")
        a = people_cur.fetchall()
        num = 0
        if a:
            num = a[-1][0] + 1
        us = (num, name, password, "", "")
        people_cur.execute(user_blank, us)
        people.commit()
        return 1
    else:
        return 0


def create_field(name, board):
    items_cur.execute(f"SELECT id FROM fields WHERE name='{name}'")
    a = items_cur.fetchall()                             
    if len(a) == 0:
        items_cur.execute("SELECT id FROM fields")
        a = items_cur.fetchall()
        num = 0
        if a:
            num = a[-1][0] + 1
        f = (num, name, int((len(board) / 3) ** 0.5), board)
        items_cur.execute(field_blank, f)
        items.commit()
        return 1
    else:
        return 0


def create_admin(name, password):                  # функция возвращает число:  
    result = check_admin(name, password)           # 0 - имя уже есть в базе;
    if result == 0:                                # 1 - админ успешно создан
        people_cur.execute("SELECT id FROM admins")
        a = people_cur.fetchall()
        num = 0
        if a:
            num = a[-1][0] + 1
        ad = (num, name, password)
        people_cur.execute(admin_blank, ad)
        people.commit()
        return 1
    else:
        return 0
        
        
def u_get_id(name):
    people_cur.execute(f'SELECT id FROM users WHERE name="{name}"')
    return people_cur.fetchall()[0]
    
    
def a_get_id(name):
    people_cur.execute(f'SELECT id FROM admins WHERE name="{name}"')
    return people_cur.fetchall()[0]
    
    
def g_get_id(name):
    items_cur.execute(f'SELECT id FROM gifts WHERE name="{name}"')
    return items_cur.fetchall()[0]
    
    
def f_get_id(name):
    items_cur.execute(f'SELECT id FROM fields WHERE name="{name}"')
    return items_cur.fetchall()[0]
    
    
def add_gift(u_id, g_id):
    people_cur.execute(f'SELECT gifts FROM users WHERE id={u_id}')
    old_gifts = str(people_cur.fetchall()[0])
    new_gifts = old_gifts + get_string_one(g_id, 3)
    people_cur.execute(f'UPDATE gifts FROM users WHERE id={u_id} TO {new_gifts}')
    
    
def add_field(u_id, f_id):
    people_cur.execute(f'SELECT fields FROM users WHERE id={u_id}')
    old_fields = str(people_cur.fetchall()[0])
    new_fields = old_fields + get_string_one(f_id, 3)
    people_cur.execute(f'UPDATE fields FROM users WHERE id={u_id} TO {new_fields}')

    
def get_list(string):
    result = []
    for index in range(0, len(string), 3):
        result.append(string[index : index + 3])
    return result
    
    
def get_string_one(num, length):
    num = '0' * (length - len(str(num))) + str(num)
    return num
        
        
def get_string_all(list1, length=3):
    res = ""
    for i in list1:
        res += get_string_one(i, length)
    return res

current_name = ""
current_mode = ""

app = Flask(__name__)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    name = request.form.get("name")
    board = str(request.form.get("code"))
    if current_name == "" or current_mode == "":
        print("BACK TO LOGIN")
        return redirect(url_for('login'))
    if board and len(board) > 2:
        print(create_field(name, board))
    return render_template("admin.html")

@app.route("/user", methods=['GET', 'POST'])
def user():
    if current_name == "" or current_mode == "":
        print("BACK TO LOGIN")
        return redirect(url_for('login'))
    return render_template("user.html")

@app.route("/reg", methods=['GET', 'POST'])
def reg():                                    # Регистрация
    global current_mode
    global current_name
    name = request.form.get('name')
    password = request.form.get('password')
    mode = request.form.get("admin")
    print(name, password, mode)
    if mode == "admin":
        res = create_admin(name, password)
        if res == 1:
            current_name = name
            current_mode = "admin"
            return redirect(url_for('admin'))
    elif mode == "user":
        res = create_user(name, password)
        if res == 1:
            current_name = name
            current_mode = "user"
            return redirect(url_for('user'))
    return render_template("reg.html")


@app.route("/login", methods=['GET', 'POST'])
def login():                                    # Вход
    global current_mode
    global current_name
    alert = [0]
    name = request.form.get('name')
    password = request.form.get('password')
    mode = request.form.get("admin")
    if mode == "admin":
        res = check_admin(name, password)
        if res == 2:
            current_name = name
            current_mode = "admin"
            return redirect(url_for('admin'))
        elif res == 1:
            alert = [1]
    elif mode == "user":
        res = check_user(name, password)
        if res == 2:
            current_name = name
            current_mode = "user"
            return redirect(url_for('user'))
    return render_template("login.html", mes=alert)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)