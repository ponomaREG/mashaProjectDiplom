
import re
from datetime import datetime,timezone,timedelta

def validationEmail(email):
    return re.match("[^@]+@[^@]+\.[^@]+", email) is not None


def ctf():
    expiry = int((datetime.now(timezone.utc) + timedelta(seconds=15)).timestamp())
    print(str(expiry).encode())

expiry = int((datetime.now(timezone.utc) + timedelta(seconds=15)).timestamp())
print(expiry)
ctf()