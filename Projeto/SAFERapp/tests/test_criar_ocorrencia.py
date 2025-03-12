from selenium.webdriver.support.ui import Select
from django.test import LiveServerTestCase
from selenium import webdriver
from SAFERapp.beans.Ocorrencia import Ocorrencia
from SAFERapp.models import CustomUser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

import time

class TestCriarOcorrenciaSemLogin(LiveServerTestCase):
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
        self.driver.get(self.live_server_url)
        self.driver.maximize_window()
        botao_registrar = self.driver.find_element(By.CLASS_NAME, 'btnRegister')
        botao_registrar.click()
        time.sleep(0.5)
    def test_criar_ocorrencia(self):

        nome_input = self.driver.find_element(By.ID, "id_Nome_Autor")
        celular_input = self.driver.find_element(By.ID, "id_Celular_Autor")
        select_box = self.driver.find_element(By.ID, "id_Relacao_Autor")
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        select = Select(select_box)

        nome_input.send_keys("testAutor")
        celular_input.send_keys("1")
        select.select_by_value('discente')

        butao_proximo.click()
        time.sleep(0.5)

        input_nome_animal = self.driver.find_element(By.ID, "id_Nome_Animal")
        local_evento = Select(self.driver.find_element(By.ID, "id_Local"))
        input_referencia = self.driver.find_element(By.ID, "id_Referencia")
        tipo_caso = Select(self.driver.find_element(By.ID, "id_Tipo_Caso"))
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page2"]/button[2]')


        input_nome_animal.send_keys("Animal de teste")
        local_evento.select_by_value("ru")
        input_referencia.send_keys("Referencia do caso")
        tipo_caso.select_by_value("presenca")
        butao_proximo.click()
        time.sleep(0.5)

        descricao = self.driver.find_element(By.ID, "id_Descricao")
        botao_enviar = self.driver.find_element(By.XPATH, '//*[@id="page3"]/button[2]')
        descricao.send_keys("Descrição do caso")
        botao_enviar.click()
        time.sleep(0.5)
        Alert(self.driver).accept()

        self.assertTrue(Ocorrencia.objects.filter(Nome_Autor="testAutor").exists())

    def test_criar_ocorrencia_sem_nome(self):


        celular_input = self.driver.find_element(By.ID, "id_Celular_Autor")
        select_box = self.driver.find_element(By.ID, "id_Relacao_Autor")
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        select = Select(select_box)

        celular_input.send_keys("1")
        select.select_by_value('discente')

        butao_proximo.click()
        time.sleep(0.5)
        erro_mensagem = self.driver.find_element(By.XPATH, '//*[@id="page1"]/div[1]/p[1]/div')

        self.assertIn("Preencha este campo.", erro_mensagem.text)


    def test_criar_ocorrencia_sem_celular(self):

        nome_input = self.driver.find_element(By.ID, "id_Nome_Autor")
        select_box = self.driver.find_element(By.ID, "id_Relacao_Autor")
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        select = Select(select_box)

        nome_input.send_keys("testAutor")
        select.select_by_value('discente')

        butao_proximo.click()
        time.sleep(0.5)
        erro_mensagem = self.driver.find_element(By.XPATH, '//*[@id="page1"]/div[2]/p[1]/div')

        self.assertIn("Preencha este campo.", erro_mensagem.text)


    def test_criar_ocorrencia_sem_animal(self):

        nome_input = self.driver.find_element(By.ID, "id_Nome_Autor")
        celular_input = self.driver.find_element(By.ID, "id_Celular_Autor")
        select_box = self.driver.find_element(By.ID, "id_Relacao_Autor")
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        select = Select(select_box)

        nome_input.send_keys("testAutor")
        celular_input.send_keys("1")
        select.select_by_value('discente')

        butao_proximo.click()
        time.sleep(0.5)

        local_evento = Select(self.driver.find_element(By.ID, "id_Local"))
        input_referencia = self.driver.find_element(By.ID, "id_Referencia")
        tipo_caso = Select(self.driver.find_element(By.ID, "id_Tipo_Caso"))
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page2"]/button[2]')

        local_evento.select_by_value("ru")
        input_referencia.send_keys("Referencia do caso")
        tipo_caso.select_by_value("presenca")
        butao_proximo.click()
        time.sleep(0.5)

        erro_mensagem = self.driver.find_element(By.XPATH, '//*[@id="page2"]/div[1]/p[1]/div')
        self.assertIn("Preencha este campo.", erro_mensagem.text)

    def test_criar_ocorrencia_sem_referencia(self):

        nome_input = self.driver.find_element(By.ID, "id_Nome_Autor")
        celular_input = self.driver.find_element(By.ID, "id_Celular_Autor")
        select_box = self.driver.find_element(By.ID, "id_Relacao_Autor")
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        select = Select(select_box)

        nome_input.send_keys("testAutor")
        celular_input.send_keys("1")
        select.select_by_value('discente')

        butao_proximo.click()
        time.sleep(0.5)

        input_nome_animal = self.driver.find_element(By.ID, "id_Nome_Animal")
        local_evento = Select(self.driver.find_element(By.ID, "id_Local"))
        tipo_caso = Select(self.driver.find_element(By.ID, "id_Tipo_Caso"))
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page2"]/button[2]')

        input_nome_animal.send_keys("Animal de teste")
        local_evento.select_by_value("ru")
        tipo_caso.select_by_value("presenca")
        butao_proximo.click()
        time.sleep(0.5)
        erro_mensagem = self.driver.find_element(By.XPATH, '//*[@id="page2"]/div[3]/p[1]/div')
        self.assertIn("Preencha este campo.", erro_mensagem.text)


