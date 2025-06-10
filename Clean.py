import mysql.connector
import os
import matplotlib.pyplot as plt

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="univa_student"
)

if db.is_connected():
    print("")
    print("٩(^ ᗜ ^ )و ´- U r connected to the database!")
else:
    print("(๑>؂•̀๑)ᕗ oops! Failed to connect to the database!")
    print("")

def insert_data(db):
    while True:
        nama = input("( ◡̀_◡́ )✎ 🗒 The name please, ").strip()
        if not nama:
            print("🛎 Name cannot be empty, good people.") 
            continue 
        kelas = input("( ◡̀_◡́)✎🗒 The class please, ").strip()
        if not kelas:
            print("🛎 Class cannot be empty, good people.")
            continue        
        alamat = input("( ◡̀_◡́)✎🗒 The address please, ").strip()
        if not alamat:
            print("🛎 Address cannot be empty, good people.")
            continue
        pendidikan = input("( ◡̀_◡́)✎🗒 Are you SMA or SMK student? ").strip()
        if not pendidikan:
            print("🛎 What is your Educational Level, good people?")
            continue
        break
    
    val = (nama, kelas, alamat, pendidikan)
    cursor = db.cursor()
    
    sql = "INSERT INTO students_tbl (student_name, student_grade, student_address, level_pend) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, val)
    db.commit()
    print("")
    print("{} ദ്ദി(˵ •̀ ᴗ - ˵ ) The data is added successfully".format(cursor.rowcount))
    print("")

def show_data(db):
    cursor = db.cursor()
    print("\nWelcome to the data filter menu ( •̀ ᴗ •́ ) where you can, ")
    print("1. Display all data")
    print("2. Display the data according to Classes")
    print("3. Display the data according to Student's name")
    choice = input("So, which one do you want?  ").strip()
    
    if choice == "1":
        sql = "SELECT * FROM students_tbl"
        val = ()
    elif choice == "2":
        kelas = input("( °ヮ° ) ? Which class u wanna see? ").strip() 
        sql = "SELECT * FROM students_tbl WHERE student_grade = %s"
        val = ("%{}%".format(kelas),)
    elif choice == "3":
        nama = input("( °ヮ° ) ? Which student u wanna see? ").strip()
        sql = "SELECT * FROM students_tbl WHERE student_name LIKE %s"
        val = ("%{}%".format(nama),)
    else:
        print("🛎 Invalid input! Showing you all the data . . .")
        sql = "SELECT * FROM students_tbl"
        val = ()
    
    cursor.execute(sql, val)
    result = cursor.fetchall()
    
    if not result:
        print("")
        print("Data not found, i'm sorry (• ᴖ •｡ )")
        print("")
    else:
        header = "{:<10} {:<30} {:<15} {:<19} {:<15}".format("Special ID", "Goverment Name", "Class and Major", "Address", "Education Level")
        print(header)
        print("-" * len(header))
        for data in result:
            row = "{:<10} {:<30} {:<15} {:<19} {:<15}".format(data[0], data[1], data[2], data[3], data[4])
            print(row)


def update_data(db):
    cursor = db.cursor()
    show_data(db)
    id = input("(•؎ •)✎ Which student's id u wanna update? ").strip()
    nama = input("(•؎ •)✎🗒 New name, please ").strip()
    kelas = input("(•؎ •)✎🗒 New class, please ").strip()
    alamat = input("(•؎ •)✎🗒 New Address, please ").strip()
    pendidikan = input("(•؎ •)✎🗒 New Education Level, please ").strip()
    
    sql = "UPDATE students_tbl SET student_name = %s, student_grade = %s, student_address = %s, level_pend = %s WHERE student_id = %s"
    val = (nama, kelas, alamat, pendidikan, id)
    cursor.execute(sql, val)
    db.commit()
    print("")
    print("{} ദ്ദി(˵ •̀ ᴗ - ˵ ) The data is updated successfully".format(cursor.rowcount))
    print("")
    
def delete_data(db):
    cursor = db.cursor()
    show_data(db)
    student_id = input("(•؎ •)✎ Which id u wanna delete? ").strip()
    sql = "DELETE FROM students_tbl WHERE student_id = %s"
    val = (student_id,)
    cursor.execute(sql, val)
    db.commit()
    print("")
    print("{} ദ്ദി(˵ •̀ ᴗ - ˵ ) The data is deleted successfully".format(cursor.rowcount))
    print("")

