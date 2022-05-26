import csv
import psycopg2
from psycopg2 import extras
from typing import List

from psycopg2.pool import ThreadedConnectionPool

pool = ThreadedConnectionPool(5, 100, "dbname=cs307_2 user=checker password=123456 host=localhost")  # 创建连接池连接
conn = pool.getconn()
# conn = psycopg2.connect("host=localhost dbname=cs307_2 user=checker password=123456")
cur = conn.cursor()


def load_data(cur, path, table, page_size=100):
    list = []
    with open(path, 'r', encoding='utf-8') as f:
        f.readline()
        reader = csv.reader(f)
        for row in reader:
            one_record = []
            c = True
            for item in row:
                if c:
                    c = False
                    continue
                if item != '':
                    one_record.append(item)
                else:
                    one_record.append(None)
            list.append(one_record)
    psycopg2.extras.execute_values(cur, "INSERT INTO " + table + " VALUES %s;", list, page_size=page_size)


def importFour():
    cur.execute(
        """truncate table center,contract,enterprise,model,"order",staff,stock,storage cascade;""")
    path_pre = r"C:\Users\21414\PycharmProjects\database\proj2\Flask\bootstrap\Lin\files"
    page_size = 1000
    load_data(cur, path_pre + '/center.csv', 'center', page_size)
    load_data(cur, path_pre + '/enterprise.csv', 'enterprise', page_size)
    load_data(cur, path_pre + '/model.csv', 'model', page_size)
    load_data(cur, path_pre + '/staff.csv', 'staff', page_size)


def end():
    conn.commit()
    # conn.close()
    # close all connection
    pool.putconn(conn, key=None, close=False)  # 这里close设置为true则会从连接池中关闭conn对象的连接
    pool.closeall()  # 会关闭连接池内所有的连接

def stockIn():
    with open(r'files\in_stoke_test.csv', 'r',
              encoding='utf-8') as f:
        f.readline()
        reader = csv.reader(f)
        for row in reader:
            try:
                supply_center = row[1]
                product_model = row[2]
                supply_staff_num = row[3]
                date = row[4]
                purchase_price = row[5]
                quantity = row[6]
                if whetherSupplyCenterExist(supply_center) and \
                        whetherProductModelExist(product_model) and \
                        whetherStaffExist(supply_staff_num) and \
                        getCenterByStaffNumber(supply_staff_num) == supply_center and \
                        getStaffTypeByStaffNumber(supply_staff_num) == 'Supply Staff':
                    cur.execute("""insert into stock (supply_center, product_model, supply_staff_number, date, purchase_price, quantity) 
                                values ('%s', '%s', '%s', to_date('%s', 'yyyy-mm-dd'), '%s', '%s');"""
                                % (supply_center, product_model, supply_staff_num, date, purchase_price, quantity))
                    # update storage
                    cur.execute("""select s.quantity
                                    from storage s
                                    where s.product_model = '%s'
                                      and s.supply_center = '%s';"""
                                % (product_model, supply_center))
                    ans = cur.fetchall()
                    conn.commit()
                    if len(ans) == 0:
                        cur.execute("""insert into storage (supply_center, product_model, quantity) 
                                    values ('%s', '%s', '%s');"""
                                    % (supply_center, product_model, quantity))
                    else:
                        cur.execute("""update storage
                                        set quantity = %d
                                        where supply_center = '%s'
                                          and product_model = '%s';""" % (
                            int(ans[0][0]) + int(quantity), supply_center, product_model))
            except psycopg2.Error as e:
                print(e)
            continue
    return


def whetherStaffExist(staff_number: str) -> bool:
    cur.execute("""select count(*) from staff where number = '%s';""" % staff_number)
    ans = int(cur.fetchall()[0][0]) > 0
    conn.commit()
    return ans


def whetherProductModelExist(product_model: str) -> bool:
    cur.execute("""select count(*) from model where model.model = '%s';""" % product_model)
    ans = int(cur.fetchall()[0][0]) > 0
    conn.commit()
    return ans


def whetherSupplyCenterExist(supply_center: str) -> bool:
    cur.execute("""select count(*) from center where name = '%s';""" % supply_center)
    ans = int(cur.fetchall()[0][0]) > 0
    conn.commit()
    return ans


def getStaffTypeByStaffNumber(staff_number: str) -> str:
    cur.execute("""select type from staff where number = '%s';""" % staff_number)
    ans = cur.fetchall()
    conn.commit()
    if len(ans) == 0:
        return ''
    else:
        return ans[0][0]


