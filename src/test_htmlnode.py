import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_none_nodes(self):
        node = HTMLNode()
        self.assertIsNone(node.tag, None)
        self.assertIsNone(node.value, None)
        self.assertIsNone(node.children, None)
        self.assertIsNone(node.props, None)

    def test_props_to_html(self):
        node = HTMLNode("test", "lookatest", [], {"href": "https://www.test.com"})
        self.assertEqual(' href="https://www.test.com"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode(
            "test",
            "lookatest",
            [],
            {"href": "https://www.test.com"},
        )
        self.assertEqual(
            "HTMLNode(test, lookatest, [], {'href': 'https://www.test.com'})",
            repr(node),
        )


if __name__ == "__main__":
    unittest.main()


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click Me!", props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)
