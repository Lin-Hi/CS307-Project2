import os
import psycopg2
from flask_bootstrap import Bootstrap
import sys

from psycopg2.pool import ThreadedConnectionPool

sys.path.append(r'C:\Users\21414\PycharmProjects\database\proj2')
from flask import Flask, render_template, request, url_for, session, flash, make_response
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = '42'
bootstrap = Bootstrap(app)
import Lin.function as api


def get_db_connection():
    # conn = psycopg2.connect(host='localhost',
    #                         database='cs307_2',
    #                         user='checker',
    #                         password='123456')
    pool = ThreadedConnectionPool(5, 100, "dbname=cs307_2 user=checker password=123456 host=localhost")  # 创建连接池连接
    conn = pool.getconn()
    return conn


@app.route('/enterprise/insert/', methods=['GET', 'POST'])
def enterprise_insert():
    from form_enterprise_C import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        supply_center = request.form['supply_center']
        industry = request.form['industry']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("insert into enterprise (name" + (
            ', country' if country != '' else '') + (
                        ', city' if city != '' else '') + (
                        ', supply_center' if supply_center != '' else '') + (
                        ', industry' if industry != '' else '') + ") values (" + ("'" + name + "'"
                                                                                  + ((
                                                                                             ', \'' + country + '\'') if country != '' else '')
                                                                                  + ((
                                                                                             ', \'' + city + '\'') if city != '' else '')
                                                                                  + ((
                                                                                             ', \'' + supply_center + '\'') if supply_center != '' else '')
                                                                                  + ((
                                                                                             ', \'' + industry + '\'') if industry != '' else '')
                                                                                  + ")"))
        conn.commit()
    return render_template("ent_insert.html",
                           form=form)


@app.route('/staff/insert/', methods=['GET', 'POST'])
def staff_insert():
    from form_staff_C import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        number = request.form['number']
        supply_center = request.form['supply_center']
        mobile_number = request.form['mobile_number']
        type = request.form['type']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("insert into staff (name" + (
            ', age' if age != '' else '') + (
                        ', gender' if gender != '' else '') + (
                        ', number' if number != '' else '') + (
                        ', supply_center' if supply_center != '' else '') + (
                        ', mobile_number' if mobile_number != '' else '') + (
                        ', type' if type != '' else '') +
                    ") values (" + ("'" + name + "'" + ((
                                                                ', ' + age + ' ') if age != '' else '') + ((
                                                                                                                   ', \'' + gender + '\'') if gender != '' else '') + (
                                        (
                                                ', \'' + number + '\'') if number != '' else '') + ((
                                                                                                            ', \'' + supply_center + '\'') if supply_center != '' else '') + (
                                        (
                                                ', \'' + mobile_number + '\'') if mobile_number != '' else '') + ((
                                                                                                                          ', \'' + type + '\'') if type != '' else '')
                                    + ")"))
        conn.commit()
    return render_template("staff_insert.html",
                           form=form)


@app.route('/model/insert/', methods=['GET', 'POST'])
def model_insert():
    from form_model_C import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        number = request.form['number']
        model = request.form['model']
        name = request.form['name']
        unit_price = request.form['unit_price']
        conn = get_db_connection()
        cur = conn.cursor()
        col = (' number,' if number != '' else '') + (
            ' model, ') + (
                  ' name,' if name != '' else '') + (
                  ' unit_price,' if unit_price != '' else '')
        col = col.rstrip(",")
        cur.execute("insert into model (" + col +
                    ") values (" + ((("'" + number + "'") if number != '' else '') + ((
                ',  \'' + model + ' \' ')) + ((
                                                      ', \'' + name + '\'') if name != '' else '') + ((
                                                                                                              ', ' + unit_price + '') if unit_price != '' else '')
                                    + ")"))
        conn.commit()
    return render_template("model_insert.html",
                           form=form)


@app.route('/center/insert/', methods=['GET', 'POST'])
def center_insert():
    from form_center_C import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("insert into center ( name ) values (" + ("'" + name + "'" + ")"))
        conn.commit()
    return render_template("center_insert.html",
                           form=form)


