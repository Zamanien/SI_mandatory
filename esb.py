from bottle import get, post, run, response, request
import json, auth, esb_transform as transform

# r.hset("user:12345", mapping={"id": "1", "email": "@a", "token": "12345"})
# r.hset("user:67890", mapping={"id": "2", "email": "@b", "token": "67890"})

messages = [
    {
        "f768ff7c-893f-48be-8afc-837ff2390f38/recipies/french tomatoes/1654964418": {
            "c": "Prepare this , cook that hwatever",
            "a": "service a",
        }
    },
    {
        "f768ff7c-893f-48be-8afc-837ff2390f38/shows/french tomatoes/1654964418": {
            "c": "Prepare this , cook that hwatever",
            "a": "service a",
        }
    },
    {
        "f768ff7c-893f-48be-8afc-837ff2390f38/animals/french tomatoes/1654964418": {
            "c": "Prepare this , cook that hwatever",
            "a": "service a",
        }
    },
]

############## THIS IS ABOUT READING MESSAGES
@get("/provider/<id>/from/<last_message_id>/limit/<limit:int>")
def _(id, last_message_id, limit):
    auth.verify_token()
    response.content_type = "application/json"
    try:
        # validation
        if limit <= 0:
            raise Exception(f"limit cannot be {limit}")
        start_index = -1
        # for message in messages[id]:
        #     print(message)
        #     if message["id"] == last_message_id:
        #         start_index = messages[id].index(message)
        for i in range(len(messages[id])):
            if last_message_id in messages[id][i].values():
                start_index = i + 1
                break

        # validation that index exists
        if start_index == -1:
            raise Exception(f"no message with id {last_message_id}")

        # Handle response
        return json.dumps(messages[id][start_index : limit + start_index])
    except Exception as ex:
        response.status = 400
        return str(ex)


############## THIS IS ABOUT WRITING MESSAGES
@post("/provider/<provider_id>/topic/<topic>")
def _(provider_id, topic):
    # todo: get the provider id from the token
    auth.verify_token()
    content_type = request.headers.get("Content-Type", None)
    if content_type not in transform.allowed_types:
        response.status = 415
        return {
            "code": "invalid_content_type",
            "description": f"Received: {content_type}, we support: {transform.allowed_types}",
        }
    transform.save_message(
        body=request.body, topic=topic, type=content_type, author=provider_id
    )


# message =


##############
run(host="127.0.0.1", port=3000, debug=True, reloader=True)
