import os
import django
import sys  
from pathlib import Path 
    # Adiciona o caminho do diretório do projeto ao sys.path
projeto_root = Path(__file__).resolve().parent.parent
sys.path.append(str(projeto_root))

def get_auth_users():

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projeto.settings')
    # Configura o ambiente Django
    django.setup()

    from django.contrib.auth.models import User # importa auth.models para coletar dados da tabela auth_user

    # Listar todos os usuários da tabela auth_user
    usuarios = User.objects.all()
    for usuario in usuarios:
        print(usuario.username, usuario.email, usuario.is_staff, usuario.is_superuser)

get_auth_users()