from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

class LoginRequiredMiddleware(BaseMiddleware):
    """
    Custom middleware that forces a user to be logged in.
    If user is AnonymousUser raise an exception.
    Intended to be used with AuthMiddlewareStack.
    """

    async def __call__(self, scope, receive, send):
        user = scope['user']
        if not user.is_authenticated:
            raise PermissionDenied(_('Login required'))
        return await super().__call__(scope, receive, send)


class TokenAuthMiddleware(BaseMiddleware):
    """
    This middleware populates scope['user'] from a token
    """
    header_name = 'authorization'
    keyword = 'Token'
    model = None

    async def __call__(self, scope, receive, send):
        # Get authorization header
        auth = self.get_authorization_header(scope).split()

        if auth and auth[0].lower() == self.keyword.lower().encode() and \
            len(auth) == 2:
            try:
                token = auth[1].decode()
            except UnicodeError:
                pass

            user, token = await self.authenticate_credentials(token)
            if user is not None:
                scope['user'] = user
                scope['auth'] = token

        return await super().__call__(scope, receive, send)

    
    async def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = await sync_to_async(model.objects.select_related('user').get)(key=key)
        except model.DoesNotExist:
            return None, token

        if not token.user.is_active:
            raise PermissionDenied(_('User inactive or deleted.'))

        return token.user, token
    
    def get_authorization_header(self, scope):
        header_list = scope['headers']
        for key, value in header_list:
            if key.decode().lower() == 'authorization':
                return value
        return ''

    
    def get_model(self):
        """
        Provides flexibility. If another model for tokens is being used
        then subclass this class and override `model` property
        """
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token
