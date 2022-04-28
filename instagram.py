
import requests
from datetime import datetime
import json
import os
from bs4 import BeautifulSoup



class Instagram:
    """ Instagram Client, the main means for interacting with Instagram. """

    def __init__(self) -> None:
        self.session = None

    def load(self, session) -> None:
        """ Session file address """
        try:
            with open(session, "r") as f:
                self.session = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("[-] Session file not found ...!")

    def check_session_exists(self, username : str):
        # check the session file exists
        try:
            session_file = f"session_{username}.json"
            self.load(session_file)
            return True
        except FileNotFoundError:
            return False
        
    
    def login(self, username: str, password: str) -> None:
        """ Account Login """

        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())
        response = requests.get(link)

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": response.cookies['csrftoken']
        }

        login_response = requests.post(login_url, data=payload, headers=header)
        json_data = json.loads(login_response.text)

        if json_data["authenticated"]:
            cookies = login_response.cookies
            __cookie = cookies.get_dict()
            self.session = __cookie
            session_info = f"[+] Successful\ncsrf_token: , {__cookie['csrftoken']}\nsession_id: {__cookie['sessionid']}"
            with open(f"session_{username}.json", "w") as f:
                f.write(json.dumps(__cookie, indent=4))
            print(session_info)
        else:
            raise Exception(login_response.text)

    def user_information(self, user: str) -> str:
        """ Receive user information using a username. """
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "x-csrftoken": self.session['csrftoken'],
        }
        url = f'https://www.instagram.com/{user}/'
        response = requests.get(url, headers=header, cookies=self.session)
        # check invalid username
        if(response.status_code == 404):
            raise Exception("target username not found !")
        
        suop = BeautifulSoup(response.content, "html.parser")
        for info in suop.find_all("script", {"type": "text/javascript"}):
            if (info.get_text()).startswith("window._sharedData = "):
                __info_user = (info.get_text()).replace(
                    "window._sharedData = ", "")
                __json_data = json.loads(__info_user.replace(";", ""))

                biography = __json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["biography"]
                fbid = __json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["fbid"]
                full_name = __json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["full_name"]
                highlight_reel_count = __json_data["entry_data"][
                    "ProfilePage"][0]["graphql"]["user"]["highlight_reel_count"]
                followers = __json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]
                following = __json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_follow"]["count"]
                data = f"#==========#\n[+] full_name : {full_name}\n[+] fbid : {fbid}\n[+] highlight_reel_count : {highlight_reel_count}\n[+] followers : {followers}\n[+] following : {following}\n[+] biography : {biography}"
                try:
                    os.mkdir(user)
                except:
                    pass

                with open(f"{user}/information_{user}.json", "w") as f:
                    __json_write = __json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
                    f.write(json.dumps(__json_write, indent=4))
                return data

