from django.test import TestCase, LiveServerTestCase

from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from SAFERapp.models import CustomUser
from selenium.webdriver.chrome.options import Options
from django.urls import reverse

import time

from selenium.webdriver.common.alert import Alert
"""
Testes da funcionalidade de excluir conta
"""
class TestExcluirConta(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--disable-password-generation")  # Desativa sugestões de senha
        chrome_options.add_argument("--disable-save-password-bubble")  # Desativa popup de salvar senha
        chrome_options.add_argument("--disable-popup-blocking")  # Desativa bloqueio de popups
        chrome_options.add_argument("--disable-notifications")  # Desativa notificações
        chrome_options.add_argument("--incognito")  # Modo anônimo para evitar sugestões baseadas em histórico
        cls.driver = webdriver.Chrome(options=chrome_options)
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
            time.sleep(0.5)

            self.driver.get(self.live_server_url+reverse('telaPerfil', kwargs={'username': self.user.nome}))

            time.sleep(1)
            botao_apagar = self.driver.find_element(By.XPATH, '/html/body/div/div/form[2]/button')
            botao_apagar.click()

            Alert(self.driver).accept()
            time.sleep(0.5)
            Alert(self.driver).accept()
            time.sleep(0.8)

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
                time.sleep(0.5)
                self.driver.get(self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))

                time.sleep(1)
                botao_apagar = self.driver.find_element(By.XPATH, '/html/body/div/div/form[2]/button')
                botao_apagar.click()


                Alert(self.driver).accept()
                time.sleep(0.9)
                Alert(self.driver).accept()

                time.sleep(0.8)
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
                    time.sleep(0.5)

                    self.driver.get(self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))


                    time.sleep(1)
                    botao_apagar = self.driver.find_element(By.XPATH, '/html/body/div/div/form[2]/button')
                    botao_apagar.click()


                    Alert(self.driver).accept()
                    time.sleep(0.9)
                    Alert(self.driver).accept()

                    time.sleep(0.5)
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
                        time.sleep(0.5)
                        self.driver.get(
                            self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))

                        time.sleep(1)
                        botao_apagar = self.driver.find_element(By.XPATH, '/html/body/div/div/form[2]/button')
                        botao_apagar.click()
                        time.sleep(1)
                        Alert(self.driver).accept()
                        time.sleep(0.9)
                        Alert(self.driver).accept()

                        self.assertFalse(CustomUser.objects.filter(email="testuser@test.com").exists())

