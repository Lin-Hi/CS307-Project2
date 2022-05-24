import os
import psycopg2
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, url_for, session, flash
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = '42'
bootstrap = Bootstrap(app)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='cs307_2',
                            user='checker',
                            password='123456')
    return conn


@app.route('/hello/')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'human')
        response = '<h1>Hello %s!<h1>\n<h2>Have a good day :)<h2>' % name
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response


# @app.route('/whole/')
# def whole():
#     return render_template('home.html')


@app.route('/test/', methods=('GET', 'POST'))
def bootstrap_test():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        print(name)
        print(age)
        return redirect(url_for('hello'))

    conn = get_db_connection()
    cur = conn.cursor()

    # get annual sales rank
    sql = "select * from enterprise"
    cur.execute(sql)
    content = cur.fetchall()

    # # 获取表头
    # sql = "SHOW FIELDS FROM enterprise"
    # cur.execute(sql)
    labels = ["name", "country", "city", "supply_center", "industry"]
    # labels = [l[0] for l in labels]

    return render_template('bootstrap_test.html', labels=labels, content=content)


@app.route('/enterprise/insert/', methods=['GET', 'POST'])
def enterprise_insert():
    from form_enterprise_CD import RegisterForm
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
        # content = cur.fetchall()

        # # 获取表头
        # sql = "SHOW FIELDS FROM enterprise"
        # cur.execute(sql)
        # labels = ["name", "country", "city", "supply_center", "industry"]
        # labels = [l[0] for l in labels]

        # return render_template('show_result.html', labels=labels, content=content)
        # return redirect('/login/')

        # 出现一个闪现信息;
        # flash("用户%s已经注册成功， 请登录....." % (username))
        # return redirect(url_for('login'))

    return render_template("ent_insert.html",
                           form=form)


@app.route('/enterprise/delete/', methods=['GET', 'POST'])
def enterprise_delete():
    from form_enterprise_CD import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        supply_center = request.form['supply_center']
        industry = request.form['industry']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("delete from enterprise where " + "name = '" + name + "' " +
                    (('and country=\'' + country + "'") if country != '' else '') +
                    (('and city=\'' + city + "'") if city != '' else '') +
                    (('and supply_center=\'' + supply_center + "'") if supply_center != '' else '') +
                    (('and industry=\'' + industry + "'") if industry != '' else '') +
                    "")
        conn.commit()
    return render_template("ent_delete.html",
                           form=form)


def test():
    print("test")


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
                print("select " + columns + " from enterprise  where " + combine)
            else:
                cur.execute("select " + columns + " from enterprise ")
                print("select " + columns + " from enterprise ")

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
            print(label)
            return render_template('show_result.html', labels=label, content=content)
    return render_template("ent_select.html",
                           form=form)


@app.route('/')
def home():
    return render_template('home.html')

    # conn = get_db_connection()
    # cur = conn.cursor()
    #
    # # get annual sales rank
    # sql = "select * from enterprise"
    # cur.execute(sql)
    # content = cur.fetchall()
    #
    # # # 获取表头
    # # sql = "SHOW FIELDS FROM enterprise"
    # # cur.execute(sql)
    # labels = ["name", "country", "city", "supply_center", "industry"]
    # # labels = [l[0] for l in labels]
    #
    # return render_template('index.html', labels=labels, content=content)


# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         author = request.form['author']
#         pages_num = int(request.form['pages_num'])
#         review = request.form['review']
#
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute('INSERT INTO books (title, author, pages_num, review)'
#                     'VALUES (%s, %s, %s, %s)',
#                     (title, author, pages_num, review))
#         conn.commit()
#         cur.close()
#         conn.close()
#         return redirect(url_for('index'))
#
#     return render_template('create.html')


if __name__ == '__main__':
    app.run()