@app.route('/enterprise/delete/', methods=['GET', 'POST'])
def enterprise_delete():
    from form_enterprise_D import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        supply_center = request.form['supply_center']
        industry = request.form['industry']
        conn = get_db_connection()
        cur = conn.cursor()
        sql = ("delete from enterprise where " +
               ((' name=\'' + name + "' and") if name != '' else '') +
               ((' country=\'' + country + "' and") if country != '' else '') +
               ((' city=\'' + city + "' and") if city != '' else '') +
               ((' supply_center=\'' + supply_center + "' and") if supply_center != '' else '') +
               ((' industry=\'' + industry + "' and") if industry != '' else '') +
               "")
        sql = sql.rstrip(" and")
        cur.execute(sql)
        conn.commit()
    return render_template("ent_delete.html",
                           form=form)


@app.route('/staff/delete/', methods=['GET', 'POST'])
def staff_delete():
    from form_staff_D import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        number = request.form['number']
        supply_center = request.form['supply_center']
        mobile_number = request.form['mobile_number']
        type = request.form['type']
        conn = get_db_connection()
        cur = conn.cursor()
        sql = ("delete from staff where " +
               ((' name=\'' + name + "' and") if name != '' else '') +
               (('age=' + age + " and") if age != '' else '') +
               ((' gender=\'' + gender + "' and") if gender != '' else '') +
               ((' number=\'' + number + "' and") if number != '' else '') +
               ((' supply_center=\'' + supply_center + "' and") if supply_center != '' else '') +
               ((' mobile_number=\'' + mobile_number + "' and") if mobile_number != '' else '') +
               ((' type=\'' + type + "' and") if type != '' else '') +
               "")
        sql = sql.rstrip('and')
        cur.execute(sql)
        conn.commit()
    return render_template("staff_delete.html",
                           form=form)


@app.route('/model/delete/', methods=['GET', 'POST'])
def model_delete():
    from form_model_D import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        number = request.form['number']
        model = request.form['model']
        name = request.form['name']
        unit_price = request.form['unit_price']
        conn = get_db_connection()
        cur = conn.cursor()
        sql = ("delete from model where " +
               ((' number=\'' + number + "' and") if number != '' else '') +
               ((' model=\'' + model + "' and") if model != '' else '') +
               ((' name=\'' + name + "' and") if name != '' else '') +
               ((' unit_price=' + unit_price + " and") if unit_price != '' else '') +
               "")
        sql = sql.rstrip(" and")
        cur.execute(sql)
        conn.commit()
    return render_template("model_delete.html",
                           form=form)


@app.route('/center/delete/', methods=['GET', 'POST'])
def center_delete():
    from form_center_D import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        sql = ("delete from center where " +
               (' name=\'' + name + "'") +
               "")
        cur.execute(sql)
        conn.commit()
    return render_template("center_delete.html",
                           form=form)


@app.route('/enterprise/update/', methods=['GET', 'POST'])
def enterprise_update():
    from form_enterprise_U import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        supply_center = request.form['supply_center']
        industry = request.form['industry']
        conn = get_db_connection()
        cur = conn.cursor()
        if (name != '') | (country != '') | (city != '') | (supply_center != '') | (industry != ''):
            allcols = [name, country, city, supply_center, industry]
            cols = ""
            colname = ["name", "country", "city", "supply_center", "industry"]
            for i in range(len(allcols)):
                if allcols[i] != "":
                    cols += colname[i] + " = '" + allcols[i] + "',"
            if cols != "":
                cols = cols.rstrip(",")
            constraint = request.form['constraint']
            if constraint != '2':
                combine = ""
                allconsvals = [request.form['name_filter'], request.form['country_filter'], request.form['city_filter'],
                               request.form['supply_center_filter'], request.form['industry_filter']]
                for i in range(len(allconsvals)):
                    if allconsvals[i] != "":
                        combine += colname[i] + " = '" + allconsvals[i] + "' and "
                combine = combine.rstrip("and ")
                cur.execute("update enterprise set " + cols + " where " + combine)
            else:
                cur.execute("update enterprise set " + cols)
            conn.commit()
    return render_template("ent_update.html",
                           form=form)


