import csv
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


@app.route('/hello1')
def hello1():
    return jsonify({'msg': 'Hello, World!', 'data': [3, 6, 1, 3, 5]})


@app.route('/hello2')
def hello2():
    # don't need to call jsonify if we return a dictionary
    return {'msg': 'Hello, World!', 'data': [3, 6, 1, 3, 5]}


@app.route('/hello3')
def hello3():
    # if we don't have a dictionary (or don't want to create one), we can call jsonify this way
    return jsonify(msg='Hello, World!', data=[3, 6, 1, 3, 5])


@app.route('/students')
def get_students():
    with open('data/students.csv') as f:
        reader = csv.DictReader(f)
        data = [s for s in reader]
        return data


@app.route('/students/<int:student_id>')
def get_student(student_id):
    with open('data/students.csv') as f:
        reader = csv.DictReader(f)
        # not the most efficient way, but it will work for this simple example
        data = [s for s in reader if s['student_id'] == str(student_id)]
        return data


@app.route('/students', methods=['POST'])
def post_student():
    with open('data/students.csv', 'a') as f:
        writer = csv.DictWriter(f, ['student_id', 'name', 'program'])
        # dangerous, no data validation in this example (and no authentication either)
        writer.writerow(request.json)
    return {'success': True}, 200


@app.route('/v2/students')
def get_students_v2():
    con = sqlite3.connect('data/students.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from student;")
    students = [dict(row) for row in cur]
    # students = []
    # for row in cur:
    #     students.append(dict(row))
    con.close()
    return students


@app.route('/v2/students/<int:student_id>')
def get_student_v2(student_id):
    con = sqlite3.connect('data/students.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"select * from student where student_id = {student_id};")
    student = dict(cur.fetchone())
    con.close()
    return student


@app.route('/v2/students', methods=['POST'])
def post_student_v2():
    data = request.json
    student_id = data.get('student_id', None)
    name = data.get('name', None)
    program = data.get('program', None)

    if not name:
        return {'success': False,
                'student_id': int(student_id) if student_id else None,
                'msg': 'Missing name'}, 409

    con = sqlite3.connect('data/students.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if student_id:
        statement = f"insert into student(student_id, name, program) values ({student_id}, '{name}', '{program}');"
    else:
        statement = f"insert into student(name, program) values ('{name}', '{program}') returning student_id;"
    try:
        cur.execute(statement)
    except sqlite3.IntegrityError as e:
        con.close()
        return {'success': False,
                'student_id': int(student_id),
                'msg': 'A student with this id already exists'}, 409
    if not student_id:
        student_id = cur.fetchone()[0]
    con.commit()
    con.close()
    return {'success': True, 'student_id': int(student_id)}, 200


if __name__ == '__main__':
    app.run()
