from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Profile
import time

class SistemaEditarPerfilTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha123')
        Profile.objects.create(user=self.user)

    def test_usuario_edita_perfil(self):
        # Login
        self.selenium.get(f'{self.live_server_url}{reverse("login")}')
        self.selenium.find_element('name', 'email').send_keys(self.user.email)
        self.selenium.find_element('name', 'senha').send_keys('senha123')
        self.selenium.find_element('xpath', '//button[@type="submit"]').click()

        # Ir para página de configuração
        self.selenium.get(f'{self.live_server_url}{reverse("perfil_config")}')

        # Atualizar bio
        bio_input = self.selenium.find_element('name', 'bio')
        bio_input.clear()
        bio_input.send_keys('Bio alterada via Selenium')

        self.selenium.find_element('xpath', '//button[@type="submit"]').click()

        time.sleep(1)