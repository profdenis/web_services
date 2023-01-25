from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # return f'<a href="{url_for("hello_world")}">Link to hello</a>'
    # return render_template('index.html',
    #                        hello_link=url_for('hello_world'),
    #                        goodbye_link=url_for('goodbye'))
    links = [url_for('hello_world'), url_for('goodbye')]
    return render_template('index.html', links=links)


@app.route('/hello-world')
def hello_world():  # put application's code here
    return render_template('hello.html')


@app.route('/goodbye')
def goodbye():
    links = [url_for('hello_world'), url_for('index')]
    return render_template('goodbye.html', links=links)


if __name__ == '__main__':
    app.run()
