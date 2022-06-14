import redis, os, random, stub_send_email


records_expiration = 120


redis_port = os.environ.get("redis_port")
redis_pass = os.environ.get("redis_pass")

r = redis.Redis(
    host="localhost",
    port=redis_port,
    db=0,
    password=redis_pass,
    charset="utf-8",
    decode_responses=True,
)


def generate_save_send(email):
    code = random.randint(1000, 9999)
    r.set(email, code, ex=records_expiration)
    stub_send_email.send_email(
        receiver_email=email,
        random_auth_code=code,
    )


def verify(email, code):
    db_code = r.get(email)
    if code == db_code:
        r.delete(email)
        return True
    return False
