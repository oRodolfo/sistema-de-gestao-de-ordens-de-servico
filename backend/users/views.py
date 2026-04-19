from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Usuario, Grupo, GrupoUsuario
from users.serializers import UsuarioSerializer, CriarUsuarioSerializer, LoginSerializer, GrupoSerializer, GrupoUsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CriarUsuarioSerializer
        return UsuarioSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class GrupoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = GrupoUsuario.objects.all()
    serializer_class = GrupoUsuarioSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Dados inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'Email ou senha inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=usuario.username, password=password)
        if user is None:
            return Response({'error': 'Email ou senha inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': usuario.id,
                'email': usuario.email,
                'nome': usuario.nome,
            }
        }, status=status.HTTP_200_OK)