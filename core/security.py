from jose import jwt, JWTError
from passlib.context import CryptContext
import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_in: int = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The data to include in the token.
        expires_in (int, optional): The expiration time in seconds. Defaults to None.

    Returns:
        str: The encoded JWT token.

    Raises:
        JWTError: If there's an error during encoding the token.
    """
    to_encode = data.copy()
    
    # Set expiration time if provided
    if expires_in:
        expire = datetime.utcnow() + timedelta(seconds=expires_in)
        to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError as error:
        logging.error(f"Error encoding JWT token: {str(error)}")
        raise error

def verify_password(plain_password, hashed_password):
    '''Verify a plain password against a hashed password.'''

    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    '''Hash a plain password using the configured hashing scheme.'''
    return pwd_context.hash(password)
