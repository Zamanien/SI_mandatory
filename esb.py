from bottle import get, post, run, response, request
import json, auth, esb_transform as transform
import redis
from datetime import datetime


r = redis.Redis(
    host="localhost", port=9000, db=0, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81", charset="utf-8", decode_responses=True
)


# r.hset("user:12345", mapping={"id": "1", "email": "@a", "token": "12345"})
# r.hset("user:67890", mapping={"id": "2", "email": "@b", "token": "67890"})

############## THIS IS ABOUT READING MESSAGES
@get("/topic/<topic>/limit/<limit:int>")
def _(topic, limit):
    auth.verify_token()
    response.content_type = "application/json"
    try:
        #Validation
        if limit <= 0:
            raise Exception(f"limit cannot be {limit}")
        
        #Get keys related to partial search of 'Topic'
        keys = r.keys('*'+topic+'*')
        #Validation
        if keys == None:
            raise Exception(f'No keys found with {topic}')

        timestamps = {}
        messages = {}
        n = 0
        #Loop thrigh keys and timestamps of those keys
        for key in keys:
            message = r.hgetall(key)
            messages[n]=message
            timestamps[n]=datetime.fromtimestamp(int(key[-10:]))
            n+=1
        
        #Sort by timestamps & retrieve their keys
        sorted_timestamps=list(dict(sorted(timestamps.items(),key= lambda x:x[1])).keys())
        #index by custom limit (latest timestamps)
        index_out = sorted_timestamps[-limit:]

        #Dict comprehension -> return messages matching indexed keys
        return {k:messages[k] for k in index_out}


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
