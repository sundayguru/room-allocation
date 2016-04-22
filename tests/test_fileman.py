import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.fileman import FileMan

class TestFileMan(unittest.TestCase):
	"""Test cases for Fileman class"""

	def test_fileman_init_sets_the_file_location(self):
		f = FileMan('test.txt')
		self.assertNotEqual(f.file_location, '')

	def test_fileman_init_raise_valueerror_when_filename_is_not_string(self):
		self.assertRaises(ValueError, FileMan, ['write_test.txt'])

	def test_fileman_read(self):
		f = FileMan('read_test.txt')
		f.remove()
		f.write('hello')
		f.write('world')
		self.assertEqual(f.read(), ['hello','world'])

	def test_fileman_write(self):
		f = FileMan('write_test.txt')
		f.write('great')
		self.assertNotEqual(f.read(), False)

	def test_fileman_write_raise_valueerror_when_data_is_not_string(self):
		f = FileMan('write_test.txt')
		self.assertRaises(ValueError, f.write, ['great'])

	def test_fileman_replace_replaces_the_file_content(self):
		f = FileMan('replace_test.txt')
		f.write('great')
		f.replace('better')
		self.assertEqual(f.read()[0], 'better')

	def test_fileman_replace_writes_to_file(self):
		f = FileMan('replace_test.txt')
		f.replace('great')
		self.assertEqual(f.read()[0], 'great')


	def test_fileman_replace_raise_valueerror_when_data_is_not_string(self):
		f = FileMan('write_test.txt')
		self.assertRaises(ValueError, f.replace, ['great'])

	def test_fileman_remove_returns_false_for_none_file(self):
		f = FileMan('testy.txt')
		self.assertEqual(f.remove(),False)

	def test_fileman_remove(self):
		f = FileMan('remove_test.txt')
		f.write('great')
		self.assertEqual(f.read()[0], 'great')
		f.remove()
		self.assertEqual(f.read(), False)

	def test_fileman_validate_returns_false_for_none_file(self):
		f = FileMan('testy.txt')
		self.assertEqual(f.validate(),False)

	def test_fileman_validate_returns_true_for_a_file(self):
		f = FileMan('test.txt')
		f.write('hello')
		self.assertEqual(f.validate(),True)

	def test_fileman_pickledump(self):
		f = FileMan('test_pickle.pkl')
		r = f.pickle_dump({'a':'value 1','b':'value 2'})
		self.assertEqual(r,True)

	def test_fileman_pickleload(self):
		f = FileMan('test_pickle.pkl')
		f.remove()
		f.pickle_dump({'a':'value 1','b':'value 2'})
		r = f.pickle_load()
		self.assertEqual(r['a'],'value 1')

if __name__ == '__main__':
    unittest.main()
