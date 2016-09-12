from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time
import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_name')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512,
            delta = 5
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Jim will visit the website and check to see it is a todo site
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #First Jim will add an item to his grocery list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Buy peacock feathers')

        #When Jim presses enter he will see his list item added to the list and the url
        #will reflect his change to a new specific unique url for his list
        inputbox.send_keys(Keys.ENTER)
        jim_list_url = self.browser.current_url
        self.assertRegex(jim_list_url, '/lists/.+')

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        #Then Jim will add another item to his list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        #Now Jim checks to see the two items are displayed
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        #Jim quits and a new person, Joe opens the website
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        #Joe visits the website
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly', page_text)

        #Joe starts a new list with the following items: 1. Buy milk
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #Joe has a unique URL
        joe_url = self.browser.current_url
        self.assertRegex(joe_url, '/lists/.+')
        self.assertNotEqual(jim_list_url, joe_url)

        #Again check there is not any residual list text
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly', page_text)

        #lastly he will exit
        self.browser.quit()