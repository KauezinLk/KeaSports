from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_size = getattr(settings, "FILE_UPLOAD_MAX_MEMORY_SIZE", 5 * 1024 * 1024)
    if value.size > max_size:
        max_mb = max_size / (1024 * 1024)
        raise ValidationError(f"Arquivo maior que o limite permitido de {max_mb:.0f} MB.")


def validate_excel_extension(value):
    allowed_extensions = {".xlsx", ".xls"}
    extension = Path(value.name).suffix.lower()
    if extension not in allowed_extensions:
        raise ValidationError("Envie apenas arquivos Excel nos formatos .xlsx ou .xls.")


def validate_image_extension(value):
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    extension = Path(value.name).suffix.lower()
    if extension not in allowed_extensions:
        raise ValidationError("Envie apenas imagens .jpg, .jpeg, .png ou .webp.")
