# Deploy do KeaSports no Render

Este projeto esta preparado para rodar no Render com Django, PostgreSQL, Gunicorn e WhiteNoise.

## Comandos do Render

Use estes comandos no Web Service:

```bash
bash build.sh
```

```bash
python manage.py migrate --noinput && gunicorn keasports.wsgi:application --bind 0.0.0.0:$PORT --workers ${WEB_CONCURRENCY:-2} --threads ${GUNICORN_THREADS:-2} --timeout ${GUNICORN_TIMEOUT:-120} --access-logfile - --error-logfile -
```

O primeiro e o **Build Command**. O segundo e o **Start Command**.

## Passo a passo

1. Suba o projeto para o GitHub.
2. No Render, crie um **New Web Service** a partir do repositorio.
3. Escolha runtime **Python** e plano **Free** para comecar.
4. Configure o Build Command:

```bash
bash build.sh
```

5. Configure o Start Command:

```bash
python manage.py migrate --noinput && gunicorn keasports.wsgi:application --bind 0.0.0.0:$PORT --workers ${WEB_CONCURRENCY:-2} --threads ${GUNICORN_THREADS:-2} --timeout ${GUNICORN_TIMEOUT:-120} --access-logfile - --error-logfile -
```

6. Crie um banco PostgreSQL. Pode ser Render PostgreSQL, Neon, Supabase ou outro provedor compativel.
7. Adicione as variaveis de ambiente abaixo.
8. Faca o deploy.
9. Depois do deploy, crie o superusuario pelo Shell do Render.

## Variaveis obrigatorias

Configure no Render:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=uma-chave-segura-e-longa
DJANGO_ADMIN_URL=admin-seguro/
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
DJANGO_MEDIA_STORAGE=local
WEB_CONCURRENCY=2
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=120
```

O Render define `RENDER_EXTERNAL_HOSTNAME` automaticamente. O projeto usa essa variavel para liberar o host em `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

Se usar dominio proprio, adicione tambem:

```text
DJANGO_ALLOWED_HOSTS=seudominio.onrender.com,seudominio.com,www.seudominio.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://seudominio.onrender.com,https://seudominio.com,https://www.seudominio.com
```

## Banco de dados

O projeto prefere `DATABASE_URL` em producao. Se `DATABASE_URL` existir, ela sobrescreve as variaveis `DB_*`.

Variaveis alternativas:

```text
DB_ENGINE=django.db.backends.postgresql
DB_NAME=nome_do_banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=host
DB_PORT=5432
DB_CONN_MAX_AGE=60
DB_SSL_REQUIRE=False
```

Use `DB_SSL_REQUIRE=True` apenas quando o provedor exigir SSL na conexao.

## Arquivos estaticos

O build executa:

```bash
npm ci
npm run build:css
python manage.py collectstatic --noinput
```

O Django serve os arquivos de `/static/` com WhiteNoise em producao. O CSS gerado fica em:

```text
keasports/static/css/output.css
```

E o `collectstatic` publica tudo em:

```text
staticfiles/
```

## Media e uploads

Com `DJANGO_MEDIA_STORAGE=local`, uploads funcionam no Render Free, mas o disco do servico web e efemero. Arquivos enviados podem sumir em redeploys, restarts ou novas instancias.

Para producao real, use storage S3 compativel:

```text
DJANGO_MEDIA_STORAGE=s3
AWS_STORAGE_BUCKET_NAME=seu-bucket
AWS_ACCESS_KEY_ID=sua-chave
AWS_SECRET_ACCESS_KEY=sua-chave-secreta
AWS_S3_REGION_NAME=sa-east-1
AWS_LOCATION=media
AWS_QUERYSTRING_AUTH=False
```

Para Cloudflare R2, Supabase Storage ou MinIO, adicione:

```text
AWS_S3_ENDPOINT_URL=https://seu-endpoint-s3
```

Se usar CDN/dominio proprio:

```text
AWS_S3_CUSTOM_DOMAIN=cdn.seudominio.com
```

## Django Admin

O admin usa a rota configurada em:

```text
DJANGO_ADMIN_URL=admin-seguro/
```

Depois do deploy, abra o Shell do Render e rode:

```bash
python manage.py createsuperuser
```

Se preferir criar via comando unico:

```bash
DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@seudominio.com DJANGO_SUPERUSER_PASSWORD='senha-forte-aqui' python manage.py createsuperuser --noinput
```

## Seguranca de producao

Em `DEBUG=False`, o projeto ativa:

- cookies seguros para sessao e CSRF;
- redirecionamento HTTPS;
- `SECURE_PROXY_SSL_HEADER` para o proxy do Render;
- HSTS;
- `X_FRAME_OPTIONS=DENY`;
- `SECURE_CONTENT_TYPE_NOSNIFF=True`;
- `REFERRER_POLICY=same-origin`;
- URL do admin por variavel de ambiente.

## Verificacao local antes do deploy

No PowerShell:

```powershell
cd "C:\Users\bueno\OneDrive\Desktop\KeaSports"
.\.venv\Scripts\Activate.ps1
$env:DJANGO_DEBUG="True"
$env:DJANGO_SECRET_KEY="local-test-key"
$env:DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
python manage.py check
npm run build:css
python manage.py collectstatic --noinput
```

## Observacoes

- Nao suba `.env` para o GitHub.
- Nao use SQLite em producao.
- Para ate cerca de 300 usuarios simultaneos no inicio, use PostgreSQL externo, `WEB_CONCURRENCY=2`, `GUNICORN_THREADS=2`, cache/CDN quando possivel e storage externo para media.
- O app Django ainda usa `label = "api_s"` por compatibilidade com migrations antigas. Isso nao impede o deploy.
