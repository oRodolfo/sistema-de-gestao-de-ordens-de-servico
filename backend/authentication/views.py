from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from usuario.models import Usuario
from grupo.models import Grupo
from grupo_usuario.models import GrupoUsuario


class TokenObtainPairView(APIView):
    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')

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

        if not check_password(senha, usuario.senha_hash):
            return Response(
                {'erro': 'Credenciais inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        vinculos = GrupoUsuario.objects.filter(id_usuario=usuario.id_usuario)
        ids_grupos = [v.id_grupo for v in vinculos]

        grupos_usuario = list(
            Grupo.objects.filter(id_grupo__in=ids_grupos)
            .values_list('desc_grupo', flat=True)
        )

        refresh = RefreshToken()
        refresh['id_usuario'] = usuario.id_usuario
        refresh['nome'] = usuario.nome
        refresh['email'] = usuario.email
        refresh['grupos'] = grupos_usuario

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': {
                'id_usuario': usuario.id_usuario,
                'nome': usuario.nome,
                'email': usuario.email,
                'grupos': grupos_usuario
            }
        })