import sqlite3

conn = sqlite3.connect('sellingitem.db', check_same_thread=False)

cur = conn.cursor()

cur.execute(""" CREATE TABLE IF NOT EXISTS selling(
            Number_item TEXT,
            Price INT,
            Day INT,
            Month INT,
            Year INT,
            Delivery_price INT,
            Full_and_partial TEXT);
""")
conn.commit()


def plus_data(data):
    try:
        if data[0].isdigit():
            cur.execute(
                f"SELECT Number_item, Full_and_partial FROM selling WHERE Number_item = '{data[0]}'")
            one = cur.fetchone()
            conn.commit()
            if one == None or one[1] == 'частичная':
                cur.execute(
                    f"INSERT INTO selling(Number_item, Price, Day, Month, Year, Delivery_price, Full_and_partial) VALUES(?, ?, ?, ?, ?, ?, ?)", data)
                conn.commit()
                return True
            else:
                return False
        else:
            cur.execute(
                f"INSERT INTO selling(Number_item, Price, Day, Month, Year, Delivery_price, Full_and_partial) VALUES(?, ?, ?, ?, ?, ?, ?)", data)
            conn.commit()
            return True
    except sqlite3.Error as e:
        print('Все хуевое, а именно:', e)
        return False


def minus_data(num_item):
    try:
        cur.execute(f"SELECT * FROM selling WHERE Number_item = '{num_item}'")
        one_rezult = cur.fetchone()
        if one_rezult != None:
            cur.execute(
                f"DELETE FROM selling WHERE Number_item = + '{num_item}'")
            conn.commit()
            return True
        else:
            return False
    except sqlite3.Error as y:
        print('Все хуево с удалением данных, а именно:', y)
        return False


def report(month, year):
    try:
        profit = 0
        delivery = 0
        cur.execute(
            f"SELECT Price, Delivery_price FROM selling WHERE Month = '{month}' and Year = '{year}'")
        searchable = cur.fetchall()
        conn.commit()
        for cout in range(len(searchable)):
            profit += searchable[cout][0]
            delivery += searchable[cout][1]
        summ = len(searchable)
        return summ, profit, delivery

    except sqlite3.Error as v:
        print('Все хуево с отчетом, а именно:', v)
        summ = -1
        profit = -1
        return summ, profit
