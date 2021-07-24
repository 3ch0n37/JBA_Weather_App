import sys

import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
api_key = ''
db = SQLAlchemy(app)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        list = []
        rows = Weather.query.all()
        for row in rows:
            r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={row.name}&appid={api_key}&units=metric')
            r = r.json()
            list.append({
                'name': r['name'],
                'state': r['weather'][0]['main'],
                'temperature': r['main']['temp'],
                'id': row.id
            })
        return render_template('index.html', cities=list)
    elif request.method == 'POST':
        city = request.form['city_name']
        entry = Weather(name=city)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        db.create_all()
        app.run(host=arg_host, port=arg_port)
    else:
        db.create_all()
        app.run()
