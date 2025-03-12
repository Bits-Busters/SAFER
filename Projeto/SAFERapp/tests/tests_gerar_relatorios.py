from django.test import TestCase, LiveServerTestCase

from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from SAFERapp.models import CustomUser
from selenium.webdriver.chrome.options import Options
from django.urls import reverse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

import time

from selenium.webdriver.common.alert import Alert
"""
Testes da funcionalidade de trocar senha
"""
class TestGerarRelatorio(LiveServerTestCase):
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
            self.user = CustomUser.objects.create_user(nome="test", email="testuser@test.com", password="Testpassword1.")
            self.user.tipo_usuario = "admin"
            self.user.save()
            self.driver.maximize_window()  # Maximiza a janela
            self.senha = "Testpassword1."
            existe = CustomUser.objects.filter(email="testuser@test.com").exists()
            self.assertTrue(existe)
    def test_gerar_relatorio(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.driver.get(self.live_server_url)
        current_url = self.driver.current_url
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Gerar Relatório").click()

        time.sleep(1)
        self.assertEqual(self.driver.current_url, current_url+"relatorios/")

    def test_gerar_relatorio_sem_permissao(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.user.tipo_usuario = "comum"
        self.user.save()
        self.driver.get(self.live_server_url)
        current_url = self.driver.current_url
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)
        # Alterando a URL no Selenium
        self.driver.get( current_url+"/relatorios/")


        time.sleep(1)
        self.assertNotEqual(self.driver.current_url, current_url+"relatorios/")
    def test_filtro_local(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.driver.get(self.live_server_url)
        current_url = self.driver.current_url
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "id_LocalCaso").click()
        dropdown = self.driver.find_element(By.ID, "id_LocalCaso")
        dropdown.find_element(By.XPATH, "//option[. = 'RU']").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Gerar Relatório").click()

        # 4 | click | id=id_LocalCaso | 
        self.driver.find_element(By.ID, "id_LocalCaso").click()
        # 5 | select | id=id_LocalCaso | label=RU
        dropdown = self.driver.find_element(By.ID, "id_LocalCaso")
        dropdown.find_element(By.XPATH, "//option[. = 'RU']").click()
        # 6 | click | css=.btn:nth-child(6) | 
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(6)").click()

        time.sleep(1)
        self.assertEqual(self.driver.current_url, current_url+"relatorios/")

    def test_filtro_tipo(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.driver.get(self.live_server_url)
        current_url = self.driver.current_url
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "id_StatusCaso").click()
        dropdown = self.driver.find_element(By.ID, "id_StatusCaso")
        dropdown.find_element(By.XPATH, "//option[. = 'Aberto']").click()
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Gerar Relatório").click()

        time.sleep(1)
        self.assertEqual(self.driver.current_url, current_url+"relatorios/")

    def test_filtro_data_inicial(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.driver.get(self.live_server_url)
        current_url = self.driver.current_url
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "id_DataInicial").click()
        self.driver.find_element(By.ID, "id_DataInicial").send_keys("2025-03-04")
        time.sleep(0.5)
        self.driver.find_element(By.LINK_TEXT, "Gerar Relatório").click()

        time.sleep(1)
        self.assertEqual(self.driver.current_url, current_url+"relatorios/")