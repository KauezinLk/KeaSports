from django import forms
from .models import Participante

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante # Define qual Modelo este Formulário irá manipular.
        fields = ['nome', 'data_nascimento', 'equipe', 'cpf', 'sexo', 'tamanho_camisa']  
        labels = {
            'cpf': 'CPF',  # Força o rótulo em caixa alta
        }
