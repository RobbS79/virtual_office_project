import pandas as pd
### Defines function which reads .csv format of bank_statement, drops unnecessary columns, handles white spaces and sets correct data types ### 
def pre_processed(folder,file_name):#reads .csv function takes 1. folder, the folder name where the bank_statement is saved; 2. file_name, actual name of bank_statement in the folder
    statement = pd.read_csv("/Users/rob/Desktop/virtual_office/Accounting/"+folder+file_name+".csv", encoding = "utf-16") #reads .csv folder TO DO: 1. adjust for own PATH to the folder and file_name; 2. adjust encoding argument;
    statement1 = statement.drop(columns=["Mena","IBAN partnera","BIC SWIFT kód banky partnera","Číslo účtu partnera","Kategória", "CC kód banky partnera","Popis transakcie","Referenčné číslo","Variabilný symbol", "Referencia platiteľa","Adresa platiteľa", "Adresa príjemcu"], axis=1, inplace=True)#drops unnecessary columns - adjust
    statement.fillna('-', inplace=True) #handles white spaces
    statement['Suma'] = statement['Suma'].str.replace(',','.') #handles decimal sign
    statement['Suma'] = statement['Suma'].str.replace("\xa0","") #handles \xa0 symbol (in my case required)
    statement = statement.astype({"Suma": float}) #sets correct data type for the Price column
    statement['Dátum splatnosti'] = statement['Dátum splatnosti'].astype(str) #sets correct data type for the Date_record column
    return statement

#In the condition    
def loads_condition(json_file):
    with open(json_file) as json_condition:
        data = json.load(json_condition)
    return(data)    
    
    


### Categorises the statement according to desired structure of cash-flow transaction recorded in the bank_statement, from pre_processed output (statement) ### 
def categorise_statement(statement,condition,by_column):#function takes arguments 1. processed bank_statement (statement); 2. structure for categorising records (condition); 3. names of columns to be categoised by (by_column)
    category = []
    for i in range(len(statement)):
        value = statement[str(by_column[0])][i]#categorising by the first column in by_column
    
        for cat,transaction in condition.items():
            if value in transaction:
                category.append(str(cat))
            else:
                continue
        
        ### CRITICAL STEP - where the conflict in categorisation occurs ###
        if value == "-":
            if statement[str(by_column[1])][i] == "Výber kartou" or statement[str(by_column[1])][i] == "Výber hotovosti":#categorising by the second column in by_column and comparing it with defined text in that column
                category.append("Withdrawal/Return")
            elif statement[str(by_column[1])][i] == "Poplatok" or statement[str(by_column[1])][i] == "Kartový poplatok":
                category.append("Cost")
            elif statement[str(by_column[1])][i] == "Vklad hotovosti" or statement[str(by_column[1])][i] == "Vklad cez ATM":
                category.append("Deposit/Investment")
            elif statement[str(by_column[1])][i] == "Platobný príkaz na úhradu (EB Sporopay)" :
                category.append("Else ...")
            else:
                category.append("-manually-")
                
        elif value == "self-company-name":
                category.append("-manually-")
            
    statement["category"] = category
    return(statement)

### Populate structure of cash-flow transactions ###
structure = {"Revenue":[...],
"Cost":[...],
"Tax":[...],
"Correction":[...],
"Deduction":[...],
"Correction":[...]}

def loads_partners(partners_csv_file):
    partners_data = pd.read_csv(partners_csv_file) #reads .csv folder TO DO: 1. adjust for own PATH to the folder and file_name; 2. adjust encoding argument;
    
    partner_ids = []
    for i in range(len(partners_data)):
        entry = partners_data.iloc[i][0]
        partner_ids.append(str(id(entry)))

    partners_data["partner_id"] = partner_ids
    return(partners_data)

### Replace folder and file_name in parenthesis and within the quotes ###
bank_statement = pre_processed("Fin_mngmnt/Inputs/bank_statements/","72021")
by_column = ["Partner","Typ transakcie"]

### Final data clensing ###
categorised = categorise_statement(bank_statement,structure,by_column)
statement1 = categorised.drop(columns=["Typ transakcie"], axis=1, inplace=True)
categorised

def classificates(dataset,partners_data):

    '''equity_transaction = {
    "ZENTAK":"111111111111111",
      "KENTAK":"222222222222222",
      "Peto":"333333333333333",
      "Robo":"444444444444444"
      }'''

    classified_data = []
    ids = []
    for i in range(len(dataset)):

        partner = dataset["partner"][i]
        category = dataset["category"][i]
        for j in range(len(partners_data)):
            if partner == partners_data["partner"][j] and ("Return" not in category) and ("Investment" not in category):
                #classes = partners_data["class"]
                classified_data.append(partners_data["class"][j])
                ids.append(partners_data["partner_id"][j])

            elif ("Return" in category) or ("Investment" in category):
                classified_data.append("Payables/Receivables")
                for k,v in equity_transaction.items():
                    if k in category:
                        ids.append(v)
                    else:
                        pass
                break

    dataset["class"] = classified_data
    dataset["IDs"] = ids
    return(dataset)
#works on particular model of business processes
