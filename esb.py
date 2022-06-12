from bottle import get, post, delete, run, response, request
import json, auth, esb_transform as transform

############## THIS IS ABOUT READING MESSAGES
@get("/topic/<topic>/limit/<limit:int>")
def _(topic, limit):
    auth.verify_token()
    content_type = validate_content_type()
    response.content_type = content_type
    try:
        # Validation
        if limit <= 0:
            raise Exception(f"limit cannot be {limit}")
        return transform.get_messages(topic, limit, content_type)

    except Exception as ex:
        raise
        response.status = 400
        return str(ex)


############## THIS IS ABOUT WRITING MESSAGES
@post("/topic/<topic>")
def _(topic):
    token_data = auth.verify_token()
    provider_id = token_data["provider_id"]
    print(provider_id)
    content_type = validate_content_type()
    return transform.save_message(
        body=request.body, topic=topic, type=content_type, author=provider_id
    )


@delete("/message/<message_id>")
def _(message_id):
    token_data = auth.verify_token()
    provider_id = token_data["provider_id"]
    return transform.delete_message(message_id, provider_id)


def validate_content_type():
    content_type = request.headers.get("Content-Type", None)
    if content_type not in transform.allowed_types:
        response.status = 415
        return {
            "code": "invalid_content_type",
            "description": f"Received: {content_type}, we support: {transform.allowed_types}",
        }
    return content_type


# message =


##############
run(host="127.0.0.1", port=3000, debug=True, reloader=True)
