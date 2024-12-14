from django.test import TestCase
from SAFERapp.models import Usuario
from faker import Faker
from random import choice

RELACOES_UFRPE = ['visitante', 'terceirizado', 'tecnico', 'discente', 'docente']
# Create your tests here.

class TestModelsO(TestCase):

    @classmethod
    def setUpTestData():
        print("Iniciando teste dos modelos")

    def setUp():
        print("Testes dos métodos")
    def teste_atualizar_informacoes(self):
        print("Método: atualizar_informacoes")
        # Dados iniciais 
        nome_teste = Faker.name()
        email_teste = Faker.email()
        
        
        user = Usuario.objects.create(Nome=nome_teste, Email=email_teste, Senha=senha_teste)

        # Novos informações de atualização

        novo_nome_teste = Faker.name()
        novo_email_teste = Faker.email()
        
        

        # Teste de atualização de informações
        user.atualizar_infomacoes(nome=novo_nome_teste, email=novo_email_teste,)
        self.assertEqual(user.Nome, novo_nome_teste)
        self.assertEqual(user.Email, novo_email_teste)

        print("atualizar_informacoes() passou")