@app.route('/staff/update/', methods=['GET', 'POST'])
def staff_update():
    from form_staff_U import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        number = request.form['number']
        supply_center = request.form['supply_center']
        mobile_number = request.form['mobile_number']
        type = request.form['type']
        conn = get_db_connection()
        cur = conn.cursor()
        if (name != '') | (age != '') | (gender != '') | (number != '') | (supply_center != '') | (
                mobile_number != '') | (type != ''):
            allcols = [name, age, gender, number, supply_center, mobile_number, type]
            cols = ""
            colname = ["name", "age", "gender", "number", "supply_center", "mobile_number", "type"]
            for i in range(len(allcols)):
                if allcols[i] != "":
                    if colname[i] == 'age':
                        cols += colname[i] + " = " + allcols[i] + ","
                    else:
                        cols += colname[i] + " = '" + allcols[i] + "',"
            if cols != "":
                cols = cols.rstrip(",")
            constraint = request.form['constraint']
            if constraint != '2':
                combine = ""
                allconsvals = [request.form['name_filter'], request.form['age_filter'], request.form['gender_filter'],
                               request.form['number_filter'], request.form['supply_center_filter'],
                               request.form['mobile_number_filter'], request.form['type_filter']]
                for i in range(len(allconsvals)):
                    if allconsvals[i] != "":
                        if colname[i] == "age":
                            combine += colname[i] + " = " + allconsvals[i] + " and "
                        else:
                            combine += colname[i] + " = '" + allconsvals[i] + "' and "
                combine = combine.rstrip("and ")
                cur.execute("update staff set " + cols + " where " + combine)
            else:
                cur.execute("update staff set " + cols)
            conn.commit()
    return render_template("staff_update.html",
                           form=form)


@app.route('/model/update/', methods=['GET', 'POST'])
def model_update():
    from form_model_U import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        number = request.form['number']
        model = request.form['model']
        name = request.form['name']
        unit_price = request.form['unit_price']
        conn = get_db_connection()
        cur = conn.cursor()
        if (number != '') | (model != '') | (name != '') | (unit_price != ''):
            allcols = [number, model, name, unit_price]
            cols = ""
            colname = ["number", "model", "name", "unit_price"]
            for i in range(len(allcols)):
                if allcols[i] != "":
                    if colname[i] == 'unit_price':
                        cols += colname[i] + " = " + allcols[i] + ", "
                    else:
                        cols += colname[i] + " = '" + allcols[i] + "', "
            if cols != "":
                cols = cols.rstrip(", ")
            constraint = request.form['constraint']
            if constraint != '2':
                combine = ""
                allconsvals = [request.form['number_filter'], request.form['model_filter'], request.form['name_filter'],
                               request.form['unit_price_filter']]
                for i in range(len(allconsvals)):
                    if allconsvals[i] != "":
                        if colname[i] == 'unit_price':
                            combine += colname[i] + " = " + allconsvals[i] + " and "
                        else:
                            combine += colname[i] + " = '" + allconsvals[i] + "' and "
                combine = combine.rstrip("and ")
                cur.execute("update model set " + cols + " where " + combine)
            else:
                cur.execute("update model set " + cols)
            conn.commit()
    return render_template("model_update.html",
                           form=form)


@app.route('/center/update/', methods=['GET', 'POST'])
def center_update():
    from form_center_U import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        cols = "name = '" + name + "'"
        constraint = request.form['constraint']
        if constraint != '2':
            combine = "name = '" + request.form['name_filter'] + "'"
            cur.execute("update center set " + cols + " where " + combine)
        else:
            cur.execute("update center set " + cols)
        conn.commit()
    return render_template("center_update.html",
                           form=form)


