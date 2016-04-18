import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.fileman import FileMan

class TestFileMan(unittest.TestCase):
	"""Test cases for Fileman class"""

	def test_fileman_init_sets_the_file_location(self):
		f = FileMan('test.txt')
		self.assertNotEqual(f.file_location, '')

	def test_fileman_read(self):
		f = FileMan('test.txt')
		self.assertEqual(f.read(), ['hello\n','world'])

	def test_fileman_read_returns_false_for_none_file(self):
		f = FileMan('testy.txt')
		self.assertEqual(f.read(),False)

	def test_fileman_write(self):
		f = FileMan('write_test.txt')
		f.write('great')
		self.assertNotEqual(f.read(), False)

	def test_fileman_replace_replaces_the_file_content(self):
		f = FileMan('replace_test.txt')
		f.write('great')
		f.replace('better')
		self.assertEqual(f.read()[0], 'better')

	def test_fileman_replace_writes_to_file(self):
		f = FileMan('replace_test.txt')
		f.replace('great')
		self.assertEqual(f.read()[0], 'great')

	def test_fileman_remove(self):
		f = FileMan('remove_test.txt')
		f.write('great')
		self.assertEqual(f.read()[0], 'great')
		f.remove()
		self.assertEqual(f.read(), False)

if __name__ == '__main__':
    unittest.main()
