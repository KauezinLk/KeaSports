from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.test import TestCase, override_settings
from django.urls import reverse

from eventos.models import ArquivoExcel, Corredor, Corrida, Inscricao, Participante
from eventos.signals import extrair_dados_excel
from eventos.views.corrida_views import calcular_rankinkg


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


@override_settings(STORAGES=TEST_STORAGES)
class RankinkgTests(TestCase):
    def criar_arquivo_resultado(self):
        post_save.disconnect(extrair_dados_excel, sender=ArquivoExcel)
        try:
            return ArquivoExcel.objects.create(
                nome="Etapa Teste",
                data_corrida="01/05/2026",
                local="Sorocaba",
                arquivo="uploads/etapa-teste.xlsx",
            )
        finally:
            post_save.connect(extrair_dados_excel, sender=ArquivoExcel)

    def test_pontuacao_categoria_desce_quando_atleta_ja_pontuou_no_geral(self):
        arquivo = self.criar_arquivo_resultado()

        for posicao in range(1, 12):
            Corredor.objects.create(
                arquivo=arquivo,
                colocacao=posicao,
                numero=str(posicao),
                nome=f"Atleta {posicao}",
                categoria="M 35-39",
                tempo_segundos=float(posicao),
                tempo_formatado=f"00:{posicao:02d}:00",
                Vel_media="12 km/h",
            )

        ranking_geral, ranking_categoria = calcular_rankinkg()

        self.assertEqual(ranking_geral["M"][0]["nome"], "Atleta 1")
        self.assertEqual(ranking_geral["M"][0]["pontos"], 21)
        self.assertEqual(ranking_categoria["35 - 39"]["M"][0]["nome"], "Atleta 6")
        self.assertEqual(ranking_categoria["35 - 39"]["M"][0]["pontos"], 10)
        self.assertEqual(ranking_categoria["35 - 39"]["M"][4]["nome"], "Atleta 10")
        self.assertEqual(ranking_categoria["35 - 39"]["M"][4]["pontos"], 2)
        self.assertEqual(ranking_categoria["35 - 39"]["M"][5]["nome"], "Atleta 11")
        self.assertEqual(ranking_categoria["35 - 39"]["M"][5]["pontos"], 1)

    def test_ranking_geral_feminino_considera_apenas_mulheres(self):
        arquivo = self.criar_arquivo_resultado()

        for posicao in range(1, 27):
            Corredor.objects.create(
                arquivo=arquivo,
                colocacao=posicao,
                numero=str(posicao),
                nome=f"Homem {posicao}",
                categoria="35 a 39 anos - Masculino",
                tempo_segundos=float(posicao),
                tempo_formatado=f"00:{posicao:02d}:00",
                Vel_media="12 km/h",
            )

        for indice, posicao in enumerate(range(27, 33), start=1):
            Corredor.objects.create(
                arquivo=arquivo,
                colocacao=posicao,
                numero=str(posicao),
                nome=f"Mulher {indice}",
                categoria="40 a 44 anos - Feminino",
                tempo_segundos=float(posicao),
                tempo_formatado=f"00:{posicao:02d}:00",
                Vel_media="12 km/h",
            )

        ranking_geral, ranking_categoria = calcular_rankinkg()

        self.assertEqual(ranking_geral["M"][0]["nome"], "Homem 1")
        self.assertEqual(ranking_geral["M"][0]["pontos"], 21)
        self.assertEqual(ranking_geral["F"][0]["nome"], "Mulher 1")
        self.assertEqual(ranking_geral["F"][0]["pontos"], 21)
        self.assertEqual(ranking_geral["F"][4]["nome"], "Mulher 5")
        self.assertEqual(ranking_geral["F"][4]["pontos"], 12)
        self.assertEqual(ranking_categoria["40 - 44"]["F"][0]["nome"], "Mulher 6")
        self.assertEqual(ranking_categoria["40 - 44"]["F"][0]["pontos"], 10)
