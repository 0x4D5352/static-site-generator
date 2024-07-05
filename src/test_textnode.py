import unittest
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    extract_children_from_text,
)
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        text_node = TextNode("This is a text node", TextType.TEXT)
        text_node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)
        self.assertEqual(text_node, text_node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode(
            "This is a different node", TextType.ITALIC, "https://www.google.com"
        )
        self.assertNotEqual(node, node2)

    def test_wrong_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_missing_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://test.com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_wrong_text(self):
        node = TextNode("this is one text node", TextType.BOLD, "https://www.test.com")
        node2 = TextNode(
            "this is another text node", TextType.BOLD, "https://www.test.com"
        )
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("this is a text node", TextType.TEXT, "https://www.test.com")
        self.assertEqual(
            "TextNode(this is a text node, TextType.TEXT, https://www.test.com)",
            repr(node),
        )

    def test_to_html_node(self):
        text_node = TextNode("this is a text node", TextType.TEXT)
        self.assertEqual(
            text_node_to_html_node(text_node), LeafNode(None, text_node.text)
        )
        bold_node = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(
            text_node_to_html_node(bold_node), LeafNode("b", bold_node.text)
        )
        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        self.assertEqual(
            text_node_to_html_node(italic_node), LeafNode("i", italic_node.text)
        )
        code_node = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(
            text_node_to_html_node(code_node), LeafNode("code", code_node.text)
        )
        link_node = TextNode("this is a link node", TextType.LINK, "https://test.com")
        self.assertEqual(
            text_node_to_html_node(link_node),
            LeafNode("a", link_node.text, {"href": link_node.url}),
        )
        image_node = TextNode(
            "this is an image node", TextType.IMAGE, "https://test.com"
        )
        self.assertEqual(
            text_node_to_html_node(image_node),
            LeafNode("img", None, {"src": image_node.url, "alt": image_node.text}),
        )
        bad_node = TextNode("this is a bad node", "bad")
        self.assertRaises(ValueError, text_node_to_html_node, bad_node)

    def test_extract_children(self):
        text = "somethingsomethingsomething"
        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()
