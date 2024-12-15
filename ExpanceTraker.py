import database as db
import datetime
import matplotlib.pyplot as plt
import numpy as np

class ExpenseTracker:

    def add_expense(self, name, cost, date,Expance_type):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not isinstance(cost, (int, float)):
            raise ValueError("Cost must be a number")
        if not isinstance(date, datetime.date):
            raise ValueError("Date must be a datetime.date object")
        if not isinstance(Expance_type,str):
            raise ValueError("Expance Type must be in string")
        db.db_cursor.execute("insert into expances(expance_name,expance_cost,expance_date,expance_type) values(%s,%s,%s,%s)",(name,cost,date,Expance_type))
        db.con.commit()
        print(db.db_cursor.rowcount ,' data is inserted')

    def view_expense_chart(self):
        print('Enter Your Choice.')
        while True:
            choice=input('1. Month pie Chart\n2. Year chart\n3. Exit\n')
            if choice=='3':
                menu()
                break
            match choice:
                case '1':
                    m=input('Enter a month you want to see the pie chart(MM): ')
                    y=input('Enter a year you want to see the pie chart(YYYY): ')
                    sql="select expance_date,expance_cost,expance_type from expances"
                    db.db_cursor.execute(sql)
                    result=db.db_cursor.fetchall()
                    Grossary_cost=0
                    Food_B=0
                    shopping=0
                    Bill_rent=0
                    Transport=0
                    Other=0
                    for i in result:
                        if m==i[0].strftime("%m") and y==i[0].strftime("%Y"):
                            if i[2]=='Grossary':
                                Grossary_cost+=i[1]
                            elif i[2]=='Food & Beverage':
                                Food_B+=i[1]
                            elif i[2]=='Shopping':
                                shopping+=i[1]
                            elif i[2]=='Bill-rent':
                                Bill_rent+=i[1]
                            elif i[2]=='Transport':
                                Transport+=i[1]
                            elif i[2]=='Other':
                                Other+=i[1]
                    total=Grossary_cost+Food_B+shopping+Bill_rent+Transport+Other         
                    cost=np.array((Grossary_cost,Food_B,shopping,Bill_rent,Transport,Other))
                    mylable=np.array(('Grossary','Food & Beverage','Shopping','Bill-rent','Transport','Other'))
                    plt.pie(cost,labels=mylable,autopct='%1.f%%',shadow=True)
                    plt.title(f" :: {m}/{y} MONTH PIE CHART ::")
                    plt.xlabel(f"=> Total Expanses of {m}/{y} month is {total} ")
                    plt.show()

                case '2':
                    y1=input('Enter a year you want to see the total Expance(YYYY): ')
                    sql="select expance_date,expance_cost,expance_type from expances"
                    db.db_cursor.execute(sql)
                    result=db.db_cursor.fetchall()
                    jan_sum,feb_sum,march_sum,april_sum,may_sum,june_sum,july_sum,aug_sum,sep_sum,oct_sum,nov_sum,dec_sum=0,0,0,0,0,0,0,0,0,0,0,0
                    for i in result:
                        if y1==i[0].strftime("%Y"):
                            if i[0].strftime("%m")=='01':
                                jan_sum+=i[1]
                            if i[0].strftime("%m")=='02':
                                feb_sum+=i[1]
                            if i[0].strftime("%m")=='03':
                                march_sum+=i[1]
                            if i[0].strftime("%m")=='04':
                                april_sum+=i[1]
                            if i[0].strftime("%m")=='05':
                                may_sum+=i[1]
                            if i[0].strftime("%m")=='06':
                                june_sum+=i[1]
                            if i[0].strftime("%m")=='07':
                                july_sum+=i[1]
                            if i[0].strftime("%m")=='08':
                                aug_sum+=i[1]
                            if i[0].strftime("%m")=='09':
                                sep_sum+=i[1]
                            if i[0].strftime("%m")=='10':
                                oct_sum+=i[1]
                            if i[0].strftime("%m")=='11':
                                nov_sum+=i[1]
                            if i[0].strftime("%m")=='12':
                                dec_sum+=i[1]    
                    x=np.array(('Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec'))
                    y=np.array((jan_sum,feb_sum,march_sum,april_sum,may_sum,june_sum,july_sum,aug_sum,sep_sum,oct_sum,nov_sum,dec_sum))   
                    plt.xlabel(f" Expance Month\n\n=> The total expance of {y1} is {sum(y)}")
                    plt.ylabel('Expance Cost')
                    plt.title(f":: {y1} YEAR TOTAL EXPANCES :: ")        
                    plt.bar(x,y)
                    plt.show()
                
                case _:
                    print('Invalid choice')

    def execute_command(self, command):
        match command:
            case '1':
                name = input("Enter expense name: ")
                cost = float(input("Enter expense cost: "))
                date=db.enter_date()
                print('Enter expance type from given below')
                while True:
                    print('Enter Your choice\n 1) Grossary  2) Food & Beverage  3) Shopping  4) Bill-rent  5) Transport  6) Other ')
                    choice=input()
                    match choice:
                        case '1':
                            type='Grossary'
                            break
                        case '2':
                            type='Food & Beverage'
                            break
                        case '3':
                            type='Shopping'
                            break
                        case '4':
                            type='Bill-rent'
                            break
                        case '5':
                            type='Transport'
                            break
                        case '6':
                            type='Other'
                            break
                        case _:
                            print('Invalid choice')
                self.add_expense(name, cost, date,type)
            case '2':
                while True:
                    print('Enter your choice :')
                    print('1. particular date\n2. Grossary\n3. Food & Beverage\n4. Shopping\n5. Bill-rent \n6. Transport\n7. Other\n8. Exit')
                    choice=(input())
                    if choice=='8':
                        menu()
                        break
                    match choice:
                        case '1':
                            date = datetime.date.fromisoformat(input("Enter expense date (YYYY-MM-DD): "))
                            sql="select * from expances where expance_date=%s"
                            db.db_cursor.execute(sql,(date,))
                            db.bet_expances(db.db_cursor) # For print data
                            sql="select sum(expance_cost) from expances where expance_date=%s"
                            db.db_cursor.execute(sql,(date,))
                            for i in db.db_cursor:
                                for  j in i:
                                    print(f"The total Expance of {date} if {j} rupees")
                                print()
                            
                        case '2':
                            s_date=input('Enter strat date(YYYY-MM-DD): ')
                            e_date=db.enter_date()
                            sql="select * from expances where expance_type='Grossary' and expance_date between %s AND %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expances(db.db_cursor)
                            sql="select sum(expance_cost) from expances where expance_type='Grossary'and expance_date between %s and %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expenditure(db.db_cursor,s_date,e_date)
                        case '3':
                            s_date=input('Enter strat date(YYYY-MM-DD): ')
                            e_date=db.enter_date()
                            sql="select * from expances where expance_type='Food & Beverage' and expance_date between %s AND %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expances(db.db_cursor)
                            sql="select sum(expance_cost) from expances where expance_type='Food & Beverage'and expance_date between %s and %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expenditure(db.db_cursor,s_date,e_date)
                        case '4':
                            s_date=input('Enter strat date(YYYY-MM-DD): ')
                            e_date=db.enter_date()
                            sql="select * from expances where expance_type='Shopping' and expance_date between %s AND %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expances(db.db_cursor)
                            sql="select sum(expance_cost) from expances where expance_type='Shopping'and expance_date between %s and %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expenditure(db.db_cursor,s_date,e_date)
                        case '5':
                            s_date=input('Enter strat date(YYYY-MM-DD): ')
                            e_date=db.enter_date()
                            sql="select * from expances where expance_type='Bill-rent' and expance_date between %s AND %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expances(db.db_cursor)
                            sql="select sum(expance_cost) from expances where expance_type='Bill-rent'and expance_date between %s and %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expenditure(db.db_cursor,s_date,e_date)
                        case '6':
                            s_date=input('Enter strat date(YYYY-MM-DD): ')
                            e_date=db.enter_date()
                            sql="select * from expances where expance_type='Transport' and expance_date between %s AND %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expances(db.db_cursor)
                            sql="select sum(expance_cost) from expances where expance_type='Transport'and expance_date between %s and %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expenditure(db.db_cursor,s_date,e_date)
                        case '7':
                            s_date=input('Enter strat date(YYYY-MM-DD): ')
                            e_date=db.enter_date()
                            sql="select * from expances where expance_type='Other' and expance_date between %s AND %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expances(db.db_cursor)
                            sql="select sum(expance_cost) from expances where expance_type='Other'and expance_date between %s and %s"
                            db.db_cursor.execute(sql,(s_date,e_date,))
                            db.bet_expenditure(db.db_cursor,s_date,e_date)
                        case _:
                            print('Invalid choice')
            # delete perticular expance
            case '3':
                date = db.enter_date()
                sql="select * from expances where expance_date=%s"
                db.db_cursor.execute(sql,(date,))
                db.bet_expances(db.db_cursor)
                while True:
                    sql1="select expance_id from expances where expance_date=%s"
                    db.db_cursor.execute(sql1,(date,))
                    expance_id_list=db.db_cursor.fetchall()
                    l=[]
                    for i in expance_id_list:
                        for j in i:
                            l.append(j)
                    print(f"Expance id :{l}")
                    expance_id=int(input('Select expance id from above: '))
                    if expance_id in l:   
                        sql="DELETE FROM expances WHERE expance_id=%s"
                        db.db_cursor.execute(sql,(int(expance_id),))
                        db.con.commit()
                        if db.db_cursor.rowcount>0:
                            print(f"Your Expance is deleted sucessfully.")
                            break
                    else:
                        print('Not Found')
                        print(' 1.For continue\n 2.For Exit')
                        E=input()
                        if E=='2':
                            break
            # Delete month/day expances & for clear expances
            case '4':
                while True:
                    print('1. Delete specific date expances\n2. Delete specific month expances\n3. Clear All expances\n4. Exit')
                    choice=input()
                    if choice=='4':
                        menu()
                        break
                    match choice:
                        case '1':
                            date=db.enter_date()
                            sql="DELETE FROM expances WHERE expance_date=%s"
                            db.db_cursor.execute(sql,(date,))
                            db.con.commit()
                            print(db.db_cursor.rowcount)
                            if db.db_cursor.rowcount>0:
                                print('Your expances is deleted sucessfully.')
                        case '2':
                            m=input('Enter month you want to delete(MM): ')
                            y=input('Enter year you want to delete(YYYY): ')
                            sql="select expance_id,expance_date from expances"
                            db.db_cursor.execute(sql)
                            result=db.db_cursor.fetchall()
                            id_list=[]
                            for i in result:
                                if m==i[1].strftime("%m") and y==i[1].strftime("%Y"):
                                    id_list.append(i[0])
                            temp=0
                            for i in range(len(id_list)):
                                sql1="delete from expances where expance_id=%s"
                                db.db_cursor.execute(sql1,(id_list[i],))
                                db.con.commit()
                                temp+=db.db_cursor.rowcount
                            if temp>0:
                                print(f"All Expances from the {m} month has been successfully deleted.")
                        case '3':
                            sql="TRUNCATE TABLE expances"
                            db.db_cursor.execute(sql)
                            db.con.commit()
                            if db.db_cursor.rowcount>0:
                                print('Your all expances is deleted.')
                        case _:
                            print('Invalid choice.')
            # Save expances in file   
            case '5':
                while True:
                    print('1. For month\n2. For year\n3. Exit')
                    choice=input()
                    if choice=='3':
                        menu()
                        break
                    match choice:
                        case '1':
                            m=input('Enter month you want to save(MM): ')
                            y=input('Enter year you want to save(YYYY): ')
                            sql="select expance_date,expance_cost,expance_type,expance_name from expances"
                            db.db_cursor.execute(sql)
                            result=db.db_cursor.fetchall()
                            cost_list=[]
                            # space method 
                            def space(s):
                                s1=' '
                                for i in range(len(str(s)),10):
                                    s1+=' '
                                return s1
                            for i in result:
                                if m==i[0].strftime("%m") and y==i[0].strftime("%Y"):
                                    cost_list.append((i[0],i[1],i[2],i[3]))
                            filename=input('Enter file name: ')
                            with open(filename+'.txt', 'a+') as f:
                                for i in cost_list:
                                    f.write(f"Expance name: {i[3]}{space(i[3])}Expance cost: {i[1]}{space(i[1])}Expance type: {i[2]}{space(i[2])} Expance date: {i[0]}\n")
                            print(f"Data is saved in a {filename}")
                        case '2':
                            y=input('Enter year you want to delete(YYYY): ')
                            sql="select expance_date,expance_cost,expance_type,expance_name from expances"
                            db.db_cursor.execute(sql)
                            result=db.db_cursor.fetchall()
                            data_list=[]
                            def space(s):
                                s1=' '
                                for i in range(len(str(s)),10):
                                    s1+=' '
                                return s1
                            for i in result:
                                if y==i[0].strftime("%Y"):
                                    data_list.append((i[0],i[1],i[2],i[3]))
                            filename=input('Enter file name: ')
                            with open(filename+'.txt', 'a+') as f:
                                for i in data_list:
                                    f.write(f"Expance name: {i[3]}{space(i[3])}Expance cost: {i[1]}{space(i[1])}Expance type: {i[2]}{space(i[2])} Expance date: {i[0]}\n")
                            print(f"Data is saved in a {filename}")
                        case _:
                            print('Invalid choice')
            # Total expance for a month in categories wise
            case '6':
                while True:
                    print('1. Total GROSSARY expance for a month\n2. Total FOOD & BEVERAGE expance for a month\n3. Total SHOPPING expance for a month\n4. Total BILL-RENT expance for a month\n5. Total TRANSPORT expance for a month\n6. Total OTHER expance for a month\n7. Exit ')
                    choice=input()
                    if choice=='7':
                        menu()
                        break
                    match choice:
                        case '1':
                            print(f"\n=> The total monthly expanses are Rs. {db.cate_total_expance('Grossary')}\n")
                        case '2':
                             print(f"\n=> The total monthly expanses are Rs. {db.cate_total_expance('Food & Beverage')}\n")
                        case '3':
                             print(f"\n=> The total monthly expanses are Rs. {db.cate_total_expance('Shopping')}\n")
                        case '4':
                             print(f"\n=> The total monthly expanses are Rs. {db.cate_total_expance('Bill-rent')}\n")
                        case '5':
                             print(f"\n=> The total monthly expanses are Rs. {db.cate_total_expance('Transport')}\n")
                        case '6':
                             print(f"\n=> The total monthly expanses are Rs. {db.cate_total_expance('Other')}\n")
                        case _:
                            print('Invalid choice')
            case '7':
                date = db.enter_date()
                sql="select * from expances where expance_date=%s"
                db.db_cursor.execute(sql,(date,))
                db.bet_expances(db.db_cursor)
                while True:
                    sql1="select expance_id from expances where expance_date=%s"
                    db.db_cursor.execute(sql1,(date,))
                    expance_id_list=db.db_cursor.fetchall()
                    l=[]
                    for i in expance_id_list:
                        for j in i:
                            l.append(j)
                    print(f"Expance id :{l}")
                    print('For Exit :0')
                    expance_id=int(input('Select expance id from above: '))
                    if expance_id==0:
                        break
                    if expance_id in l:   
                        while True:
                            choice=input('select choice you want to update\n 1.Expance name\n 2.Expance cost\n 3.Expance date\n 4.Expance type\n 5.Exit\n')
                            if choice=='5':
                                break
                            match choice:
                                case '1':
                                    name=input('Enter new Expance name: ')
                                    sql="update expances set expance_name=%s where expance_id=%s"
                                    db.db_cursor.execute(sql,(name,expance_id,))
                                    db.con.commit()
                                case '2':
                                    cost=input('Enter new Expance cost: ')
                                    sql="update expances set expance_cost=%s where expance_id=%s"
                                    db.db_cursor.execute(sql,(cost,expance_id,))
                                    db.con.commit()
                                case '3':
                                    date=datetime.date.fromisoformat(input("Enter new expense date (YYYY-MM-DD): "))
                                    sql="update expances set expance_date=%s where expance_id=%s"
                                    db.db_cursor.execute(sql,(date,expance_id,))
                                    db.con.commit()
                                case '4':
                                    print('Enter Your choice\n 1) Grossary  2) Food & Beverage  3) Shopping  4) Bill-rent  5) Transport  6) Other ')
                                    type=input('Enter new Expance type from above: ')
                                    sql="update expances set expance_type=%s where expance_id=%s"
                                    db.db_cursor.execute(sql,(type,expance_id,))
                                    db.con.commit()
                                case _:
                                    print('Invalid choice')
                    else:
                        print('Not Found')
            case '8':
                self.view_expense_chart()
            case _:
                print("Invalid command")

def menu(): 
    et = ExpenseTracker()
    while True:
        command = input("Enter command \n1. Add expances\n2. View expances\n3. Delete perticular expance\n4. Delete month/day expances & for clear expances\n5. Save expances\n6. Total expance for a month in categories wise\n7. Update Expance\n8. Expance chart\n9. Exit\n")
        if command == '9':
            break
        et.execute_command(command)

def main():
    print()
    print("             ::    WELCOME TO EXPANCE TRACKER    ::                  ")
    print('1.Login\n2.sign in')
    choice=int(input())
    if choice==1:
        while True:
            username=input('Enter your Username: ')
            password=input('Enter your Password: ')
            if (username,password) in db.users_data():
                print('Login sucessfully')
                menu()
                break
            else:
                print('Your password/username is wrong please ReEnter')
    if choice==2:
        while True:
            Username=input('Enter your Username: ')
            password=input('Enter your password: ')
            if (Username,password) in db.users_data():
                print('Re-Enter')
            else:
                x=db.db_cursor.execute("insert into users(username,password) values(%s,%s)",(Username,password))
                db.con.commit()
                print('Account created sucessfully')
                menu()
                break
                
main()        
        