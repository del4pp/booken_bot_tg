import sqlite3

conn = sqlite3.connect("booken.db", check_same_thread=False)
cursor = conn.cursor()

def inser_book_in_db(book_link):
    sql = 'insert into book_url(product_link)values(\'{0}\');'.format(book_link)
    cursor.execute(sql)
    conn.commit()

def check_new_book(book_link):
    sql = 'select product_link from book_url where product_link = \'{0}\';'.format(book_link)
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    if result:
        return result
    else:
        return None

def insert_bugs(bug_desk):
    sql = 'insert into bugs(error_desc)values(\'{0}\')'.format(str(bug_desk))
    cursor.execute(sql)
    conn.commit()