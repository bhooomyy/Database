import os,csv,pandas as pd
import re
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
    tableName=query.lower().split('from')[1].strip()
    tablePath=os.path.join(setPath(userName),tableName+'.csv')
    
    df=pd.read_csv(tablePath)
    columns=[col.split('.')[0] for col in df.columns]
    df.columns=columns
   
    if(chunk[1]=='*'):
        print(df)
        return
    
    select_part = query.split('select')[1].split('from')[0].strip()
    isValid=True
    result=[]
    if ',' in select_part:
        cols = [col.strip() for col in select_part.split(',')]
    else:
        cols = [select_part.strip()]
    
    for col in cols:
        if col in df.columns:
            result.append(col)
        else:
            isValid = False
            print(f'Error: Column "{col}" does not exist in the table.')
    
    if isValid:
        print(df[result])
    else:
        print('Error: Invalid columns in the query.')

def updateQuery(query,userName):
    chunk=query.split(' ')
    tablepath=os.path.join(setPath(userName),chunk[1].strip()+'.csv')
    parts = re.split(r'\bset\b|\bwhere\b', query, flags=re.IGNORECASE)
    requestedCol = parts[1].strip()
    requestedCol=requestedCol.split(',')
    conditions = parts[2].strip() 
    #many conditions connected by AND OR , Asuume we have one condition here
    req_col=[req_col.split('=')[0] for req_col in requestedCol]
    req_val=[req_val.split('=')[1] for req_val in requestedCol]

    condition_name=conditions.split('=')[0]
    condition_val=conditions.split('=')[1]
    
    df=pd.read_csv(tablepath,na_values=['NULL', 'NONE'])
    csv_col_names={col.split('.')[0]:col for col in df.columns}
    #csv_col_type=[col.split('.')[1] for col in df.columns]
    
    fetch_col=[]
    fetch_col=[condition_name]+req_col
   
    isValid=True
    for col in fetch_col:
        if col not in csv_col_names:
            print(f'Error {col} doesn\'t exist in table')
            isValid=False
    
    if isValid:
        condition_type_check_full=csv_col_names[condition_name]
        condition_type_check=condition_type_check_full.split('.')[1]
        if condition_type_check=='INTEGER':
            condition_val=int(condition_val)
        elif condition_type_check=='VARCHAR':
            condition_val=condition_val
        elif condition_type_check=='FLOAT' or condition_type_check=='DOUBLE':
            condition_val=float(condition_val)

        # isNaN=False
        # for row in df.iterrows():
        #     if pd.isna(str(row[condition_type_check_full])) and pd.isna(condition_val):
        #         isNaN=True

        for index,row in df.iterrows():
            if row[condition_type_check_full]==condition_val:
                for j,col in enumerate(req_col):
                    full_col=csv_col_names[col]
                    col_type=full_col.split('.')[1]

                    # if isNaN:
                    if pd.isna(row[full_col]):
                        if col_type=='INTEGER':
                            df.at[index,full_col]=0
                        elif col_type=='VARCHAR':
                            df.at[index,full_col]="'"
                        elif col_type in ['FLOAT','DOUBLE']:
                            df.at[index,full_col]=0.0

                    if col_type=='INTEGER':
                        req_val[j]=int(req_val[j])
                    elif col_type=='VARCHAR':
                        req_val[j]=req_val[j]
                    elif col_type in ['FLOAT','DOUBLE']:
                        req_val[j]=float(req_val[j])
                    
                    df.at[index,full_col]=req_val[j]
        
        df.to_csv(tablepath, index=False)
        print(f'Success: Table "{chunk[1]}" updated.')
    else:
        print('Error: Data not updated due to validation errors.')

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
        if 'from' not in query.lower():
            print('Error: Invalid query format. Expected "SELECT <columns_name> FROM <table_name>".')
            return
        selectQuery(query,userName)
    elif command=='update':
        if 'set' and 'where' not in query.lower():
            print('Error: Invalid query format. Expected "UPDATE <table_name> SET <column1_name> = <value1>,... WHERE <condition>".')
        updateQuery(query,userName)
    else:
        print('Error: Unsupported query type.')