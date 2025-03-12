from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from SAFERapp.models import CustomUser
from selenium.webdriver.common.by import By

import time
"""
Checa se os usuários do tipo analista, gestor e administrador possuem acesso a lista de ocorrencias e se elas aparecem vazias caso nao possua ocorrencias
"""

class TestAcessoChamado(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.driver.maximize_window()
        self.senha = 'testpassword'

    def test_visualizar_lista_analista(self):
        """
        Verifica se analista tem acesso a chamados em aberto
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='analista')

        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)

        # 1- Clicar no botão "Ocorrências em Aberto".
        chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
        chamados_abertos.click()

        self.assertIn(reverse("telaChamados", kwargs={"tipoChamado":"chamados-em-aberto"}), self.driver.current_url)


    def test_visualizar_lista_gestor(self):
        """
        Verifica se gestor tem acesso a chamados em aberto
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='gestor')

        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)

        # 1- Clicar no botão "Ocorrências em Aberto".
        chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
        chamados_abertos.click()

        self.assertIn(reverse("telaChamados", kwargs={"tipoChamado": "chamados-em-aberto"}), self.driver.current_url)

    def test_visualizar_lista_administrador(self):
        """
        Verifica se administrador tem acesso a chamados em aberto
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='admin')

        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)

        # 1- Clicar no botão "Ocorrências em Aberto".
        chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
        chamados_abertos.click()

        self.assertIn(reverse("telaChamados", kwargs={"tipoChamado": "chamados-em-aberto"}), self.driver.current_url)

    def test_verificar_lista_vazia_analista(self):
            """
            Verifica se aparece uma lista vazia de chamados em aberto
            """
            self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='analista')

            self.driver.get(self.live_server_url)
            email_input = self.driver.find_element(By.ID, 'login')
            senha_input = self.driver.find_element(By.ID, 'password')
            email_input.send_keys(self.user.email)
            senha_input.send_keys(self.senha)

            butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
            butao_login.click()
            time.sleep(0.5)

            # 1- Clicar no botão "Ocorrências em Aberto".
            chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
            chamados_abertos.click()

            lista_chamado = self.driver.find_elements(By.CLASS_NAME, 'list-group')[0].find_elements(By.TAG_NAME, 'li')

            self.assertEqual(len(lista_chamado), 0)
    def test_verificar_lista_vazia_gestor(self):
            """
            Verifica se aparece uma lista vazia de chamados em aberto
            """
            self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='gestor')

            self.driver.get(self.live_server_url)
            email_input = self.driver.find_element(By.ID, 'login')
            senha_input = self.driver.find_element(By.ID, 'password')
            email_input.send_keys(self.user.email)
            senha_input.send_keys(self.senha)

            butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
            butao_login.click()
            time.sleep(0.5)

            # 1- Clicar no botão "Ocorrências em Aberto".
            chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
            chamados_abertos.click()

            lista_chamado = self.driver.find_elements(By.CLASS_NAME, 'list-group')[0].find_elements(By.TAG_NAME, 'li')

            self.assertEqual(len(lista_chamado), 0)
    def test_verificar_lista_vazia_administrador(self):
            """
            Verifica se aparece uma lista vazia de chamados em aberto
            """
            self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='admin')

            self.driver.get(self.live_server_url)
            email_input = self.driver.find_element(By.ID, 'login')
            senha_input = self.driver.find_element(By.ID, 'password')
            email_input.send_keys(self.user.email)
            senha_input.send_keys(self.senha)

            butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
            butao_login.click()
            time.sleep(0.5)

            # 1- Clicar no botão "Ocorrências em Aberto".
            chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
            chamados_abertos.click()

            lista_chamado = self.driver.find_elements(By.CLASS_NAME, 'list-group')[0].find_elements(By.TAG_NAME, 'li')

            self.assertEqual(len(lista_chamado), 0)