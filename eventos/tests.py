from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from eventos.models import Corrida, Inscricao, Participante


CPF_VALIDO = "52998224725"
CPF_VALIDO_2 = "39053344705"
TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(STORAGES=TEST_STORAGES)
class CadastroParticipanteTests(TestCase):
    def test_cadastro_cria_participante_sem_corrida(self):
        response = self.client.post(
            reverse("register"),
            {
                "nome_completo": "Maria Corredora",
                "cpf": CPF_VALIDO,
                "password": "SenhaForte123!",
                "confirmar_senha": "SenhaForte123!",
                "data_nascimento": "1990-05-10",
                "sexo": "F",
                "tamanho_camisa": "M",
                "equipe": "Kea Team",
            },
        )

        self.assertRedirects(response, reverse("cadastro"))
        self.assertTrue(User.objects.filter(username=CPF_VALIDO).exists())

        participante = Participante.objects.get(cpf=CPF_VALIDO)
        self.assertEqual(participante.nome, "Maria Corredora")
        self.assertEqual(participante.usuario.username, CPF_VALIDO)
        self.assertFalse(Inscricao.objects.filter(participante=participante).exists())


@override_settings(STORAGES=TEST_STORAGES)
class InscricaoCorridaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=CPF_VALIDO,
            password="SenhaForte123!",
            first_name="Joao Corredor",
        )
        self.participante = Participante.objects.create(
            usuario=self.user,
            nome="Joao Corredor",
            cpf=CPF_VALIDO,
            data_nascimento=date(1991, 4, 20),
            sexo="M",
            tamanho_camisa="G",
            equipe="Equipe A",
        )
        self.corrida_1 = Corrida.objects.create(
            nome="Corrida Centro",
            local="Centro",
            data=date.today() + timedelta(days=10),
        )
        self.corrida_2 = Corrida.objects.create(
            nome="Corrida Praia",
            local="Praia",
            data=date.today() + timedelta(days=30),
        )
        self.client.login(username=CPF_VALIDO, password="SenhaForte123!")

    def test_inscricao_cria_vinculo_sem_duplicar_participante(self):
        response = self.client.post(
            reverse("inscrever_corrida", args=[self.corrida_1.id]),
            {
                "cpf": CPF_VALIDO,
                "nome": "Joao Corredor Atualizado",
                "data_nascimento": "1991-04-20",
                "sexo": "M",
                "tamanho_camisa": "M",
                "equipe": "Equipe B",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Participante.objects.filter(cpf=CPF_VALIDO).count(), 1)
        self.assertTrue(
            Inscricao.objects.filter(
                participante=self.participante,
                corrida=self.corrida_1,
            ).exists()
        )

        self.participante.refresh_from_db()
        self.assertEqual(self.participante.nome, "Joao Corredor Atualizado")
        self.assertEqual(self.participante.equipe, "Equipe B")

    def test_mesmo_participante_pode_se_inscrever_em_multiplas_corridas(self):
        for corrida in (self.corrida_1, self.corrida_2):
            self.client.post(
                reverse("inscrever_corrida", args=[corrida.id]),
                {
                    "cpf": CPF_VALIDO,
                    "nome": "Joao Corredor",
                    "data_nascimento": "1991-04-20",
                    "sexo": "M",
                    "tamanho_camisa": "G",
                    "equipe": "Equipe A",
                },
            )

        self.assertEqual(
            Inscricao.objects.filter(participante=self.participante).count(),
            2,
        )

    def test_inscricao_repetida_na_mesma_corrida_nao_duplica(self):
        payload = {
            "cpf": CPF_VALIDO,
            "nome": "Joao Corredor",
            "data_nascimento": "1991-04-20",
            "sexo": "M",
            "tamanho_camisa": "G",
            "equipe": "Equipe A",
        }

        self.client.post(reverse("inscrever_corrida", args=[self.corrida_1.id]), payload)
        response = self.client.post(
            reverse("inscrever_corrida", args=[self.corrida_1.id]),
            payload,
        )

        self.assertContains(response, "Você já estava inscrito nesta corrida.")
        self.assertEqual(
            Inscricao.objects.filter(
                participante=self.participante,
                corrida=self.corrida_1,
            ).count(),
            1,
        )

    def test_usuario_nao_pode_inscrever_cpf_de_outra_pessoa(self):
        Participante.objects.create(
            nome="Outra Pessoa",
            cpf=CPF_VALIDO_2,
            data_nascimento=date(1995, 1, 1),
            sexo="F",
            tamanho_camisa="P",
        )

        response = self.client.post(
            reverse("inscrever_corrida", args=[self.corrida_1.id]),
            {
                "cpf": CPF_VALIDO_2,
                "nome": "Outra Pessoa",
                "data_nascimento": "1995-01-01",
                "sexo": "F",
                "tamanho_camisa": "P",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Inscricao.objects.filter(corrida=self.corrida_1).exists())
