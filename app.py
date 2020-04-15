from cmd import Cmd
from getpass import getpass
import requests
from datetime import datetime
from webbrowser import open

class Erika(Cmd):
    prompt = 'erika> '
    intro = "Welcome to Erika, a simple social command line social network! Type help for a list of commands."

    def __init__(self):
        super().__init__()
        self.user_id = None
        self.login_status = False
    
    def do_login(self, args):
        """
        Usage:         login {userid}
        Description:   Log into Erika.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid. e.g. login {userid}.")
            return
        userid = parameters[0] 
        password = getpass("Enter your password: ") 
        payload = {'UserID':userid, 'Password':password}
        req = requests.post('http://127.0.0.1:5000/api/v1/user/login', json=payload)
        if req.status_code == 200:
            self.login_status = True
            self.user_id = userid
            print("Logged in as {}.".format(userid))
        else:
            print(req.text)
            
    def do_logout(self, args):
        """
        Usage:         logout
        Description:   Logout of current user.
        """
        if len(args) != 0:
            print("This command takes no arguments!")
            return
        self.user_id = None
        self.login_status = False
        print("Logged out of current user.")
    
    def do_exit(self, args):
        """
        Usage:         exit
        Description:   Exit Erika.
        """
        if len(args) != 0:
            print("This command takes no arguments!")
            return
        print("See you later!")
        return True

    def do_create_account(self, args):
        """
        Usage:         create_account {userid}
        Description:   Create an account.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid. e.g. create_account {userid}.")
            return

        userid = parameters[0] 
        if not userid.isalnum():
            print("Only alphanumeric characters are allowed in userid!") 
            return

        password = getpass("Enter a password: ") 
        if not password.isalnum():
            print("Only alphanumeric characters are allowed in userid!") 
            return

        birthday = input("Enter your birthdate (dd/mm/yyyy): ") 
        if not self.isDateValid(birthday):
            print("Please enter a valid date!")
            return

        bio = input("Enter a short bio: ")

        payload = {'UserID':userid, 'Password':password, 'Birthday':birthday, 'Bio':bio}
        req = requests.post('http://127.0.0.1:5000/api/v1/user', json=payload)
        if req.status_code == 200:
            print("You can now log in as {}".format(userid))
        else:
            print(req.text)
    
    def do_delete_account(self, args):
        """
        Usage:         delete_account {userid}
        Description:   Delete your account.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid e.g. delete_account {userid}.")
            return
        userid = parameters[0]
        if self.user_id != userid:
            print("Log in to delete your account!")
        else:
            req = requests.delete('http://127.0.0.1:5000/api/v1/user/{}'.format(repr(userid)))
            if req.status_code == 200:
                self.login_status = False
                self.user_id = None
            else:
                print(req.text)
    
    def do_show_me(self, args):
        """
        Usage:         show_me 
        Description:   Show your information.
        """
        if len(args) != 0:
            print("This command takes no arguments!")
            return
        elif self.user_id != None:
            req = requests.get('http://127.0.0.1:5000/api/v1/user/{}'.format(repr(self.user_id)))
            if req.status_code == 200:
                user_info = req.json()
                print("----------------------------------------------------------------------------------------------------------------------------")
                print("UserID: {}\nBirthday: {}\nBio: {}".format(user_info[0]['UserID'], user_info[0]['Birthday'], user_info[0]['Bio']))
                print("----------------------------------------------------------------------------------------------------------------------------")
            else:
                print(req.text)
        else:
            print("Log in to view your information!")
    
    def do_show_my_following(self, args):
        """
        Usage:         show_my_following 
        Description:   Show who you follow.
        """
        if len(args) != 0:
            print("This command takes no arguments!")
            return
        elif self.user_id != None:
            req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/following'.format(repr(self.user_id)))
            if req.status_code == 200:
                user_info = req.json()
                print("-------------------------------------------------Following------------------------------------------------------------------")
                for user in user_info:
                    print(user['FollowingID'])
                print("----------------------------------------------------------------------------------------------------------------------------")
            else:
                print(req.text)
        else:
            print("Log in to view your information!")

    def do_show_my_followers(self, args):
        """
        Usage:         show_my_followers 
        Description:   Show your followers.
        """
        if len(args) != 0:
            print("This command takes no arguments!")
            return
        elif self.user_id != None:
            req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/followers'.format(repr(self.user_id)))
            if req.status_code == 200:
                user_info = req.json()
                print("-------------------------------------------------Followers------------------------------------------------------------------")
                for user in user_info:
                    print(user['FollowerID'])
                print("----------------------------------------------------------------------------------------------------------------------------")
            else:
                print(req.text)
        else:
            print("Log in to view your information!")
    
    def do_show_user(self, args):
        """
        Usage:         show_user {userid}
        Description:   Show a user's information.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid. e.g. show_user {userid}.")
            return
        userid = parameters[0]
        req = requests.get('http://127.0.0.1:5000/api/v1/user/{}'.format(repr(userid)))
        if req.status_code == 200:
            user_info = req.json()
            print("----------------------------------------------------------------------------------------------------------------------------")
            print("UserID: {}\nBirthday: {}\nBio: {}".format(user_info[0]['UserID'], user_info[0]['Birthday'], user_info[0]['Bio']))
            print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print(req.text)
    
    def do_show_user_following(self, args):
        """
        Usage:         show_user_following {userid}
        Description:   Show who a user follows.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid e.g. show_user_following {userid}.")
            return
        userid = parameters[0]
        req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/following'.format(repr(userid)))
        if req.status_code == 200:
            user_info = req.json()
            print("-------------------------------------------------Following------------------------------------------------------------------")
            for user in user_info:
                print(user['FollowingID'])
            print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print(req.text)

    def do_show_user_followers(self, args):
        """
        Usage:         show_user_followers {userid}
        Description:   Show a user's followers.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid e.g. show_user_followers {userid}.")
            return
        userid = parameters[0]
        req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/followers'.format(repr(userid)))
        if req.status_code == 200:
            user_info = req.json()
            print("-------------------------------------------------Followers------------------------------------------------------------------")
            for user in user_info:
                print(user['FollowerID'])
            print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print(req.text)
    
    def do_follow_user(self, args):
        """
        Usage:         follow_user {userid}
        Description:   Follow a user.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid e.g. follow_user {userid}.")
            return
        elif self.user_id != None:
            userid = parameters[0]
            payload = {'FollowerID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/user/{}/follow'.format(repr(userid)), json=payload)
            if req.status_code == 200:
                print("You followed {}!".format(userid))
            else:
                print(req.text)
        else:
            print("Log in to follow a user!")
    
    def do_unfollow_user(self, args):
        """
        Usage:         unfollow_user {userid}
        Description:   Unfollow a user.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a userid e.g. unfollow_user {userid}.")
            return
        elif self.user_id != None:
            userid = parameters[0]
            payload = {'FollowerID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/user/{}/unfollow'.format(repr(userid)), json=payload)
            if req.status_code == 200:
                print("You unfollowed {}!".format(userid))
            else:
                print(req.text)
        else:
            print("Log in to unfollow a user!")
    
    def do_show_topics(self, args):
        """
        Usage:         show_topics
        Description:   Show all topics.
        """
        if len(args) != 0:
            print("This command takes no arguments!")
            return
        req = requests.get('http://127.0.0.1:5000/api/v1/topics')
        if req.status_code == 200:
            topic_info = req.json()
            print("---------------------------------------------------Topics-------------------------------------------------------------------")
            for topic in topic_info:
                print(topic['TopicID'])
            print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print(req.text)
    
    def do_show_topics_following(self, args):
        """
        Usage:         show_topics_following
        Description:   Show all topics you follow.
        """
        if len(args) != 0:
            print("This command takes no arguments!")
            return
        elif self.user_id != None:
            req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/topics/following'.format(repr(self.user_id)))
            if req.status_code == 200:
                topic_info = req.json()
                print("-------------------------------------------------Following------------------------------------------------------------------")
                for topic in topic_info:
                    print(topic['TopicID'])
                print("----------------------------------------------------------------------------------------------------------------------------")
            else:
                print(req.text)
        else:
            print("Log in to view your information!")

    def do_follow_topic(self, args):
        """
        Usage:         follow_topic {topicid}
        Description:   Follow a topic.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a topicid e.g. follow_topic {topicid}.")
            return
        elif self.user_id != None:
            topicid = parameters[0]
            payload = {'UserID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/topic/{}/follow'.format(repr(topicid.replace('#','%23'))), json=payload)
            if req.status_code == 200:
                print("You followed {}!".format(topicid))
            else:
                print(req.text)
        else:
            print("Log in to follow a topic!")
    
    def do_unfollow_topic(self, args):
        """
        Usage:         unfollow_topic {topicid}
        Description:   Unfollow a topic.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a topicid e.g. unfollow_topic {topicid}.")
            return
        elif self.user_id != None:
            topicid = parameters[0]
            payload = {'UserID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/topic/{}/unfollow'.format(repr(topicid.replace('#','%23'))), json=payload)
            if req.status_code == 200:
                print("You unfollowed {}!".format(topicid))
            else:
                print(req.text)
        else:
            print("Log in to unfollow a topic!")
    
    def do_create_post(self, args):
        """
        Usage:         create_post text|image|both
        Description:   Create a new post. Valid post types are text, image, both.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Enter a post type e.g. create_post text")
            return
        type_of_post = parameters[0]
        if type_of_post.lower() not in ['text', 'image', 'both']:
            print("Valid post types are text, image, both.")
            return
        elif self.user_id != None:
            body = ''
            image_url = ''
            if type_of_post.lower() == 'image' or type_of_post.lower() == 'both':
                image_url = input("Provide a URL to your image: ")
            if type_of_post.lower() == 'text' or type_of_post.lower() == 'both':
                body = input("Provide a post body: ")
            datetime_arr = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(' ')
            payload = {'Type':type_of_post, 'Body':body, 'ImageURL':image_url, 'CreatedBy':self.user_id, 'DateCreated':datetime_arr[0], 'TimeCreated':datetime_arr[1]}
            req = requests.post('http://127.0.0.1:5000/api/v1/post', json=payload)
            if req.status_code == 200:
                req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/posts/lastpost'.format(repr(self.user_id)))
                post_info = req.json()
                print("----------------------------------------------------Post--------------------------------------------------------------------")
                if type_of_post.lower() == 'image' or type_of_post.lower() == 'both':
                    print("PostID: {}\nBody: {}\nImageURL: {}\nCreatedBy: {}\nCreatedOn: {}".format(post_info[0]['PostID'], post_info[0]['Body'], post_info[0]['ImageURL'], post_info[0]['CreatedBy'], post_info[0]['DateCreated'] + ' ' + post_info[0]['TimeCreated']))
                else:
                    print("PostID: {}\nBody: {}\nCreatedBy: {}\nCreatedOn: {}".format(post_info[0]['PostID'], post_info[0]['Body'], post_info[0]['CreatedBy'], post_info[0]['DateCreated'] + ' ' + post_info[0]['TimeCreated']))
                print("----------------------------------------------------------------------------------------------------------------------------")
            else:
                print(req.text)
        else:
            print("Log in to create a post!")

    def do_delete_post(self, args):
        """
        Usage:         delete_post {postid}
        Description:   Delete a post. 
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Enter a postid e.g. delete_post {postid}")
            return
        post_id = parameters[0]
        if self.user_id != None:
            req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/posts/{}'.format(repr(self.user_id), post_id))
            if req.status_code == 200:
                req = requests.delete('http://127.0.0.1:5000/api/v1/post/{}'.format(post_id))
                print("Post deleted!")
            else:
                print(req.text)
        else:
            print("You must be logged in to delete a post!")
            return
    
    def do_respond_post(self, args):
        """
        Usage:         respond_post {postid} text|image|both
        Description:   Respond to a post with text, image, or both.
        """
        parameters = args.split()
        if len(parameters) != 2:
            print("Provide a postid and a response type e.g. respond_post {postid} text|image|both.")
            return
        elif self.user_id != None:
            post_id = parameters[0]
            type_of_post = parameters[1]
            if type_of_post.lower() not in ['text', 'image', 'both']:
                print("Valid post types are text, image, both.")
                return
            body = ''
            image_url = ''
            if type_of_post.lower() == 'image' or type_of_post.lower() == 'both':
                image_url = input("Provide a URL to your image: ")
            if type_of_post.lower() == 'text' or type_of_post.lower() == 'both':
                body = input("Provide a post body: ")
            datetime_arr = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(' ')
            payload = {'Type':type_of_post, 'Body':body, 'ImageURL':image_url, 'CreatedBy':self.user_id, 'DateCreated':datetime_arr[0], 'TimeCreated':datetime_arr[1]}
            req = requests.post('http://127.0.0.1:5000/api/v1/post/{}/respond'.format(post_id), json=payload)
            if req.status_code == 200:
                req = requests.get('http://127.0.0.1:5000/api/v1/post/{}'.format(post_id))
                post_info = req.json()

                print("----------------------------------------------------Post--------------------------------------------------------------------")
                if post_info[0]['Type'].lower() == 'image' or post_info[0]['Type'].lower() == 'both':
                    print("PostID: {}\nBody: {}\nImageURL: {}\nCreatedBy: {}\nCreatedOn: {}".format(post_info[0]['PostID'], post_info[0]['Body'], post_info[0]['ImageURL'], post_info[0]['CreatedBy'], post_info[0]['DateCreated'] + ' ' + post_info[0]['TimeCreated']))
                else:
                    print("PostID: {}\nBody: {}\nCreatedBy: {}\nCreatedOn: {}".format(post_info[0]['PostID'], post_info[0]['Body'], post_info[0]['CreatedBy'], post_info[0]['DateCreated'] + ' ' + post_info[0]['TimeCreated']))
                                
                req = requests.get('http://127.0.0.1:5000/api/v1/post/{}/responses'.format(post_id))
                response_info = req.json()
                print("-------------------------------------------------Responses------------------------------------------------------------------")
                for response in response_info:
                    if type_of_post.lower() == 'image' or type_of_post.lower() == 'both':
                        print("ResponseID: {}\nBody: {}\nImageURL: {}\nCreatedBy: {}\nCreatedOn: {}".format(response['ResponseID'], response['Body'], response['ImageURL'], response['CreatedBy'], response['DateCreated'] + ' ' + response['TimeCreated']))
                    else:
                        print("ResponseID: {}\nBody: {}\nCreatedBy: {}\nCreatedOn: {}".format(response['ResponseID'], response['Body'], response['CreatedBy'], response['DateCreated'] + ' ' + response['TimeCreated']))
                    print("----------------------------------------------------------------------------------------------------------------------------")
            else:
                print(req.text)
        else:
            print("Log in to respond to a post!")

    def do_show_my_posts(self, args):
        """
        Usage:         show_my_posts
        Description:   Shows all your own posts. 
        """
        if self.user_id != None:
            req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/posts'.format(repr(self.user_id)))
            post_info = req.json()
            if len(post_info) == 0:
                print("You have no posts!")
                return
            print("------------------------------------------------------Posts----------------------------------------------------------------")
            for post in post_info:
                if post['Type'].lower() == 'image' or post['Type'].lower() == 'both':
                    print("PostID: {}\nBody: {}\nImageURL: {}\nCreatedBy: {}\nCreatedOn: {}".format(post['PostID'], post['Body'], post['ImageURL'], post['CreatedBy'], post['DateCreated'] + ' ' + post['TimeCreated']))
                else:
                    print("PostID: {}\nBody: {}\nCreatedBy: {}\nCreatedOn: {}".format(post['PostID'], post['Body'], post['CreatedBy'], post['DateCreated'] + ' ' + post['TimeCreated']))
                print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print("Log in to view your posts!")
            return
    
    def do_show_post_user(self, args):
        """
        Usage:         show_post_user {userid} all|new
        Description:   Shows posts by a user. Viewing new posts requires following user.
        """
        parameters = args.split()
        if len(parameters) != 2:
            print("Provide a userid and a valid view option e.g. show_post_user {userid} all|new.")
            return
        user_id = parameters[0]
        view_option = parameters[1]
        if view_option.lower() not in ['all', 'new']:
            print("Valid view options are all, new.")
            return
        elif view_option.lower() == 'all':
            if self.user_id == None:
                req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/posts'.format(repr(user_id)))
            elif self.user_id == user_id:
                return self.do_show_my_posts(args)
            else:
                payload = {'FollowerID':self.user_id}
                req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/posts'.format(repr(user_id)), json=payload)
        else:
            if self.user_id != None:
                payload = {'FollowerID':self.user_id}
                req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/posts/unread'.format(repr(user_id)), json=payload)
            else:
                print("Log in to view new posts!")
                return

        if req.status_code == 200:
            post_info = req.json()
            if len(post_info) == 0:
                print("No new posts!")
                return
            print("----------------------------------------------------{} Posts---------------------------------------------------------------".format(view_option.capitalize()))
            for post in post_info:
                if post['Type'].lower() == 'image' or post['Type'].lower() == 'both':
                    print("PostID: {}\nBody: {}\nImageURL: {}\nCreatedBy: {}\nCreatedOn: {}".format(post['PostID'], post['Body'], post['ImageURL'], post['CreatedBy'], post['DateCreated'] + ' ' + post['TimeCreated']))
                else:
                    print("PostID: {}\nBody: {}\nCreatedBy: {}\nCreatedOn: {}".format(post['PostID'], post['Body'], post['CreatedBy'], post['DateCreated'] + ' ' + post['TimeCreated']))
                print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print(req.text)

    
    def do_show_post_topic(self, args):
        """
        Usage:         show_post_topic {topicid} all|new
        Description:   Shows posts in a topic. Viewing new posts requires following topic.
        """
        parameters = args.split()
        if len(parameters) != 2:
            print("Provide a topicid and a valid view option e.g. show_post_topic {topicid} all|new.")
            return

        topic_id = parameters[0]
        view_option = parameters[1]
        if view_option.lower() not in ['all', 'new']:
            print("Valid view options are all, new.")
            return
        elif view_option.lower() == 'all':
            if self.user_id == None:
                req = requests.get('http://127.0.0.1:5000/api/v1/topic/{}/posts'.format(repr(topic_id.replace('#','%23'))))
            else:
                payload = {'FollowerID':self.user_id}
                req = requests.get('http://127.0.0.1:5000/api/v1/topic/{}/posts'.format(repr(topic_id.replace('#','%23'))), json=payload)
        else:
            if self.user_id != None:
                payload = {'FollowerID':self.user_id}
                req = requests.get('http://127.0.0.1:5000/api/v1/topic/{}/posts/unread'.format(repr(topic_id.replace('#','%23'))), json=payload)
            else:
                print("Log in to view new posts!")
                return

        if req.status_code == 200:
            post_info = req.json()
            if len(post_info) == 0:
                print("No new posts!")
                return
            print("----------------------------------------------------{} Posts---------------------------------------------------------------".format(view_option.capitalize()))
            for post in post_info:
                if post['Type'].lower() == 'image' or post['Type'].lower() == 'both':
                    print("PostID: {}\nBody: {}\nImageURL: {}\nCreatedBy: {}\nCreatedOn: {}".format(post['PostID'], post['Body'], post['ImageURL'], post['CreatedBy'], post['DateCreated'] + ' ' + post['TimeCreated']))
                else:
                    print("PostID: {}\nBody: {}\nCreatedBy: {}\nCreatedOn: {}".format(post['PostID'], post['Body'], post['CreatedBy'], post['DateCreated'] + ' ' + post['TimeCreated']))
                print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print(req.text)
    
    def do_open_link(self, args):
        """
        Usage:         open_link {link}
        Description:   Open a link in your browser.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a link to open e.g. open_link {link}.")
            return
        else:
            open(parameters[0])
    
    def isDateValid(self, date):
        day, month, year = date.split('/')
        try:
            datetime(int(year), int(month), int(day))
        except ValueError:
            return False
        return True
    
    def emptyline(self):
        pass

if __name__ == '__main__':
    Erika().cmdloop()