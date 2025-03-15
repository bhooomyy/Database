import os,csv
current_directory=os.getcwd()

def setPath(userName):
    checkTable=os.path.join(current_directory,userName)
    os.chdir(checkTable)
    return checkTable

def createQuery(columns, userName,tableName):
    tablePath = os.path.join(setPath(userName), tableName + '.csv')
    if os.path.exists(tablePath):
        print('Table already exists.')
    else:
        with open(tablePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            print('Table created!')
            columnName=[]
            columnType=[]
            for col in columns.split(','):
                columnParts=col.strip().split()
                columnName.append(columnParts[0])
                columnType.append(columnParts[1])
            writer.writerow(columnName)
            
def insertQuery(chunk,userName):
    tableFound=False
    tableName=chunk[2].split('(')[0].strip()
    checkTable=setPath(userName)
    checkTable=os.listdir(checkTable)
    for table in checkTable:
        if table.__eq__(tableName+'.csv'):
            tableFound=True
            with open(userName+'.csv',mode='w',newline='') as file:
                writer=csv.writer(file)
                columns=chunk[2].split('(')[1]
                columns=columns.split(',')
                columns=[col.strip() for col in columns]
                columns[len(columns)-1]=columns[len(columns)-1].replace(')','')
                writer.writerow(columns)
    if not tableFound:
        print('No such table exists')

def typeOfQuery(query, userName):
    chunk = query.split(' ')
    if not chunk:
        print('Error: Empty query.')
        return
    command = chunk[0].lower()
    if command == 'create':
        if len(chunk) < 3 or not chunk[1].lower() == 'table':
            print('Error: Invalid query format. Expected "CREATE TABLE <table_name>".')
            return
        tableName=chunk[2].split('(')[0]
        tableDefination=' '.join(chunk[2:])
        columns=tableDefination.split('(')[1].strip(')').strip()
        createQuery(columns, userName, tableName)
    elif command == 'insert':
        insertQuery(chunk, userName)
    else:
        print('Error: Unsupported query type.')