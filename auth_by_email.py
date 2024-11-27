import hashlib
import time
import uuid

from py4web import action, request, abort, redirect, URL
from py4web.core import Fixture
from py4web.utils.form import Form, FormStyleBulma
from pydal import Field
from pydal.validators import IS_EMAIL, IS_NOT_EMPTY
from yatl.helpers import A


class AuthByEmail(Fixture):
    
    pass


class Enforcer(Fixture):
    
    pass                        
            