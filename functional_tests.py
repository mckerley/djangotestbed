from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		#Jim will visit the website and check to see it is a todo site
		self.browser.get('http://localhost:8000')

		self.assertIn('To-do', self.browser.title)
		self.fail() #Work still to do
		#First Jim will add an item to his grocery list
		#Then Jim will add another item to his list
		#Then he will note he has a unique url
		#lastly he will exit
if __name__ == '__main__':
	unittest.main(warnings='ignore')