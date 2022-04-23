from .instagram import Instagram

insta = Instagram()

USERNAME = ""
PASSWORD = ""

insta.login(USERNAME, PASSWORD) # Or Load File Session

info = insta.user_information("Hidden0612")

print(info)
