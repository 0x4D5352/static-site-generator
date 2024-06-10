import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD.value)
        node2 = TextNode("This is a text node", TextType.BOLD.value)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD.value)
        node2 = TextNode(
            "This is a different node", TextType.ITALIC.value, "https://www.google.com"
        )
        self.assertNotEqual(node, node2)

    def test_wrong_type(self):
        node = TextNode("This is a text node", TextType.BOLD.value)
        node2 = TextNode("This is a text node", TextType.ITALIC.value)
        self.assertNotEqual(node, node2)

    def test_missing_url(self):
        node = TextNode("This is a text node", TextType.BOLD.value, "https://test.com")
        node2 = TextNode("This is a text node", TextType.BOLD.value)
        self.assertNotEqual(node, node2)

    def test_wrong_text(self):
        node = TextNode(
            "this is one text node", TextType.BOLD.value, "https://www.test.com"
        )
        node2 = TextNode(
            "this is another text node", TextType.BOLD.value, "https://www.test.com"
        )
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode(
            "this is a text node", TextType.TEXT.value, "https://www.test.com"
        )
        self.assertEqual(
            "TextNode(this is a text node, TextType.TEXT, https://www.test.com)",
            repr(node),
        )


if __name__ == "__main__":
    unittest.main()
