from rest_framework import viewsets, status
from rest_framework.response import Response
from users.models import Usuario
from users.serializers import UsuarioSerializer, CriarUsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CriarUsuarioSerializer
        return UsuarioSerializer