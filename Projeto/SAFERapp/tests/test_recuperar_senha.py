from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from SAFERapp.models import CustomUser
from django.urls import reverse
from django.core import mail
import time
"""
Faz testes de interface e confere se está redirecionando corretamente 
"""
class TestInterface(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(3)  # Aguarda os elementos carregarem

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_solicita_redefinicao_senha(self):
        """ Testa de redireciona corretamente para as páginas """
        self.driver.get(self.live_server_url)
        self.driver.maximize_window()  # Maximiza a janela
        
        # Encontra e clica no botão Esqueci a senha
        esqueci_senha_butao = self.driver.find_element(By.ID, "passwordRecover")
        esqueci_senha_butao.click()
        self.assertIn("senha-reset", self.driver.current_url) # Verifica se foi redirecionado corretamente

        # Prenche o formulário
        email_input = self.driver.find_element(By.ID, "id_email")
        email_input.send_keys("testuser@example.com")
        # Aperta o botão "Enviar redefinição de senha"
        botao_submit = self.driver.find_element(By.XPATH, "/html/body/div/form/button")
        botao_submit.click()
        
        # Verifica se foi redirecionado para pagina de email enviado
        self.assertIn("senha-reset-feito", self.driver.current_url)

"""
Realiza testes no backend da aplicação
"""
class TestBackend(TestCase):
   
    def setUp(self):
        """Cria um usuário de teste para verificar a redefinição de senha"""
        self.user = CustomUser.objects.create_user(
            nome="testuser", email="testuser@example.com", password="testpassword"
        )
        mail.outbox = [] 
        
        """ 
        Faz testes de requisições de envio de email da redefinição de senha
        """
    def test_enviar_email_redefinicao_senha(self):

        """
        Faz teste para usuário comum
        """
        self.user.tipo_usuario = "Comum"
        # Envia a solicitação de redefinição de senha
        self.client.post(reverse('password_reset'), {'email': self.user.email})
        # Verifique se o e-mail foi enviado
        self.assertEqual(len(mail.outbox), 1)  # Verifica se um e-mail foi enviado

        # Confirma o destinatário
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        mail.outbox = [] #zera caixa de email
        
        
        """
        Faz teste para analista
        """
        self.user.tipo_usuario = "Analista"
        # Envia a solicitação de redefinição de senha
        self.client.post(reverse('password_reset'), {'email': self.user.email})
        # Verifique se o e-mail foi enviado
        self.assertEqual(len(mail.outbox), 1)  # Verifica se um e-mail foi enviado

        # Confirma o destinatário
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        mail.outbox = [] #zera caixa de email
        
        
        """
        Faz teste para gestor
        """
        self.user.tipo_usuario = "Gestor"
        # Envia a solicitação de redefinição de senha
        self.client.post(reverse('password_reset'), {'email': self.user.email})
        # Verifique se o e-mail foi enviado
        self.assertEqual(len(mail.outbox), 1)  # Verifica se um e-mail foi enviado

        # Confirma o destinatário
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        mail.outbox = []#zera caixa de email
        
        
        """
        Faz teste para administrador
        """
        self.user.tipo_usuario = "Administrador"
        # Envia a solicitação de redefinição de senha
        self.client.post(reverse('password_reset'), {'email': self.user.email})
        # Verifique se o e-mail foi enviado
        self.assertEqual(len(mail.outbox), 1)  # Verifica se um e-mail foi enviado

        # Confirma o destinatário
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        

    def test_redefinir_senha_comum(self):
        self.user.tipo_usuario = "Comum"
        self.user.password = "testpassword"

    def test_redefinir_senha_analista(self):
        pass
    
    def test_redefinir_senha_gestor(self):
        pass

    def test_redefinir_senha_administrador(self):
        pass