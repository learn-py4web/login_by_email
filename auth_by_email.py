import hashlib
import time
import uuid

from py4web import action, request, abort, redirect, URL
from py4web.core import Fixture
from py4web.utils.form import Form, FormStyleBulma
from pydal import Field
from pydal.validators import IS_EMAIL
from yatl.helpers import A


class AuthByEmail(Fixture):
    
    def __init__(self, session):
        self.session = session
        self.__prerequisites__ = [session]
        
        # Registers the endpoints. 
        
        # Endpoint for login form. 
        @action('auth/login', method=['GET', 'POST'])
        @action.uses('auth/login.html', session)
        def _():
            login_form = Form([Field('email', requires=IS_EMAIL())], csrf_session=session, formstyle=FormStyleBulma)
            if login_form.accepted:
                # Creates an invitation session secret for the invitation. 
                invitation_secret = str(uuid.uuid4())
                session['invitation_secret'] = invitation_secret
                # And the time. 
                t = str(time.time())
                # Signes email and secret and time. 
                h = hashlib.sha256()
                h.update(login_form.vars['email'].encode('utf-8'))
                h.update(invitation_secret.encode('utf-8'))
                h.update(t.encode('utf-8'))
                # Instead of emailing the link, we redirect the user to a page where they can click on it.
                # This is done just for demo purposes obviously, as we do not have email sending capabilities.  
                login_email = URL('auth/validate', vars=dict(email=login_form.vars['email'], time=t, signature=h.hexdigest()), scheme=True)
                # We should email this URL, but we just go to it. 
                redirect(URL('auth/click', vars=dict(url=login_email)))
            return dict(login_form=login_form)
        
        # This endpoint is used just to let the user click on the link. 
        @action('auth/click')
        @action.uses('auth/click.html', session)
        def _():
            url = request.query.get('url')
            return dict(link=A(url, _href=url))
        
        # Endpoint for access from login. 
        @action('auth/validate')
        @action.uses(session)
        def _():
            email = request.query.get('email')
            t = request.query.get('time')
            signature = request.query.get('signature')
            # Checks the signature. 
            h = hashlib.sha256()
            h.update(email.encode('utf-8'))
            h.update(session['invitation_secret'].encode('utf-8'))
            h.update(t.encode('utf-8'))
            if h.hexdigest() != signature:
                abort(403)
            # Checks the time. 
            if float(t) < time.time() - 60 * 5:
                abort(403)
            # We are good. 
            session['email'] = email
            redirect(URL('index'))
            
        @action('auth/logout')
        @action.uses(session)
        def _():
            session.clear()
            redirect(URL('index'))
            
    def get_user_email(self):
        return self.session.get('email')
        
    def on_success(self, context):
        context["template_inject"] = {"user_email": self.get_user_email()}

            
            