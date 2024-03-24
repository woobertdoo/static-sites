import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "test")])
        self.assertRaises(ValueError, node.to_html)

    def test_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_one_level(self):
        node = ParentNode("p", [
            LeafNode(tag="b", value="bold"),
            LeafNode(value="normal"),
            LeafNode(tag="i", value="italic"),
            LeafNode(value="normal")
        ])
        expected_str = '<p><b>bold</b>normal<i>italic</i>normal</p>'
        self.assertEqual(node.to_html(), expected_str)

    def test_two_level(self):
        node = ParentNode("p", [
            ParentNode("i", [LeafNode(tag="b", value="doublenested")]),
            LeafNode(value="normal"),
            LeafNode(tag="i", value="italic"),
            LeafNode(value="normal")
        ])
        expected_str = '<p><i><b>doublenested</b></i>normal<i>italic</i>normal</p>'
        self.assertEqual(node.to_html(), expected_str)