@app.route('/enterprise/select/', methods=['GET', 'POST'])
def enterprise_select():
    from form_enterprise_R import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        supply_center = request.form['supply_center']
        industry = request.form['industry']
        conn = get_db_connection()
        cur = conn.cursor()
        if (name != '2') | (country != '2') | (city != '2') | (supply_center != '2') | (industry != '2'):
            columns = ((' name,') if name != '2' else '') + ((' country,') if country != '2' else '') + (
                (' city,') if city != '2' else '') + ((' supply_center,') if supply_center != '2' else '') + (
                          (' industry,') if industry != '2' else '')
            columns = columns.rstrip(",")
            colname = ["name", "country", "city", "supply_center", "industry"]
            constraint = request.form['constraint']
            if constraint != '2':
                combine = ""
                allconsvals = [request.form['name_filter'], request.form['country_filter'], request.form['city_filter'],
                               request.form['supply_center_filter'], request.form['industry_filter']]
                for i in range(len(allconsvals)):
                    if allconsvals[i] != "":
                        combine += colname[i] + " = '" + allconsvals[i] + "' and "
                combine = combine.rstrip("and ")
                cur.execute("select " + columns + " from enterprise  where " + combine)
            else:
                cur.execute("select " + columns + " from enterprise ")
            content = cur.fetchall()
            #
            # # # 获取表头
            # # sql = "SHOW FIELDS FROM enterprise"
            # # cur.execute(sql)
            label = []
            if name != '2':
                label.append('name')
            if country != '2':
                label.append('country')
            if city != '2':
                label.append('city')
            if supply_center != '2':
                label.append('supply_center')
            if industry != '2':
                label.append('industry')
            conn.commit()
            return render_template('show_result.html', title="Enterprise", labels=label, content=content)
    return render_template("ent_select.html",
                           form=form)


@app.route('/staff/select/', methods=['GET', 'POST'])
def staff_select():
    from form_staff_R import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        number = request.form['number']
        supply_center = request.form['supply_center']
        mobile_number = request.form['mobile_number']
        type = request.form['type']
        conn = get_db_connection()
        cur = conn.cursor()
        if (name != '2') | (age != '2') | (gender != '2') | (number != '2') | (supply_center != '2') | (
                mobile_number != '2') | (type != '2'):
            columns = ((' name,') if name != '2' else '') + ((' age,') if age != '2' else '') + (
                (' gender,') if gender != '2' else '') + (
                          (' number,') if number != '2' else '') + (
                          (' supply_center,') if supply_center != '2' else '') + (
                          (' mobile_number,') if mobile_number != '2' else '') + (
                          (' type,') if type != '2' else '')
            columns = columns.rstrip(",")
            colname = ["name", "age", "gender", "number", "supply_center", "mobile_number", "type"]
            constraint = request.form['constraint']
            if constraint != '2':
                combine = ""
                allconsvals = [request.form['name_filter'], request.form['age_filter'], request.form['gender_filter'],
                               request.form['number_filter'], request.form['supply_center_filter'],
                               request.form['mobile_number_filter'], request.form['type_filter']]
                for i in range(len(allconsvals)):
                    if allconsvals[i] != "":
                        if colname[i] == "age":
                            combine += colname[i] + " = " + allconsvals[i] + " and "
                        else:
                            combine += colname[i] + " = '" + allconsvals[i] + "' and "
                combine = combine.rstrip("and ")
                cur.execute("select " + columns + " from staff  where " + combine)
            else:
                cur.execute("select " + columns + " from staff ")
            content = cur.fetchall()
            label = []
            if name != '2':
                label.append('name')
            if age != '2':
                label.append('age')
            if gender != '2':
                label.append('gender')
            if number != '2':
                label.append('number')
            if supply_center != '2':
                label.append('supply_center')
            if mobile_number != '2':
                label.append('mobile_number')
            if type != '2':
                label.append('type')
            conn.commit()
            return render_template('show_result.html', title="Staff", labels=label, content=content)
    return render_template("staff_select.html",
                           form=form)


@app.route('/model/select/', methods=['GET', 'POST'])
def model_select():
    from form_model_R import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        number = request.form['number']
        model = request.form['model']
        name = request.form['name']
        unit_price = request.form['unit_price']
        conn = get_db_connection()
        cur = conn.cursor()
        if (number != '2') | (model != '2') | (name != '2') | (unit_price != '2'):
            columns = ((' number,') if number != '2' else '') + ((' model,') if model != '2' else '') + (
                (' name,') if name != '2' else '') + ((' unit_price,') if unit_price != '2' else '')
            columns = columns.rstrip(",")
            colname = ["number", "model", "name", "unit_price"]
            constraint = request.form['constraint']
            if constraint != '2':
                combine = ""
                allconsvals = [request.form['number_filter'], request.form['model_filter'], request.form['name_filter'],
                               request.form['unit_price_filter']]
                for i in range(len(allconsvals)):
                    if allconsvals[i] != "":
                        if colname[i] == 'unit_price':
                            combine += colname[i] + " = " + allconsvals[i] + " and "
                        else:
                            combine += colname[i] + " = '" + allconsvals[i] + "' and "
                combine = combine.rstrip("and ")
                cur.execute("select " + columns + " from model  where " + combine)
            else:
                cur.execute("select " + columns + " from model ")
            content = cur.fetchall()
            label = []
            if number != '2':
                label.append('number')
            if model != '2':
                label.append('model')
            if name != '2':
                label.append('name')
            if unit_price != '2':
                label.append('unit_price')
            conn.commit()
            return render_template('show_result.html', title="Model", labels=label, content=content)
    return render_template("model_select.html",
                           form=form)


