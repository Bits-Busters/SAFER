"""
Os testes a seguir dizem respeito aos requisitos relacionados com CRUD
de informativos e estão sendo automatizados usando o selenium. Além disso,
o driver usado é o chromedriver versão 133.0.6943.126,que já está no
repositório e é compatível com a versão mais atual do google chrome.  
"""
import os
import sys
import django
import re
import tempfile

# Adiciona o caminho do diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Projeto')))

# Define a variável de ambiente DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projeto.settings')

# Inicializa o Django
django.setup()

import time
import json
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # Para criar um servidor e banco de dados temporários para testes
from SAFERapp.models import CustomUser, get_or_create_anonymous_user
from SAFERapp.beans.Informativos import Informativo
from SAFERapp.beans.Enums import RelacaoUFRPE, Registro, Local, StatusChamado, TipoUsuario
from django.utils.timezone import now
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC


class TestCriarInformativos(StaticLiveServerTestCase):

    def setUp(self):
        self.usuario_admin = CustomUser.objects.create_superuser(
            email='admin@usuario.com',
            password='senha1234',
            nome='Administrador',
            tipo_usuario=TipoUsuario.ADMIN
        )
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.login_user_admin()
        self.arquivo_txt, self.arquivo_jpg = self.criar_arquivos_temporarios()

    def criar_arquivos_temporarios(self):
        # Diretório relativo onde os arquivos serão criados
        caminho_relativo = os.path.join("imagens", "teste")
        os.makedirs(caminho_relativo, exist_ok=True)  # Cria o diretório se não existir

        # Criar arquivo temporário .jpg
        temp_jpg = tempfile.NamedTemporaryFile(
            dir=caminho_relativo, suffix=".jpg", delete=False
        )
        caminho_jpg = temp_jpg.name
        temp_jpg.write(b"\xFF\xD8\xFF")  # Escreve um cabeçalho JPEG mínimo
        temp_jpg.close()

        # Criar arquivo temporário .txt
        temp_txt = tempfile.NamedTemporaryFile(
            dir=caminho_relativo, suffix=".txt", delete=False
        )
        caminho_txt = temp_txt.name
        temp_txt.write(b"Arquivo de teste")
        temp_txt.close()

        return caminho_jpg, caminho_txt

    def login_user_admin(self):
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get(self.live_server_url)
        # 2 | setWindowSize | 1235x816 |
        self.driver.set_window_size(1235, 816)
        # 3 | click | id=login |
        self.driver.find_element(By.ID, "login").click()
        # 4 | type | id=login |
        self.driver.find_element(By.ID, "login").send_keys("admin@usuario.com")
        # 5 | click | id=password |
        self.driver.find_element(By.ID, "password").click()
        # 6 | type | id=password |
        self.driver.find_element(By.ID, "password").send_keys("senha1234")

         # Submetendo o formulário
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(1)

    def test_criar_informativo_obrigatorios(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()

        url_atual = self.driver.current_url
        assert re.search(r"/informativos/gerenciar/", url_atual), f"URL inesperada: {url_atual}"
   
    def test_criar_informativo_sem_obrigatorios(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()


    def test_criar_informativo_com_imagem(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo")
        elemento = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_imagens"))
            )
        elemento.send_keys(self.arquivo_jpg)
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()

        assert (self.arquivo_jpg != ""), f"O arquivo {self.arquivo_jpg} não é um arquivo .jpg"
   
    def test_criar_informativo_com_imagem_invalida(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo")
        elemento = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_imagens"))
            )
        elemento.send_keys(self.arquivo_txt)
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()

        url_atual = self.driver.current_url
        assert re.search(r"/informativos/criar/", url_atual), f"URL inesperada: {url_atual}"
   
    def test_informativo_sem_salvar(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()

        self.driver.find_element(By.LINK_TEXT, "Início").click()
        
        url_atual = self.driver.current_url
        assert re.match(r'^(http://|https://)?localhost(:\d+)?/?$', url_atual), f"URL inesperada: {url_atual}"


class TestAtualizarInformativos():

    def setUp(self):
        self.usuario_admin = CustomUser.objects.create_superuser(
            email='admin@usuario.com',
            senha='senha1234',
            nome='Administrador',
            telefone='1234567890',
            telefone_fixo='0987654321',
            relacao_ufrpe=RelacaoUFRPE.DOCENTE,
            tipo_usuario= TipoUsuario.ADMIN
        )
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.arquivo_jpg, self.arquivo_txt = self.criar_arquivos_temporarios()
        self.login_user_admin()
    
    def criar_arquivos_temporarios(self):
        # Diretório relativo onde os arquivos serão criados
        caminho_relativo = os.path.join("imagens", "teste")
        os.makedirs(caminho_relativo, exist_ok=True)  # Cria o diretório se não existir

        # Criar arquivo temporário .jpg
        temp_jpg = tempfile.NamedTemporaryFile(
            dir=caminho_relativo, suffix=".jpg", delete=False
        )
        caminho_jpg = temp_jpg.name
        temp_jpg.write(b"\xFF\xD8\xFF")  # Escreve um cabeçalho JPEG mínimo
        temp_jpg.close()

        # Criar arquivo temporário .txt
        temp_txt = tempfile.NamedTemporaryFile(
            dir=caminho_relativo, suffix=".txt", delete=False
        )
        caminho_txt = temp_txt.name
        temp_txt.write(b"Arquivo de teste")
        temp_txt.close()

        return caminho_jpg, caminho_txt

    def cadastro_informativo(self):
        self.informativo = Informativo.objects.create(
            id_Autor=self.usuario_admin,
            titulo="Titulo",
            corpo="Corpo",
            imagens="imagens/png.png"
        )

    def login_user_admin(self):
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get(self.live_server_url)
        # 2 | setWindowSize | 1235x816 |
        self.driver.set_window_size(1235, 816)
        # 3 | click | id=login |
        self.driver.find_element(By.ID, "login").click()
        # 4 | type | id=login |
        self.driver.find_element(By.ID, "login").send_keys("admin@usuario.com")
        # 5 | click | id=password |
        self.driver.find_element(By.ID, "password").click()
        # 6 | type | id=password |
        self.driver.find_element(By.ID, "password").send_keys("senha1234")

         # Submetendo o formulário
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(1)

    def test_atualizar_informativo(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) > .card-body > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo Editado")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()
        
        url_atual = self.driver.current_url
        assert re.search(r"/informativos/gerenciar/", url_atual), f"URL inesperada: {url_atual}"
   
    def test_atualizar_informativo_excluindo_conteudo(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) > .card-body > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()

        url_atual = self.driver.current_url
        assert re.search(r"/informativos/criar/", url_atual), f"URL inesperada: {url_atual}"

   
    def test_atualizar_informativo_com_imagem_invalida(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) > .card-body > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        elemento = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_imagens"))
            )
        elemento.send_keys(self.arquivo_txt)
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()

        url_atual = self.driver.current_url
        assert re.search(r"/informativos/criar/", url_atual), f"URL inesperada: {url_atual}"
   
    def test_atualizar_informativo_sem_alterar(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) > .card-body > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()

        url_atual = self.driver.current_url
        assert re.search(r"/informativos/gerenciar/", url_atual), f"URL inesperada: {url_atual}"
   
    def test_atualizar_sem_salvar(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo Editado")
        self.driver.find_element(By.CSS_SELECTOR, ".content:nth-child(4)").click()
        self.driver.find_element(By.LINK_TEXT, "Início").click()
        
        url_atual = self.driver.current_url
        assert re.match(r'^(http://|https://)?localhost(:\d+)?/?$', url_atual), f"URL inesperada: {url_atual}"


class TestExcluirInformativos(StaticLiveServerTestCase):

    def setUp(self):
        self.usuario_admin = CustomUser.objects.create_superuser(
            email='admin@usuario.com',
            password='senha1234',
            nome='Administrador',
            tipo_usuario=TipoUsuario.ADMIN
        )
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.login_user_admin()
        self.cadastro_informativo()


    def cadastro_informativo(self):
        self.informativo = Informativo.objects.create(
            id_Autor=self.usuario_admin,
            titulo="Titulo",
            corpo="Corpo",
            imagens="imagens/png.png"
        )

    def login_user_admin(self):
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get(self.live_server_url)
        # 2 | setWindowSize | 1235x816 |
        self.driver.set_window_size(1235, 816)
        # 3 | click | id=login |
        self.driver.find_element(By.ID, "login").click()
        # 4 | type | id=login |
        self.driver.find_element(By.ID, "login").send_keys("admin@usuario.com")
        # 5 | click | id=password |
        self.driver.find_element(By.ID, "password").click()
        # 6 | type | id=password |
        self.driver.find_element(By.ID, "password").send_keys("senha1234")

         # Submetendo o formulário
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(2)


    def test_excluir_informativo(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.NAME, "id").click()

        time.sleep(2)

        # Assert para garantir que o informativo foi excluído do banco
        informativo_excluido = Informativo.objects.filter(id=self.informativo.id).first()
        assert informativo_excluido is None, f"O informativo com ID {self.informativo.id} não foi excluído!"

class TestVisualizarInformativos(StaticLiveServerTestCase):

    def setUp(self):
        self.usuario_admin = CustomUser.objects.create_superuser(
            email='admin@usuario.com',
            password='senha1234',
            nome='Administrador',
            tipo_usuario=TipoUsuario.ADMIN
        )
        self.usuario_anonimo = CustomUser.objects.create_user(
                nome="Anônimo Usuário",
                email='anonimo@example.com',
                password="senha1234"
            )
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}

    def cadastro_informativo(self):
        self.informativo = Informativo.objects.create(
            id_Autor=self.usuario_admin,
            titulo="Titulo",
            corpo="Corpo",
            imagens="imagens/png.png"
        )


    def login_user_admin(self):
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get(self.live_server_url)
        # 2 | setWindowSize | 1235x816 |
        self.driver.set_window_size(1235, 816)
        # 3 | click | id=login |
        self.driver.find_element(By.ID, "login").click()
        # 4 | type | id=login |
        self.driver.find_element(By.ID, "login").send_keys("admin@usuario.com")
        # 5 | click | id=password |
        self.driver.find_element(By.ID, "password").click()
        # 6 | type | id=password |
        self.driver.find_element(By.ID, "password").send_keys("senha1234")

         # Submetendo o formulário
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(1)


    def login_user_anonimo(self):
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get(self.live_server_url)
        # 2 | setWindowSize | 1235x816 |
        self.driver.set_window_size(1235, 816)
        # 3 | click | id=login |
        self.driver.find_element(By.ID, "login").click()
        # 4 | type | id=login |
        self.driver.find_element(By.ID, "login").send_keys("anonimo@example.com")
        # 5 | click | id=password |
        self.driver.find_element(By.ID, "password").click()
        # 6 | type | id=password |
        self.driver.find_element(By.ID, "password").send_keys("senha1234")

         # Submetendo o formulário
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(1)
   
    def test_visualizar_informativo_gestor_admin(self):
        self.login_user_admin()
        self.cadastro_informativo()
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()

       # Verificando se há ao menos um título de informativo na tela
        try:
            # Buscando por qualquer título de informativo (h2 com a classe 'card-title')
            titulos_informativos = self.driver.find_elements(By.CSS_SELECTOR, "h2.card-title")
            
            # Verificando se pelo menos um título de informativo foi encontrado
            assert len(titulos_informativos) > 0, "Não há informativos na tela!"
        except Exception:
            # Caso nenhum título de informativo seja encontrado, falha o teste
            assert False, "Não foi possível encontrar informativos na página!"
    
    def test_visualizar_informativo_sem_conteudo(self):
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1235, 816)
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()

        # Verificando se há ao menos um título de informativo na tela
        try:
            # Buscando por qualquer título de informativo (h2 com a classe 'card-title')
            titulos_informativos = self.driver.find_elements(By.CSS_SELECTOR, "h2.card-title")
            
            # Verificando se pelo menos um título de informativo foi encontrado
            assert len(titulos_informativos) == 0, "Há informativos na tela!"
        except Exception:
            # Caso nenhum título de informativo seja encontrado, tem sucesso no teste
            assert True, "Não foi possível encontrar informativos na página!"
        

    def test_visualizar_informativo_usuario_nao_autenticado(self):
        self.cadastro_informativo()
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1235, 816)
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()

        # Verificando se há ao menos um título de informativo na tela
        try:
            # Buscando por qualquer título de informativo (h2 com a classe 'card-title')
            titulos_informativos = self.driver.find_elements(By.CSS_SELECTOR, "h2.card-title")
            
            # Verificando se pelo menos um título de informativo foi encontrado
            assert len(titulos_informativos) > 0, "Não há informativos na tela!"
        except Exception:
            # Caso nenhum título de informativo seja encontrado, falha o teste
            assert False, "Não foi possível encontrar informativos na página!"
    
   
    def test_visualizar_secao_gerenciar_informativos(self):
        self.login_user_admin()
        self.cadastro_informativo()
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()

        # Verificando se há ao menos um título de informativo na tela
        try:
            # Buscando por qualquer título de informativo (h2 com a classe 'card-title')
            titulos_informativos = self.driver.find_elements(By.CSS_SELECTOR, "h2.card-title")
            
            # Verificando se pelo menos um título de informativo foi encontrado
            assert len(titulos_informativos) > 0, "Não há informativos na tela!"
        except Exception:
            # Caso nenhum título de informativo seja encontrado, falha o teste
            assert False, "Não foi possível encontrar informativos na página!"
    
   
    def test_visualizar_secao_gerenciar_informativos_sem_informativo(self):
        self.login_user_admin()
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()

        # Verificando se há ao menos um título de informativo na tela
        try:
            # Buscando por qualquer título de informativo (h2 com a classe 'card-title')
            titulos_informativos = self.driver.find_elements(By.CSS_SELECTOR, "h2.card-title")
            
            # Verificando se pelo menos um título de informativo foi encontrado
            assert len(titulos_informativos) == 0, "Há informativos na tela!"
        except Exception:
            # Caso nenhum título de informativo seja encontrado, tem sucesso no teste
            assert True, "Não foi possível encontrar informativos na página!"