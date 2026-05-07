from rest_framework_simplejwt.authentication import JWTAuthentication
from usuario.models import Usuario
from rest_framework.exceptions import AuthenticationFailed

# Customizando a autenticação JWT para buscar o usuário com base no id_usuario presente no token
class CustomJWTAuthentication(JWTAuthentication):
    #sobrescrevendo o método get_user para buscar o usuário com base no id_usuario presente no token
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('id_usuario') #pegando o id_usuario do token
            return Usuario.objects.get(id_usuario=user_id) #buscando o usuário com base no id_usuario presente no token
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuário não encontrado') #se o usuário não for encontrado, lança uma exceção de autenticação falhou
        
       # 1. Lê o id_usuario de dentro do token
       # 2. Busca o usuário correspondente na tabela usuario
       # 3. Define esse usuário como request.user (ele representa o usuário real do sistema TechOrder)