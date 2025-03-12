"""
Os testes a seguir dizem respeito aos requisitos relacionados com promoção
de usuários e estão sendo automatizados usando o selenium. Além disso,
o driver usado é o chromedriver versão 133.0.6943.126, que já está no
repositório e é compatível com a versão mais atual do google chrome.  
"""

"""
Os testes a seguir estão com algum problema relacionado à achar o elemento
dropdown para a troca do tipo de usuário.
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
import re
from selenium.webdriver.support import expected_conditions as EC

class TestePromocaoUsuario(StaticLiveServerTestCase):

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

        self.usuario_admin2 = CustomUser.objects.create_superuser(
                nome="Admin2",
                email = "admin2@usuario.com",
                password="senha1234",
                tipo_usuario=TipoUsuario.ADMIN
        )
        
        # Inicializa o navegador
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.login_user_admin()

    def tearDown(self):
        self.driver.quit()

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
    
    def test_realiza_promocao(self):
        self.driver.find_element(By.LINK_TEXT, "Gerenciar Usuários").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item:nth-child(1) > button").click()
        time.sleep(1)
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "tipo_usuario"))
        )
        dropdown.find_element(By.XPATH, "//option[. = 'Administrador']").click()
        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()

    def test_descarta_promocao(self):
        self.driver.find_element(By.LINK_TEXT, "Gerenciar Usuários").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item:nth-child(1) > button").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Início").click()
    
    def test_promover_sem_selecionar_tipo(self):
        self.driver.find_element(By.LINK_TEXT, "Gerenciar Usuários").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item:nth-child(1) > button").click()
        time.sleep(1)
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "tipo_usuario"))
        )
        dropdown.click()
        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()

    def test_promover_cargo_maximo(self):
        self.driver.find_element(By.LINK_TEXT, "Gerenciar Usuários").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item:nth-child(2) > button").click()
        time.sleep(1)
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "tipo_usuario"))
        )
        dropdown.find_element(By.XPATH, "//option[. = 'Administrador']").click()
        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()
    
    def test_promover_usuario_mesmo_cargo(self):
        self.driver.find_element(By.LINK_TEXT, "Gerenciar Usuários").click()
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, ".list-group-item:nth-child(2) > button").click()
        time.sleep(1)
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "tipo_usuario"))
        )
        dropdown.find_element(By.XPATH, "//option[. = 'Administrador']").click()
        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(4)").click()