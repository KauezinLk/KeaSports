from rest_framework import serializers
from .models import Participante

# O serializer converte o modelo Participante para JSON e valida os dados que chegam do React.

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'  # Inclui todos os campos do modelo

