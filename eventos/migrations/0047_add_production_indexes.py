# Generated for production hardening.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_s", "0046_add_upload_validators"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arquivoexcel",
            name="criado_em",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="arquivoexcel",
            name="nome",
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="corredor",
            name="categoria",
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="corredor",
            name="colocacao",
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name="corredor",
            name="nome",
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="corredor",
            name="tempo_segundos",
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="corrida",
            name="data",
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name="participante",
            name="nome",
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AddIndex(
            model_name="corredor",
            index=models.Index(
                fields=["arquivo", "colocacao"],
                name="api_s_corre_arquivo_15e3e2_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="corredor",
            index=models.Index(
                fields=["arquivo", "categoria", "tempo_segundos"],
                name="api_s_corre_arquivo_35722b_idx",
            ),
        ),
    ]
