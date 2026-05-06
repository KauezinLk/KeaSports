import datetime
import logging

import pandas as pd
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ArquivoExcel, Corredor


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = {"#", "N", "Nome", "Categoria", "Tempo", "Vel. Média"}


def parse_tempo_segundos(tempo):
    tempo_str = str(tempo or "").strip()
    if not tempo_str:
        return None, tempo_str

    for fmt in ("%H:%M:%S.%f", "%H:%M:%S"):
        try:
            parsed = datetime.datetime.strptime(tempo_str, fmt)
            return (
                parsed.hour * 3600
                + parsed.minute * 60
                + parsed.second
                + parsed.microsecond / 1e6
            ), tempo_str
        except ValueError:
            continue

    return None, tempo_str


@receiver(post_save, sender=ArquivoExcel)
def extrair_dados_excel(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        df = pd.read_excel(instance.arquivo.path)
        df.columns = df.columns.str.strip()

        missing_columns = REQUIRED_COLUMNS - set(df.columns)
        if missing_columns:
            logger.warning(
                "ArquivoExcel %s ignorado: colunas ausentes %s",
                instance.pk,
                sorted(missing_columns),
            )
            return

        if "#" in df.columns:
            df = df.sort_values(by="#", ascending=True)

        corredores = []
        for _, row in df.iterrows():
            colocacao_str = str(row.get("#", "")).replace("º", "").replace("Âº", "").strip()
            try:
                colocacao_num = int(colocacao_str)
            except (TypeError, ValueError):
                logger.warning(
                    "Linha ignorada no ArquivoExcel %s: colocacao invalida %r",
                    instance.pk,
                    colocacao_str,
                )
                continue

            tempo_segundos, tempo_formatado = parse_tempo_segundos(row.get("Tempo", ""))

            corredores.append(
                Corredor(
                    arquivo=instance,
                    colocacao=colocacao_num,
                    numero=row.get("N", ""),
                    nome=row.get("Nome", ""),
                    categoria=row.get("Categoria", ""),
                    equipe=row.get("Equipe", ""),
                    tempo_segundos=tempo_segundos,
                    tempo_formatado=tempo_formatado,
                    Vel_media=row.get("Vel. Média", ""),
                )
            )

        if corredores:
            with transaction.atomic():
                Corredor.objects.bulk_create(corredores, batch_size=500)

    except Exception:
        logger.exception("Falha ao processar ArquivoExcel %s", instance.pk)
