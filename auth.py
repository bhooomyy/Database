import os
import csv
import pandas as pd
import hashlib

usersDatabase='/Users/bhoomi/Documents/Projects/userDatabase.csv'
current_directory=os.getcwd()
special_chars = "!@#$%^&*(),.?\":{}|<>"

def validatePassword(password):
    if not password[0].isupper():
        print('Weak password. (First character must be capital) Enter a new password')
        return False
    else:
        if(not any(char.isdigit() for char in password)):
            print('Try again. Please keep atleast 1 digit in your password')
            return False
        else:
            if(not any(char in special_chars for char in password)):
                print('Try again. Please keep atleast 1 special character in your password')
                return False
            else:
                cnt=0
                for char in password:
                    if not char.isdigit() and char not in special_chars:
                        cnt+=1
                if(cnt>=6):
                    return True
                else:
                    print('There must be 6 characters')
                    return False

def validateUser(userName):
    users=os.listdir(current_directory)
    for user in users:
        if user.__eq__(userName):
            print('Existing user found.')
            return False
    else:
        return True

def validateReEnteredPassword(password,reEnterPassword):
    if(not(password.__eq__(reEnterPassword))):
        print('password mis-match error. Try again')
        return False
    else:
        return True

def validateNewUser(userName,password,reEnterPassword):
    flagUser=validateUser(userName)
    flagPassword=validatePassword(password)
    while(not flagPassword):
        flagPassword=validatePassword(password)
    flagRepeatedPassword=validateReEnteredPassword(password,reEnterPassword)
    while(not flagRepeatedPassword):
        flagRepeatedPassword=validateReEnteredPassword(password,reEnterPassword)
    if(flagUser and flagPassword and flagRepeatedPassword):
        os.mkdir(userName)
        return True
    else:
        return False
        
def EnterUserName():
    return input('Enter your username: ')

def EnterPassword():
    return input('Enter your password: ')

def re_EnterPassword():
    return input('re-Enter your password: ')

def signUp():
    userName=EnterUserName()
    password=EnterPassword()
    while(not validatePassword(password)):
        password=EnterPassword()
    reEnterPassword=re_EnterPassword()
    while((not validateReEnteredPassword(password,reEnterPassword))):
        password=EnterPassword()
        reEnterPassword=re_EnterPassword()
    email=input('Enter your email: ')

    if not os.path.exists(usersDatabase):
        with open(usersDatabase,mode='w',newline='') as file:
            writer=csv.writer(file)
            writer.writerow(['userName','password','reEnterPassword','email'])
    
    flag=validateNewUser(userName,password,reEnterPassword)
    if(flag):
        with open(usersDatabase,mode='a',newline='') as file:
            writer=csv.writer(file)
            password=hashlib.sha256(password.encode('utf-8')).hexdigest()
            reEnterPassword=hashlib.sha256(reEnterPassword.encode('utf-8')).hexdigest()
            writer.writerow([userName,password,reEnterPassword,email])
            print(f'{userName} added successfully!')


def login():
    userName=EnterUserName()
    password=EnterPassword()
    while(not validatePassword(password)):
        password=EnterPassword()
    password=hashlib.sha256(password.encode('utf-8')).hexdigest()
    df=pd.read_csv(usersDatabase)
    found=False
    for index in range(0,len(df)):
        if df.iloc[index]['userName'].__eq__(userName) and df.iloc[index]['password'].__eq__(password):
            print('Login Successful!')
            found=True
            userDB=os.path.join(current_directory,userName)
            os.chdir(userDB)
            tables=os.listdir(userDB)
            for table in tables:
                print(table)
            else:
                print('No Table exists!')
            return userName
        elif df.iloc[index]['userName'].__eq__(userName) or df.iloc[index]['password'].__eq__(password):
            print('Wrong username or passsword!')
            found=True
    if(not found):
        print('No such user exist!')
    return None
    

def forgotPassword():
    userName=input('Enter username: ')
    df=pd.read_csv(usersDatabase)
    if(userName in df['userName'].values):
        newPassword=EnterPassword()
        while(not validatePassword(newPassword)):
            newPassword=EnterPassword()
        reEnterPassword=re_EnterPassword()
        while(not validateReEnteredPassword(newPassword,reEnterPassword)):
            newPassword=EnterPassword()
            reEnterPassword=re_EnterPassword()
        newPassword=hashlib.sha256(newPassword.encode('utf-8')).hexdigest()
        reEnterPassword=hashlib.sha256(reEnterPassword.encode('utf-8')).hexdigest()
        df.loc[df['userName'] == userName, ['password', 'reEnterPassword']] = [newPassword, reEnterPassword]
        df.to_csv(usersDatabase, index=False)
        print('Password updated successfully!')
    else:
        print('No such user Exists!')
