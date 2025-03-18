import psycopg2
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '7529c3c1523778a1e9137ec6d675080a67ae1ebdcd034633c26a1efe6c7facc8'


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgrespw@localhost:49153/vulnarable_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False) 


admin.add_view(ModelView(User, db.session))

def get_db_connection():
    return psycopg2.connect(
        dbname="vulnarable_db",
        user="postgres",
        password="postgrespw",
        host="localhost",  
        port="49153"
    )

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login", methods=["POST","GET"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM public.users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('main.html', username=username)
        else:
            flash("Unknown email or password.", "danger")
            return redirect(url_for("home"))

    except Exception as ex:
        flash(f"SQL Error: {str(ex)}", "danger")
        return redirect(url_for("home"))
        
if __name__ == "__main__":
    app.run(debug=True)