def getCenterByStaffNumber(staff_number: str) -> str:
    cur.execute("""select supply_center from staff where number = '%s';""" % staff_number)
    ans = cur.fetchall()
    conn.commit()
    if len(ans) == 0:
        return ''
    else:
        return ans[0][0]


def placeOrder():
    f = open(r'files\task2_test_data_final_public.tsv', 'r', encoding='utf-8')
    f.readline()
    reader = csv.reader(f)
    for row in reader:
        try:
            content = row[0].split('\t')
            contract_num = content[0]
            enterprise = content[1]
            product_model = content[2]
            quantity = int(content[3])
            contract_manager_num = content[4]
            contract_date = content[5]
            estimated_delivery_date = content[6]
            lodgement_date = content[7]
            salesman_num = content[8]
            contract_type = content[9]
            if whetherStorageEnough(enterprise, product_model, quantity) and \
                    getStaffTypeByStaffNumber(salesman_num) == 'Salesman':
                if not whetherContractNumberExist(contract_num):
                    cur.execute("""insert into contract values ('%s', '%s', '%s', '%s', '%s');"""
                                % (contract_num, contract_manager_num, enterprise, contract_type, contract_date))
                    # print('insert into contract !')
                if whetherContractInformationCorrect(contract_num, enterprise, contract_manager_num, contract_date,
                                                     contract_type):
                    cur.execute("""insert into "order" values ('%s', '%s', '%s', '%s', '%s', '%s');"""
                                % (contract_num, product_model, salesman_num, quantity, estimated_delivery_date,
                                   lodgement_date))
                    # print("insert into order !")
                    # update storage
                    cur.execute("""select e.supply_center from enterprise e where e.name = '%s';"""
                                % enterprise)
                    ans = cur.fetchall()
                    conn.commit()
                    supply_center = ans[0][0]
                    cur.execute("""select s.quantity
                                from storage s
                                where s.product_model = '%s'
                                  and s.supply_center = '%s';"""
                                % (product_model, supply_center))
                    ans = cur.fetchall()
                    conn.commit()
                    new_quantity = str(int(ans[0][0]) - quantity)
                    cur.execute("""update storage
                                    set quantity = {}
                                    where supply_center = '{}'
                                      and product_model = '{}';""" .format(
                        new_quantity, supply_center, product_model))
        except psycopg2.Error as e:
            print(e)
            conn.rollback()
            continue
    return


def whetherContractNumberExist(contract_number: str) -> bool:
    cur.execute("""select count(*)
                    from contract
                    where contract_number = '%s';""" % contract_number)
    ans = int(cur.fetchall()[0][0]) > 0
    conn.commit()
    return ans


def whetherContractInformationCorrect(contract_number: str, enterprise: str, contract_manager: str, contract_date: str,
                                      contract_type: str) -> bool:
    cur.execute("""select count(*)
                    from contract
                    where contract_number = '%s'
                      and contract_manager_number = '%s'
                      and enterprise_name = '%s'
                      and contract_type = '%s'
                      and contract_date = '%s';"""
                % (contract_number, contract_manager, enterprise, contract_type, contract_date))
    ans = cur.fetchall()
    conn.commit()
    if len(ans) == 0:
        return False
    else:
        return int(ans[0][0]) > 0


def whetherStorageEnough(enterprise: str, product_model: str, quantity: int) -> bool:
    cur.execute("""select s.quantity
                    from storage s
                    where s.product_model = '%s'
                      and s.supply_center in (select e.supply_center
                                              from enterprise e
                                              where e.name = '%s');"""
                % (product_model, enterprise))
    ans = cur.fetchall()
    conn.commit()
    if len(ans) == 0:
        return False
    else:
        return int(ans[0][0]) >= quantity


