

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
from django.test import Client
from django.contrib.auth import authenticate, login

# Create your tests here.


class TesteOcorrencias(StaticLiveServerTestCase):
    
    def setUp(self):
        self.usuario_anonimo = CustomUser.objects.create_user(
                nome="Anônimo Usuário",
                email='anonimo@example.com',
                password="senha1234"
            )

        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.login_user_anonimo()

   
    def tearDown(self):
        self.driver.quit()
   

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
    
    def wait_for_window(self, timeout = 2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        if len(wh_now) > len(self.vars["window_handles"]):
            return set(wh_now).difference(set(self.vars["window_handles"])).pop()
        return None

    """
    Inicio de Testes de visualização de ocorrências
    """
    def criar_ocorrencia_teste(self):
        self.ocorrencia = Ocorrencia.objects.create(
            Autor=self.usuario_anonimo,
            Nome_Autor=self.usuario_anonimo.nome,
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
        self.driver.find_element(By.LINK_TEXT, "Meus Chamados").click()
   
    def test_visualizar_ocorrenciar_existentes(self):
        self.criar_ocorrencia_teste()
        self.driver.find_element(By.LINK_TEXT, "Meus Chamados").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item > button").click()
        self.vars["win8450"] = self.wait_for_window(2000)
        self.driver.switch_to.window(self.vars["win8450"])


    def test_visualizar_ocorrencia_atualizada(self):
        self.criar_ocorrencia_teste()
        self.atualizar_ocorrencia_teste()
        self.driver.find_element(By.LINK_TEXT, "Meus Chamados").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item > button").click()
        self.vars["win8450"] = self.wait_for_window(2000)
        self.driver.switch_to.window(self.vars["win8450"])
    """
    Fim de Testes de visualização de ocorrências
    """