@app.route('/center/select/', methods=['GET', 'POST'])
def center_select():
    from form_center_R import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        conn = get_db_connection()
        cur = conn.cursor()
        columns = "name"
        constraint = request.form['constraint']
        if constraint != '2':
            combine = "name = '" + request.form['name_filter'] + "'"
            cur.execute("select " + columns + " from center  where " + combine)
        else:
            cur.execute("select " + columns + " from center ")
        content = cur.fetchall()
        label = []
        label.append('name')
        conn.commit()
        return render_template('show_result.html', title="Center", labels=label, content=content)
    return render_template("center_select.html",
                           form=form)


@app.route('/show_result/', methods=['GET'])
def show_result(label, content):
    return render_template('show_result.html', title="Show_result", labels=label, content=content)


@app.route('/getAllStaffCount/', methods=['GET'])
def getAllStaffCount():
    content = api.getAllStaffCount()
    label = ['type', 'count']
    return render_template('show_result.html', title="Get All Staff Count", labels=label, content=content, )


@app.route('/getContractCount/', methods=['GET'])
def getContractCount():
    content = [[api.getContractCount()]]
    label = ['Count']
    return render_template('show_result.html', title="Get Contract Count", labels=label, content=content, )


@app.route('/getOrderCount/', methods=['GET'])
def getOrderCount():
    content = [[api.getOrderCount()]]
    label = ['Count']
    return render_template('show_result.html', title="Get Order Count", labels=label, content=content, )


@app.route('/getNeverSoldProductCount/', methods=['GET'])
def getNeverSoldProductCount():
    content = [[api.getNeverSoldProductCount()]]
    label = ['Count']
    return render_template('show_result.html', title="Get Never Sold Product Count", labels=label, content=content, )


@app.route('/getFavoriteProductModel/', methods=['GET'])
def getFavoriteProductModel():
    content = api.getFavoriteProductModel()
    label = ['Model', 'Count']
    return render_template('show_result.html', title="Get Favorite Product Model", labels=label, content=content, )


@app.route('/getAvgStockByCenter/', methods=['GET'])
def getAvgStockByCenter():
    content = api.getAvgStockByCenter()
    label = ['Center', 'AvgStock']
    return render_template('show_result.html', title="Get AvgStock By Center", labels=label, content=content, )


@app.route('/', methods=['GET', 'POST'])
def home():
    a = request
    print(request)
    if (request.method == 'POST'):
        if (request.form.get('product_number') != None):
            content = api.getProductByNumber(request.form.get('product_number'))
            label = ['supply_center', 'product_model', 'quantity']
            return render_template('show_result.html', title="Get Product By Number", labels=label, content=content, )
        if (request.form.get('contract_number') != None):
            content1, content2 = api.getContractInfo(request.form.get('contract_number'))
            label1 = ['contract_number', 'enterprise', 'manager', 'supply_center']
            label2 = ['product_model', 'salesman', 'quantity', 'unit_price', 'estimate_delivery_date', 'lodgement_date']
            return render_template('show_contract.html', title="Get ContractInfo", labels1=label1, content1=[content1], labels2=label2, content2=content2)

    if len(request.args) > 0:
        print(request.args.get('api'))
        if request.args.get('api') == 'importFour':
            api.importFour()
        if request.args.get('api') == 'oneStepImport':
            api.oneStepImport()
        if request.args.get('api') == 'stockIn':
            api.stockIn()
        if request.args.get('api') == 'placeOrder':
            api.placeOrder()
        if request.args.get('api') == 'updateOrder':
            api.updateOrder()
        if request.args.get('api') == 'deleteOrder':
            api.deleteOrder()
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
