import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir, "book_database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db = SQLAlchemy(app)

class Book(db.Model):
	title = db.Column(db.String(80), unique = True, nullable = False, primary_key = True)
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

@app.route("/update", methods = ["GET", "POST"])

def update():
	oldtitle = request.form.get("oldtitle")
	oldprice = request.form.get("oldprice")
	newtitle = request.form.get("newtitle")
	newprice = request.form.get("newprice")
	book = Book.query.filter_by(title = oldtitle).first()
	book.title = newtitle
	book.price = newprice
	db.session.commit()
	return redirect("/")


@app.route("/delete", methods = ["GET", "POST"])

def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title = title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True)