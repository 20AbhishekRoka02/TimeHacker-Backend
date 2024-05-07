from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta, datetime, timezone

from jose import JWTError, jwt

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    # else:
    #     expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


            
    

if __name__=="__main__":
    print(os.environ["SECRET_KEY"])
    print(os.environ["ALGORITHM"])
    # print(verify_password("12345678","$2b$12$GzkuZRgJJ9AHJAyZ424t2uI.UGJboBMSkJMkwQ73pn2L.aDlpRESu"))