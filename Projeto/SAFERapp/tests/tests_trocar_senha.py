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
class TestTrocarSenha(LiveServerTestCase):
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
            self.driver.maximize_window()  # Maximiza a janela
            self.senha = "Testpassword1."
            existe = CustomUser.objects.filter(email="testuser@test.com").exists()
            self.assertTrue(existe)
    def test_repetir_senha(self):
        """
        Teste de exclusão de conta de Administrador
        """
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

        self.driver.find_element(By.ID, "id_old_password").click()
        self.driver.find_element(By.ID, "id_old_password").send_keys(self.senha)
        self.driver.find_element(By.ID, "id_new_password1").click()
        self.driver.find_element(By.ID, "id_new_password1").send_keys(self.senha)
        self.driver.find_element(By.ID, "id_new_password2").click()
        self.driver.find_element(By.ID, "id_new_password2").send_keys(self.senha)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        self.assertTrue(self.user.check_password(self.senha))


    def test_conta_inexistente(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)
        novaSenha = "1234"

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)
        self.driver.get(
            self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))

        time.sleep(1)
        self.user.delete()
        # 4 | click | id=id_old_password | 
        self.driver.find_element(By.ID, "id_old_password").click()
        # 5 | type | id=id_old_password | nBr13210..
        self.driver.find_element(By.ID, "id_old_password").send_keys(self.senha)
        # 6 | click | id=id_new_password1 | 
        self.driver.find_element(By.ID, "id_new_password1").click()
        # 7 | type | id=id_new_password1 | 1234
        self.driver.find_element(By.ID, "id_new_password1").send_keys(novaSenha)
        # 8 | click | id=id_new_password2 | 
        self.driver.find_element(By.ID, "id_new_password2").click()
        # 9 | type | id=id_new_password2 | 1234
        self.driver.find_element(By.ID, "id_new_password2").send_keys(novaSenha)
        # 10 | click | css=.btn-primary | 
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        self.assertFalse(CustomUser.objects.filter(email="testuser@test.com").exists())

    def test_senha_fraca(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)
        novaSenha = "1234"

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)
        self.driver.get(
            self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))

        time.sleep(1)
        # 4 | click | id=id_old_password | 
        self.driver.find_element(By.ID, "id_old_password").click()
        # 5 | type | id=id_old_password | nBr13210..
        self.driver.find_element(By.ID, "id_old_password").send_keys(self.senha)
        # 6 | click | id=id_new_password1 | 
        self.driver.find_element(By.ID, "id_new_password1").click()
        # 7 | type | id=id_new_password1 | 1234
        self.driver.find_element(By.ID, "id_new_password1").send_keys(novaSenha)
        # 8 | click | id=id_new_password2 | 
        self.driver.find_element(By.ID, "id_new_password2").click()
        # 9 | type | id=id_new_password2 | 1234
        self.driver.find_element(By.ID, "id_new_password2").send_keys(novaSenha)
        # 10 | click | css=.btn-primary | 
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        self.assertFalse(self.user.check_password(novaSenha))

    def test_senha_previamente_utilizada(self):
        """
        Teste de exclusão de conta de Administrador
        """
        self.driver.get(self.live_server_url)
        
        # Reobtenção dos elementos para garantir que não sejam "stale"
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        
        email_input.send_keys(self.user.email)
        senha_input.send_keys(self.senha)

        novaSenha = "Aa1029384756."
        
        # Reobtenção do botão de login
        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        
        # Espera até a página ser carregada corretamente após login
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Meu Perfil")))

        self.driver.get(self.live_server_url + reverse('telaPerfil', kwargs={'username': self.user.nome}))

        # Espera até os campos de senha estarem presentes na tela de perfil
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_old_password")))

        # Preenche os campos de senha
        self.driver.find_element(By.ID, "id_old_password").send_keys(self.senha)
        self.driver.find_element(By.ID, "id_new_password1").send_keys(novaSenha)
        self.driver.find_element(By.ID, "id_new_password2").send_keys(novaSenha)

        # Clica no botão de alteração de senha
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        # Espera o alerta aparecer e o aceita
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

        # Reobtenção dos campos de login para enviar nova senha
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys(novaSenha)

        # Reobtenção do botão de login e clique
        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()

        # Espera até a tela de "Meu Perfil" ser carregada
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Meu Perfil")))

        # Clica no link "Meu Perfil"
        self.driver.find_element(By.LINK_TEXT, "Meu Perfil").click()

        # Espera até os campos de senha estarem novamente visíveis
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "id_old_password")))

        # Preenche os campos de senha com os dados antigos e novos
        self.driver.find_element(By.ID, "id_old_password").send_keys(novaSenha)
        self.driver.find_element(By.ID, "id_new_password1").send_keys(self.senha)
        self.driver.find_element(By.ID, "id_new_password2").send_keys(self.senha)

        # Clica no botão para alterar a senha
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        # Espera o alerta aparecer e o aceita
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()
        # Verifica se a senha antiga foi alterada corretamente
        self.user.refresh_from_db()
        time.sleep(0.8)
        self.assertFalse(self.user.check_password(self.senha))


