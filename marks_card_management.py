import re
import mysql.connector
myConnnection =""
cursor=""
userName=""
password =""

#module to check sql connectivity
def MYSQLconnectionCheck ():       
    global myConnection
    global userName
    global password
    userName = input("\n ENTER MYSQL SERVER'S USERNAME : ")
    password = input("\n ENTER MYSQL SERVER'S PASSWORD : ")

    myConnection=mysql.connector.connect(host="localhost",user=userName,passwd=password , auth_plugin='mysql_native_password' )
    if myConnection:
        print("\n CONGRATULATIONS ! YOUR MYSQL CONNECTION HAS BEEN ESTABLISHED !")
        cursor=myConnection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS SMS")
        cursor.execute("COMMIT")
        cursor.close()
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD !")

#MODULE TO ESTABLISHED MYSQL CONNECTION
def MYSQLconnection ():
    global userName
    global password
    global myConnection
    myConnection=mysql.connector.connect(host="localhost",user=userName,passwd=password , database="SMS" , auth_plugin='mysql_native_password' )
    if myConnection:
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION !")
    myConnection.close()

#MODULE FOR NEW STUDENT ENTRY
def newStudent():
    if myConnection:
        cursor=myConnection.cursor()
        createTable ="""CREATE TABLE IF NOT EXISTS STUDENT(USN VARCHAR(10) PRIMARY KEY,SNAME VARCHAR(30),
        FNAME VARCHAR(30),MNAME VARCHAR(30),PHONE VARCHAR(12),SADDRESS VARCHAR(100),SBRANCH VARCHAR(8),SSEM VARCHAR(5),
        SBLOODGROUP VARCHAR(5))"""
        cursor.execute(createTable)
        usn=input(" ENTER STUDENT'S USN: ")
        sname=input(" ENTER STUDENT'S NAME : ")
        fname=input(" ENTER FATHER'S NAME : ")
        mname=input(" ENTER MOTHER'S NAME : ")
        phone=input(" ENTER CONTACT NO. : ")
        address=input(" ENTER ADDRESS : ")
        sbranch =input(" ENTER BRANCH : ")
        ssem=input(" ENTER SEMESTER : ")
        sblood=input(" ENTER STUDENT'S BLOOD GROUP: ")

        sql="INSERT INTO STUDENT(USN,SNAME,FNAME,MNAME,PHONE,SADDRESS,SBRANCH,SSEM,SBLOODGROUP) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(usn,sname,fname,mname,phone,address,sbranch,ssem,sblood)
        cursor.execute(sql,values)
        cursor.execute("COMMIT")
        cursor.close()
        print("\nNew Student Details Entered Successfully !!")
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION !!")

#MODULE TO DISPLAY STUDENT'S DATA
def displayStudent():
    cursor=myConnection.cursor()
    if myConnection:
        cursor.execute("SELECT * FROM STUDENT")
        data=cursor.fetchall()
        print(data)
        cursor.close()
    else:
        print("\nSomthing Went Wrong ,Please Try Again !")
  
#MODULE TO UPDATE STUDENT'S DATA      
def updateStudent():
    cursor=myConnection.cursor()
    if myConnection:
        usn=input("ENTER USN OF THE STUDENT")
        sql="SELECT * FROM STUDENT WHERE USN= %s"
        cursor.execute(sql,(usn,))
        data=cursor.fetchall()
        if data:
            print("PRESS 1 FOR NAME")
            print("PRESS 2 FOR BRANCH")
            print("PRESS 3 FOR SEM")
            choice=int(input("Enter Your Choice"))
            if choice==1:
                name=input("ENTER NAME OF THE STUDENT :")
                sql="UPDATE STUDENT SET SNAME= %s WHERE USN =%s"
                cursor.execute(sql,(name,usn))
                cursor.execute("COMMIT")
                print("NAME UPDATED")
            elif choice == 2:
                std=input("ENTER BRANCH OF THE STUDENT :")
                sql="UPDATE STUDENT SET SBRANCH= %s WHERE USN=%s"
                cursor.execute(sql,(std,usn))
                cursor.execute("COMMIT")
                print("BRANCH UPDATED")

            elif choice==3:
                roll_no=int(input("ENTER SEM OF THE STUDENT :"))
                sql="UPDATE STUDENT SET SSEM= %s WHERE USN = %s"
                cursor.execute(sql,(roll_no,usn))
                cursor.execute("COMMIT")
                print("SEM UPDATED")
            else:
                print("Record Not Found Try Again !")
                cursor.close()
        else:
            print("\nSomthing Went Wrong ,Please Try Again !")

