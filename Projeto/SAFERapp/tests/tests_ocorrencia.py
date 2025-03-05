

"""
Os testes a seguir dizem respeito aos requisitos relacionados com CRUD
de ocorrencias e estão sendo automatizados usando o selenium. Além disso,
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
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.beans.Enums import RelacaoUFRPE, Registro, Local, StatusChamado
from django.utils.timezone import now
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




driver = webdriver.Chrome()


# Create your tests here.


class TesteOcorrencias(StaticLiveServerTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario_anomino = get_or_create_anonymous_user();


    def setUp(self):
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.live_server_url = "http://localhost:8000" # URL do servidor local
        self.login_user_anonimo()
   
    def tearDown(self):
        self.driver.quit()
   
    def login_user_anonimo(self):
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get("http://localhost:8000/")
        # 2 | setWindowSize | 1235x816 |
        self.driver.set_window_size(1235, 816)
        # 3 | click | id=login |
        self.driver.find_element(By.ID, "login").click()
        # 4 | type | id=login |
        self.driver.find_element(By.ID, "login").send_keys("anonimo@usuario.com")
        # 5 | click | id=password |
        self.driver.find_element(By.ID, "password").click()
        # 6 | type | id=password |
        self.driver.find_element(By.ID, "password").send_keys("senha1234")
   
    """
    Inicio de Testes de visualização de ocorrências
    """
    def criar_ocorrencia_teste(self):
        self.ocorrencia = Ocorrencia.objects.create(
            Autor=self.usuario,
            Nome_Autor=self.usuario_anomino.nome,
            Celular_Autor="000000000000",
            Telefone_Autor="0000000000",
            Relacao_Autor="VISITANTE",
            Tipo_Caso=Registro.PRESENCA,
            Descricao="Descrição do caso de teste",
            Nome_Animal="Preguiça",
            Local=Local.RU,
            Referencia="Referência do caso",
            DataHora=now(),
            Status=StatusChamado.ABERTO
        )
   
    def atualizar_ocorrencia_teste(self):
        self.ocorrencia.alterar_descricao("Descrição atualizada")
   
    def test_visualizar_ocorrencias_inexistente(self):
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1235, 816)
        self.driver.find_element(By.CSS_SELECTOR, "#headerRight #hrButton > .btnLoggin").click()
        self.driver.find_element(By.LINK_TEXT, "Meus Chamados").click()
   
    def test_visualizar_ocorrenciar_existentes(self):
        self.criar_ocorrencia_teste()
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1235, 816)
        self.driver.find_element(By.LINK_TEXT, "Meus Chamados").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item > button").click()
        self.vars["win8450"] = self.wait_for_window(2000)
        self.driver.switch_to.window(self.vars["win8450"])


    def test_visualizar_ocorrencia_atualizada(self):
        self.criar_ocorrencia_teste()
        self.atualizar_ocorrencia_teste()
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1235, 816)
        self.driver.find_element(By.LINK_TEXT, "Meus Chamados").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item > button").click()
        self.vars["win8450"] = self.wait_for_window(2000)
        self.driver.switch_to.window(self.vars["win8450"])
    """
    Fim de Testes de visualização de ocorrências
    """


