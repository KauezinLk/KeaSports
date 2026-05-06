# KeaSports

## 📌 Descrição

KeaSports é um sistema web desenvolvido em Django para gerenciamento de eventos de corrida, inscrições de participantes e consulta de resultados. O projeto permite cadastrar corridas, registrar participantes, importar resultados por planilhas Excel e visualizar classificações com filtros e paginação.

O sistema foi construído com foco em organização de dados esportivos, fluxo de inscrição e apresentação clara das informações para usuários e administradores.

## 🚀 Funcionalidades

- Cadastro e listagem de corridas com nome, local, data e imagem.
- Inscrição de participantes em corridas.
- Cadastro de participantes com CPF, data de nascimento, equipe, sexo e tamanho de camisa.
- Cálculo automático de idade e categoria por faixa etária.
- Validação e busca de participante por CPF durante a inscrição.
- Área de autenticação com cadastro, login, logout e histórico do usuário.
- Upload de arquivos Excel com resultados de corrida.
- Extração automática de dados da planilha para registros de classificação.
- Consulta de resultados por arquivo.
- Filtros por nome e categoria usando `django-filter`.
- Paginação de resultados.
- Administração dos dados pelo Django Admin.
- Suporte a imagens de corridas, resultados e banner base do site.

## 🛠️ Tecnologias utilizadas

- Python
- Django 5.2
- Django REST Framework
- PostgreSQL
- Django Filter
- Widget Tweaks
- Pandas
- OpenPyXL
- Pillow
- Tailwind CSS
- HTML templates do Django
- Git e GitHub

## 📂 Estrutura do projeto

```text
.
├── eventos/
│   ├── migrations/          # Migrações do banco de dados
│   ├── static/              # Arquivos estáticos do app
│   ├── templates/           # Templates HTML do sistema
│   ├── templatetags/        # Tags customizadas para templates
│   ├── views/               # Views separadas por domínio
│   ├── admin.py             # Configurações do Django Admin
│   ├── filters.py           # Filtros de resultados
│   ├── forms.py             # Formulários do sistema
│   ├── models.py            # Modelos principais
│   ├── signals.py           # Processamento automático de planilhas
│   └── urls.py              # Rotas do app
├── keasports/
│   ├── static/              # CSS gerado e estáticos globais
│   ├── settings.py          # Configurações do Django
│   ├── urls.py              # Rotas principais
│   ├── asgi.py
│   └── wsgi.py
├── input.css                # Entrada do Tailwind CSS
├── package.json             # Scripts e dependências do frontend
├── requirements.txt         # Dependências Python
└── manage.py                # Utilitário de gerenciamento Django
```

## ⚙️ Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/KauezinLk/KeaSports.git
cd KeaSports
```

### 2. Crie e ative um ambiente virtual

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências Python

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

O projeto está configurado para usar PostgreSQL. Ajuste as credenciais em `keasports/settings.py` conforme o seu ambiente local:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'KeaBase',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
```

Crie o banco no PostgreSQL antes de executar as migrações.

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Rode o servidor

```bash
python manage.py runserver
```

Acesse no navegador:

```text
http://127.0.0.1:8000/
```

Painel administrativo:

```text
http://127.0.0.1:8000/admin/
```

## 🎨 Frontend / Estilo

O frontend utiliza templates HTML do Django com classes utilitárias do Tailwind CSS. O CSS principal é carregado nos templates por meio de arquivos estáticos do Django.

Arquivo de entrada do Tailwind:

```text
input.css
```

Arquivo CSS gerado:

```text
keasports/static/css/output.css
```

Scripts disponíveis:

```bash
npm install
npm run build:css
```

Durante o desenvolvimento, também é possível usar:

```bash
npm run dev:css
```

## 🧠 Aprendizados

- Estruturação de um projeto Django com app principal e views organizadas por domínio.
- Modelagem de dados relacionais com participantes, corridas, arquivos e classificações.
- Uso de PostgreSQL como banco de dados principal.
- Implementação de autenticação com usuários do Django.
- Criação de formulários com `ModelForm`.
- Processamento de arquivos Excel com Pandas e OpenPyXL.
- Uso de signals para automatizar a criação de registros após upload de arquivos.
- Aplicação de filtros dinâmicos com `django-filter`.
- Integração de templates Django com Tailwind CSS.
- Organização de arquivos estáticos e mídia no Django.

## 🔮 Melhorias futuras

- Migrar credenciais sensíveis para variáveis de ambiente.
- Criar testes automatizados para models, views e fluxos principais.
- Melhorar tratamento de erros na importação de planilhas.
- Adicionar validações mais robustas para formatos de arquivos enviados.
- Implementar permissões mais detalhadas para usuários e administradores.
- Criar dashboards administrativos com métricas de inscrições e resultados.
- Melhorar a responsividade e acessibilidade das páginas.
- Preparar configurações separadas para desenvolvimento e produção.
- Adicionar documentação da estrutura esperada das planilhas Excel.

## 👨‍💻 Autor

Kaue Bueno de Freitas  
LinkedIn: https://www.linkedin.com/in/kaue-bueno-0b3171347  
GitHub: https://github.com/KauezinLk/KeaSports
