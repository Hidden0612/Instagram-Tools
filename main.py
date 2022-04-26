import instagram

def main():
    insta = instagram.Instagram()

    USERNAME = ""
    PASSWORD = ""

    #  load the session
    if not insta.check_session_exists(USERNAME):
        # login
        insta.login(USERNAME, PASSWORD)
    info = insta.user_information("instagram")

    print(info)


if __name__ == "__main__":
    main()