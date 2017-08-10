import uuid
import bcrypt


def token_string():
    """Generate a unique string with the uuid4 protocol"""
    return uuid.uuid4()


def encrypt_string( string ):
    """Encrypts any provided string with Bcrypt"""

    password_bytes = string.encode( 'utf-8' )
    return bcrypt.hashpw( password_bytes, bcrypt.gensalt() )


def password_match( hashed_password, string ):
    """Check if a Bcrypted and a not crypted passwords match."""
    
    password_bytes = string.encode( 'utf-8' )
    hash_bytes = hashed_password.encode( 'utf-8' )

    if bcrypt.checkpw( password_bytes, hash_bytes ):
        return True  # match
    else:
        return False  # Don't match

