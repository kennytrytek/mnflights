from webapp2 import Route

from .views.home import HomeRequestHandler
from .views.login import (
    CreateAccountHandler, CreateNewPasswordHandler, ForgotPasswordHandler,
    LoginRequestHandler, LogoutRequestHandler)

view_endpoints = [
    Route('/', handler=HomeRequestHandler),
    Route('/login', handler=LoginRequestHandler),
    Route('/create_account', handler=CreateAccountHandler),
    Route('/create_new_password', CreateNewPasswordHandler),
    Route('/forgot_password', handler=ForgotPasswordHandler),
    Route('/logout', handler=LogoutRequestHandler)
]
