import mysql.connector as sql
import datetime as dt
con = sql.connect(host="localhost", user="root", password="root", database="h_tracker") #Con=connection
cur = con.cursor() #cur=cursor
def log_new_habit(id):
    global c
    cur.execute("select habits from tracker where id=%s"%(id))
    data_sql = cur.fetchall()
    data = data_sql[0][0].split(',') #Splitting because data_sql will be a single string of habits, each seperated by a space, and we want to convert it into a list of habits
    if len(l)==0 and len(data)!=0:
        print("All habits have been logged for the day")
        c=1
    else:
        habit_name = input("Enter the name of the habit: ")
        if habit_name in l:
            l.remove(habit_name) #l will be the list of habits of the specified id
            x=','.join(l)
            cur.execute("update h_updater set habits_left='%s' where id=%s"%(x,id))
            x=dt.date.today() # The date it was logged
            y=dt.datetime.now().time() #the time it was logged
            cur.execute("insert into time_tracker values('%s','%s','%s',%s)"%(x,y,habit_name,id))
            con.commit()
            print("Habit logged successfully")
            c=0
def view_habits_left(id):
    cur.execute("select habits_left from h_updater where id=%s"%(id))
    data_sql = cur.fetchall()
    data = data_sql[0][0].split(',') #Splitting because data_sql will be a single string of habits, each seperated by a space, and we want to convert it into a list of habits
    for i in data: # here i will be each habit
        if i in l:
            print(i)
    print("These are the habits left to be logged for the day")
def view_streak(id):
    cur.execute("select streak from tracker where id=%s"%(id))
    data_sql = cur.fetchall()
    streak = data_sql[0][0]
    print("You have a streak of %s days"%(streak))
id =int(input("Enter your user id (to create a new id, enter 0): "))
if id == 0:
    name = input("Enter your name: ")
    habits = input("Enter the habits you want to track, seperated by a comma(','): ")
    cur.execute("insert into tracker(name,habits,streak,last_streak_date) values('%s','%s',%s,'%s')"%(name,habits,0,dt.date.today()))
    con.commit()
    print("User created successfully")
    id = cur.lastrowid #lastrowid will give the id of the last inserted row, which is the id of the user we just created 
    print("Your user id is ",id)
    cur.execute("insert into h_updater(habits_left,id) values ('%s',%s)"%(habits,id))
    con.commit()
cur.execute("select name from tracker where id=%s" % (id))
name = cur.fetchall()
print("Welcome ",name[0][0],"!")
cur.execute("select last_date from tracker where id=%s" % (id))
date = cur.fetchall()[0][0] #last_date will give the last date the user logged a habit, and we need to check if the user has logged a habit on the current date or not, if not then we need to reset the habits left to be logged for the new day
if dt.date.today() != date:
    l = [] #l will be the list of habits of the specified id
    cur.execute("select habits from tracker where id=%s" % (id))
    data_sql = cur.fetchall()
    data = data_sql[0][0].split(',') #Splitting because data_sql will be a single string of habits, each seperated by a space, and we want to convert it into a list of habits
    for i in data:
        l.append(i)
    date = dt.date.today()
    '''Here we are using h_updater table to store the habits of the user, because we need to update the habits of the user when they log a habit, and we don't want to update the habits in the tracker table because it will affect the streak calculation
    and here its reset to all th regular habits of the user, because the user has logged in on a new day, so we need to reset the habits to be logged for the new day'''
    x=','.join(l)
    cur.execute("update h_updater set habits_left='%s' where id=%s"%(x,id))
else:
    l = [] #l will be the list of habits left of the specified id
    cur.execute("select habits_left from h_updater where id=%s"%(id))
    data_sql = cur.fetchall()
    data = data_sql[0][0].split(',') #Splitting because data_sql will be a single string of habits, each seperated by a space, and we want to convert it into a list of habits
    for i in data:
        l.append(i)
while True:
    print("1. Log a new habit")
    print("2. View habits left to log")
    print("3. View current streak")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        log_new_habit(id)
    elif choice == 2:
        view_habits_left(id)
    elif choice == 3:
        cur.execute("select last_streak_date from tracker where id=%s"%(id))
        data_sql = cur.fetchall()
        last_date = data_sql[0][0]
        if last_date + dt.timedelta(days=1)==dt.date.today():
             if l==[] and c==1:
                cur.execute("update tracker set streak=streak+1 where id=%s"%(id))
                con.commit()
                c+=1
        view_streak(id)
    elif choice == 4:
        break
    cur.execute("select last_streak_date from tracker where id=%s"%(id))
    data_sql = cur.fetchall()
    last_date = data_sql[0][0]
    if last_date + dt.timedelta(days=1)==dt.date.today():
        if l==[] and c==1:
            cur.execute("update tracker set streak=streak+1 where id=%s"%(id))
            con.commit()
con.close()
