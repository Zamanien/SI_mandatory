from dotenv import load_dotenv

# load env file
load_dotenv()

from bottle import request, response, view, run, template
import os
import bottle
import auth
import twofa
import stub_cpr_registry

# READ ENV VARS
mitid_url = os.environ.get("mitid_url")
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
    email = stub_cpr_registry.find_email(cpr)
    twofa.generate_save_send(email=email)
    return


##############################
@app.post("/2fa")
def two_fa():
    email = request.forms["email"]
    code = request.forms["code"]
    print(email, code)
    if twofa.verify(email, code):
        provider_token = auth.generate_esb_token()
        return template("secret_page", provider_token=provider_token)
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


try:
    import production

    application = app
except Exception as ex:
    run(app, host="127.0.0.1", port=port, debug=True, reloader=True, server="paste")
