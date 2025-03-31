from flask import Flask, redirect, request, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
import secrets
import json
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('saml')

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# SAML設定ファイルのパスを指定
SAML_SETTINGS_FILE = '/app/settings.json'

def init_saml_auth(req):
    with open(SAML_SETTINGS_FILE) as f:
        settings_data = json.load(f)

    saml_settings = OneLogin_Saml2_Settings(settings_data)
    return OneLogin_Saml2_Auth(req, custom_base_path="./")

def prepare_flask_request(request):
    # リクエストデータを適切な形式に変換
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': request.environ.get('SERVER_PORT', '8000'),
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy(),
        'query_string': request.query_string.decode('utf-8')
    }

@app.route("/")
def index():
    return "Welcome! <a href='/login'>Login with SAML</a>"

@app.route("/login")
def login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route("/logout")
def logout():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    session.clear()
    return redirect(auth.logout())

@app.route("/acs", methods=["POST"])
def acs():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)

    request_id = None
    if 'AuthNRequestID' in session:
        request_id = session['AuthNRequestID']

    auth.process_response(request_id=request_id)
    errors = auth.get_errors()

    logger.debug(f"SAML Errors: {errors}")
    logger.debug(f"SAML Error Reason: {auth.get_last_error_reason()}")

    if not errors:
        if auth.is_authenticated():
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlSessionIndex'] = auth.get_session_index()
            return f"Successfully authenticated as {session['samlNameId']}"

    return f"Authentication failed: {', '.join(errors)} - {auth.get_last_error_reason()}"

@app.route("/metadata")
def metadata():
    # SPのメタデータを提供
    saml_settings = OneLogin_Saml2_Settings(json_file=SAML_SETTINGS_FILE)
    metadata = saml_settings.get_sp_metadata()
    return metadata, 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
