# register.py
"""
Production-ready Selenium Python script for 'User Registration' feature.
Scenarios:
  1. Valid registration details
  2. Invalid email format
  3. Weak password
Includes validation, error handling, and reporting.
"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class RegistrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "https://example.com/register" # Replace with actual URL
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(self.base_url)

    def fill_registration_form(self, name, email, password):
        self.wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(name)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "submit").click()

    def test_valid_registration(self):
        """Scenario: User enters valid registration details"""
        logging.info("Testing valid registration scenario")
        self.fill_registration_form("Test User", "testuser@example.com", "StrongPass123!")
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "welcome-message")))
            welcome_text = self.driver.find_element(By.ID, "welcome-message").text
            self.assertIn("Welcome", welcome_text)
            logging.info("Account created and redirected to welcome page.")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"Account was not created or not redirected: {e}")

    def test_invalid_email_registration(self):
        """Scenario: User enters invalid email format during registration"""
        logging.info("Testing registration with invalid email format")
        self.fill_registration_form("Test User", "invalid-email-format", "StrongPass123!")
        try:
            error_elem = self.wait.until(EC.presence_of_element_located((By.ID, "error-message")))
            error_text = error_elem.text
            self.assertIn("invalid email", error_text.lower())
            logging.info("Error message for invalid email format displayed.")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"No error for invalid email: {e}")
        # Ensure account is not created
        self.assertFalse(self.driver.find_elements(By.ID, "welcome-message"))

    def test_weak_password_registration(self):
        """Scenario: User enters weak password during registration"""
        logging.info("Testing registration with weak password")
        self.fill_registration_form("Test User", "testuser@example.com", "123")
        try:
            error_elem = self.wait.until(EC.presence_of_element_located((By.ID, "error-message")))
            error_text = error_elem.text
            self.assertIn("password", error_text.lower())
            logging.info("Error message for weak password displayed.")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"No error for weak password: {e}")
        # Ensure account is not created
        self.assertFalse(self.driver.find_elements(By.ID, "welcome-message"))

if __name__ == "__main__":
    unittest.main()
