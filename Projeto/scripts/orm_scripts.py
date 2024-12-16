from pathlib import Path 
import sys
import os
import django
# Adiciona o caminho do diretório (ProjetoArquiteturaDeSoftware/Projeto) do projeto ao sys.path desse arquivo 
projeto_root = Path(__file__).resolve().parent.parent
sys.path.append(str(projeto_root))

# Configurando ambiente django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projeto.settings')
django.setup()

import SAFERapp.models

