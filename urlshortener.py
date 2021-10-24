import os
import pandas as pd
import sqlite3
from flask import Flask, jsonify, abort, request, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_ops import *

app = Flask(__name__)

if not os.path.exists('urls.db'):
    connection = sqlite3.connect('urls.db')
    df = pd.DataFrame(columns=['long_url', 'short_url', 'views'])
    df.views = pd.to_numeric(df.views)
    df.to_sql('urls', connection)


engine = create_engine(f"sqlite:///urls.db")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/shorten', methods=['POST'])
def create_url():
    if not (request.json and 'urlToShorten' in request.json):
        abort(400)

    long_url = request.json['urlToShorten']
    db_create_url(session, long_url=long_url)
    new_url = db_read_url_by_long(session, long_url)

    response = make_response(jsonify({"shortenedUrl": "http://localhost:5000/" + str(new_url.short_url)}))
    response.status = 201
    return response


@app.route('/<string:short_url>', methods=['GET'])
def get_url(short_url: str):
    short_url = int(short_url.split('/')[-1])
    url = db_read_url_by_short(session, short_url)
    if not url:
        abort(404)
    db_plus_view(session, short_url)
    response = make_response(jsonify({'redirectTo': url.long_url}))
    response.headers['location'] = url.long_url
    response.status = 301
    return response


@app.route('/<string:short_url>/views', methods=['GET'])
def get_url_views(short_url: str):
    short_url = int(short_url.split('/')[-1])
    url = db_read_url_by_short(session, short_url)
    if not url:
        abort(404)
    response = make_response(jsonify({'viewCount': url.views}))
    response.status = 200
    return response


if __name__ == '__main__':
    app.run(debug=True)
