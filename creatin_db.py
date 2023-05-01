from datetime import datetime
from dateutil.relativedelta import relativedelta
import sqlite3
import os.path as path
from http.server import HTTPServer, CGIHTTPRequestHandler

BASE_DIR = path.dirname(path.abspath(__file__))
db_path = path.join(BASE_DIR, 'judge.db')
con = sqlite3.connect(db_path)
cur = con.cursor()


def cgi_init():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    httpd.serve_forever()


def create_db():
    defendant_table = """create table if not exists defendants(
    id_def integer primary key,
    fullname text not null,
    birthdate text not null,
    address text not null
    )
    """
    judge_table = """create table if not exists judges(
    id_judge integer primary key,
    fullname text not null,
    w_exp integer not null,
    closed_cases integer default 0
    )"""
    cases_table = """create table if not exists cases(
    id_case integer primary key,
    id_def integer not null,
    id_judge integer not null,
    start_date text not null,
    end_date text default null,
    guilty integer default null,
    info text,
    closed integer,
    foreign key (id_def) references defendants (id_def),
    foreign key (id_judge) references judges (id_judge)
    )
    """
    cur.execute(defendant_table)
    cur.execute(judge_table)
    cur.execute(cases_table)

    def_data = [
        ('Petrov I.V.', '2000-11-10', 'country, city, street, house'),
        ('Ivanov D.A.', '1969-04-02', 'country, city, street, house'),
        ('Chernov I.V.', '1985-07-23', 'country, city, street, house')
    ]
    judge_data = [
        ('Jimmy McGill', 0, ''),
        ('Dolores Umbridge', 60, 17),
        ('The Judge', 20, 100)
    ]
    case_data = [
        (1, 2, datetime.now(), None, None, 'main info', 0),
        (2, 2, datetime.now() - relativedelta(years=14), datetime.now() - relativedelta(years=13), 1, 'main info', 1),
        (3, 3, datetime.now() - relativedelta(years=2), None, None, 'main info', 0),
        (3, 3, datetime.now() - relativedelta(months=5), datetime.now() - relativedelta(months=4), 0, 'main info', 1)
    ]
    cur.executemany('insert into defendants(fullname, birthdate, address) values(?,?,?)', def_data)
    con.commit()
    cur.executemany('insert into judges(fullname, w_exp, closed_cases) values(?,?,?)', judge_data)
    con.commit()
    cur.executemany(
        'insert into cases(id_def, id_judge, start_date, end_date, guilty, info, closed) values(?,?,?,?,?,?,?)',
        case_data
    )
    con.commit()

    # вывод судей которые закрыли хотябы одно дело(по тем что в бд)
    for row in cur.execute('''select * from judges
                           where id_judge in (select id_judge from cases
                           where closed = 1)'''):
        print(row)
    cur.execute("select * from defendants where strftime('%Y',birthdate)>'1990'")
    print(cur.fetchall())
    for row in cur.execute("select * from defendants where id_def in (select id_def from cases where guilty=0)"):
        print(row)
    con.close()


if __name__ == '__main__':
    # create_db()
    # print('База создана')
    cgi_init()
