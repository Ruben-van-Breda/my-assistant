"""
Authentication component for handling user authentication and session management.
"""
from flask import session
from functools import wraps
from flask import redirect, url_for

class Auth:
    """Authentication handler class"""
    
    @staticmethod
    def login(email: str, password: str) -> bool:
        """
        Validate user credentials and set session.
        
        @param email - User's email address
        @param password - User's password
        @returns True if login successful, False otherwise
        """
        if password == 'ewout':
            session['userId'] = email
            return True
        return False
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return 'userId' in session
    
    @staticmethod
    def logout():
        """Clear user session"""
        session.pop('userId', None)

def login_required(f):
    """
    Decorator to require login for routes.
    
    @param f - Function to decorate
    @returns Decorated function that checks authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not Auth.is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function 