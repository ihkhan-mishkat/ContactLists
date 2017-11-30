from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import Select

from population_script import add_contact

User = get_user_model()


class UserStoryTest(StaticLiveServerTestCase):
    SITE_NAME = 'Contact Lists'

    def setUp(self):
        user = User(username="mishkat", email="mishkat@interconnectionbd.com",
                    first_name="Mishkat", last_name="Khan")
        user.set_password('password')
        user.save()
        add_contact('abc', user)
        add_contact('zxc', user)
        add_contact('qwe', user)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_login_and_enter_a_contact(self):
        # Mishkat goes to website
        self.browser.get(self.live_server_url)

        # He notices the title of the website
        self.assertEqual(self.SITE_NAME, self.browser.title)

        # He clicks the login link
        self.browser.find_element_by_link_text('Log in').click()

        # Mishkat fills outs his information
        username_inputbox = self.browser.find_element_by_name('username')
        username_inputbox.send_keys('mishkat')

        password_inputbox = self.browser.find_element_by_name('password')
        password_inputbox.send_keys('password')

        # He clicks button to login
        self.browser.find_element_by_class_name('btn').click()

        # He can now see the contacts page and sees text welcoming him
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('mishkat', header_text)

        # Mishkat wants to add a new contact
        self.browser.find_element_by_class_name('btn').click()
        # Modal appears
        self.browser.switch_to_active_element()
        # Starts typing in new contact
        new_name_inputbox = self.browser.find_element_by_id('newName')
        new_name_inputbox.send_keys('Mishkat')

        new_email_inputbox = self.browser.find_element_by_id('newEmail')
        new_email_inputbox.send_keys('mishkat@interconnectionbd.com')

        new_phone_inputbox = self.browser.find_element_by_id('newPhone')
        new_phone_inputbox.send_keys('+8801913783954')

        new_address_inputbox = self.browser.find_element_by_id('newAddress')
        new_address_inputbox.send_keys('434/1, N. Kazipara, Mirpur, Dhaka-1216')

        # Submits the new contact
        self.browser.find_element_by_css_selector('button[class="btn btn-primary"]').click()

        # Focus back to main page
        self.browser.switch_to.default_content()

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

