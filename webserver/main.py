from flask import Flask, redirect, request, session, Response
from onelogin.saml2.auth import OneLogin_Saml2_Auth, OneLogin_Saml2_Settings

import secrets
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# SAML設定ファイルのパスを指定
SAML_SETTINGS_FILE = '/app/settings.json'

def init_saml_auth(req):
    with open(SAML_SETTINGS_FILE) as f:
        settings = json.load(f)
    return OneLogin_Saml2_Auth(req, custom_base_path="./")

@app.route("/")
def index():
    return "Welcome! <a href='/login'>Login with SAML</a>"

@app.route("/login")
def login():
    req = {
        "https": "off",
        "http_host": "localhost:8000",
        "script_name": "/"
    }
    auth = init_saml_auth(req)
    saml_login_url = auth.login()
    return redirect(saml_login_url)

@app.route("/logout")
def logout():
    req = {
        "https": "off",
        "http_host": "localhost:8000",
        "script_name": "/"
    }
    auth = init_saml_auth(req)
    saml_logout_url = auth.logout()
    return redirect(saml_logout_url)

@app.route("/acs", methods=["POST"])
def acs():
    req = {
        "https": "off",
        "http_host": "localhost:8000",
        "script_name": "/"
    }
    auth = init_saml_auth(req)
    auth.process_response(request.form["SAMLResponse"])
    if auth.is_authenticated():
        session["user"] = auth.get_nameid()
        return f"Hello {session['user']}"
    return "Authentication failed"

@app.route("/sso", methods=["GET", "POST"])
def sso():
    req_data = {
        "https": "off",
        "http_host": request.host,
        "script_name": request.path,
        "get_data": request.args.copy(),
        "post_data": request.form.copy(),
    }

    auth = OneLogin_Saml2_Auth(req_data, custom_base_path="./")
    return redirect(auth.login())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