def search_data(db):
    cursor = db.cursor()
    keyword = input("(•؎ •)✎ What keyword u use to look for the data? ").strip()
    sql = ("SELECT * FROM students_tbl WHERE student_name LIKE %s OR ""student_grade LIKE %s OR student_address LIKE %s OR level_pend LIKE %s")
    val = ("%{}%".format(keyword), "%{}%".format(keyword), "%{}%".format(keyword), "%{}%".format(keyword))
    cursor.execute(sql, val)
    result = cursor.fetchall()

    if not result:
        print("")
        print("Data not found, i'm sorry (• ᴖ •｡ )")
        print("")
    else:
        header = "{:<10} {:<30} {:<15} {:<30} {:<19}".format("Special ID", "Goverment Name", "Grade and Class", "Address", "Education Level")
        print(header)
        print("-" * len(header))
        for data in result:
            row = "{:<10} {:<30} {:<15} {:<30} {:<19}".format(data[0], data[1], data[2], data[3], data[4])
            print(row)

def show_dashboard(db):
    cursor = db.cursor()
    
    query_students = "SELECT student_grade, COUNT(*) FROM students_tbl GROUP BY student_grade"
    cursor.execute(query_students)

    result_students = cursor.fetchall()
    classes = [row[0] for row in result_students]
    counts_students = [row[1] for row in result_students]

    query_pendidikan = "SELECT level_pend, COUNT(*) FROM students_tbl GROUP BY level_pend"
    cursor.execute(query_pendidikan)
    result_pendidikan = cursor.fetchall()
    levels = [row[0] for row in result_pendidikan]
    counts_pendidikan = [row[1] for row in result_pendidikan]

    fig, axs = plt.subplots(2, 2, figsize=(14, 12))

    axs[0, 0].bar(classes, counts_students, color='dodgerblue')
    axs[0, 0].set_title('Number of students per class')
    axs[0, 0].set_xlabel('Grade and Class')
    axs[0, 0].set_ylabel('Number of students')

    axs[0, 1].pie(counts_students, labels=classes, autopct='%1.1f%%', startangle=80, colors=plt.cm.Paired.colors)
    axs[0, 1].set_title('Student Percentage per Class')
    axs[0, 1].axis('equal')

    axs[1, 0].bar(levels, counts_pendidikan, color='seagreen')
    axs[1, 0].set_title('Number of students per education level')
    axs[1, 0].set_xlabel('Education Level')
    axs[1, 0].set_ylabel('Number of students')

    axs[1, 1].pie(counts_pendidikan, labels=levels, autopct='%1.1f%%', startangle=80, colors=plt.cm.Paired.colors)
    axs[1, 1].set_title('Student Percentage per Education Level')
    axs[1, 1].axis('equal')

    plt.suptitle('Dashboard Data of UNIVA Students', fontsize=10)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def show_menu(db):
    print("")
    print("========= SARCHIVE DATABASE : UNIVA STUDENTS =========")
    print("")
    print("Welcome to the UNIVA Student Database (˵ •̀ ᴗ - ˵) ✧")
    print("What do you want to do today?")
    print("")
    print("1. Insert New Student's Data?")
    print("2. Display Student's Data?")
    print("3. Update Old Student's Data?")
    print("4. Delete Student's Data?")
    print("5. Search Student's Data?")
    print("6. Shows Data Dashboard?")
    print("0. Exit?")
    print("—------------------------------------------------------")
    menu = input("(｡- .•) Please choose the menu: ").strip()

    os.system("cls" if os.name == "nt" else "clear")
    
    if menu == "1":
        insert_data(db)
    elif menu == "2":
        show_data(db)
    elif menu == "3":
        update_data(db)
    elif menu == "4":
        delete_data(db)
    elif menu == "5":
        search_data(db)
    elif menu == "6":
        show_dashboard(db)
    elif menu == "0":
        print("")
        print("(„• ֊ •„)੭✧ Thank you for using this application!")
        print("Bye bye and c u next time (^._.^)ﾉ")
        print("")
        exit()
    else:
        print("🛎 O-oh! Please choose another menu.")

if __name__ == "__main__":
    while True:
        show_menu(db)