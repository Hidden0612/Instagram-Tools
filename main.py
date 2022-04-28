import instagram
from optparse import OptionParser

def main():
    # parse the options
    parser = OptionParser("python %prog [options] -u USERNAME -p PASSWORD INSTAGRAM")
    parser.add_option("-u", "--user", dest="username",
                    help="username to login to the instagram")
    parser.add_option("-p", "--pass", dest="password",
                    help="password to login to the instagram")

    # check the options values
    options, args = parser.parse_args()
    if(not options.username):
        parser.error('the username (-u) can not be empty !')
    if(not args):
        parser.error('the target username can not be empty !')

    # make a instagram object
    USERNAME = options.username
    PASSWORD = options.password
    TARGET = args[0]
    insta = instagram.Instagram()

    #  load the session
    if not insta.check_session_exists(USERNAME):
        # check password option
        if(not options.password):
            parser.error(f'can not find the session for \"{USERNAME}\", please enter the password (-p) to login ')
        # login
        insta.login(USERNAME, PASSWORD)

    # get information
    info = insta.user_information(TARGET)
    print(info)

if __name__ == "__main__":
    main()