def updateOrder():
    f = open(r'files\update_final_test.tsv', 'r', encoding='utf-8')
    f.readline()
    reader = csv.reader(f)
    for row in reader:
        try:
            content = row[0].split('\t')
            contract_number = content[0]
            product_model = content[1]
            salesman_number = content[2]
            quantity = int(content[3])
            estimate_delivery_date = content[4]
            lodgement_date = content[5]
            if whetherSalesmanHasOrder(salesman_number, contract_number, product_model):

                cur.execute("""select s.quantity
                                        from storage s
                                        where s.product_model = '%s'
                                          and s.supply_center = (select e.supply_center
                                                                 from enterprise e
                                                                 where e.name = (select c.enterprise_name
                                                                                 from contract c
                                                                                 where c.contract_number = '%s'));"""
                            % (product_model, contract_number))
                res = cur.fetchall()
                conn.commit()
                if len(res) == 0:
                    continue
                else:
                    original_storage_quantity = int(res[0][0])

                cur.execute("""select o.quantity
                                from "order" o
                                where o.contract_number = '%s'
                                  and product_model = '%s'
                                  and salesman_number = '%s';""" % (contract_number, product_model, salesman_number))
                res = cur.fetchall()
                conn.commit()
                if len(res) == 0:
                    continue
                else:
                    original_order_quantity = int(res[0][0])
                new_storage_quantity = original_storage_quantity + original_order_quantity - quantity

                if new_storage_quantity >= 0:
                    cur.execute("""update "order"
                                    set quantity                = %d,
                                        estimated_delivery_date = '%s',
                                        lodgement_date          = '%s'
                                    where contract_number = '%s'
                                      and product_model = '%s'
                                      and salesman_number = '%s';"""
                                % (quantity, estimate_delivery_date, lodgement_date, contract_number, product_model,
                                   salesman_number))
                    cur.execute("""update storage s
                                    set quantity = %d
                                    where s.product_model = '%s'
                                      and s.supply_center = (select e.supply_center
                                                             from enterprise e
                                                             where e.name = (select c.enterprise_name
                                                                             from contract c
                                                                             where c.contract_number = '%s'));"""
                                % (new_storage_quantity, product_model, contract_number))
                    if quantity == 0:
                        cur.execute("""delete
                                        from "order"
                                        where product_model = '%s'
                                          and contract_number = '%s'
                                          and salesman_number = '%s';""" % (
                            product_model, contract_number, salesman_number))
        except psycopg2.Error as e:
            print(e)
        continue
    return


def whetherSalesmanHasOrder(salesman_number: str, contract_number: str, product_model: str) -> bool:
    cur.execute("""select count(*)
                    from "order"
                    where salesman_number = '%s'
                      and product_model = '%s'
                      and contract_number = '%s';""" % (salesman_number, product_model, contract_number))
    ans = cur.fetchall()[0][0] > 0
    conn.commit()
    return ans


def deleteOrder():
    f = open(r'files\delete_final.tsv', 'r', encoding='utf-8')
    f.readline()
    reader = csv.reader(f)
    for row in reader:
        content = row[0].split(' ')
        contract_number = content[0]
        salesman_number = content[1]
        seq = content[2]
        cur.execute("""select t2.product_model
                        from (select *
                              from (select *, row_number() over (order by estimated_delivery_date,product_model) as row_number
                                    from "order" o1
                                    where o1.salesman_number = '%s'
                                      and o1.contract_number = '%s') t1
                              where t1.row_number = %s) t2""" % (salesman_number, contract_number, seq))
        res = cur.fetchall()
        conn.commit()
        if len(res) == 0:
            continue
        else:
            product_model = res[0][0]

        cur.execute("""select e.supply_center
                        from enterprise e
                        where e.name =
                              (select enterprise_name
                               from contract
                               where contract_number = '%s');""" % contract_number)
        res = cur.fetchall()
        conn.commit()
        if len(res) == 0:
            continue
        else:
            supply_center = res[0][0]

        cur.execute("""select quantity
                        from "order"
                        where contract_number = '%s'
                          and product_model = '%s'
                          and salesman_number = '%s';""" % (contract_number, product_model, salesman_number))
        res = cur.fetchall()
        conn.commit()
        if len(res) == 0:
            continue
        else:
            order_quantity = int(res[0][0])

        cur.execute("""select s.quantity
                        from storage s
                        where s.supply_center = '%s'
                          and s.product_model = '%s';""" % (supply_center, product_model))
        res = cur.fetchall()
        conn.commit()
        if len(res) == 0:
            continue
        else:
            initial_storage_quantity = int(res[0][0])
        new_storage_quantity = initial_storage_quantity + order_quantity

        cur.execute("""delete
                        from "order"
                        where product_model = '%s'
                          and contract_number = '%s'
                          and salesman_number = '%s';""" % (product_model, contract_number, salesman_number))
        cur.execute("""update storage
                        set quantity = %d
                        where supply_center = '%s'
                          and product_model = '%s';""" % (new_storage_quantity, supply_center, product_model))
    return


