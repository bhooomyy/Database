import os,csv,pandas as pd
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
            header=[f"{name}.{type}" for name, type in zip(columnName, columnType)]
            writer.writerow(header) 
            
def insertQuery(query,userName):
    temp=query.split(' ')
    if(temp[1].lower()=='into'):
        tableName=temp[2].split('(')[0]
        tableDef=''.join(temp[2:])
        #print(f'{tableDef}')
        tableFound=False
        tablePath = os.path.join(setPath(userName), tableName + '.csv')
        if os.path.exists(tablePath):
            tableFound=True
            columns=tableDef.split('(')[1].strip().split(',')
            columns[len(columns)-1]=columns[len(columns)-1].strip().split(')')[0]
            values=tableDef.split('(')[2].strip().split(',')
            values[len(values)-1]=values[len(values)-1].strip(')')
            #print(df)
            result=[]
            if(len(columns)==len(values)):
                df=pd.read_csv(tablePath)
                csv_col_names=[col.split('.')[0] for col in df.columns]
                csv_col_type=[col.split('.')[1] for col in df.columns]
                #print(f'{csv_col_names}  {csv_col_type}')
                isValid=True
                for col in columns:
                    if col not in csv_col_names:
                        print(f'Error {col} doesn\'t exist in table')
                        isValid=False
                        #return
                result=[]
                if isValid:
                    for i,col in enumerate(csv_col_names):
                            col_name=csv_col_names[i]
                            col_type=csv_col_type[i]
                            if(col_name in columns):
                                value=values[columns.index(col_name)]
                                if (col_type == 'INTEGER' and value.isdigit()) or \
                                    ((col_type == 'VARCHAR' and isinstance(value, str)) and (value.startswith("'") and value.endswith("'"))) or \
                                    (col_type == 'FLOAT' and value.replace('.', '', 1).isdigit()) or \
                                    (col_type == 'DOUBLE' and value.replace('.', '', 1).isdigit()):
                                    result.append(value)
                                else:
                                    isValid=False
                                    print(f"Error: Invalid data type for column '{col_name}'.")
                                    #return
                            else:
                                if col_type=='VARCHAR':
                                    result.append('NONE')
                                else:
                                    result.append('NULL')
                if isValid:
                    with open(tableName+'.csv',mode='a',newline='') as file:
                        writer=csv.writer(file)
                        writer.writerow(result)
                        print(f'Success: Data inserted into "{tableName}".')
                else:
                    print('Error: Data not inserted due to validation errors.')

            elif len(columns) != len(values):
                print(f"Error: Number of columns ({len(columns)}) does not match number of values ({len(values)}).")
                return
    
def selectQuery(query,userName):
    chunk=query.split(' ')
    tablePath=os.path.join(setPath(userName),chunk[3]+'.csv')
    if(chunk[1]=='*'):
        df=pd.read_csv(tablePath)
        columns=[col.split('.')[0] for col in df.columns]
        df.columns=columns
        print(df)

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
        if chunk[1].lower() != 'into':
            print('Error: Invalid query format. Expected "INSERT INTO <table_name>".')
            return
        insertQuery(query, userName)
    elif command == 'select':
        if chunk[2].lower() != 'from':
            print('Error: Invalid query format. Expected "SELECT <columns_name> FROM <table_name>".')
            return
        selectQuery(query,userName)
    else:
        print('Error: Unsupported query type.')