
"""
Os testes a seguir dizem respeito aos requisitos relacionados com CRUD
de informativos e estão sendo automatizados usando o selenium. Além disso,
o driver usado é o chromedriver versão 133.0.6943.126,que já está no
repositório e é compatível com a versão mais atual do google chrome.  
"""
import os
import sys
import django

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


class TestCriarInformativos():

    def setUp(self):
        self.usuario_admin = CustomUser.objects.create_superuser(
            email='admin@usuario.com',
            senha='senha1234',
            nome='Administrador'
        )
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.login_user_admin()


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
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(5)").click()
        self.driver.find_element(By.CSS_SELECTOR, "body").click()
        self.driver.find_element(By.CSS_SELECTOR, ".meta tr:nth-child(2) > td").click()
        self.driver.find_element(By.CSS_SELECTOR, ".content:nth-child(4)").click()
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        element = self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()
   
    def test_criar_informativo_sem_obrigatorios(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()


    def test_criar_informativo_com_imagem(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo")
        self.driver.find_element(By.ID, "id_imagens").click()
        self.driver.find_element(By.ID, "id_imagens").send_keys("C:\\fakepath\\png.png")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()
   
    def test_criar_informativo_com_imagem_invalida(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("Corpo")
        self.driver.find_element(By.ID, "id_imagens").click()
        self.driver.find_element(By.ID, "id_imagens").send_keys("C:\\fakepath\\txt.txt")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()
   
    def test_criar_informativo_sem_salvar(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btnInfo").click()
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo")
        self.driver.find_element(By.ID, "id_corpo").click()


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
        self.login_user_admin()


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
   
    def test_atualizar_informativo_excluindo_conteudo(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) > .card-body > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.ID, "id_corpo").click()
        self.driver.find_element(By.ID, "id_corpo").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()
   
    def test_atualizar_informativo_com_imagem_invalida(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) > .card-body > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.ID, "id_imagens").click()
        self.driver.find_element(By.ID, "id_imagens").send_keys("C:\\fakepath\\txt.txt")
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()
   
    def test_atualizar_informativo_sem_alterar(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) > .card-body > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btnLoggin:nth-child(6)").click()
   
    def test_atualizar_sem_salvar(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(2) a").click()
        self.driver.find_element(By.ID, "id_titulo").click()
        self.driver.find_element(By.ID, "id_titulo").send_keys("Titulo Editado")
        self.driver.find_element(By.CSS_SELECTOR, ".content:nth-child(4)").click()
        element = self.driver.find_element(By.LINK_TEXT, "Cadastrar Ocorrência")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()


class TestExcluirInformativos():

    def setUp(self):
        self.usuario_admin = CustomUser.objects.create_superuser(
            email='admin@usuario.com',
            senha='senha1234',
            nome='Administrador',
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
        # 3 | click | id=login |
        self.driver.find_element(By.ID, "login").click()
        # 4 | type | id=login |
        self.driver.find_element(By.ID, "login").send_keys("admin@usuario.com")
        # 5 | click | id=password |
        self.driver.find_element(By.ID, "password").click()
        # 6 | type | id=password |
        self.driver.find_element(By.ID, "password").send_keys("senha1234")


    def test_excluir_informativo(self):
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
        self.driver.find_element(By.NAME, "id").click()


class TestVisualizarInformativos():

    def setUp(self):
        self.usuario_admin = CustomUser.objects.create_superuser(
            email='admin@usuario.com',
            senha='senha1234',
            nome='Administrador',
        )
        self.usuario_anonimo = CustomUser.objects.create_user(
                nome="Anônimo Usuário",
                email='anonimo@example.com',
                password="senha1234"
            )
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.live_server_url = "http://localhost:8000" # URL do servidor local


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
   
    def test_visualizar_informativo_sem_conteudo(self):
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1236, 816)
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()


    def test_visualizar_informativo_usuario_nao_autenticado(self):
        self.cadastro_informativo()
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1236, 816)
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
   
    def test_visualizar_secao_gerenciar_informativos(self):
        self.login_user_admin()
        self.cadastro_informativo()
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
   
    def test_visualizar_secao_gerenciar_informativos_sem_informativo(self):
        self.login_user_admin()
        self.driver.find_element(By.LINK_TEXT, "Informativos").click()
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btnInfo").click()
