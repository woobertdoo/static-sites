import unittest

from textnode import TextNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text", "bold")
        node2 = TextNode("This is a node", "bold")
        self.assertNotEqual(node, node2)

    def test_nodesplit(self):
        node = TextNode("This is text with a **code block** word", text_type_text)
        new_nodes = TextNode.split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_bold),
            TextNode(" word", text_type_text)
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
