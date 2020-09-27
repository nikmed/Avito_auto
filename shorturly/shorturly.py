from flask import Flask, redirect, request, render_template, abort
import os
import dbworker 
import validators
from werkzeug.exceptions import HTTPException


#Configuration
DATABASE='database.db'
DEBUG = False




app = Flask(__name__)
app.config.update(dict(
	DATABASE = os.path.join(app.root_path, DATABASE),
	DEBUG = True
	))


def init_db(dbname = DATABASE):
	global db 
	db = dbworker.db(dbname)


@app.route('/', methods=['GET'])
def home():
    return render_template ('index.html')


@app.route('/', methods=['POST'])
def get_short():
	url = request.form.get('URL')
	short_url = request.form.get('short_url') if request.form.get('short_url') != None else ''

	if validators.url(url):
		if short_url != '':
			link, err = db.insert_custom(url, short_url)
		else:
			link, err = db.insert(url)
		if err: 
			return render_template ('index.html', answer = link)
		else:
			abort(400, link)
			return link
	else:
		abort(400, 'Invalid url')


@app.route('/<string:short_url>', methods=['GET'])
def redirect_to_url(short_url):
	link, err= db.queue_read(short_url)
	if err:
		return redirect(link)
	else:
		abort(400, link)



if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5050))
    app.run(host = '127.0.0.1', port = port, debug = DEBUG)