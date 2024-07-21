import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware  # Correct import here
from channels.db import database_sync_to_async
from django.db import close_old_connections
from core.models import User  # Ensure this import path is correct




@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        
        # Extract token from query string
        query_string = scope['query_string'].decode()
        token_key = None
        if 'access=' in query_string:
            token_key = query_string.split('access=')[1]
        
        if token_key:
            try:
                payload = jwt.decode(token_key, settings.SECRET_KEY, algorithms=["HS256"])
                scope['user'] = await get_user(payload['user_id'])
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
