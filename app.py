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

gift_blank = "INSERT INTO gifts (id, name, description, image, date) VALUES (%s, %s, %s, %s, %s)"

field_blank = "INSERT INTO fields (id, name, size, board, changeable) VALUES (%s, %s, %s, %s, 1)"


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
        people_cur.execute(f"CREATE TABLE {name} (id INTEGER(10), name VARCHAR(45), moves INTEGER(10), size INTEGER(10), board VARCHAR(7500))")
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
cur_gift = []
cur_board = []

app = Flask(__name__)
@app.route("/")
def to_reg():
    return redirect(url_for('reg', mes=[-1]))
    
@app.route("/create_board", methods=['GET', 'POST'])
def create_board():
    global cur_board
    items_cur.execute("SELECT name FROM fields WHERE changeable=1")
    nboards_changeable = list(items_cur.fetchall())
    items_cur.execute("SELECT board FROM fields WHERE changeable=1")
    boards_changeable = list(items_cur.fetchall())
    items_cur.execute("SELECT name FROM fields WHERE changeable=0")
    nboards_unchangeable = list(items_cur.fetchall())
    items_cur.execute("SELECT board FROM fields WHERE changeable=0")
    
    boards_unchangeable = list(items_cur.fetchall())
    name = request.form.get("name")
    board = str(request.form.get("code"))
    if current_name == "" or current_mode == "":
        return redirect(url_for('login', mes=[0]))
    if board and len(board) > 2:
        create_field(name, board)
    people_cur.execute("SELECT name FROM users")
    us = list(people_cur.fetchall())
    return render_template("create_board.html", k=us, s=cur_board[1])

@app.route("/create_prize", methods=['GET', 'POST'])
def create_prize():
    global cur_gift
    name = request.form.get("name")
    date = request.form.get("date")
    descr = request.form.get("descr")
    image = request.form.get("img")
    dele = request.form.get("del")
    if dele == "1" and image and descr and date and name:
        items_cur.execute("SELECT id FROM gifts")
        a = items_cur.fetchall()
        num = 0
        if a:
            num = a[-1][0] + 1
        items_cur.execute(gift_blank, (num, name, descr, image, date))
        items.commit()
        cur_gift = []
        return redirect(url_for('admin'))
    if dele == "0":
        if cur_gift[0] != "":
            items_cur.execute(f"DELETE FROM gifts WHERE name='{cur_gift[0]}'")
            items.commit()
        cur_gift = []
        return redirect(url_for('admin'))
    return render_template("create_prize.html", n=cur_gift[0], i=cur_gift[1], de=cur_gift[2], d=cur_gift[3])

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    global cur_gift
    global cur_board
    items_cur.execute("SELECT name FROM fields WHERE changeable=1")
    nboards_changeable = list(items_cur.fetchall())
    items_cur.execute("SELECT name FROM fields WHERE changeable=0")
    nboards_unchangeable = list(items_cur.fetchall())
    items_cur.execute("SELECT name FROM gifts")
    gifts = list(items_cur.fetchall())
    name = request.form.get("name")
    if current_name == "" or current_mode == "":
        return redirect(url_for('login', mes=[0]))
    if type(name) != None:
        if str(name) == "g":
            cur_gift = ["", "", "", ""]
            return redirect(url_for('create_prize'))
        elif str(name) == "b":
            cur_board = ["", ""]
            return redirect(url_for('create_board'))
        elif str(name)[-1] == "g":
            cur_gift.append(str(name[:-1]))
            items_cur.execute(f"SELECT image FROM gifts WHERE name='{str(name[:-1])}'")
            cur_gift.append(items_cur.fetchone())
            items_cur.execute(f"SELECT description FROM gifts WHERE name='{str(name[:-1])}'")
            cur_gift.append(items_cur.fetchone())
            items_cur.execute(f"SELECT date FROM gifts WHERE name='{str(name[:-1])}'")
            cur_gift.append(items_cur.fetchone())
            return redirect(url_for('create_prize'))
        elif str(name)[-1] == "b":
            cur_board = []
            items_cur.execute(f"SELECT size FROM fields WHERE name='{str(name[:-1])}'")
            cur_board.append(items_cur.fetchone())
            items_cur.execute(f"SELECT board FROM fields WHERE name='{str(name[:-1])}'")
            cur_board.append(items_cur.fetchone()) 
            return redirect(url_for('create_board'))
    return render_template("admin.html", nc=nboards_changeable, nu=nboards_unchangeable, g=gifts)

