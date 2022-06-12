import uuid
import jwt
from jwt.exceptions import InvalidSignatureError
from bottle import request, response

jwt_secret = "secret"
algorithm = "HS256"


def verify_token():
    auth = request.headers.get("Authorization", None)
    if not auth:
        response.status = 403
        return {
            "code": "authorization_header_missing",
            "description": "Authorization header is expected",
        }

    parts = auth.split()

    if parts[0].lower() != "bearer":
        response.status = 403
        return {
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer",
        }
    elif len(parts) == 1:
        response.status = 403
        return {"code": "invalid_header", "description": "Token not found"}
    elif len(parts) > 2:
        response.status = 403
        return {
            "code": "invalid_header",
            "description": "Authorization header must be Bearer + \s + token",
        }

    try:
        data = jwt.decode(parts[1], jwt_secret, algorithm)
        return data
    except InvalidSignatureError:
        response.status = 403
        return {
            "code": "invalid_signature",
            "description": "Token signature is not valid",
        }

def generate_esb_token():
    provider_id = uuid.uuid1()
    token = jwt.encode({"provider_id": str(provider_id) }, "secret", algorithm="HS256")
    print(token)
    return token