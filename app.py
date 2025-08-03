from flask import Flask
from flask import render_template, url_for, redirect
from flask import request
from flask import session

app = Flask(__name__)

# decryption key for sesison data
app.secret_key = b'catsanddogs45#33nobs'

# dummy data
data = {
    "aditya123":"mypass123"
}

# homepage
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/user")
def user():
    if "username" in session:
        return render_template("user.html")
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
                return render_template("user.html", name=session["username"])
        else:
            return redirect(url_for("home"))
        
    # initially when we visit /login
    elif request.method == "GET":
        return render_template("login.html")

# logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("userpass", None)
    return redirect(url_for("home")) 

if __name__ == "__main__":
    app.run(debug=True)