from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(5)

        # Crear superusuari inicial
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_staff_user_and_login(self):
        selenium = self.selenium
        wait = WebDriverWait(selenium, 10)

        # 1️⃣ Entrar a la pàgina d'administració
        selenium.get(f"{self.live_server_url}/admin/login/")

        # 2️⃣ Esperar que aparegui el camp de nom d'usuari
        wait.until(EC.presence_of_element_located((By.ID, "id_username")))

        # 3️⃣ Fer login amb el superusuari creat
        selenium.find_element(By.ID, "id_username").send_keys("isard")
        selenium.find_element(By.ID, "id_password").send_keys("pirineus")
        selenium.find_element(By.XPATH, "//input[@type='submit']").click()

        # 4️⃣ Asserció que el login ha funcionat
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "LOG OUT")))
