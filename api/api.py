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

@app.route('/api/v1/user/login', methods=['POST'])
def login():
    input_json = request.get_json(force=True)
    if not does_tuple_exist("User", ["UserID", "Password"], [repr(input_json['UserID']), repr(hash_password(input_json['Password']))]):
        return "Username or password is incorrect.", 400
    return 'OK'

@app.route('/api/v1/user/<user_id>', methods=['GET'])
def get_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
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
        return "User already exists!", 400
    split_birthday = split_date(input_json['Birthday'])
    user_tuple = (input_json['UserID'], hash_password(input_json['Password']), split_birthday[2], split_birthday[1], split_birthday[0], input_json['Bio'])
    query = "insert into User (UserID, Password, BirthYear, BirthMonth, BirthDay, Bio) VALUES {}".format(user_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User already deleted!", 400
    query = "delete from User where UserID=" + user_id
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>/follow', methods=['POST'])
def follow_user(user_id):   
    input_json = request.get_json(force=True)
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "You can't follow a user who doesn't exist!", 400
    elif does_tuple_exist("UserFollowsUser", ["FollowerID", "FollowingID"], [repr(input_json['FollowerID']), user_id]):
        return "You already followed this user!", 400
    user_follows_user_tuple = (input_json['FollowerID'], user_id.replace("'",""))
    query = "insert into UserFollowsUser (FollowerID, FollowingID) VALUES {}".format(user_follows_user_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>/unfollow', methods=['POST'])
def unfollow_user(user_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "You can't unfollow a user that doesn't exist!", 400
    elif not does_tuple_exist("UserFollowsUser", ["FollowerID", "FollowingID"], [repr(input_json['FollowerID']), user_id]):
        return "You already unfollowed this user!", 400
    query = "delete from UserFollowsUser where FollowerID={} and FollowingID={}".format(repr(input_json['FollowerID']), user_id)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>/followers', methods=['GET'])
def get_followers(user_id):   
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
    query = "select FollowerID from UserFollowsUser where FollowingID =" + user_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        follower_id = rv[0]
        content = {'FollowerID': follower_id}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/following', methods=['GET'])
def get_following(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
    query = "select FollowingID from UserFollowsUser where FollowerID =" + user_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        following_id = rv[0]
        content = {'FollowingID': following_id}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/topics', methods=['GET'])
def get_topics():
    query = "select * from Topic"
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        topic_id = rv[0]
        content = {'TopicID': topic_id}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/topics/following', methods=['GET'])
def get_topics_you_follow(user_id):
    query = "select TopicID from UserFollowsTopic where FollowerID=" + user_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        topic_id = rv[0]
        content = {'TopicID': topic_id}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/topic/<topic_id>/follow', methods=['POST'])
def follow_topic(topic_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "You can't follow a topic that doesn't exist!", 400
    elif does_tuple_exist("UserFollowsTopic", ["TopicID", "FollowerID"], [topic_id, repr(input_json['UserID'])]):
        return "You are already following this topic!", 400
    user_follows_topic_tuple = (input_json['UserID'], topic_id.replace("'",""))
    query = "insert into UserFollowsTopic (FollowerID, TopicID) VALUES {}".format(user_follows_topic_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/topic/<topic_id>/unfollow', methods=['POST'])
def unfollow_topic(topic_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "You can't unfollow a topic that doesn't exist!", 400
    elif not does_tuple_exist("UserFollowsTopic", ["TopicID", "FollowerID"], [topic_id, repr(input_json['UserID'])]):
        return "You already unfollowed this topic!", 400
    query = "delete from UserFollowsTopic where FollowerID={} and TopicID={}".format(repr(input_json['UserID']), topic_id)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/post/<post_id>', methods=['GET'])
def get_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "Post doesn't exist!", 400
    query = "select PostID, Type, Body, ImageURL, CreatedBy, YearCreated, MonthCreated, DayCreated, HourCreated, MinuteCreated, SecondCreated from Post where PostID =" + post_id
    rv = select_rows(query)
    post_id, post_type, body, image_url, created_by, year_created, month_created, day_created, hour_created, minute_created, second_created = rv[0]
    date_created = create_date_str(year_created, month_created, day_created)
    time_created = create_time_str(hour_created, minute_created, second_created)
    payload = []
    content = {'PostID': post_id, 'Type': post_type, 'Body': body, 'ImageURL': image_url, 'CreatedBy': created_by, 'DateCreated': date_created, 'TimeCreated':time_created}
    payload.append(content)
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/posts/lastpost', methods=['GET'])
def get_last_post_by_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
    query = "select max(PostID) from Post where CreatedBy =" + user_id
    rv = select_rows(query)
    post_id = rv[0][0]
    query = "select PostID, Type, Body, ImageURL, CreatedBy, YearCreated, MonthCreated, DayCreated, HourCreated, MinuteCreated, SecondCreated from Post where PostID =" + str(post_id)
    rv = select_rows(query)
    post_id, post_type, body, image_url, created_by, year_created, month_created, day_created, hour_created, minute_created, second_created = rv[0]
    date_created = create_date_str(year_created, month_created, day_created)
    time_created = create_time_str(hour_created, minute_created, second_created)
    payload = []
    content = {'PostID': post_id, 'Type': post_type, 'Body': body, 'ImageURL': image_url, 'CreatedBy': created_by, 'DateCreated': date_created, 'TimeCreated': time_created}
    payload.append(content)
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/posts/<post_id>', methods=['GET'])
def get_post_by_user(user_id, post_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
    elif not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post doesn't exist!", 400
    query = "select * from Post where CreatedBy={} and PostID={}".format(user_id, post_id)
    rv = select_rows(query)
    post_id, post_type, body, image_url, created_by, year_created, month_created, day_created, hour_created, minute_created, second_created = rv[0]
    date_created = create_date_str(year_created, month_created, day_created)
    time_created = create_time_str(hour_created, minute_created, second_created)
    payload = []
    content = {'PostID': post_id, 'Type': post_type, 'Body': body, 'ImageURL': image_url, 'CreatedBy': created_by, 'DateCreated': date_created, 'TimeCreated': time_created}
    payload.append(content)
    return jsonify(payload)
    
@app.route('/api/v1/user/<user_id>/posts', methods=['GET'])
def get_posts_by_user(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
    query = "select * from Post where CreatedBy =" + user_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        post_id, post_type, body, image_url, created_by, year_created, month_created, day_created, hour_created, minute_created, second_created = rv
        date_created = create_date_str(year_created, month_created, day_created)
        time_created = create_time_str(hour_created, minute_created, second_created)
        content = {'PostID': post_id, 'Type': post_type, 'Body': body, 'ImageURL': image_url, 'CreatedBy': created_by, 'DateCreated': date_created, 'TimeCreated': time_created}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/user/<user_id>/posts/follow', methods=['GET'])
def get_new_posts_by_user_that_you_follow(user_id):
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
    pass

@app.route('/api/v1/user/<user_id>/posts/lastread', methods=['POST'])
def update_last_read_post_by_user_you_follow(user_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "User doesn't exist!", 400
    elif not does_tuple_exist("UserFollowsUser", ["FollowerID", "FollowingID"], [repr(input_json['FollowerID']), user_id]):
        return "You don't follow this user!", 400
    query = "update UserFollowsUser set LastReadPost={} where FollowerID={} and FollowingID={}".format(input_json['PostID'], repr(input_json['FollowerID']), user_id)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/topic/<topic_id>/posts/<post_id>', methods=['GET'])
def get_post_in_topic(topic_id, post_id):
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "Topic doesn't exist!", 400
    elif not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post doesn't exist!", 400
    query = "select * from Post inner join PostTopic using (PostID) where TopicID={} and PostID={}".format(topic_id, post_id)
    rv = select_rows(query)
    post_id, post_type, body, image_url, created_by, year_created, month_created, day_created, hour_created, minute_created, second_created, topic_id = rv[0]
    date_created = create_date_str(year_created, month_created, day_created)
    time_created = create_time_str(hour_created, minute_created, second_created)
    payload = []
    content = {'PostID': post_id, 'Type': post_type, 'Body': body, 'ImageURL': image_url, 'CreatedBy': created_by, 'DateCreated': date_created, 'TimeCreated': time_created}
    payload.append(content)
    return jsonify(payload)

@app.route('/api/v1/topic/<topic_id>/posts', methods=['GET'])
def get_posts_in_topic(topic_id):
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "Topic doesn't exist!", 400
    query = "select * from Post inner join PostTopic using (PostID) where TopicID=" + topic_id
    rvs = select_rows(query)
    payload = []
    content = {}
    for rv in rvs:
        post_id, post_type, body, image_url, created_by, year_created, month_created, day_created, hour_created, minute_created, second_created, topic_id = rv
        date_created = create_date_str(year_created, month_created, day_created)
        time_created = create_time_str(hour_created, minute_created, second_created)
        content = {'PostID': post_id, 'Type': post_type, 'Body': body, 'ImageURL': image_url, 'CreatedBy': created_by, 'DateCreated': date_created, 'TimeCreated': time_created}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/v1/topic/<topic_id>/posts/following', methods=['GET'])
def get_new_posts_in_topic_that_you_follow(topic_id):
    if not does_tuple_exist("Topic", ["Topic"], [topic_id]):
        return "Topic doesn't exist!", 400
    pass

@app.route('/api/v1/topic/<topic_id>/posts/lastread', methods=['POST'])
def update_last_read_post_in_topic_you_follow(topic_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("Topic", ["TopicID"], [topic_id]):
        return "Topic doesn't exist!", 400
    elif not does_tuple_exist("UserFollowsTopic", ["FollowerID", "TopicID"], [repr(input_json['UserID']), topic_id]):
        return "You don't follow this topic!", 400
    query = "update UserFollowsTopic set LastReadPost={} where FollowerID={} and TopicID={}".format(input_json['PostID'], repr(input_json['UserID']), topic_id)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/post', methods=['POST'])
def create_post():
    input_json = request.get_json(force=True)
    split_date_created = split_date(input_json['DateCreated'])
    split_time_created = split_time(input_json['TimeCreated'])
    body = input_json['Body']
    topic_list = extract_topics_from_body(body)
    # fill in topic table
    if not topic_list:
        return "A post must have at least 1 topic associated with it starting with a '#'! For e.g. #ILoveTopics.", 400 
    for topic in topic_list:
        if not does_tuple_exist("Topic", ["TopicID"], [repr(topic)]):
            query = "insert into Topic (TopicID) VALUES ('{}')".format(topic)
            execute_and_commit(query)
        else:
            break
    # fill in post table
    post_tuple = (input_json['Type'], body, input_json['ImageURL'], input_json['CreatedBy'], split_date_created[2], split_date_created[1], split_date_created[0], split_time_created[0], split_time_created[1], split_time_created[2])
    query = "insert into Post (Type, Body, ImageURL, CreatedBy, YearCreated, MonthCreated, DayCreated, HourCreated, MinuteCreated, SecondCreated) VALUES {}".format(post_tuple)
    execute_and_commit(query)
    # fill in table that associates topics with posts, the most recent post is the one just created
    query = "select max(PostID) from Post"
    rv = select_rows(query)
    for topic in topic_list:
        post_topic_tuple = (rv[0][0], topic)
        query = "insert into PostTopic (PostID, TopicID) VALUES {}".format(post_topic_tuple)
        execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [repr(post_id)]):
        return "Post already deleted!", 400
    query = 'delete from Post where PostID=' + post_id
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/post/<post_id>/react', methods=['GET'])
def get_reactions_to_post(post_id):
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "Post doesn't exist!", 400
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
        return 'Choose a valid reaction: ' + str(valid_reactions), 400
    if not does_tuple_exist("Post", ["PostID"], [post_id]):
        return "Post doesn't exist!", 400
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
        return "Post doesn't exist!", 400
    input_json = request.get_json(force=True)
    split_date_created = split_date(input_json['DateCreated'])
    split_time_created = split_time(input_json['TimeCreated'])
    body = input_json['Body']
    post_tuple = (input_json['Type'], body, input_json['ImageURL'], input_json['CreatedBy'], split_date_created[2], split_date_created[1], split_date_created[0], split_time_created[0], split_time_created[1], split_time_created[2])
    query = "insert into Post (Type, Body, ImageURL, CreatedBy, YearCreated, MonthCreated, DayCreated, HourCreated, MinuteCreated, SecondCreated) VALUES {}".format(post_tuple)
    execute_and_commit(query)
    # fill in table that associates topics with posts, the most recent post is the one just created, responses inherit the topic of their parent
    query = "select max(PostID) from Post"
    rv1 = select_rows(query)
    query = "select TopicID from PostTopic where PostID=" + post_id
    rv2 = select_rows(query)
    for rv in rv2:
        post_topic_tuple = (rv1[0][0], rv[0])
        query = "insert into PostTopic (PostID, TopicID) VALUES {}".format(post_topic_tuple)
        execute_and_commit(query)
    # fill in response table
    post_response_tuple = (post_id, rv1[0][0])
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
        return "Group already exists!", 400
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
        return "Group already deleted!", 400
    query = 'delete from UserGroup where GroupID=' + group_id
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/group/<group_id>/join', methods=['POST'])
def join_group(group_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("UserGroup", ["GroupID"], [group_id]):
        return "Group doesn't exist!", 400
    elif does_tuple_exist("UserJoinsGroup", ["UserID", "GroupID"], [repr(input_json['UserID']), group_id]):
        return "You already joined this group!", 400
    input_json = request.get_json(force=True)
    user_join_group_tuple = (input_json['UserID'], group_id.replace("'",""))
    query = "insert into UserJoinsGroup (UserID, GroupID) VALUES {}".format(user_join_group_tuple)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/group/<group_id>/leave', methods=['POST'])
def leave_group(group_id):
    input_json = request.get_json(force=True)
    if not does_tuple_exist("UserGroup", ["GroupID"], [group_id]):
        return "Group doesn't exist!", 400
    elif not does_tuple_exist("UserJoinsGroup", ["UserID", "GroupID"], [repr(input_json['UserID']), group_id]):
        return "You already left this group!", 400
    input_json = request.get_json(force=True)
    query = "delete from UserJoinsGroup where UserID={} and GroupID={}".format(repr(input_json['UserID']), group_id)
    execute_and_commit(query)
    return 'OK'

@app.route('/api/v1/user/<user_id>/message', methods=['POST'])
def message_user(user_id):   
    input_json = request.get_json(force=True)
    if not does_tuple_exist("User", ["UserID"], [user_id]):
        return "You can't message a user who doesn't exist!", 400
    elif not does_tuple_exist("UserFollowsUser", ["FollowerID", "FollowingID"], [repr(input_json['SenderID']), user_id]):
        return "You can't message a user you don't follow!", 400

    # create a conversation between users if it doesn't already exist
    if does_tuple_exist("Conversation", ["User1", "User2"], [repr(input_json['SenderID']), user_id]) \
        or does_tuple_exist("Conversation", ["User1", "User2"], [user_id, repr(input_json['SenderID'])]):
        query = "select ConversationID from Conversation where User1={} and User2={} or User1={} and User2={}".format(user_id, repr(input_json['SenderID']), repr(input_json['SenderID']), user_id)
    else:
        conversation_tuple = (input_json['SenderID'], user_id.replace("'",""))
        query = "insert into Conversation (User1, User2) VALUES {}".format(conversation_tuple)
        execute_and_commit(query)
        query = "select max(ConversationID) from Conversation"

    rv = select_rows(query)
    conversation_id = rv[0][0]
    # now send the actual message
    split_date_created = split_date(input_json['DateSent'])
    split_time_created = split_time(input_json['TimeSent'])
    message_tuple = (conversation_id, input_json['SenderID'], input_json['Body'], split_date_created[2], split_date_created[1], split_date_created[0], split_time_created[0], split_time_created[1], split_time_created[2])
    query = '''insert into Message (ConversationID, SenderID, Body, YearSent, MonthSent, DaySent, HourSent, MinuteSent, SecondSent) VALUES {}'''.format(message_tuple)
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

def does_tuple_exist(table, keys, key_vals):
    condition = ""
    if len(keys) == 1:
        condition = keys[0] + "=" + key_vals[0]
    else:
        for key, key_val in zip(keys, key_vals):
            condition += key + "=" + key_val
            if key == keys[len(keys) - 1]:
                break
            else:               
                condition += " and "
    query = "select * from {} where {}".format(table, condition)
    rv = select_rows(query)
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
    return str(day) + '/' + str(month) + '/' + str(year)

def split_date(date):
    date_arr = date.split('/')
    date_arr_int = []
    for num_str in date_arr:
        date_arr_int.append(int(num_str))
    return date_arr_int

def create_time_str(hour, minute, second):
    return str(hour) + ':' + str(minute) + ':' + str(second)

def split_time(time):
    time_arr = time.split(':')
    time_arr_int = []
    for num_str in time_arr:
        time_arr_int.append(int(num_str))
    return time_arr_int

def hash_password(text):
    password = text
    h = hashlib.md5(password.encode())
    return h.hexdigest()

if __name__ == '__main__':
    app.run(debug=True)
