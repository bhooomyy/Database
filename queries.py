import os,csv
current_directory=os.getcwd()

def validateCreate(chunk):
    if(chunk[1].lower().__eq__('table')):
        return True
    return False

def createQuery(chunk,userName):
    checkTable=os.path.join(current_directory,userName)
    os.chdir(checkTable)
    for tables in checkTable:
        if tables.__eq__(chunk[2]):
            print('Table alreaady exists.')
    else:
        with open(userName+'.csv',mode='w',newline='') as file:
            writer=csv.writer(file)
        print('Table created!')

def typeOfQuery(query,userName):
    chunk=[]
    chunk=query.split()
    if(chunk[0].lower().__eq__('create')):
        while not validateCreate(chunk):
            print('Invalid Query. Syntax error!')
            query=input('Enter your query: ')
            typeOfQuery(query,userName)
        if(validateCreate(chunk)):
            createQuery(chunk,userName)
    #elif chunk[0].lower().__eq__('insert'):

        