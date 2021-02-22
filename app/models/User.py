from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt
salt = bcrypt.gensalt()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    # We add a new validate_email() method to the class that a @validates('email') decorator wraps. 
    # The validate_email() method returns what the value of the email column should be, and the @validates() decorator internally handles the rest. 
    # This decorator is similar to the @bp.routes() decorator that we used previously to handle the route functions.
    # The validate_email() method uses the assert keyword to check if an email address contains an at-sign character (@). 
    # The assert keyword automatically throws an error if the condition is false, thus preventing the return statement from happening.
    @validates('email')
    def validate_email(self, key, email):
        # make sure email address contains @ character
        assert '@' in email

        return email

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 4

        # encrypt password
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # This uses the checkpw() method to compare the incoming password (that is, the password parameter) to the one saved on the User object (self.password).
    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
