import random
import string

def generate_random_email(length=10):
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "example.com"])
    email = f"{username}@{domain}"
    return email

