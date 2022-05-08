from numpy.core.defchararray import lower
import pandas as pd
import psycopg2


def add_staff(cur):
    s = input("Enter inserted columns: ")
    allcols = s.strip().split(' ')
    for i in range(len(allcols)):
        allcols[i]=allcols[i].replace("_", " ")
    cols = ""
    vals = ""
    colname = ["name", "age", "gender", "number", "supply_center", "mobile_number", "type"]
    for i in range(len(allcols)):
        if allcols[i] != "null":
            vals += "'" + allcols[i] + "'" + ","
            cols += colname[i] + ","
    if cols != "":
        vals = vals.rstrip(",")
        cols = cols.rstrip(",")
        cur.execute("insert into staff (" + cols + ") values (" + vals + ")")


def select_staff(cur):
    s = input("Enter select columns: ")
    if s != "*":
        allcols = s.strip().split(' ')
        cols = ""
        col_list = []
        for i in range(len(allcols)):
            if allcols[i] != "null":
                cols += allcols[i] + ","
                col_list.append(allcols[i])
        if cols != "":
            cols = cols.rstrip(",")
    else:
        col_list = ["name", "age", "gender", "number", "supply_center", "mobile_number", "type"]
        cols = "name, age, gender, number, supply_center, mobile_number, type"
    cons = input("Enter select constraints: ")
    if cons != 'n':
        colname = ["name", "age", "gender", "number", "supply_center", "mobile_number", "type"]
        combine = ""
        allconsvals = cons.strip().split(' ')
        for i in range(len(allconsvals)):
            allconsvals[i] = allconsvals[i].replace("_", " ")
        for i in range(len(allconsvals)):
            if allconsvals[i] != "null":
                combine += colname[i] + " = '" + allconsvals[i] + "' and "
        combine = combine.rstrip("and ")
        cur.execute("select " + cols + " from staff where " + combine)
        rows = cur.fetchall()
        data = pd.DataFrame(rows, columns=col_list)
        data.to_csv('select_cons_staff.csv')
        print(data)
    else:
        cur.execute("select " + cols + " from staff")
        rows = cur.fetchall()
        data = pd.DataFrame(rows, columns=col_list)
        data.to_csv('select_staff.csv')
        print(data)


def update_staff(cur):
    s = input("Enter update columns: ")
    allcols = s.strip().split(' ')
    for i in range(len(allcols)):
        allcols[i]=allcols[i].replace("_", " ")
    cols = ""
    colname = ["name", "age", "gender", "number", "supply_center", "mobile_number", "type"]
    for i in range(len(allcols)):
        if allcols[i] != "null":
            cols += colname[i] + " = '" + allcols[i] + "',"
    if cols != "":
        cols = cols.rstrip(",")
    cons = input("Enter update constraints: ")
    if cons != 'n':
        combine = ""
        allconsvals = cons.strip().split(' ')
        for i in range(len(allconsvals)):
            allconsvals[i] = allconsvals[i].replace("_", " ")
        for i in range(len(allconsvals)):
            if allconsvals[i] != "null":
                combine += colname[i] + " = '" + allconsvals[i] + "' and "
        combine = combine.rstrip("and ")
        cur.execute("update staff set " + cols + " where " + combine)
    else:
        cur.execute("update staff set " + cols)


def delete_staff(cur):
    s = input("Enter delete constraints: ")
    allcols = s.strip().split(' ')
    for i in range(len(allcols)):
        allcols[i]=allcols[i].replace("_", " ")
    cols = ""
    colname = ["name", "age", "gender", "number", "supply_center", "mobile_number", "type"]
    for i in range(len(allcols)):
        if allcols[i] != "null":
            cols += colname[i] + " = '" + allcols[i] + "' and "
    if cols != "":
        cols = cols.rstrip("and ")
        cur.execute("delete from staff where " + cols)


if __name__ == '__main__':
    conn = psycopg2.connect("host=localhost dbname=cs307_2 user=checker password=123456")
    cur = conn.cursor()
    operation = input()
    while operation != "q":
        if lower(operation) == 'c':
            add_staff(cur)
        if lower(operation) == 'r':
            select_staff(cur)
        if lower(operation) == 'u':
            update_staff(cur)
        if lower(operation) == 'd':
            delete_staff(cur)
        operation = input()
    conn.commit()
    conn.close()
