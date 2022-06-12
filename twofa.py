import redis
import random
import stub_send_email


records_expiration = 120


r = redis.Redis(
    host="localhost", port=9000, db=0, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81"
)


def generate_save_send(email):
    code = random.randint(1000, 9999)
    r.set(email, code, ex=records_expiration)
    stub_send_email.send_email(
        receiver_email=email,
        random_auth_code=code,
    )


def verify(email, code):
    db_code = r.get(email).decode()
    if code == db_code:
        r.delete(email)
        return True
    return False
