import os, psycopg2
#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

connection = psycopg2.connect(user="postgres",
                                              password="password123",
                                              host="127.0.0.1",
                                              port="5432",
                                              database="FinalProject")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register.html", methods =["GET", "POST"])
def register():
	if request.method == "POST":
		# getting input with name = fname in HTML form
		uname = request.form.get("uname")
		# getting input with name = lname in HTML form
		pword = request.form.get("pword")
		
		try: 
			
			cursor = connection.cursor()
			
			query = "INSERT INTO users (username, password) VALUES (%s, %s)"
			record = (uname, pword)
			cursor.execute(query, record)
			connection.commit()
		except(Exception, psycopg2.Error) as error: 
			return "Error:" + str(error)
		return redirect("/")
	return render_template('register.html')

@app.route("/login.html", methods =["GET", "POST"])
def login():
	if request.method == "POST":
		# getting input with name = fname in HTML form
		uname = request.form.get("uname")
		# getting input with name = lname in HTML form
		pword = request.form.get("pword")
		
		try: 
			
			cursor = connection.cursor()
			query = "SELECT * FROM users WHERE username = " + "'" + str(uname) + "'"
			cursor.execute(query)
			record = cursor.fetchall()
			
			if record != []:
				if record[0][1] == pword:
					session["username"] = record[0][0]
					
					return render_template("/home.html", uname = uname)
				else:
					return "Incorrect username or password"
			
		except(Exception, psycopg2.Error) as error: 
			return "Error:" + str(error)
		return redirect("/")
		
		
	return render_template('login.html')

@app.route("/home.html", methods =["GET", "POST"])
def home():
	find = request.args.get("find")
	cursor = connection.cursor()

	if find:
		
		query = f"""SELECT * FROM books WHERE title ILIKE '%{find}%' or isbn ILIKE '%{find}%' or author ILIKE '%{find}%'"""
		
		if len(find) == 4:
			try:
				intfind = int(find)
				query = f"SELECT * FROM books WHERE year = {intfind}"
			except:
				intfind = 0
		
		cursor.execute(query)

	else:
		query = "SELECT * FROM books"
		cursor.execute(query)

	rows = cursor.fetchall()

	return render_template("home.html", rows=rows)


@app.route("/logout.html", methods=["GET", "POST"])
def logout():

	return render_template('logout.html')

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):

	cursor = connection.cursor()

	# displaying the selected books info
	query = f"SELECT * FROM books WHERE isbn='{isbn}'"
	cursor.execute(query)
	book = cursor.fetchone()

	# displaying the selected books reviews
	query = f"SELECT * FROM reviews WHERE isbn='{isbn}'"
	cursor.execute(query)
	reviews = cursor.fetchall()

	if request.method == "POST":
		user = request.form.get("user")
		review = request.form.get("review")
		query = f"INSERT INTO reviews (isbn, review, username) VALUES ('{isbn}', '{review}', '{user}')"
		cursor.execute(query)
		connection.commit()

	return render_template("book.html", book=book, reviews=reviews)


if __name__=="__main__":
	app.run(debug=True)

