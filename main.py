USER_DATA = {
    "email": "hello",
    "password": "hello",
    "nickname": "hello",
    "intro": "hello",
    "avatar": "hello",
}

password = USER_DATA["password"]
new_user_data = {
    **USER_DATA,
    "password1": password,
    "password2": password,
}

new_user_data.pop("password")

print(new_user_data)
