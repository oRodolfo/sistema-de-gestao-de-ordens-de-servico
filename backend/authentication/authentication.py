from rest_framework_simplejwt.authentication import JWTAuthentication
from usuario.models import Usuario
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('id_usuario')
            return Usuario.objects.get(id_usuario=user_id)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuário não encontrado')