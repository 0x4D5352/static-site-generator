import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click Me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            node2.to_html(), '<a href="https://www.google.com">Click Me!</a>'
        )

    def test_no_children(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(None, node.children)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = node.to_html()
        self.assertEqual(
            html, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_nested_parent(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold Text"),
                        LeafNode(
                            "a", "Click Me!", props={"href": "https://www.google.com"}
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div><p><b>Bold Text</b><a href="https://www.google.com">Click Me!</a></p></div>',
        )

    def test_multiple_nests(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold Text"),
                        LeafNode(
                            "a", "Click Me!", props={"href": "https://www.google.com"}
                        ),
                        ParentNode(
                            "div",
                            [
                                LeafNode("i", "Italicized Text"),
                                LeafNode(None, "Normal Text"),
                            ],
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<div><p><b>Bold Text</b><a href="https://www.google.com">Click Me!</a><div><i>Italicized Text</i>Normal Text</div></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
