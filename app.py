from flask import Flask
from flask import render_template, url_for, redirect
from flask import request
from flask import session

import os
import dbutils as db

app = Flask(__name__)
app.config["SECRET_KEY"] = str(os.getenv("SESSION_ENCRYPTION_KEY"))

# dummy data for login
data = {
    "aditya123":"mypass123"
}

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/user")
def user():
    if "username" in session:
        cur, conn = db.db_initialize()
        rows = db.fetchall_posts(cur, conn)
        
        # Logic to display a smaller part or preview of each post
        rows_sliced = []
        for row in rows:
            row_dict = {}
            sliced_id = row["id"]
            sliced = str(row["content"])[:45]
            row_dict["id"] = sliced_id
            row_dict["content"] = sliced + "..."
            rows_sliced.append(row_dict)
        
        return render_template("user.html", name=session["username"], all_rows=rows_sliced)
    else:
        return redirect(url_for("home"))

@app.route("/login", methods=["POST", "GET"])
def login():
    # on form submission
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["userpass"] = request.form.get("userpass")

        if session["username"] in data:
            # dummy user auth
            if session["userpass"] == data[session["username"]]:
                return redirect(url_for("user"))
        else:
            return redirect(url_for("home"))
        
    # initially when we visit /login
    elif request.method == "GET":
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("userpass", None)
    return redirect(url_for("home"))

# CRUD operations here!

# Delete
@app.route("/delete/<int:pid>")
def delete(pid):
    if "username" in session:
        cur, conn = db.db_initialize()
        db.delete_posts(cur, conn, pid)
        return redirect(url_for("user")) # after deleting post
    else:
        return redirect(url_for("home"))
    
@app.route("/read/<int:pid>")
def read(pid):
    if "username" in session:
        cur, conn = db.db_initialize()
        content = db.get_single_post(cur, conn, pid)
        return render_template("read.html", content=content)
    else:
        return redirect(url_for("home"))
    
@app.route("/edit/<int:pid>", methods=["GET", "POST"])
def edit(pid):
    if "username" in session:
        if request.method == "GET":
            cur, conn = db.db_initialize()
            content = db.get_single_post(cur, conn, pid, )
            return render_template('edit.html', content=content)
        
        elif request.method == "POST":

            new_cont = request.form.get("updcontent")
            cur, conn = db.db_initialize()
            db.update_post(cur, conn, pid, new_cont)
            return redirect(url_for("user"))

    else:
        return redirect(url_for("home"))
    
@app.route("/create", methods=["GET", "POST"])
def create():
    if "username" in session:
        if request.method == "GET":
            return render_template("create.html")
        elif request.method == "POST":
            created = request.form.get("created")
            cur, conn = db.db_initialize()
            db.create_post(cur, conn, created)
            
            return redirect(url_for("user"))
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)