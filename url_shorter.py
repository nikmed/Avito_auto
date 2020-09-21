from flask import Flask, redirect, request
import os
import dbworker 
import validators

db = dbworker.db()
app = Flask(__name__)


@app.route('/')
def hello():
    return ('Hello world!')


@app.route('/<string:short_url>', methods=['GET'])
def redirect_to_url(short_url):
    return redirect(db.longurl(short_url))

@app.route('/url=<path:url>', methods=['GET'])
def get_short(url):
	if validators.url(url):
		link = db.insert(url)
		return link
	else:
		return 'Error: Invalid url'


@app.route('/custom/short=<string:short_url>/url=<path:url>', methods=['GET'])
def get_short_custom(url, short_url):
	if validators.url(url):
		link = db.insert_custom(url, short_url)
		return link
	else:
		return 'Error: Invalid url'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host = '127.0.0.1', port = port, debug = True)