import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_tag(self):
        node = LeafNode(value='Click Me!', tag='a', props={'href': "https://www.google.com"})
        expected_str = '<a href="https://www.google.com">Click Me!</a>'
        self.assertEqual(expected_str, node.to_html())

    def test_plaintext(self):
        node = LeafNode(value='Hello')
        expected_str = 'Hello'
        self.assertEqual(expected_str, node.to_html())

    def test_err(self):
        node = LeafNode(value=None)
        self.assertRaises(ValueError, node.to_html)
