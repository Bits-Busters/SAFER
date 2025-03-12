from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from SAFERapp.models import CustomUser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def login(self, email, senha):
        """
        Método auxiliar para realizar o login.
        """
        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(email)
        senha_input.send_keys(senha)
        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()

        # Espera até que o link de "Chamados Aceitos" esteja visível
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="textoNavbar"]/ul/li[6]/a')))

    def acessar_chamados_aceitos(self):
        """
        Método auxiliar para acessar a página de chamados aceitos.
        """
        chamados_aceitos = self.driver.find_element(By.XPATH, '//*[@id="textoNavbar"]/ul/li[6]/a')
        chamados_aceitos.click()

        # Verifica se a URL foi alterada para a página de chamados aceitos
        self.assertIn(reverse("telaChamados", kwargs={"tipoChamado": "chamados-aceitos"}), self.driver.current_url)

    def verificar_lista_vazia(self):
        """
        Verifica se a lista de chamados aceitos está vazia.
        """
        lista_chamado = self.driver.find_elements(By.CLASS_NAME, 'list-group')[0].find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(lista_chamado), 0)

    def test_visualizar_lista_analista(self):
        """
        Verifica se o analista tem acesso à lista de chamados aceitos.
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='analista')
        self.login(self.user.email, self.senha)
        self.acessar_chamados_aceitos()

    def test_visualizar_lista_gestor(self):
        """
        Verifica se o gestor tem acesso à lista de chamados aceitos.
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='gestor')
        self.login(self.user.email, self.senha)
        self.acessar_chamados_aceitos()

    def test_visualizar_lista_administrador(self):
        """
        Verifica se o administrador tem acesso à lista de chamados aceitos.
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='admin')
        self.login(self.user.email, self.senha)
        self.acessar_chamados_aceitos()

    def test_verificar_lista_vazia_analista(self):
        """
        Verifica se aparece uma lista vazia de chamados aceitos para o analista.
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='analista')
        self.login(self.user.email, self.senha)
        self.acessar_chamados_aceitos()
        self.verificar_lista_vazia()

    def test_verificar_lista_vazia_gestor(self):
        """
        Verifica se aparece uma lista vazia de chamados aceitos para o gestor.
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='gestor')
        self.login(self.user.email, self.senha)
        self.acessar_chamados_aceitos()
        self.verificar_lista_vazia()

    def test_verificar_lista_vazia_administrador(self):
        """
        Verifica se aparece uma lista vazia de chamados aceitos para o administrador.
        """
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", password=self.senha, tipo_usuario='admin')
        self.login(self.user.email, self.senha)
        self.acessar_chamados_aceitos()
        self.verificar_lista_vazia()
