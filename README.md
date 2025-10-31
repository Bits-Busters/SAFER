# SAFER - Sistema de Apoio à Fauna em Emergências da Rural

**Projeto acadêmico** desenvolvido por Daniel Ramos, Heitor Leander, Lucas Paiva e Mariane Elisa, no curso de Ciência da Computação da UFRPE.

**Descrição:**  
O SAFER é um sistema web para **gerenciamento de emergências envolvendo animais silvestres** na Universidade Federal Rural de Pernambuco (UFRPE). O projeto visa proteger a fauna local, conscientizar a comunidade acadêmica e agilizar respostas a incidentes com animais em áreas de risco.

---

## Funcionalidades principais

- **Registro de ocorrências:** Usuários podem reportar incidentes com animais silvestres, incluindo localização, fotos, descrição detalhada e status do chamado.  
- **Gestão de resgates:** Resgatistas podem registrar ações de resgate e acompanhar o status de cada chamado.  
- **Relatórios e análises:** O sistema gera relatórios consolidados e infográficos para análise de dados e prevenção de futuros incidentes.  
- **Posts educativos:** Administradores podem criar conteúdo para conscientização sobre preservação ambiental.  
- **Gerenciamento de usuários:** Níveis de acesso diferenciados (usuário comum, analista, gestor e administrador) para maior segurança e controle.

---

## Tecnologias utilizadas

- **Backend:** Python, Django  
- **Banco de dados:** MySQL  
- **Frontend:** HTML, CSS, JavaScript  
- **Design Patterns:** Observer, Builder, Memento, Decorator, Iterator  
- **Outros:** APIs de geolocalização, DRY principle aplicado, arquitetura em camadas

---

## Estrutura do sistema

/SAFER
├── app/                 → Código-fonte principal
├── migrations/          → Migrações do banco de dados
├── static/              → Arquivos estáticos (CSS, JS, imagens)
├── templates/           → Templates HTML
├── manage.py            → Script de gerenciamento Django
├── README.md            → Este arquivo
└── requirements.txt     → Dependências do projeto

---

## Instalação e execução

1. Clone o repositório:  
```bash
git clone https://github.com/Bits-Busters/SAFER.git
cd SAFER
````

2. Configure o ambiente Python:

```bash
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

3. Configure variáveis de ambiente (se necessário).

4. Execute migrações e inicie o servidor:

```bash
python manage.py migrate
python manage.py runserver
```

5. Acesse o sistema via navegador: `http://127.0.0.1:8000`

---

## Objetivos do projeto

* Proteger a fauna local e garantir respostas rápidas a incidentes.
* Conscientizar a comunidade acadêmica através de posts educativos.
* Coletar e analisar dados para prevenir futuros acidentes.
* Fornecer um sistema escalável e seguro, adequado para diferentes perfis de usuários.
