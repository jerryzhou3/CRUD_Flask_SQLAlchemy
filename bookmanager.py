import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir, "book_database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db = SQLAlchemy(app)

class Book(db.Model):
	title = db.Column(db.String(), unique = True, nullable = False, primary_key = True)
	price = db.Column(db.Integer(), unique = False, nullable = False, primary_key = False)

	def __repr__(self):
		return "<Title: {}, Price: {}>".format(self.title, self.price)


@app.route("/", methods = ["GET", "POST"])

def home():
	if request.form:
		book = Book(title = request.form.get("title"), price = request.form.get("price"))
		db.session.add(book)
		db.session.commit()
	books = Book.query.all()
	return render_template('home.html', books = books)


if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True)