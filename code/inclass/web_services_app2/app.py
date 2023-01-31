from flask import Flask, jsonify
from exercises_functions import is_even, is_palindrome, reverse, occurrences

app = Flask(__name__)


# Get the hello world message
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!!!!!!!!!!!!!!!!!!!'


# localhost:5000/is-even/23
# x = 23
@app.route('/is-even/<int:x>')
def is_even_route(x):
    return jsonify(is_even(x))


@app.route('/is-palindrome/<string:s>')
def is_palindrome_route(s):
    return jsonify({'function': 'is_palindrome',
                    'parameters': [s],
                    'result': is_palindrome(s)})


@app.route('/reverse/<string:s>')
def reverse_route(s):
    return jsonify({'function': 'reverse',
                    'parameters': [s],
                    'result': reverse(s)})


@app.route('/occurrences/<string:target_char>/<string:s>')
def occurrences_route(target_char, s):
    return jsonify({'function': 'occurrences',
                    'parameters': [target_char, s],
                    'result': occurrences(target_char, s)})


if __name__ == '__main__':
    app.run()
