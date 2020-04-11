from cmd import Cmd
from getpass import getpass
import requests

class Erika(Cmd):
    prompt = 'erika> '
    intro = "Welcome to Erika, a simple social command line social network! Type ? for a list of commands."

    def __init__(self):
        super().__init__()
        self.user_id = ""
        self.login_status = False
        self.connection = None

    def do_create_account(self, args):
        """
        Usage:         create_account {username}
        Description:   Create an account on Erika.
        """
        parameters = args.split()
        username = parameters[0] # add error checking, no special chars allowed only alphanum
        password = getpass("Enter a password: ") # add error checking, no special chars allowed only alphanum
        birthday = input("Enter your birthdate (dd/mm/yyyy): ") # need to implement error checking on date
        bio = input("Enter a short bio: ")
        payload = {'UserID':username, 'Password':password, 'Birthday':birthday, 'Bio':bio}
        req = requests.post('http://127.0.0.1:5000/api/v1/user', json=payload)
        if req.text == 'OK':
            print("You can now log in as {}".format(username))
        else:
            print(req.text)

    def do_login(self, args):
        """
        Usage:         login {username}
        Description:   Log into Erika.
        """
        parameters = args.split()
        username = parameters[0] # add error checking, no special chars allowed only alphanum
        password = getpass("Enter your password: ") # add error checking, no special chars allowed only alphanum
        payload = {'UserID':username, 'Password':password}
        req = requests.post('http://127.0.0.1:5000/api/v1/user/login', json=payload)
        if req.text != 'OK':
            print(req.text)
        else:
            self.login_status = True
            self.user_id = username
            print("Logged in as {}.".format(username))

    def do_logout(self, args):
        """
        Usage:         logout
        Description:   Logout of current user.
        """
        self.user_id = ""
        self.login_status = False
        print("Logged out of current user.")
    
    def do_exit(self, args):
        """
        Usage:         exit
        Description:   Exit Erika.
        """
        print("See you later!")
        return True

Erika().cmdloop()