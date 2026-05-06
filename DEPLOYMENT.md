# Deploy em producao

## Variaveis obrigatorias

Copie `.env.example` para o ambiente da hospedagem e configure:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_ADMIN_URL`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

Nunca suba `.env` para o Git.

## Comandos de release

```bash
pip install -r requirements-production.txt
npm ci
npm run build:css
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

## Servidor

Use um servidor WSGI em producao, como Gunicorn, atras de Nginx ou do proxy da plataforma:

```bash
gunicorn keasports.wsgi:application
```

O projeto usa WhiteNoise para servir `/static/` em producao. Se usar VPS com Nginx, voce tambem pode servir `staticfiles/` diretamente pelo Nginx.

Configure o proxy ou a plataforma para tratar:

- `/static/` a partir de `staticfiles/`
- `/media/` a partir de um storage persistente. Em Render/Railway, prefira S3, Cloudinary, Supabase Storage ou volume persistente.

## Media/uploads persistente

Por padrao, o projeto usa armazenamento local em desenvolvimento:

```bash
DJANGO_MEDIA_STORAGE=local
```

Em producao, configure um storage S3 compativel:

```bash
DJANGO_MEDIA_STORAGE=s3
AWS_STORAGE_BUCKET_NAME=seu-bucket
AWS_ACCESS_KEY_ID=sua-chave
AWS_SECRET_ACCESS_KEY=sua-chave-secreta
AWS_S3_REGION_NAME=sa-east-1
AWS_LOCATION=media
AWS_QUERYSTRING_AUTH=False
```

Para Supabase Storage, Cloudflare R2 ou MinIO, adicione tambem:

```bash
AWS_S3_ENDPOINT_URL=https://seu-endpoint-s3
```

Se usar dominio/CDN proprio para os uploads:

```bash
AWS_S3_CUSTOM_DOMAIN=cdn.seudominio.com
```

O bucket precisa permitir leitura publica dos arquivos de media, ou voce deve mudar `AWS_QUERYSTRING_AUTH=True` e servir URLs assinadas.

## Start command

```bash
gunicorn keasports.wsgi:application --bind 0.0.0.0:$PORT
```

## Observacoes importantes

- Nao use o disco efemero da plataforma para uploads permanentes.
- Rode `npm audit` e `pip install -r requirements-production.txt` antes de cada release.
- O app label Django ainda e `api_s` por compatibilidade com as migrations antigas.
- `Participante` representa a pessoa. `Inscricao` representa o vinculo entre participante e corrida, permitindo multiplas inscricoes por CPF.

## Antes de publicar

- Gere uma nova `DJANGO_SECRET_KEY`.
- Use banco PostgreSQL de producao, separado do desenvolvimento.
- Crie um superusuario com senha forte.
- Altere `DJANGO_ADMIN_URL`.
- Ative HTTPS.
- Rode `python manage.py check --deploy`.
- Rode `npm audit`.
- Teste cadastro, login, inscricao, resultados e upload de Excel em staging.
