import re

email_validator    = re.compile('^[a-zA-Z\d+-.]+@[a-zA-Z\d+-.]+\.[a-zA-Z]{2,3}$')
password_validator = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{10,}$')
nickname_validator = re.compile('[a-zA-Z가-힣0-9]+')