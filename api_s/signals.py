import pandas as pd
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ArquivoExcel, Corredor


@receiver(post_save, sender=ArquivoExcel)
def extrair_dados_excel(sender, instance, created, **kwargs):
    if created:  # Define se o arquivo está sendo salvo ou editado

        # df lê o arquivo Excel do caminho salvo no campo arquivo do modelo ArquivoExcel
        df = pd.read_excel(instance.arquivo.path)
        # Transforma em uma tabela e cria objetos Corredor (transforma cada linha em um corredor)

        # Remove espaços extras dos nomes das colunas (evita erro por espaços invisíveis)
        df.columns = df.columns.str.strip()

        # Organiza a tabela por colocação, se a coluna existir
        if '#' in df.columns:
            df = df.sort_values(by='#', ascending=True)

        # Cria registros no banco
        for _, row in df.iterrows():    
            # iterrows(): É um comando que permite ler linha por linha dessa tabela.
            # O primeiro item retornado por iterrows() é o número da linha (índice), mas como ele não é usado, colocamos _ para ignorá-lo.
            # O segundo item é row, que guarda os dados da linha atual, como se fosse um dicionário (row['colocacao'], row['nome'], etc.).

            
            # Remove o símbolo "º" e converte para inteiro
            colocacao_str = str(row.get('#', '')).replace('º', '').strip()
            try:
                colocacao_num = int(colocacao_str)
            except ValueError:
                colocacao_num = None  # Caso algum valor não seja número

            # Converte o tempo para número (segundos)
            tempo_str = str(row.get('Tempo', '')).strip()
            tempo_em_segundos = None
            if tempo_str:
                try:
                    t = datetime.datetime.strptime(tempo_str, "%H:%M:%S.%f")
                    tempo_em_segundos = (
                        t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6
                    )
                except ValueError:
                    # Tenta formato sem milissegundos, ex: 00:28:04
                    try:
                        t = datetime.datetime.strptime(tempo_str, "%H:%M:%S")
                        tempo_em_segundos = t.hour * 3600 + t.minute * 60 + t.second
                    except ValueError:
                        tempo_em_segundos = None  # valor inválido

            # Cria o registro no banco
            Corredor.objects.create(
                arquivo=instance,
                colocacao=colocacao_num,
                numero=row.get('N', None),
                nome=row.get('Nome', ''),
                categoria=row.get('Categoria', ''),
                equipe=row.get('Equipe', ''),
                tempo_segundos=tempo_em_segundos,   # valor numérico
                tempo_formatado=tempo_str,          # string para exibição
                Vel_media=row.get('Vel. Média', None)
            )
