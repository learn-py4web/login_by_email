import hashlib
import time
import uuid

from py4web import action, request, abort, redirect, URL
from py4web.core import Fixture
from py4web.utils.form import Form, FormStyleBulma
from pydal import Field


class AuthByEmail(Fixture):
    
    def __init__(self, session):
        self.session = session
        self.__prerequisites__ = [session]
        
        # Registers the endpoints. 
        
        # Endpoint for login form. 
        @action('auth/login', method=['GET', 'POST'])
        @action.uses(session, 'login.html')
        def _():
            login_form = Form([Field('email')], csrf_session=session, formstyle=FormStyleBulma)
            if form.accepted:
                # Creates an invitation session secret for the invitation. 
                invitation_secret = str(uuid.uuid4())
                session['invitation_secret'] = invitation_secret
                # And the time. 
                t = str(time.time())
                # Signes email and secret and time. 
                h = hashlib.sha256()
                h.update(login_form.vars.email.encode('utf-8'))
                h.update(invitation_secret.encode('utf-8'))
                h.update(t.encode('utf-8'))
                # Sends the login link. 
                login_email = URL('auth/validate', vars=dict(email=login_form.vars.email, time=t, signature=h.hexdigest()), scheme=True, host=True)
                # We should email this URL, but we just go to it. 
                redirect(login_email)
            return dict(login_form=login_form)
        
        # Endpoint for access from login. 
        @action('auth/validate')
        @action.uses(session)
        def _():
            email = request.query.get('email')
            time = request.query.get('time')
            signature = request.query.get('signature')
            # Checks the signature. 
            h = hashlib.sha256()
            h.update(email.encode('utf-8'))
            h.update(session['invitation_secret'].encode('utf-8'))
            h.update(time.encode('utf-8'))
            if h.hexdigest() != signature:
                abort(403)
            # Checks the time. 
            if float(time) < time.time() - 60 * 5:
                abort(403)
            # We are good. 
            session['email'] = email
            redirect(URL('index'))

            
            