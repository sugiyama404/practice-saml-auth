from flask import Flask, redirect, request, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth

app = Flask(__name__)
app.secret_key = "your_secret_key"

def init_saml_auth(req):
    return OneLogin_Saml2_Auth(req, custom_base_path="./")

@app.route("/")
def index():
    return "Welcome! <a href='/login'>Login with SAML</a>"

@app.route("/login")
def login():
    req = {
        "https": "on",
        "http_host": "localhost:8000",
        "script_name": "/"
    }
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route("/acs", methods=["POST"])
def acs():
    req = {
        "https": "on",
        "http_host": "localhost:8000",
        "script_name": "/"
    }
    auth = init_saml_auth(req)
    auth.process_response(request.form["SAMLResponse"])
    if auth.is_authenticated():
        session["user"] = auth.get_nameid()
        return f"Hello {session['user']}"
    return "Authentication failed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