@app.route("/view_prize", methods=['GET', 'POST'])
def view_prize():
    global cur_gift
    print("HELLLOOOO~~~~")
    name = request.form.get("name")
    date = request.form.get("date")
    descr = request.form.get("descr")
    image = request.form.get("img")
    dele = request.form.get("del")
    if dele == "1":
        items_cur.execute("SELECT id FROM gifts")
        a = items_cur.fetchall()
        num = 0
        if a:
            num = a[-1][0] + 1
        items_cur.execute(gift_blank, (num, name, descr, image, date))
        items.commit()
        cur_gift = []
        return redirect(url_for('user'))
    if dele == "0":
        if cur_gift[0] != "":
            items_cur.execute(f"DELETE FROM gifts WHERE name='{cur_gift[0]}'")
            items.commit()
        cur_gift = []
        return redirect(url_for('user'))
    return render_template("view_prize.html", n=cur_gift[0], i=cur_gift[1], de=cur_gift[2], d=cur_gift[3])

@app.route("/view_board", methods=['GET', 'POST'])
def view_board():
    items_cur.execute("SELECT name FROM fields WHERE changeable=1")
    nboards_changeable = list(items_cur.fetchall())
    items_cur.execute("SELECT board FROM fields WHERE changeable=1")
    boards_changeable = list(items_cur.fetchall())
    items_cur.execute("SELECT name FROM fields WHERE changeable=0")
    nboards_unchangeable = list(items_cur.fetchall())
    items_cur.execute("SELECT board FROM fields WHERE changeable=0")
    boards_unchangeable = list(items_cur.fetchall())
    name = request.form.get("name")
    board = str(request.form.get("code"))
    if current_name == "" or current_mode == "":
        return redirect(url_for('login', mes=[0]))
    if board and len(board) > 2:
        create_field(name, board)
    return render_template("view_board.html", nc=boards_changeable, nu=boards_unchangeable, c=boards_changeable, u=boards_unchangeable)

@app.route("/user", methods=['GET', 'POST'])
def user():
    global cur_gift
    global cur_board
    people_cur.execute(f"SELECT name FROM {current_name}")
    nboards_changeable = list(people_cur.fetchall())
    people_cur.execute(f"SELECT gifts FROM users WHERE name='{current_name}'")
    gifts = get_list(people_cur.fetchone()[0])
    gift = []
    for i in range(len(gifts)):
        items_cur.execute(f"SELECT name FROM gifts WHERE id={int(gifts[i])}")
        gift.append(items_cur.fetchone()[0])
    people_cur.execute(f"SELECT name FROM {current_name}")
    board = list(people_cur.fetchall())
    name = request.form.get("name")
    if current_name == "" or current_mode == "":
        return redirect(url_for('login', mes=[0]))
    print(name)
    if type(name) != None:
        if str(name)[-1] == "g":
            cur_gift.append(str(name[:-1]))
            items_cur.execute(f"SELECT image FROM gifts WHERE name='{str(name[:-1])}'")
            cur_gift.append(items_cur.fetchall()[0])
            items_cur.execute(f"SELECT description FROM gifts WHERE name='{str(name[:-1])}'")
            cur_gift.append(items_cur.fetchall()[0])
            items_cur.execute(f"SELECT date FROM gifts WHERE name='{str(name[:-1])}'")
            cur_gift.append(items_cur.fetchall()[0])
            return redirect(url_for('view_prize'))
        elif str(name)[-1] == "b":
            cur_board = []
            items_cur.execute(f"SELECT size FROM fields WHERE name='{str(name[:-1])}'")
            cur_board.append(items_cur.fetchone())
            items_cur.execute(f"SELECT board FROM fields WHERE name='{str(name[:-1])}'")
            cur_board.append(items_cur.fetchone())
            return redirect(url_for('view_board'))
    return render_template("user.html", nc=nboards_changeable, g=gift)

@app.route("/reg", methods=['GET', 'POST'])
def reg():                                    # Регистрация
    global current_mode
    global current_name
    alert = [-1]
    name = request.form.get('name')
    password = request.form.get('password')
    mode = request.form.get("admin")
    if len(str(name)) and not(str(name)[0].isalpha()):
        alert = [4]
    elif mode == "admin":
        res = create_admin(name, password)
        if res == 1:
            current_name = name
            current_mode = "admin"
            return redirect(url_for('admin'))
        else:
            alert = [0]
    elif mode == "user":
        res = create_user(name, password)
        if res == 1:
            current_name = name
            current_mode = "user"
            return redirect(url_for('user'))
        else:
            alert = [0]
    elif name:
        alert = [3]
    return render_template("reg.html", mes=alert)

@app.route("/login", methods=['GET', 'POST'])
def login():                                    # Вход
    global current_mode
    global current_name
    alert = [-1]
    name = request.form.get('name')
    password = request.form.get('password')
    mode = request.form.get("admin")
    if mode == "admin":
        res = check_admin(name, password)
        if res == 2:
            current_name = name
            current_mode = "admin"
            return redirect(url_for('admin'))
        else:
            alert = [res]
    elif mode == "user":
        res = check_user(name, password)
        if res == 2:
            current_name = name
            current_mode = "user"
            return redirect(url_for('user'))
        else:
            alert = [res]
    elif len(str(name)):
        alert = [3]
    return render_template("login.html", mes=alert)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)