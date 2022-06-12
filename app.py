from bottle import request, response, view, run, static_file
from dotenv import load_dotenv
import os
import jwt, bottle
import auth
import twofa
import stub_cpr_registry
from jwt.exceptions import InvalidSignatureError

# READ ENV VARS
load_dotenv()
mitid_url = os.environ.get("mitid_url")
jwt_secret = os.environ.get("jwt_secret")
algorithm = os.environ.get("algorithm")
sender_email = os.environ.get("sender_email")
receiver_email = os.environ.get("receiver_email")
password = os.environ.get("password")
port = os.environ.get("port")

app = bottle.Bottle()


##############################
@app.get("/")
@view("index")
def index():
    return dict(mitid_url=mitid_url)


# def validate_jwt(request, response):


# def get_cpr():


##############################
@app.post("/validate")
def _():
    data = auth.verify_token()
    cpr = data["cpr"]
    print(cpr)

    # TODO generate 4 digit code, send email and save email - code pair in DB
    email = stub_cpr_registry.find_email(cpr)
    twofa.generate_save_send(email=email)
    return


##############################
@app.post("/2fa")
@view("two_fa")
def two_fa():
    email = request.forms["email"]
    code = request.forms["code"]
    print(email, code)
    if twofa.verify(email, code):
        return
    else:
        response.status = 403
        return {
            "code": "invalid_auth_code",
            "description": "Wrong authorization code",
        }


##############################
@app.get("/2fa")
@view("two_fa")
def two_fa():
    return


##############################
@app.get("/secret_page")
@view("secret_page")
def two_fa():
    return


try:
    import production

    application = app
except Exception as ex:
    run(app, host="127.0.0.1", port=port, debug=True, reloader=True, server="paste")
