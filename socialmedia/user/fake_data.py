import random
import string


def generate_random_string(length=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email(first_name, last_name):
    domain = "@example.com"
    return f"{first_name.lower()}.{last_name.lower()}{domain}"


def get_users(num_of_users):
    user_data = []

    for _ in range(num_of_users):
        first_name = generate_random_string(random.randint(5, 10))
        last_name = generate_random_string(random.randint(5, 10))
        email = generate_random_email(first_name, last_name)
        password = "12345"
        user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "username": email,
            "password": password,
        }
        user_data.append(user)

    return user_data


def create_fake_user(num_of_users=50):
    from .models import User

    users = get_users(num_of_users)

    for user in users:
        u = User(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            username=user["username"],
        )
        u.set_password(user["password"])
        u.save()
