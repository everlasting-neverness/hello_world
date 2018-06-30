import psycopg2
import psycopg2.extras

DB_NAME = 'kids_db'
TABLE_NAME = 'kids'

connection = None
cursor = None

def initdb():
    global connection
    global cursor
    connection = psycopg2 \
        .connect("dbname='{db_name}' user='user1' host='localhost'" \
        .format(db_name=DB_NAME))
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
    # print(dir(kids[0]))
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

def create_kid(object):
    global cursor
    items = ['name', 'date_of_birth', 'gender', 'status', 'grade']
    for item in items:
        if item not in object:
            return 'False input'
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
    return 'ok'


validationItems = {
    'kids': ['name', 'date_of_birth', 'gender', 'status', 'grade'],
    'journal': []
}

def update_item(tableName, object):
    global cursor
    items = validationItems[tableName]
    for item in object:
        if not (item in object):
            return 'False input'
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
    return 'deleted successfully'

 # [(8, 'Ivanov Ivan', 'Male', '11.11.2015', 'attending', '1')]
# [{ 'id': 8, 'name': 'I..I..', 'gender': 'Male'}]
