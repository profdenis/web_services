import csv

from flask import Flask, jsonify, request

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