def getAllStaffCount():
    cur.execute("""select type, count(*)
                    from staff
                    group by type;""")
    ans = cur.fetchall()
    conn.commit()
    return ans


def getContractCount() -> str:
    cur.execute("""select count(*)
                    from contract;""")
    ans = cur.fetchall()[0][0]
    conn.commit()
    return ans


def getOrderCount() -> str:
    cur.execute("""select count(*)
                    from "order";""")
    ans = cur.fetchall()[0][0]
    conn.commit()
    return ans


def getNeverSoldProductCount() -> str:
    cur.execute("""select count(distinct product_model)
                    from storage
                    where quantity > 0
                      and product_model in (select product_model
                                            from storage
                                            except
                                            select product_model
                                            from "order"
                                                     join contract on "order".contract_number = contract.contract_number
                                            where contract.contract_type = 'Finished');""")
    ans = cur.fetchall()[0][0]
    conn.commit()
    return ans


def getFavoriteProductModel():
    cur.execute("""with t2 as (with t1 as (select o.product_model, sum(o.quantity) as total_sale
                                                from "order" o
                                                         join contract c on o.contract_number = c.contract_number
                                                where c.contract_type = 'Finished'
                                                group by o.product_model)
                                    select t1.*, rank() over (order by t1.total_sale desc ) as r
                                    from t1)
                        select t2.product_model, t2.total_sale
                        from t2
                        where t2.r = 1;""")
    res = cur.fetchall()
    conn.commit()
    return res


def getAvgStockByCenter():
    cur.execute("""with count as (select supply_center, count(*) as cnt from storage group by supply_center)
                    select distinct storage.supply_center, round(1.0 * sum(quantity) over (partition by storage.supply_center) / cnt,1) as average
                    from storage
                             join count on count.supply_center = storage.supply_center
                    order by storage.supply_center;""")
    ans = cur.fetchall()
    conn.commit()
    return ans


def getProductByNumber(model_number: str):
    cur.execute("""select s.supply_center, s.product_model, s.quantity
                    from storage s
                             join model on s.product_model = model.model
                    where model.number = '%s';""" % model_number)
    ans = cur.fetchall()
    conn.commit()
    return ans


def getContractInfo(contract_number: str) -> (List[str], List[List[str]]):
    cur.execute("""select c.contract_number,
                           c.enterprise_name,
                           (select s.name from staff s where s.number = c.contract_manager_number) as contract_manager_name,
                           (select e.supply_center from enterprise e where e.name = c.enterprise_name) as supply_center
                    from contract c
                    where c.contract_number = '%s';""" % contract_number)
    res = cur.fetchall()
    conn.commit()
    list_contract = [str]
    if len(res) != 0:
        list_contract = res[0]
    cur.execute("""select o.product_model,
                           (select s.name from staff s where s.number = o.salesman_number) as salesman_name,
                           o.quantity,
                           (select m.unit_price from model m where m.model = o.product_model) as uunit_price,
                           o.estimated_delivery_date,
                           o.lodgement_date
                    from "order" o
                    where o.contract_number = '%s';""" % contract_number)
    res = cur.fetchall()
    conn.commit()
    list_order = [[str]]
    if len(res) != 0:
        list_order = res
    return list_contract, list_order


