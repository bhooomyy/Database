from auth import login,signUp,forgotPassword
from queries import typeOfQuery
def greet():
    print('Press\n\t 1. Login.\n\t 2. SignUp\n\t 3. Forgot password.\n\t 0. Exit')
    return input()

print('Welcome!\n')
while True:
    choice=greet()
    if(choice.isdigit()):
        if 1<=int(choice)<=3:
            choice=int(choice)
            match choice:
                case 1:
                    # valid=False
                    # userName=None
                    # while not valid:
                    #     valid,userName=login()
                    #     if not valid:
                    #         print('Please try again.')
                    userName='bhoomi'
                    while True:
                        query=input('Enter your query: ')
                        if(query.__eq__('-1')):
                            exit(0)
                        typeOfQuery(query,userName)
                    break
                case 2:
                    signUp()
                    break
                case 3:
                    forgotPassword()
                    break
                case 0:
                    SystemExit
        else:
            print('Invalid number entered! please choose between 1 and 3 only.')
    else:
        print('Invalid choice (String/special characters are not allowed) choose a number between 1 and 3.')
