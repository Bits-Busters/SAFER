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

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            nome="testuser", email="testuser@example.com", password="testpassword"
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes((self.user.pk)))
        self.token = default_token_generator.make_token(self.user)
    def test_solicita_redefinicao_senha(self):
        """ Testa se redireciona corretamente para as páginas """
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
        time.sleep(1)
        self.assertIn("senha-reset-feito", self.driver.current_url)

    def test_redefinir_senha_comum(self):
        self.user.tipo_usuario = "Comum"
        nova_senha = "N$wP@ssw1RD"

        reset_url = f"{self.live_server_url}{reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})}"
        self.driver.get(reset_url)
        # Testa se está na página certa
        self.assertIn("set-password", self.driver.current_url)

        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")


        # Testa divergencia de senha
        password1.send_keys("12983712980372108973")
        password2.send_keys("kj23h42376dcjkwd3927")
        butao_alterar.click()

        mensagem_error = self.driver.find_element(By.XPATH, "/html/body/div/form/ul[2]/li")
        self.assertEqual(mensagem_error.text, "Os dois campos de senha não correspondem.")


        # Testa se salva nova senha se preencher campos corretamente
        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        password1.send_keys(nova_senha)
        password2.send_keys(nova_senha)
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")
        butao_alterar.click()

        # Verifica no db se a nova senha foi salva
        time.sleep(1)
        self.user.refresh_from_db()
        self.assertIn(reverse("password_reset_complete"), self.driver.current_url)
        self.assertTrue(self.user.check_password(nova_senha))

    def test_redefinir_senha_analista(self):
        self.user.tipo_usuario = "Analista"
        nova_senha = "N$wP@ssw1RD"

        reset_url = f"{self.live_server_url}{reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})}"
        self.driver.get(reset_url)
        # Testa se está na página certa
        self.assertIn("set-password", self.driver.current_url)

        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")

        # Testa divergencia de senha
        password1.send_keys("12983712980372108973")
        password2.send_keys("kj23h42376dcjkwd3927")
        butao_alterar.click()
        mensagem_error = self.driver.find_element(By.XPATH, "/html/body/div/form/ul[2]/li")
        self.assertEqual(mensagem_error.text, "Os dois campos de senha não correspondem.")

        # Testa se salva nova senha se preencher campos corretamente
        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        password1.send_keys(nova_senha)
        password2.send_keys(nova_senha)
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")
        butao_alterar.click()
        # Verifica no db se a nova senha foi salva
        time.sleep(1)
        self.user.refresh_from_db()

        self.assertIn(reverse("password_reset_complete"), self.driver.current_url)

        self.assertTrue(self.user.check_password(nova_senha))

    def test_redefinir_senha_gestor(self):
        self.user.tipo_usuario = "Gestor"
        nova_senha = "N$wP@ssw1RD"

        reset_url = f"{self.live_server_url}{reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})}"
        self.driver.get(reset_url)
        # Testa se está na página certa
        self.assertIn("set-password", self.driver.current_url)

        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")

        # Testa divergencia de senha
        password1.send_keys("12983712980372108973")
        password2.send_keys("kj23h42376dcjkwd3927")
        butao_alterar.click()

        mensagem_error = self.driver.find_element(By.XPATH, "/html/body/div/form/ul[2]/li")
        self.assertEqual(mensagem_error.text, "Os dois campos de senha não correspondem.")

        # Testa se salva nova senha se preencher campos corretamente
        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        password1.send_keys(nova_senha)
        password2.send_keys(nova_senha)
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")
        butao_alterar.click()
        # Verifica no db se a nova senha foi salva
        time.sleep(1)
        self.user.refresh_from_db()
        self.assertIn(reverse("password_reset_complete"), self.driver.current_url)
        self.assertTrue(self.user.check_password(nova_senha))

    def test_redefinir_senha_administrador(self):
        self.user.tipo_usuario = "Administrador"
        nova_senha = "N$wP@ssw1RD"

        reset_url = f"{self.live_server_url}{reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})}"
        self.driver.get(reset_url)
        # Testa se está na página certa
        self.assertIn("set-password", self.driver.current_url)

        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")

        # Testa divergencia de senha
        password1.send_keys("12983712980372108973")
        password2.send_keys("kj23h42376dcjkwd3927")
        butao_alterar.click()

        mensagem_error = self.driver.find_element(By.XPATH, "/html/body/div/form/ul[2]/li")
        self.assertEqual(mensagem_error.text, "Os dois campos de senha não correspondem.")

        # Testa se salva nova senha se preencher campos corretamente
        password1 = self.driver.find_element(By.ID, "id_new_password1")
        password2 = self.driver.find_element(By.ID, "id_new_password2")
        password1.send_keys(nova_senha)
        password2.send_keys(nova_senha)
        butao_alterar = self.driver.find_element(By.XPATH, "/html/body/div/form/button")
        butao_alterar.click()
        # Verifica no db se a nova senha foi salva
        time.sleep(1)
        self.user.refresh_from_db()
        self.assertIn(reverse("password_reset_complete"), self.driver.current_url)

        self.assertTrue(self.user.check_password(nova_senha))

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
        self.uidb64 = urlsafe_base64_encode(force_bytes((self.user.pk)))
        self.token = default_token_generator.make_token(self.user)
        """ 
        Faz testes de requisições de envio de email da redefinição de senha
        """
    def test_enviar_email_redefinicao_senha_comum(self):

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
        self.assertIn("redefinir", mail.outbox[0].body)

    def test_enviar_email_redefinicao_senha_analista(self):

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

    def test_enviar_email_redefinicao_senha_gestor(self):

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

    def test_enviar_email_redefinicao_senha_administrador(self):

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

        
    def test_email_confirmacao_senha_trocada_comum(self):
        self.user.tipo_usuario = "Comum"
        nova_senha = "N$wP@ssw1RD"
        response = self.client.post(
            reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token}),
            data={
                'new_password1': nova_senha,
                'new_password2': nova_senha
            }
        )
        print(response.content)
        self.assertEqual(response.status_code, 302)  # Deve redirecionar
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])


