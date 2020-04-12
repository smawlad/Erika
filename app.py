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
        Usage:         login {username}
        Description:   Log into Erika.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. login {username}.")
            return
        username = parameters[0] 
        password = getpass("Enter your password: ") 
        payload = {'UserID':username, 'Password':password}
        req = requests.post('http://127.0.0.1:5000/api/v1/user/login', json=payload)
        if req.status_code == 200:
            self.login_status = True
            self.user_id = username
            print("Logged in as {}.".format(username))
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
        Usage:         create_account {username}
        Description:   Create an account.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. create_account {username}.")
            return

        username = parameters[0] 
        if not username.isalnum():
            print("Only alphanumeric characters are allowed in username!") 
            return

        password = getpass("Enter a password: ") 
        if not password.isalnum():
            print("Only alphanumeric characters are allowed in username!") 
            return

        birthday = input("Enter your birthdate (dd/mm/yyyy): ") 
        if not self.isDateValid(birthday):
            print("Please enter a valid date!")
            return

        bio = input("Enter a short bio: ")

        payload = {'UserID':username, 'Password':password, 'Birthday':birthday, 'Bio':bio}
        req = requests.post('http://127.0.0.1:5000/api/v1/user', json=payload)
        if req.status_code == 200:
            print("You can now log in as {}".format(username))
        else:
            print(req.text)
    
    def do_delete_account(self, args):
        """
        Usage:         delete_account {username}
        Description:   Delete your account.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. delete_account {username}.")
            return
        username = parameters[0]
        if self.user_id != username:
            print("Log in to delete your account!")
        else:
            req = requests.delete('http://127.0.0.1:5000/api/v1/user/{}'.format(repr(username)))
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
                print("Username: {}\nBirthday: {}\nBio: {}".format(user_info[0]['UserID'], user_info[0]['Birthday'], user_info[0]['Bio']))
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
        Usage:         show_user {username}
        Description:   Show a user's information.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. show_user {username}.")
            return
        username = parameters[0]
        req = requests.get('http://127.0.0.1:5000/api/v1/user/{}'.format(repr(username)))
        if req.status_code == 200:
            user_info = req.json()
            print("----------------------------------------------------------------------------------------------------------------------------")
            print("Username: {}\nBirthday: {}\nBio: {}".format(user_info[0]['UserID'], user_info[0]['Birthday'], user_info[0]['Bio']))
            print("----------------------------------------------------------------------------------------------------------------------------")
        else:
            print(req.text)
    
    def do_show_user_following(self, args):
        """
        Usage:         show_user_following {username}
        Description:   Show who a user follows.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. show_user_following {username}.")
            return
        username = parameters[0]
        req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/following'.format(repr(username)))
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
        Usage:         show_user_followers {username}
        Description:   Show a user's followers.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. show_user_followers {username}.")
            return
        username = parameters[0]
        req = requests.get('http://127.0.0.1:5000/api/v1/user/{}/followers'.format(repr(username)))
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
        Usage:         follow_user {username}
        Description:   Follow a user.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. follow_user {username}.")
            return
        elif self.user_id != None:
            username = parameters[0]
            payload = {'FollowerID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/user/{}/follow'.format(repr(username)), json=payload)
            if req.status_code == 200:
                print("You followed {}!".format(username))
            else:
                print(req.text)
        else:
            print("Log in to follow a user!")
    
    def do_unfollow_user(self, args):
        """
        Usage:         unfollow_user {username}
        Description:   Unfollow a user.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a username. e.g. unfollow_user {username}.")
            return
        elif self.user_id != None:
            username = parameters[0]
            payload = {'FollowerID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/user/{}/unfollow'.format(repr(username)), json=payload)
            if req.status_code == 200:
                print("You unfollowed {}!".format(username))
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
        Usage:         follow_topic {topicname}
        Description:   Follow a topic.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a topicname. e.g. follow_topic {topicname}.")
            return
        elif self.user_id != None:
            topicname = parameters[0]
            payload = {'UserID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/topic/{}/follow'.format(repr(topicname.replace('#','%23'))), json=payload)
            if req.status_code == 200:
                print("You followed {}!".format(topicname))
            else:
                print(req.text)
        else:
            print("Log in to follow a topic!")
    
    def do_unfollow_topic(self, args):
        """
        Usage:         unfollow_topic {topicname}
        Description:   Unfollow a topic.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a topicname. e.g. unfollow_topic {topicname}.")
            return
        elif self.user_id != None:
            topicname = parameters[0]
            payload = {'UserID':self.user_id}
            req = requests.post('http://127.0.0.1:5000/api/v1/topic/{}/unfollow'.format(repr(topicname.replace('#','%23'))), json=payload)
            if req.status_code == 200:
                print("You unfollowed {}!".format(topicname))
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
            print("Enter a post type! e.g. create_post text")
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
    
    def do_respond_to_post(self, args):
        """
        Usage:         respond_to_post {postid}
        Description:   Respond to a post.
        """
        # implement this
        pass
    
    def do_open_link(self, args):
        """
        Usage:         open_link {link}
        Description:   Open a link in your browser.
        """
        parameters = args.split()
        if len(parameters) != 1:
            print("Provide a link to open. e.g. open_link {link}.")
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