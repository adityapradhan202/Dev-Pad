from flask import Flask
from flask import render_template, url_for, redirect
from flask import request
from flask import session

import dbutils as dutil

app = Flask(__name__)

# decryption key for sesison data
app.secret_key = b'catsanddogs45#33nobs'

# dummy data
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
        cur, conn = dutil.db_initialize()
        rows = dutil.fetchall_posts(cur, conn)
        # print(rows)
        return render_template("user.html", name=session["username"], all_rows=rows)
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

# CRUD operations here
# Delete
@app.route("/delete/<int:pid>")
def delete(pid):
    if "username" in session:
        cur, conn = dutil.db_initialize()
        dutil.delete_posts(cur, conn, pid)
        return redirect(url_for("user")) # after deleting post
    else:
        return redirect(url_for("home"))
    
@app.route("/read/<int:pid>")
def read(pid):
    if "username" in session:
        cur, conn = dutil.db_initialize()
        row = dutil.get_single_post(cur, conn, pid)
        content = row["content"]
        return render_template("read.html", content=content)
    else:
        return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)