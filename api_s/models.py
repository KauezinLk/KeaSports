from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Participante(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="participante"
    )

    corrida = models.ForeignKey('Corrida', on_delete=models.CASCADE, related_name='participantes')

    nome = models.CharField(max_length=100)

    data_nascimento = models.DateField()
    idade = models.IntegerField(blank=True, null=True)
    categoria = models.CharField(max_length=8, blank=True, null=True)

    cpf = models.CharField(max_length=11, unique=True)

    equipe = models.CharField(max_length=100, null=True, blank=True)

    TAMANHO_CAMISA = [
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
    ]

    tamanho_camisa = models.CharField(max_length=1, choices=TAMANHO_CAMISA, default='M', null=True, blank=True)

    SEXO_OPCOES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    sexo = models.CharField(max_length=1, choices=SEXO_OPCOES, default='M', null=True, blank=True)

    def calcular_categoria(self):

        if self.idade is None:
            return ""

        if self.idade <= 19:
            return "15–19"
        elif 20 <= self.idade <= 24:
            return "20–24"
        elif 25 <= self.idade <= 29:
            return "25–29"
        elif 30 <= self.idade <= 39:
            return "30–39"
        elif 40 <= self.idade <= 44:
            return "40–44"
        elif 45 <= self.idade <= 49:
            return "45–49"
        elif 50 <= self.idade <= 54:
            return "50–54"
        elif 55 <= self.idade <= 59:
            return "55–59"
        elif 60 <= self.idade <= 64:
            return "60–64"
        else:
            return "65+"

    def save(self, *args, **kwargs):

        if self.data_nascimento:
            hoje = date.today()

            self.idade = hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) <
                (self.data_nascimento.month, self.data_nascimento.day)
            )

            self.categoria = self.calcular_categoria()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.idade} anos) - {self.categoria} - {self.sexo}"


class Corrida(models.Model):

    nome = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    data = models.DateField()
    imagem = models.ImageField(upload_to='corridas/', blank=True, null=True)

    class Meta:
        verbose_name = "Inscrição Corrida"
        verbose_name_plural = "Inscrições Corridas"

    def __str__(self):
        return self.nome


class ArquivoExcel(models.Model):

    nome = models.CharField(max_length=50)
    data_corrida = models.CharField(max_length=15, null=True, blank=True)
    local = models.CharField(max_length=60, null=True, blank=True)
    arquivo = models.FileField(upload_to='uploads/')
    criado_em = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='imagens/', blank=True, null=True)

    class Meta:
        verbose_name = "Resultado"
        verbose_name_plural = "Resultados"

    def __str__(self):
        return self.nome


class Corredor(models.Model):

    participante = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name="resultados",
        null=True,
        blank=True
    )

    arquivo = models.ForeignKey(ArquivoExcel, on_delete=models.CASCADE, null=True, blank=True)

    colocacao = models.IntegerField()
    numero = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    equipe = models.CharField(max_length=100, blank=True, null=True)

    tempo_segundos = models.FloatField(null=True, blank=True)
    tempo_formatado = models.CharField(max_length=20, null=True, blank=True)

    Vel_media = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Classificação"
        verbose_name_plural = "Classificações"

    def __str__(self):
        return self.nome


class Resultados(models.Model):

    nome = models.CharField(max_length=100)
    local = models.CharField(max_length=100)
    data = models.DateField()

    def __str__(self):
        return self.nome

# IMAGEM BOAS VINDAS SITE   

class ImagemBase(models.Model):
    titulo = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='imagens/')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo