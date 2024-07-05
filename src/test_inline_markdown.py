import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    # markdown_to_blocks,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes(self):
        code_node = TextNode(
            "this is a text node with a `code block` word", TextType.TEXT
        )
        code_node_results = [
            TextNode("this is a text node with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([code_node], "`", TextType.CODE),
            code_node_results,
        )
        bold_node = TextNode("this is a text node with a **bold** word", TextType.TEXT)
        bold_node_results = [
            TextNode("this is a text node with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([bold_node], "**", TextType.BOLD),
            bold_node_results,
        )
        underscore_bold_node = TextNode(
            "this is a text node with a __bold__ word", TextType.TEXT
        )
        underscore_bold_node_results = [
            TextNode("this is a text node with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([underscore_bold_node], "__", TextType.BOLD),
            underscore_bold_node_results,
        )
        uneven_delimiter = TextNode(
            "this is a text node with a **bold word", TextType.TEXT
        )
        with self.assertRaises(Exception):
            split_nodes_delimiter([uneven_delimiter], "**", TextType.BOLD)

    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "second image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_extract_links(self):
        text = "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another one](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                (
                    "link",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another one",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_split_images(self):
        text = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextType.TEXT,
        )
        image_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image",
                TextType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(split_nodes_image([text]), image_nodes)

    def text_extract_links(self):
        text = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another one](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
            TextType.TEXT,
        )
        link_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "another one",
                TextType.LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(split_nodes_link([text]), link_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), result)


if __name__ == "__main__":
    unittest.main()
