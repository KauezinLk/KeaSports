# Generated for production hardening.

import eventos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_s", "0045_imagembase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arquivoexcel",
            name="arquivo",
            field=models.FileField(
                upload_to="uploads/",
                validators=[
                    eventos.validators.validate_file_size,
                    eventos.validators.validate_excel_extension,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="arquivoexcel",
            name="imagem",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="imagens/",
                validators=[
                    eventos.validators.validate_file_size,
                    eventos.validators.validate_image_extension,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="corrida",
            name="imagem",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="corridas/",
                validators=[
                    eventos.validators.validate_file_size,
                    eventos.validators.validate_image_extension,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="imagembase",
            name="imagem",
            field=models.ImageField(
                upload_to="imagens/",
                validators=[
                    eventos.validators.validate_file_size,
                    eventos.validators.validate_image_extension,
                ],
            ),
        ),
    ]
