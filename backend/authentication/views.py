from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from usuario.models import Usuario
from grupo_usuario.models import GrupoUsuario

class TokenObtainPairView(APIView):
    def post(self, request):
        #recebendo email e senha do corpo da requisição
        email = request.data.get('email')
        senha = request.data.get('senha')

        #validando se email e senha foram fornecidos e se estão corretos
        if not email or not senha:
            return Response(
                {'erro': 'E-mail e senha são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response(
                {'erro': 'Credenciais inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        #verificando se a senha fornecida corresponde à senha armazenada para o usuário (que está armazenada como um hash)
        if not check_password(senha, usuario.senha_hash):
            return Response(
                {'erro': 'Credenciais inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        #buscando os grupos do usuário para incluir no token
        vinculos = GrupoUsuario.objects.filter(
            usuario=usuario
        ).select_related('grupo')

        #transformando os grupos do usuário em uma lista de nomes de grupos para incluir no token
        grupos_usuario = [
            vinculo.grupo.desc_grupo
            for vinculo in vinculos
        ]

        #criando os tokens de acesso e refresh, incluindo as informações do usuário e seus grupos
        refresh = RefreshToken()
        refresh['id_usuario'] = usuario.id_usuario #identificando qual é o id usuario
        refresh['nome'] = usuario.nome #identificando quem é o usuario
        refresh['email'] = usuario.email #identificando qual é o email do usuario
        refresh['grupos'] = grupos_usuario #identificando quais são os grupos do usuario

        #criando o token de acesso a partir do token de refresh, para incluir as mesmas informações do usuário e seus grupos
        access = refresh.access_token
        access['id_usuario'] = usuario.id_usuario #identificando qual é o id usuario
        access['nome'] = usuario.nome #identificando quem é o usuario
        access['email'] = usuario.email #identificando qual é o email do usuario
        access['grupos'] = grupos_usuario #identificando quais são os grupos do usuario

        #retornando os tokens e as informações do usuário no corpo da resposta
        return Response({
            'refresh': str(refresh),
            'access': str(access),
            'usuario': {
                'id_usuario': usuario.id_usuario,
                'nome': usuario.nome,
                'email': usuario.email,
                'grupos': grupos_usuario
            }
        })