import datetime
import mysql.connector

# Connection code
con=mysql.connector.connect(host="localhost",user="root",password="",database="expance_traker")
if con.is_connected():
    print("Connected sucessfully")
else:
    print("Please Try again")
    
# Execute quary variable   
db_cursor=con.cursor()

# Users table data
def users_data():
    db_cursor.execute("select * from users")
    users_data=db_cursor.fetchall()
    return users_data

# Expance table data
def expance_data():
    db_cursor.execute("select * from expances")
    expance_data=db_cursor.fetchall()
    return expance_data

# Enter date
def enter_date():
    print('select end date \n 1.For Today Date \n 2.For Other Date')
    choice=int(input())
    if choice==1:
        e_date= datetime.date.today()
    if choice==2:
        e_date = datetime.date.fromisoformat(input("Enter expense date (YYYY-MM-DD): "))
    return e_date

# All expances between two date
def bet_expances(db_cursor):
    for i in db_cursor:
        print(f"Expance id  : {i[0]}")
        print(f"Expance name: {i[1]}")
        print(f"Expance cost: {i[2]}")
        print(f"Expance date: {i[3]}")
        print(f"Expance type: {i[4]}")
        print()

# Between two date total expenditure
def bet_expenditure(db_cursor,s_date,e_date):
    for i in db_cursor:
        for  j in i:
            print(f"Total expenditure between {s_date} and {e_date} is Rs.{j}")
        print()
        
# Categories wise total expance
def cate_total_expance(e_type):
    m=input('Enter month you want to delete(MM): ')
    y=input('Enter year you want to delete(YYYY): ')
    sql="select expance_date,expance_cost,expance_type from expances"
    db_cursor.execute(sql)
    result=db_cursor.fetchall()
    cost_list=[]
    for i in result:
        if m==i[0].strftime("%m") and y==i[0].strftime("%Y") and i[2]==e_type:
            cost_list.append(i[1])
    return sum(cost_list)     
