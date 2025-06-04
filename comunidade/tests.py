from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from comunidade.models import Community
from django.test import LiveServerTestCase
from selenium import webdriver

class CommunityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.user = cls.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.sample_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'simple image content',
            content_type='image/jpeg'
        )
        cls.comunidade_base_data = {
            'nome': 'Comunidade_Teste',
            'sobre': 'Descrição de teste',
            'profile_picture': cls.sample_image,
            'criador': cls.user
        }

    def test_nome_tag_generator(self):
        lista_tags = set()
        
        for i in range(100):
            with self.subTest(iteration=i):
                comunidade = Community(**self.comunidade_base_data)
                comunidade.nome_tag_generator()
                
                # Vê se a tag é unica
                self.assertNotIn(comunidade.nome_tag, lista_tags, 'Tag repetida')
                lista_tags.add(comunidade.nome_tag)

        # Verifica se todas as tags foram produzidas
        self.assertEqual(len(lista_tags),test_iterations,'Tag nao criada')
    
    def test_comunidade_criar_e_salvar(self):
        """Test creating and saving a Community instance"""
        comunidade = Community(**self.comunidade_base_data)
        comunidade.nome_tag_generator()  # Generate the nome_tag
        comunidade.save()
        
        # Verify the object was saved correctly
        self.assertEqual(Community.objects.count(), 1)
        comunidade_salva = Community.objects.first()
        self.assertEqual(comunidade_salva.nome, 'Comunidade_Teste')
        self.assertEqual(comunidade_salva.criador, self.user)
        self.assertTrue(comunidade_salva.profile_picture)

class CommunityE2ETest(LiveServerTestCase):

    #setup que usa a liveServerTestCase
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
    
    def test_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Harmonia', self.browser.title)