class TestCriarOcorrenciaComLogin(LiveServerTestCase):
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
        self.driver.get(self.live_server_url)
        self.driver.maximize_window()
        self.user = CustomUser.objects.create_user(nome='testUser', email="user@test.com", telefone="123456", relacao_ufrpe="discente", password='testpassword')

        email_input = self.driver.find_element(By.ID, 'login')
        senha_input = self.driver.find_element(By.ID, 'password')
        email_input.send_keys(self.user.email)
        senha_input.send_keys("testpassword")

        butao_login = self.driver.find_element(By.XPATH, '//*[@id="hrButton"]/button')
        butao_login.click()
        time.sleep(0.5)

        botao_registrar = self.driver.find_element(By.CLASS_NAME, 'btnRegister')
        botao_registrar.click()
        time.sleep(0.5)

    def test_preenchimento_automatico(self):
        nome_input = self.driver.find_element(By.ID, "id_Nome_Autor")
        celular_input = self.driver.find_element(By.ID, "id_Celular_Autor")
        select_box = self.driver.find_element(By.ID, "id_Relacao_Autor")
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        select = Select(select_box)

        print(nome_input.get_attribute('value'))

        self.assertEqual(self.user.nome, nome_input.get_attribute('value'))
        self.assertEqual(self.user.telefone, celular_input.get_attribute('value'))
        self.assertEqual(self.user.relacao_ufrpe, select.first_selected_option.text.lower())


    def test_criar_ocorrencia_sem_animal(self):

        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        butao_proximo.click()
        time.sleep(0.5)

        local_evento = Select(self.driver.find_element(By.ID, "id_Local"))
        input_referencia = self.driver.find_element(By.ID, "id_Referencia")
        tipo_caso = Select(self.driver.find_element(By.ID, "id_Tipo_Caso"))
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page2"]/button[2]')

        local_evento.select_by_value("ru")
        input_referencia.send_keys("Referencia do caso")
        tipo_caso.select_by_value("presenca")
        butao_proximo.click()
        time.sleep(0.5)

        erro_mensagem = self.driver.find_element(By.XPATH, '//*[@id="page2"]/div[1]/p[1]/div')
        self.assertIn("Preencha este campo.", erro_mensagem.text)

    def test_criar_ocorrencia_sem_referencia(self):
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page1"]/button')
        butao_proximo.click()
        time.sleep(0.5)

        input_nome_animal = self.driver.find_element(By.ID, "id_Nome_Animal")
        local_evento = Select(self.driver.find_element(By.ID, "id_Local"))
        tipo_caso = Select(self.driver.find_element(By.ID, "id_Tipo_Caso"))
        butao_proximo = self.driver.find_element(By.XPATH, '//*[@id="page2"]/button[2]')

        input_nome_animal.send_keys("Animal de teste")
        local_evento.select_by_value("ru")
        tipo_caso.select_by_value("presenca")
        butao_proximo.click()
        time.sleep(0.5)
        erro_mensagem = self.driver.find_element(By.XPATH, '//*[@id="page2"]/div[3]/p[1]/div')
        self.assertIn("Preencha este campo.", erro_mensagem.text)