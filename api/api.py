from flask import Flask, jsonify
from flask import request
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['MYSQL_HOST'] = '192.168.56.101'
app.config['MYSQL_USER'] = 'sawlad'
app.config['MYSQL_PASSWORD'] = 'sadat1998'
app.config['MYSQL_DB'] = 'ErikaDB'

mysql = MySQL(app)

@app.route('/api/v1/user/<user_id>', methods=['GET'])
def get_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User does not exist!"
    cur = mysql.connection.cursor()
    cur.execute("select UserID, BirthYear, BirthMonth, BirthDay, Bio from User where UserID =" + user_id)
    rv = cur.fetchall()
    cur.close()
    user_id, birth_year, birth_month, birth_day, bio = rv[0]
    birthday = create_date_str(birth_year, birth_month, birth_day)
    payload = []
    content = {'UserID': user_id, 'Birthday': birthday, 'Bio': bio}
    payload.append(content)
    return jsonify(payload)

@app.route('/api/v1/user', methods=['POST'])
def create_user():
    input_json = request.get_json(force=True)
    if does_tuple_exist("User", ["UserID"], [repr(input_json['UserID'])]):
        return "User already exists!"
    split_birthday = split_date(input_json['Birthday'])
    user_tuple = (input_json['UserID'], hash_password(input_json['Password']), split_birthday[2], split_birthday[1], split_birthday[0], input_json['Bio'])
    query = "insert into User (UserID, Password, BirthYear, BirthMonth, BirthDay, Bio) VALUES {}".format(user_tuple)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return 'OK'

@app.route('/api/v1/user/<user_id>', methods=['POST'])
def follow_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "You can't follow a user who doesn't exist!"
    input_json = request.get_json(force=True)
    pass

@app.route('/api/v1/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User already deleted!"
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM User WHERE UserID=' + user_id)
    mysql.connection.commit()
    cur.close()
    return 'User successfully deleted!'

@app.route('/api/v1/user/<user_id>/posts', methods=['GET'])
def get_posts_by_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User does not exist!"
    cur = mysql.connection.cursor()
    cur.execute("select * from Post where CreatedBy =" + user_id)
    rvs = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for rv in rvs:
        post_id, post_type, body, image_url, created_by, year_created, month_created, day_created = rv
        date_created = create_date_str(year_created, month_created, day_created)
        content = {'PostID': post_id, 'Type': post_type, 'DateCreated': date_created, 'Body': body, 'ImageURL': image_url, 'CreatedBy:': created_by}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/post/<post_id>', methods=['GET'])
def get_post_by_user(user_id, post_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User does not exist!"
    elif not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post does not exist!"
    cur = mysql.connection.cursor()
    cur.execute("select * from Post where CreatedBy =" + user_id + " and " + " PostID =" + post_id)
    rv = cur.fetchall()
    cur.close()
    post_id, post_type, body, image_url, created_by, year_created, month_created, day_created = rv[0]
    date_created = create_date_str(year_created, month_created, day_created)
    payload = []
    content = {'PostID': post_id, 'Type': post_type, 'DateCreated': date_created, 'Body': body, 'ImageURL': image_url, 'CreatedBy:': created_by}
    payload.append(content)
    return jsonify(payload)

@app.route('/api/v1/post', methods=['POST'])
def create_post():
    input_json = request.get_json(force=True)
    split_date_created = split_date(input_json['DateCreated'])
    post_tuple = (input_json['Type'], input_json['Body'], input_json['ImageURL'], input_json['CreatedBy'], split_date_created[2], split_date_created[1], split_date_created[0])
    query = "insert into Post (Type, Body, ImageURL, CreatedBy, YearCreated, MonthCreated, DayCreated) VALUES {}".format(post_tuple)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return 'OK'

@app.route('/api/v1/post/<post_id>/react', methods=['POST'])
def react_to_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "You can't react to a post that doesn't exist!"
    pass

@app.route('/api/v1/post/<post_id>/respond', methods=['POST'])
def respond_to_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "You can't respond to a post that doesn't exist!"
    pass

@app.route('/api/v1/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post already deleted!"
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Post WHERE PostID=' + post_id)
    mysql.connection.commit()
    cur.close()
    return 'Post successfully deleted!'

@app.route('/api/v1/group', methods=['GET'])
def get_groups():
    cur = mysql.connection.cursor()
    cur.execute("select * from UserGroup")
    rvs = cur.fetchall()
    cur.close()
    payload = []
    content = {}
    for rv in rvs:
        group_id, about, created_by = rv
        content = {'GroupID': group_id, 'About': about, 'CreatedBy': created_by}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/group', methods=['POST'])
def create_group():
    input_json = request.get_json(force=True)
    if does_tuple_exist("UserGroup", ["GroupID"], [repr(input_json['GroupID'])]):
        return "Group already exists!"
    input_json = request.get_json(force=True)
    group_tuple = (input_json['GroupID'], input_json['About'], input_json['CreatedBy'])
    query = "insert into UserGroup (GroupID, About, CreatedBy) VALUES {}".format(group_tuple)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    return 'OK'

@app.route('/api/v1/group', methods=['POST'])
def join_group():
    input_json = request.get_json(force=True)
    pass

@app.route('/api/v1/group/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    if not does_tuple_exist("UserGroup", ["GroupID"], [group_id]):
        return "Group already deleted!"
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM UserGroup WHERE GroupID=' + group_id)
    mysql.connection.commit()
    cur.close()
    return 'Group successfully deleted!'

def does_tuple_exist(table, pks, pk_vals):
    condition = ""
    # print(table)
    # print(pks)
    # print(pk_vals)
    if len(pks) == 1:
        condition = pks[0] + "=" + pk_vals[0]
    else:
        for pk, pk_val in zip(pks, pk_vals):
            condition += pk + "=" + pk_val
            print(condition)
            if pk == pks[len(pks) - 1]:
                break
            else:               
                condition += " and "
    query = "select * from {} where {}".format(table, condition)
    # print(query)
    cur = mysql.connection.cursor()
    cur.execute(query)
    rv = cur.fetchall()
    cur.close()
    if not rv:
        return False
    return True

def create_date_str(year, month, day):
    dd = str(day)
    mm = str(month)
    yyyy = str(year)
    return dd + '/' + mm + '/' + yyyy

def split_date(date):
    date_arr = date.split('/')
    date_arr_int = []
    for num_str in date_arr:
        date_arr_int.append(int(num_str))
    return date_arr_int

def hash_password(text):
    password = text
    h = hashlib.md5(password.encode())
    return h.hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
