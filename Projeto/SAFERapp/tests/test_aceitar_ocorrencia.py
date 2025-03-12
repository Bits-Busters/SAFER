from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.models import CustomUser
from selenium.webdriver.common.by import By
from django.utils.timezone import now

import time

""""
Testes para aceitar uma ocorrencia
"""


class TestAceitarOcorrencia(LiveServerTestCase):
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
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="testpassword",)
        self.ocorrencia = Ocorrencia.objects.create(
            Autor=self.user,
            Nome_Autor=self.user.nome,
            Celular_Autor="1",
            Relacao_Autor="VISITANTE",
            Tipo_Caso="presenca",
            Descricao="Descrição do caso de teste",
            Nome_Animal="Preguiça",
            Local='ru',
            Referencia="Referência do caso",
            DataHora=now(),
            Status='aberto'
        )



    def test_aceitar_ocorrencia_analista(self):
        senha = "testpassword"

        analista = CustomUser.objects.create_user(nome='testUser', email="analista@test.com", password=senha, tipo_usuario='analista')
        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(analista.email)
        senha_input.send_keys(senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)

        # 1- Clicar no botão "Ocorrências em Aberto".
        chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
        chamados_abertos.click()


        url_chamado =self.driver.find_element(By.XPATH, '/html/body/div/div/ul/li/button')
        url_chamado = url_chamado.get_attribute('onclick').split("'")[1]
        numero_chamado = int(url_chamado.split('/')[2])

        self.driver.get(self.live_server_url+reverse('telaDetalhesChamado', kwargs={'id': numero_chamado}))


        gerar_resgate_botao = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/button')
        gerar_resgate_botao.click()
        time.sleep(0.5)

        self.driver.get(self.live_server_url+reverse('telaChamados', kwargs={'tipoChamado': "chamados-aceitos"}))

        lista_chamado = self.driver.find_elements(By.CLASS_NAME, 'list-group')[0].find_elements(By.TAG_NAME, 'li')

        self.assertEqual(len(lista_chamado), 1)

    def test_aceitar_ocorrencia_gestor(self):

        senha = "testpassword"
        gestor = CustomUser.objects.create_user(nome='testUser', email="analista@test.com", password=senha,
                                                  tipo_usuario='gestor')
        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(gestor.email)
        senha_input.send_keys(senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)

        # 1- Clicar no botão "Ocorrências em Aberto".
        chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
        chamados_abertos.click()
        time.sleep(0.5)

        url_chamado =self.driver.find_element(By.XPATH, '/html/body/div/div/ul/li/button')
        url_chamado = url_chamado.get_attribute('onclick').split("'")[1]
        numero_chamado = int(url_chamado.split('/')[2])


        self.driver.get(self.live_server_url+reverse('telaDetalhesChamado', kwargs={'id': numero_chamado}))

        gerar_resgate_botao = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/button')
        gerar_resgate_botao.click()
        time.sleep(0.5)

        self.driver.get(self.live_server_url + reverse('telaChamados', kwargs={'tipoChamado': "chamados-aceitos"}))

        lista_chamado = self.driver.find_elements(By.CLASS_NAME, 'list-group')[0].find_elements(By.TAG_NAME, 'li')

        self.assertEqual(len(lista_chamado), 1)

    def test_aceitar_ocorrencia_administrador(self):

        senha = "testpassword"
        administrador = CustomUser.objects.create_user(nome='testUser', email="analista@test.com", password=senha,
                                                  tipo_usuario='admin')
        self.driver.get(self.live_server_url)
        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(administrador.email)
        senha_input.send_keys(senha)

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)

        # 1- Clicar no botão "Ocorrências em Aberto".
        chamados_abertos = self.driver.find_elements(By.XPATH, '//*[@id="textoNavbar"]/ul/li[7]/a')[0]
        chamados_abertos.click()
        time.sleep(0.5)

        url_chamado =self.driver.find_element(By.XPATH, '/html/body/div/div/ul/li/button')
        url_chamado = url_chamado.get_attribute('onclick').split("'")[1]
        numero_chamado = int(url_chamado.split('/')[2])

        self.driver.get(self.live_server_url+reverse('telaDetalhesChamado', kwargs={'id': numero_chamado}))

        gerar_resgate_botao = self.driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/button')
        gerar_resgate_botao.click()
        time.sleep(0.5)

        self.driver.get(self.live_server_url + reverse('telaChamados', kwargs={'tipoChamado': "chamados-aceitos"}))

        lista_chamado = self.driver.find_elements(By.CLASS_NAME, 'list-group')[0].find_elements(By.TAG_NAME, 'li')

        self.assertEqual(len(lista_chamado), 1)