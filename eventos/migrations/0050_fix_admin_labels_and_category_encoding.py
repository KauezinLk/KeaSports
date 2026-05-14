from django.db import migrations


def fix_category_encoding(apps, schema_editor):
    Participante = apps.get_model("api_s", "Participante")
    Corredor = apps.get_model("api_s", "Corredor")

    replacements = {
        "â€“": "-",
        "–": "-",
    }

    for model in (Participante, Corredor):
        for obj in model.objects.exclude(categoria__isnull=True).exclude(categoria=""):
            categoria = obj.categoria
            nova_categoria = categoria

            for antigo, novo in replacements.items():
                nova_categoria = nova_categoria.replace(antigo, novo)

            if nova_categoria != categoria:
                obj.categoria = nova_categoria
                obj.save(update_fields=["categoria"])


class Migration(migrations.Migration):

    dependencies = [
        ("api_s", "0049_remove_participante_corrida_inscricao"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="corrida",
            options={
                "verbose_name": "Inscrição Corrida",
                "verbose_name_plural": "Inscrições Corridas",
            },
        ),
        migrations.AlterModelOptions(
            name="inscricao",
            options={
                "verbose_name": "Inscrição",
                "verbose_name_plural": "Inscrições",
            },
        ),
        migrations.RunPython(fix_category_encoding, migrations.RunPython.noop),
    ]
