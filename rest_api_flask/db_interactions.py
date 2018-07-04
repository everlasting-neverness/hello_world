import psycopg2
import psycopg2.extras
import datetime

DB_NAME = 'kids_db'
TABLE_NAME = 'kids'

connection = None
cursor = None

def initdb():
    global connection
    global cursor
    # .connect("dbname='{db_name}' user='user1' host='localhost'" \
    connection = psycopg2.connect("dbname='{db_name}' user='user1' password='123456' host='localhost'".format(db_name=DB_NAME))
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return connection

def print_rows(cursor):
    cursor.execute("SELECT * from {table_name}".format(table_name=TABLE_NAME))
    rows = cursor.fetchall()
    print('len', len(rows))
    for row in rows:
        for column in row:
            print(column)

def commitChanges():
    global connection
    connection.commit()

def add_kid_to_db(cursor):
    cursor.execute('''insert into kids
        (name, gender, date_of_birth, status, grade)
    values
        ('Ivanov Ivan', 'Male', '11.11.2015', 'attending', '1')
    ''')

def add_log(cursor):
    params = ('11.11.2018 11:02', '11.11.2018')
    cursor.execute('''insert into logs
        (parent, arrival, departure, date, kid_id)
    values
        ('Dmitriy', %s, 'null', %s, 2)
    ''', params)
    commitChanges()
    return 'ok'

def add_kid():
    global cursor
    add_kid_to_db(cursor)
    commitChanges()


def make_dictionary(tuples):
    output = {}
    for tuple in tuples:
        output[tuple[0]] = tuple[1]
    return output


def get_kids():
    global cursor
    if not connection:
        raise Exception('No database connection')
    cursor.execute("""SELECT * from kids""")
    kids = cursor.fetchall()
    print([x for x in kids[0].items()])
    kids_list = []
    for kid in kids:
        kid = [x for x in kid.items()]
        kids_list.append(make_dictionary(kid))
    return kids_list

def get_kid(id):
    global cursor
    cursor.execute("select * from kids where id=%s" % (str(id),))
    kid = cursor.fetchone()
    print (kid)
    if not kid:
        return None
    kid = [x for x in kid.items()]
    kid = make_dictionary(kid)
    return kid

def create_item(object):
    global cursor
    items = ['name', 'date_of_birth', 'gender', 'status', 'grade']
    for item in items:
        if item not in object:
            return {'False input':'False input'}
    s = '''insert into kids
        (name, date_of_birth, gender, status, grade)
    values
        ('%(name)s',
         '%(date_of_birth)s',
         '%(gender)s',
         '%(status)s',
         '%(grade)s'
        )
    ''' % object
    cursor.execute(s)
    # % (object['name'], object['date_of_birth'], object['gender'], object['status'], object['grade']))
    commitChanges()
    return {'ok':'ok'}


validationItems = {
    'kids': ['name', 'date_of_birth', 'gender', 'status', 'grade'],
    'journal': ['kid_id', 'parent', 'arrival', 'departure', 'date']
}

def update_item(tableName, object):
    global cursor
    items = validationItems[tableName]
    for item in object:
        if not (item in object):
            return {'False input':'False input'}
    s = '''update kids set
        (name, date_of_birth, gender, status, grade)
        =
        ('%(name)s',
         '%(date_of_birth)s',
         '%(gender)s',
         '%(status)s',
         '%(grade)s'
        )
        where id = '%(id)s'
    ''' % object
    cursor.execute(s)
    commitChanges()
    return object

def delete_kid(id):
    global cursor
    cursor.execute("Delete from kids where id='%s'" % id)
    commitChanges()
    return {'deleted successfully': 'deleted successfully'}



def get_logs():
    global cursor
    if not connection:
        raise Exception('No database connection')
    cursor.execute("""SELECT * from logs where departure = 'null' and date = '%s'""" % (str(datetime.datetime.today().strftime("%d.%m.%Y")), ))
    logs = cursor.fetchall()
    print([x for x in logs[0].items()])
    logs_list = []
    for log in logs:
        log = [x for x in log.items()]
        logs_list.append(make_dictionary(log))
    return logs_list

def get_log(id):
    global cursor
    cursor.execute("select * from logs where id=%s" % (str(id),))
    log = cursor.fetchone()
    if not log:
        return None
    log = [x for x in log.items()]
    log = make_dictionary(log)
    return log

def create_log_entry(object):
    global cursor
    items = ['kid_id', 'parent', 'arrival', 'departure', 'date']
    for item in items:
        if item not in object:
            return {'False input':'False input'}
    if object['departure'] != 'null':
        print object['departure']
        return {'False input':'False input'}
    s = '''insert into logs
        (kid_id, parent, arrival, departure, date)
    values
        ('%(kid_id)s',
         '%(parent)s',
         '%(arrival)s',
         '%(departure)s',
         '%(date)s'
        )
    ''' % object
    cursor.execute(s)
    commitChanges()
    return {'ok':'ok'}

# def update_item(tableName, object):
#     global cursor
#     items = validationItems[tableName]
#     for item in object:
#         if not (item in object):
#             return 'False input'
#     if tableName == 'kids':
#         s = '''update kids set
#             (name, date_of_birth, gender, status, grade)
#             =
#             ('%(name)s',
#              '%(date_of_birth)s',
#              '%(gender)s',
#              '%(status)s',
#              '%(grade)s'
#             )
#             where id = '%(id)s'
#         ''' % object
#     else:
#         s = '''update logs set
#            (kid_id, parent, arrival, departure, date)
#             =
#             ('%(kid_id)s',
#          '%(parent)s',
#          '%(arrival)s',
#          '%(departure)s',
#          '%(date)s')
#             where id = '%(id)s'
#         ''' % object
#     cursor.execute(s)
#     commitChanges()
#     return object

def update_log(object, id):
    global cursor
    kid_id = object['kid_id']
    cursor.execute("SELECT * from logs where kid_id = '%s' and id = '%s' and date = '%s'" % (kid_id, id, str(datetime.datetime.today().strftime("%d.%m.%Y"))))
    q = cursor.fetchone()
    if not q:
        return {'False input':'False input'}
    q = [x for x in q.items()]
    q = make_dictionary(q)
    if q['departure'] != 'null':
        return {'False input':'False input'}
    s = '''update logs set
       (parent, arrival, departure, date)
       =
      ('%(parent)s',
     '%(arrival)s',
     '%(departure)s',
     '%(date)s')
      where kid_id = '%(kid_id)s'
        ''' % object
    cursor.execute(s)
    commitChanges()
    return object

def delete_item(tableName, id):
    global cursor
    if tableName == 'kids':
        cursor.execute("Delete from kids where id='%s'" % id)
    else:
        cursor.execute("Delete from logs where id='%s'" % id)
    commitChanges()
    return 'deleted successfully'

# def get_items(tableName):
#     global cursor
#     if not connection:
#         raise Exception('No database connection')
#     cursor.execute("SELECT * from {table_name}").format(table_name=tableName)
#     items = cursor.fetchall()
#     # print(dir(kids[0]))
#     # print([x for x in logs[0].items()])
#     items_list = []
#     for item in items:
#         item = [x for x in items.items()]
#         items_list.append(make_dictionary(item))
#     return items_list
