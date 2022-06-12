import xmltodict
import redis, json, uuid, time, calendar, csv, io
import yaml

allowed_types = {
    "application/json",
    "application/xml",
    "application/x-yaml",
    "text/tab-separated-values",
}

records_expiration = 120

r = redis.Redis(
    host="localhost", port=9000, db=0, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81", charset="utf-8", decode_responses=True
)


def save_message(body, type, topic, author):
    if type == "application/json":
        body_dict = json.load(body)
    elif type == "application/xml":
        body_dict = xmltodict.parse(body)
    elif type == "application/x-yaml":
        body_dict = yaml.safe_load(body)
        print(body_dict)
    elif type == "text/tab-separated-values":
        body_dict = ""
        byte_str = body.read()
        text_obj = byte_str.decode("UTF-8")
        rd = csv.reader(io.StringIO(text_obj), delimiter="\t", quotechar='"')
        print(rd[1])
        # for row in rd:
        #     print(row)

    message = body_dict["message"]

    message_id = uuid.uuid1()

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    key = f"provider:{author}/topic:{topic}/uid:{message_id}/timestamp:{time_stamp}"

    r.hset(key, "m", message)
    r.hset(key, "a", author)
