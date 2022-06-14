# this is a stub service, it expects a certain CPR number, and it returns the assisciated email
# if the CPR is not the expected one, then it raises en error
import os


def find_email(cpr):
    return os.environ.get("stub_receiver_email")