#MODULE TO ENTER TOTAL(I+E)MARKS OF THE STUDENT
def marksStudent () :
    if myConnection:
        cursor=myConnection.cursor()
        createTable ="""CREATE TABLE IF NOT EXISTS MARKS(USN VARCHAR(10) PRIMARY KEY, ME INT,CNS INT,DBMS INT,ATC INT,
        ADP INT,UNIX INT,CNSL INT,DBMSL INT,EVS INT,TOTAL INT ,PERCENT INT)"""
        cursor.execute(createTable)
        usn=input("ENTER USN OF THE STUDENT :")
        me=int(input("\n ENTER MARKS OF MANAGEMENT AND ENTREPRENEURSHIP FOR IT INDUSTRY  : "))
        cns=int(input("\n ENTER MARKS OF COMPUTER NETWORKS AND SECURITY  : "))
        dbms=int(input("\n ENTER MARKS OF DATABASE MANAGEMENT SYSTEM   : "))
        atc=int(input("\n ENTER MARKS OF AUTOMATA THEORY AND COMPUTABILITY  : "))
        adp=int(input("\n ENTER MARKS OF APPLICATION DEVELOPMENT USING PYTHON : "))
        unix=int(input("\n ENTER MARKS OF UNIX PROGRAMMING  : "))
        cnsl=int(input("\n ENTER MARKS OF COMPUTER NETWORK LABORATORY  : "))
        dbmsl=int(input("\n ENTER MARKS OF DBMS LABORATORY  : "))
        evs=int(input("\n ENTER MARKS OF ENVIRONMENTAL STUDIES   : "))
        total = me + cns + dbms + atc + adp + unix + cnsl + dbmsl + evs
        percent = total/9
        sql="INSERT INTO MARKS(USN,ME,CNS,DBMS,ATC,ADP,UNIX,CNSL,DBMSL,EVS,TOTAL,PERCENT) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(usn,me,cns,dbms,atc,adp,unix,cnsl,dbmsl,evs,total,percent)
        cursor.execute(sql,values)
        cursor.execute("COMMIT")
        cursor.close()
        print("\nMarks of the Student Entered Successfully !")
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION !")

#MODULE TO GENERATE REPORT CARD OF ONE STUDENTS
def reportCardOneStudent():
    cursor=myConnection.cursor()
    cursor1=myConnection.cursor()
    if myConnection:
        usn=input("ENTER USN OF THE STUDENT :")
        
        cursor=myConnection.cursor()
        sql="SELECT * FROM MARKS WHERE USN= %s"
        cursor.execute(sql,(usn,))
        data=cursor.fetchall()
        
        cursor1=myConnection.cursor()
        sql1="SELECT PERCENT FROM MARKS WHERE USN= %s"
        cursor1.execute(sql1,(usn,))
        res=cursor1.fetchall()
        data1= re.sub(r'[\[\]\(\), ]', '', str(res))
        #data1 = [int(i) for i in set(data2)]
        #data1=sum(res)
        #data1 = map(int, res)  #[45,]
        if data:
            print(data)
            if(int(data1)>=90) :
                print("SGPA=10")
            elif(int(data1)>=80 and int(data1)<90) :
                print("SGPA=>9")
            elif(int(data1)>=70 and int(data1)<80) :
                print("SGPA=>8")
            elif(int(data1)>=60 and int(data1)<70) :
                print("SGPA=>7")     
            elif(int(data1)>=50 and int(data1)<60) :
                print("SGPA=>6")
            elif(int(data1)>=40 and int(data1)<50) :
                print("SGPA=>5")
            elif(int(data1)>=30 and int(data1)<40) :
                print("SGPA=>4")
            elif(int(data1)>=20 and int(data1)<30) :
                print("SGPA=>3")
            elif(int(data1)>=10 and int(data1)<20) :
                print("SGPA=>2")
            else:
                print("SGPA =>1")
        else:
            print("Record Not Found , Please Try Again !")
            cursor.close()
            cursor1.close()
    else:
        print("\nSomthing Went Wrong ,Please Try Again !")
        
#MODULE TO PROVIDE HELP FOR USER
def helpMe():
 print("Please, Visit The Offcial Website Of BNM!!!")

print("******************************************************************")
print("|--------------------SESSION 2021-22 ----------------------|")
print("| WELCOME |")
print("| BNM STUDENT REPORT CARD |")
print("|--------------------------------------------------------------|")
print("******************************************************************")
myConnection = MYSQLconnectionCheck ()
if myConnection:
    MYSQLconnection ()
    while(1):
        print("|-------------------------------------------------------------|")
        print("| Enter 1 - New Admission. |")
        print("| Enter 2 - Display Student's Data. |")
        print("| Enter 3 - Update Students's Data . |")
        print("| Enter 4 - Add Student's Marks Detail. |")
        print("| Enter 5 - Generate Student Wise Report Card. |")
        print("| Enter 6- Exit. |")
        print("| Enter 0(ZERO) - Help. |")
        print("|-------------------------------------------------------------|")

        choice=int(input("PLEASE ENTER YOUR CHOICE : "))
        if choice==1:
            newStudent()
        elif choice==2:
            displayStudent()
        elif choice==3:
            updateStudent()
        elif choice==4:
            marksStudent()
        elif choice==5:
            reportCardOneStudent()
        elif choice==6:
            myConnection.close()
            break
        elif choice==0:
            helpMe()
        else:
            print("Sorry ,May Be You Are Giving Me Wrong Input, Please Try Again !!! ")
    else:
            print("Check Your MYSQL Connection First !!! ")
