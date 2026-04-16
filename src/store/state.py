"""
State Module stores all the centralized info to run the application smoothly
and distributes the info all over the application whereever needed.
"""

class AppState:
    """App State Class to store centralized info"""
    
    is_logged_in = False
    cookies = None
    _listeners = []

    @classmethod
    def add_listener(cls, callback):
        """Register a function to be called when the state changes"""
        cls._listeners.append(callback)

    @classmethod
    def set_login_state(cls, logged_in, cookies=None):
        """Update state and notify all registered UI components"""
        cls.is_logged_in = logged_in
        cls.cookies = cookies
        for callback in cls._listeners:
            callback()