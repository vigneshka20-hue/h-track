import mysql.connector as sql
import datetime as dt
con = sql.connect(host="localhost", user="root", password="password", database="habit_tracker") #Con=connection
cur = con.cursor() #cur=cursor
# ask to enter user id and password
def log_new_habit():
    habit_name = input("Enter the name of the habit: ")
    cur.execute("select habits from tracker where id=%s)"%(id))
    data = cur.fetchall()
    if len(l)==0 and len(data)!=0:
        print("All habits have been logged for the day")
    elif habit_name in data:
        l.remove(habit_name) #l will be the list of habits of the specified id
        x=dt.date.today()
        y=dt.datetime.time()
        cur.execute("inser into time_tracker values('%s','%s','%s')"%(x,y,habit_name))
        con.commit()
        print("Habit logged successfully")