def oneStepExport(product_number_list: [str], contract_number_list: [str]) -> str:
    final_output = ''
    # Q6
    q6_list = getAllStaffCount()
    length_6 = 0
    for i in q6_list:
        length_6 = max(length_6, len(i[0]))
    length_6 += 5
    output_6 = 'Q6\n'
    for i in q6_list:
        output_6 += ('{type_name:<' + str(length_6) + '}{num}\n').format(type_name=i[0], num=i[1])
    final_output += output_6

    # Q7
    q7_num = getContractCount()
    output_7 = 'Q7 %s\n' % q7_num
    final_output += output_7

    # Q8
    q8_num = getOrderCount()
    output_8 = 'Q8 %s\n' % q8_num
    final_output += output_8

    # Q9
    q9_num = getNeverSoldProductCount()
    output_9 = 'Q9 %s\n' % q9_num
    final_output += output_9

    # Q10
    q10_list = getFavoriteProductModel()
    output_10 = 'Q10\n'
    length_10 = 0
    for row in q10_list:
        length_10 = max(length_10, len(row[0]))
    length_10 += 5
    for row in q10_list:
        output_10 += ('{model:<' + str(length_10) + '}{num}\n').format(model=row[0], num=row[1])
    final_output += output_10

    # Q11
    q11_list = getAvgStockByCenter()
    length_11 = 0
    for row in q11_list:
        length_11 = max(length_11, len(row[0]))
    length_11 += 5
    output_11 = 'Q11\n'
    for row in q11_list:
        output_11 += ('{center:<' + str(length_11) + '}{num}\n').format(center=row[0], num=row[1])
    final_output += output_11

    # Q12
    for product_number in product_number_list:
        output_12 = 'Q12\n'
        q12_list = getProductByNumber(product_number)
        length0_12 = 13
        length1_12 = 13
        for row in q12_list:
            length0_12 = max(length0_12, len(row[0]))
            length1_12 = max(length1_12, len(row[1]))
        length0_12 += 5
        length1_12 += 5
        output_12 += ('{center:<' + str(length0_12) + '}{model:<' + str(length1_12) + '}{quantity}\n').format(
            center='supply_center', model='product_model', quantity='quantity')
        for row in q12_list:
            output_12 += ('{center:<' + str(length0_12) + '}{model:<' + str(length1_12) + '}{quantity}\n').format(
                center=row[0], model=row[1], quantity=row[2])
        final_output += output_12

    # Q13
    for contract_number in contract_number_list:
        q13_list1, q13_list2 = getContractInfo(contract_number)
        output_13 = 'Q13\n'
        if len(q13_list1) > 3:
            output_13 += 'contract_number: {}\n' \
                         'enterprise: {}\n' \
                         'manager: {}\n' \
                         'supply_center: {}\n' \
                .format(q13_list1[0], q13_list1[1], q13_list1[2], q13_list1[3])
        length0_13 = 13
        length1_13 = 8
        length2_13 = 8
        length3_13 = 10
        length4_13 = 22

        if len(q13_list2[0]) == 6:
            for row in q13_list2:
                length0_13 = max(length0_13, len(str(row[0])))
                length1_13 = max(length1_13, len(str(row[1])))
                length2_13 = max(length2_13, len(str(row[2])))
                length3_13 = max(length3_13, len(str(row[3])))
                length4_13 = max(length4_13, len(str(row[4])))
            length0_13 += 5
            length1_13 += 5
            length2_13 += 5
            length3_13 += 5
            length4_13 += 5
            output_13 += (
                    '{:<' + str(length0_13) + '}{:<' + str(length1_13) + '}{:<' + str(length2_13) + '}{:<' + str(
                length3_13) + '}{:<' + str(length4_13) + '}{}\n').format(
                'product_model', 'salesman', 'quantity', 'unit_price', 'estimate_delivery_date', 'lodgement_date'
            )
            for row in q13_list2:
                output_13 += (
                        '{0:<' + str(length0_13) + '}{1:<' + str(length1_13) + '}{2:<' + str(length2_13) + '}{3:<' + str(
                    length3_13) + '}{4:<' + str(length4_13) + '}{5}\n').format(
                    row[0], row[1], row[2], row[3], str(row[4]), str(row[5])
                )
        final_output += output_13

    return final_output


if __name__ == '__main__':
    product_number_list = ['A50L172']
    contract_number_list = ['CSE0000106', 'CSE0000209', 'CSE0000306']
    importFour()
    conn.commit()
    stockIn()
    conn.commit()
    placeOrder()
    conn.commit()
    updateOrder()
    conn.commit()
    deleteOrder()
    # operation = input()
    # while operation != "q":
    #     if operation == "12":
    #         a = input()
    #         print(getProductByNumber(a))
    #     if operation == "13":
    #         a = input()
    #         print(getContractInfo(a))
    #     if operation == "6":
    #         getStaffTypeByStaffNumber()
    #     operation = input()
    print(getProductByNumber("FK39705"))
    print(getProductByNumber("E8T2037"))
    print(getProductByNumber("T28310Y"))
    print(getContractInfo("CSE0000326"))
    print(getContractInfo("CSE0000420"))
    # print(getProductByNumber("F6L2495"))
    # conn.commit()
    conn.commit()
    # conn.close()    # print(getProductByNumber("F6L2495"))
    # f = open('my_output.txt', 'w', encoding='utf-8')
    # f.write(oneStepExport(product_number_list, contract_number_list))
    # f.close()
    end()
