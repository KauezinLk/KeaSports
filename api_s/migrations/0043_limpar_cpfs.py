# Generated migration to clean CPF data before altering field length

from django.db import migrations


def limpar_cpfs(apps, schema_editor):
    """Remove formatação dos CPFs existentes no banco"""
    Participante = apps.get_model('api_s', 'Participante')
    for participante in Participante.objects.all():
        cpf_limpo = ''.join(filter(str.isdigit, participante.cpf))
        if cpf_limpo != participante.cpf:
            participante.cpf = cpf_limpo
            participante.save(update_fields=['cpf'])


def reverter_cpfs(apps, schema_editor):
    """Não é possível reverter de forma segura"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api_s', '0042_alter_participante_tamanho_camisa'),
    ]

    operations = [
        migrations.RunPython(limpar_cpfs, reverter_cpfs),
    ]