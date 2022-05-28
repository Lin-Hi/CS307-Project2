import csv
import psycopg2
from psycopg2 import extras
from typing import List

from psycopg2.pool import ThreadedConnectionPool

dbname = 'cs307_2'
password = '123456'
user = 'checker'

pool = ThreadedConnectionPool(5, 100,
                              "dbname={} user={} password={} host=localhost".format(dbname, user, password))  # 创建连接池连接
conn = pool.getconn()
# conn = psycopg2.connect("host=localhost dbname=cs307_2 user=checker password=123456")
cur = conn.cursor()


def whetherUserExist(user_name: str) -> bool:
    cur.execute("""select count(*)
from pg_catalog.pg_user
where usename = '%s';""" % user_name)
    ans = int(cur.fetchall()[0][0]) > 0
    conn.commit()
    return ans


def addSalesmanUser(salesman_num: str):
    if whetherUserExist('s{}'.format(salesman_num)):
        return
    cur.execute("""create user s{}};
alter user s{} password '123456';
grant select on "order" to s{};
create policy salesman_order on "order" for select to s{} using (salesman_number = '{}');
alter table "order" enable row level security ;"""
                .format(salesman_num, salesman_num, salesman_num, salesman_num, salesman_num))
    conn.commit()
    return


def addManagerUser(manager_num: str):
    if whetherUserExist('c{}'.format(manager_num)):
        return
    cur.execute("""create user c{};
alter user c{} password '123456';

grant select on "order" to c{};
grant select on contract to c{};

create policy manager_order
    on "order"
    for select to c{}
    using (contract_number in (select contract.contract_number
                               from contract
                               where contract_manager_number = '{}'));
alter table "order"
    enable row level security;

create policy manager_contract
    on contract
    for select to c{}
    using (contract_manager_number = '{}');
alter table contract
    enable row level security;""".format(manager_num, manager_num, manager_num, manager_num,
                                         manager_num, manager_num, manager_num, manager_num))
    conn.commit()
    return


def addTopUser(user_number: str):
    if whetherUserExist('t{}'.format(user_number)):
        return
    cur.execute("""create user t%s superuser password '123456';""" % user_number)


def changeUser(user_name):
    if not whetherUserExist(user_name):
        return
    user = user_name
    pool = ThreadedConnectionPool(5, 100, "dbname={} user={} password={} host=localhost"
                                  .format(dbname, user, password))
    conn = pool.getconn()
    cur = conn.cursor()
    return


if __name__ == '__main__':
    print(1)
