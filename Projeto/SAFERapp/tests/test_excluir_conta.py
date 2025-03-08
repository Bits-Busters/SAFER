from django.test import TestCase, LiveServerTestCase

from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from SAFERapp.models import CustomUser
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import time

from selenium.webdriver.common.alert import Alert
"""
Testes da funcionalidade de excluir conta
"""
class TestExcluirConta(LiveServerTestCase):
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
            self.user = CustomUser.objects.create_user(nome="test", email="testuser@test.com", password="testpassword")
            self.driver.maximize_window()  # Maximiza a janela
            self.senha = "testpassword"
            existe = CustomUser.objects.filter(email="testuser@test.com").exists()
            self.assertTrue(existe)
    def test_excluir_conta_comum(self):
            """
            Teste de exclusão de conta de usuário comum
            """
            self.user.tipo_usuario = "Comum"
            self.driver.get(self.live_server_url)
            email_input = self.driver.find_element(By.ID, 'login')
            senha_input = self.driver.find_element(By.ID, 'password')
            email_input.send_keys(self.user.email)
            senha_input.send_keys(self.senha)

            butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
            butao_login.click()
            time.sleep(0.7)
            self.driver.get(self.live_server_url+reverse('telaPerfil', kwargs={'username': self.user.nome}))


            botao_apagar = self.driver.find_element(By.CLASS_NAME, 'btn-danger')
            botao_apagar.click()
            Alert(self.driver).accept()

            time.sleep(1)
            self.assertFalse(CustomUser.objects.filter(email="testuser@test.com").exists())

    def test_excluir_conta_analista(self):
                """
                Teste de exclusão de conta de analista
                """
                self.user.tipo_usuario = "Analista"
                self.driver.get(self.live_server_url)
                email_input = self.driver.find_element(By.ID, 'login')
                senha_input = self.driver.find_element(By.ID, 'password')
                email_input.send_keys(self.user.email)
                senha_input.send_keys(self.senha)

                butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
                butao_login.click()
                time.sleep(0.7)
                self.driver.get(self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))

                botao_apagar = self.driver.find_element(By.CLASS_NAME, 'btn-danger')
                botao_apagar.click()
                Alert(self.driver).accept()

                time.sleep(1)
                self.assertFalse(CustomUser.objects.filter(email="testuser@test.com").exists())

    def test_excluir_conta_gestor(self):
                    """
                    Teste de exclusão de conta de gestor
                    """
                    self.user.tipo_usuario = "gestor"
                    self.driver.get(self.live_server_url)
                    email_input = self.driver.find_element(By.ID, 'login')
                    senha_input = self.driver.find_element(By.ID, 'password')
                    email_input.send_keys(self.user.email)
                    senha_input.send_keys(self.senha)

                    butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
                    butao_login.click()

                    self.driver.get(self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))


                    time.sleep(1)
                    botao_apagar = self.driver.find_element(By.CLASS_NAME, 'btn-danger')
                    botao_apagar.click()
                    Alert(self.driver).accept()

                    time.sleep(1)
                    self.assertFalse(CustomUser.objects.filter(email="testuser@test.com").exists())

    def test_excluir_conta_administrador(self):
                        """
                        Teste de exclusão de conta de Administrador
                        """
                        self.user.tipo_usuario = "Comum"
                        self.driver.get(self.live_server_url)
                        email_input = self.driver.find_element(By.ID, 'login')
                        senha_input = self.driver.find_element(By.ID, 'password')
                        email_input.send_keys(self.user.email)
                        senha_input.send_keys(self.senha)

                        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
                        butao_login.click()

                        time.sleep(0.7)
                        self.driver.get(
                            self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))

                        botao_apagar = self.driver.find_element(By.CLASS_NAME, 'btn-danger')
                        botao_apagar.click()
                        Alert(self.driver).accept()

                        time.sleep(1)
                        self.assertFalse(CustomUser.objects.filter(email="testuser@test.com").exists())

