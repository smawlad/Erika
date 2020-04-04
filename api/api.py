from flask import Flask, jsonify
from flask import request
from flask_mysqldb import MySQL
import hashlib
import unicodedata

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
        return "User doesn't exist!"
    query = "select UserID, BirthYear, BirthMonth, BirthDay, Bio from User where UserID =" + user_id
    rv = select_rows(query)
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
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User already deleted!"
    query = 'delete from User where UserID=' + user_id
    execute_and_commit(query)
    return 'User successfully deleted!'

@app.route('/api/v1/user/<user_id>/follow', methods=['POST'])
def follow_user(user_id):   
    input_json = request.get_json(force=True)
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "You can't follow a user who doesn't exist!"
    elif does_tuple_exist("UserFollowsUser", ["FollowerID", "FollowingID"], [repr(input_json['FollowerID']), user_id]):
        return "You already followed this user!"
    user_follows_user_tuple = (input_json['FollowerID'], user_id.replace("'",""))
    query = "insert into UserFollowsUser (FollowerID, FollowingID) VALUES {}".format(user_follows_user_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>/unfollow', methods=['POST'])
def unfollow_user(user_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "You can't unfollow a user that doesn't exist!"
    elif not does_tuple_exist("UserFollowsUser", ["FollowerID", "FollowingID"], [repr(input_json['FollowerID']), user_id]):
        return "You already unfollowed this user!"
    query = "delete from UserFollowsUser where FollowerID={} and FollowingID={}".format(repr(input_json['FollowerID']), user_id)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>/followers', methods=['GET'])
def get_followers(user_id):   
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!"
    query = "select FollowerID from UserFollowsUser where FollowingID =" + user_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        follower_id = rv
        content = {'FollowerID': follower_id}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/following', methods=['GET'])
def get_following(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!"
    query = "select FollowingID from UserFollowsUser where FollowerID =" + user_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        following_id = rv
        content = {'FollowingID': following_id}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/posts/follow', methods=['GET'])
def get_posts_by_user_that_you_follow(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!"
    input_json = request.get_json(force=True)
    pass

@app.route('/api/v1/user/<user_id>/posts', methods=['GET'])
def get_posts_by_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!"
    query = "select * from Post where CreatedBy =" + user_id
    rvs = select_rows(query)
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
        return "User doesn't exist!"
    elif not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post doesn't exist!"
    rv = select_rows("select * from Post where CreatedBy =" + user_id + " and " + " PostID =" + post_id)
    post_id, post_type, body, image_url, created_by, year_created, month_created, day_created = rv[0]
    date_created = create_date_str(year_created, month_created, day_created)
    payload = []
    content = {'PostID': post_id, 'Type': post_type, 'DateCreated': date_created, 'Body': body, 'ImageURL': image_url, 'CreatedBy:': created_by}
    payload.append(content)
    return jsonify(payload)

@app.route('/api/v1/topic/<topic_id>/posts', methods=['GET'])
def get_posts_in_topic(topic_id):
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "Topic doesn't exist!"
    query = "select * from Post where CreatedBy =" + user_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        post_id, post_type, body, image_url, created_by, year_created, month_created, day_created = rv
        date_created = create_date_str(year_created, month_created, day_created)
        content = {'PostID': post_id, 'Type': post_type, 'DateCreated': date_created, 'Body': body, 'ImageURL': image_url, 'CreatedBy:': created_by}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/topic/<topic_id>/posts/<post_id>', methods=['GET'])
def get_post_in_topic(topic_id, post_id):
    if not does_tuple_exist("Topic", ["Topic"], [topic_id]):
        return "Topic doesn't exist!"
    elif not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post doesn't exist!"
    input_json = request.get_json(force=True)
    pass

@app.route('/api/v1/topics', methods=['GET'])
def get_topics():
    query = "select * from Topic"
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        topic_id = rv
        content = {'TopicID': topic_id}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/topic/<topic_id>/follow', methods=['POST'])
def follow_topic(topic_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "You can't follow a topic that doesn't exist!"
    elif does_tuple_exist("UserFollowsTopic", ["TopicID", "UserID"], [topic_id, repr(input_json['UserID'])]):
        return "You are already following this topic!"
    user_follows_topic_tuple = (input_json['UserID'], topic_id.replace("'",""))
    query = "insert into UserFollowsTopic (UserID, TopicID) VALUES {}".format(user_follows_topic_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/topic/<topic_id>/unfollow', methods=['POST'])
def unfollow_topic(topic_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "You can't unfollow a topic that doesn't exist!"
    elif not does_tuple_exist("UserFollowsTopic", ["TopicID", "UserID"], [topic_id, repr(input_json['UserID'])]):
        return "You already unfollowed this topic!"
    query = "delete from UserFollowsTopic where UserID={} and TopicID={}".format(repr(input_json['UserID']), topic_id)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/post', methods=['POST'])
def create_post():
    input_json = request.get_json(force=True)
    split_date_created = split_date(input_json['DateCreated'])
    body = input_json['Body']
    topic_list = extract_topics_from_body(body)
    if not topic_list:
        return "A post must have at least 1 topic associated with it starting with a '#'! For e.g. #ILoveTopics." 
    for topic in topic_list:
        if not does_tuple_exist("Topic", ["TopicID"], [repr(topic)]):
            query1 = "insert into Topic (TopicID) VALUES ('{}')".format(topic)
            execute_and_commit(query1)
    post_tuple = (input_json['Type'], body, input_json['ImageURL'], input_json['CreatedBy'], split_date_created[2], split_date_created[1], split_date_created[0])
    query2 = "insert into Post (Type, Body, ImageURL, CreatedBy, YearCreated, MonthCreated, DayCreated) VALUES {}".format(post_tuple)
    execute_and_commit(query2)
    query3 = "select PostID from Post where".format(post_tuple)
    for topic in topic_list:
        post_topic_tuple = (post_id, topic)
        query4 = "insert into PostTopic (PostID, TopicID) VALUES {}".format(post_topic_tuple)
        execute_and_commit(query4)
    return 'OK'

@app.route('/api/v1/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post already deleted!"
    query = 'delete from Post where PostID=' + post_id
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/post/<post_id>/react', methods=['GET'])
def get_reactions_to_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "Post doesn't exist!"
    query = "select * from UserReactsToPost where PostID =" + post_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        user_id, post_id, reaction = rv
        content = {'UserID': user_id, 'PostID': post_id, 'Reaction': reaction}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/post/<post_id>/react', methods=['POST'])
def react_to_post(post_id):
    input_json = request.get_json(force=True)
    valid_reactions = ['Like', 'Dislike', 'Love', 'Funny', 'Sad', 'WTF']
    if input_json['Reaction'] not in valid_reactions:
        return 'Choose a valid reaction: ' + str(valid_reactions)
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "Post doesn't exist!"
    elif does_tuple_exist("UserReactsToPost", ["UserID", "PostID"], [repr(input_json['UserID']), post_id]):
        query = "update UserReactsToPost set Reaction='{}' where UserID='{}' and PostID='{}'".format(input_json['Reaction'], input_json['UserID'], post_id)
    else:
        user_react_tuple = (input_json['UserID'], post_id, input_json['Reaction'])
        query = "insert into UserReactsToPost (UserID, PostID, Reaction) VALUES {}".format(user_react_tuple)    
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/post/<post_id>/respond', methods=['POST'])
def respond_to_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "Post doesn't!"
    input_json = request.get_json(force=True)
    split_date_created = split_date(input_json['DateCreated'])
    body = input_json['Body']
    # topic_list = extract_topics_from_body(body)
    # if not topic_list:
    #     return "A post must have at least 1 topic associated with it starting with a '#'! For e.g. #ILoveTopics." 
    # for topic in topic_list:
    #     if not does_tuple_exist("Topic", ["TopicID"], [repr(topic)]):
    #         query = "insert into Topic (TopicID) VALUES ('{}')".format(topic)
    #         execute_and_commit(query)
    post_tuple = (input_json['Type'], body, input_json['ImageURL'], input_json['CreatedBy'], split_date_created[2], split_date_created[1], split_date_created[0])
    query = "insert into Post (Type, Body, ImageURL, CreatedBy, YearCreated, MonthCreated, DayCreated) VALUES {}".format(post_tuple)
    execute_and_commit(query)
    post_response_tuple = (post_id.replace("'",""), response_id)
    query = "insert into PostResponse (PostID, ResponseID) VALUES {}".format(post_response_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/group', methods=['GET'])
def get_groups():
    query = "select * from UserGroup"
    rvs = select_rows(query)
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
    group_tuple = (input_json['GroupID'], input_json['About'], input_json['CreatedBy'])
    user_join_group_tuple = (input_json['CreatedBy'], input_json['GroupID'])
    query1 = "insert into UserGroup (GroupID, About, CreatedBy) VALUES {}".format(group_tuple)
    query2 = "insert into UserJoinsGroup (UserID, GroupID) VALUES {}".format(user_join_group_tuple)
    execute_and_commit(query1)
    execute_and_commit(query2)
    return 'OK'

@app.route('/api/v1/group/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    if not does_tuple_exist("UserGroup", ["GroupID"], [group_id]):
        return "Group already deleted!"
    query = 'delete from UserGroup where GroupID=' + group_id
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/group/<group_id>/join', methods=['POST'])
def join_group(group_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("UserGroup", ["GroupID"], [group_id]):
        return "Group doesn't exist!"
    elif does_tuple_exist("UserJoinsGroup", ["UserID", "GroupID"], [repr(input_json['UserID']), group_id]):
        return "You already joined this group!"
    input_json = request.get_json(force=True)
    user_join_group_tuple = (input_json['UserID'], group_id.replace("'",""))
    query = "insert into UserJoinsGroup (UserID, GroupID) VALUES {}".format(user_join_group_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/group/<group_id>/leave', methods=['POST'])
def leave_group(group_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("UserGroup", ["GroupID"], [group_id]):
        return "Group doesn't exist!"
    elif not does_tuple_exist("UserJoinsGroup", ["UserID", "GroupID"], [repr(input_json['UserID']), group_id]):
        return "You already left this group!"
    input_json = request.get_json(force=True)
    query = "delete from UserJoinsGroup where UserID={} and GroupID={}".format(repr(input_json['UserID']), group_id)
    execute_and_commit(query)
    return 'OK'

def select_rows(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

def execute_and_commit(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

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
            #print(condition)
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

def extract_topics_from_body(body):
    topic_list = []
    for i in range(len(body)):
        if body[i] == '#':
            for j in range(i+1, len(body)):
                # this is such ugly code, need to refactor it
                topic_to_append = ""
                if j == len(body) - 1:
                    if unicodedata.category(body[j]).startswith('P'):
                        topic_to_append += body[i:j]
                    else:
                        topic_to_append += body[i:j+1]
                    break
                elif body[j] == ' ' or unicodedata.category(body[j]).startswith('P'):
                    topic_to_append += body[i:j]
                    break
            topic_list.append(topic_to_append)   
    return topic_list


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
