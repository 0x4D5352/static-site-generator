import unittest
from htmlnode import ParentNode, LeafNode
from markdown_blocks import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
)


class TestMarkdownToHtml(unittest.TestCase):
    def test_markdown_to_blocks(self):
        example_one = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        answer_one = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]
        self.assertEqual(markdown_to_blocks(example_one), answer_one)

    def test_markdown_to_blockstwo(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block(self):
        example_one = "# this block has a heading"
        example_two = "## this block is also a heading"
        example_three = """```python
 def foo():
     print("hello world!")
 ```"""
        example_four = """> greentext
> aka quote blocks
> look at all that"""
        example_five = """* test
* another test
* yet another test"""
        example_six = """- look at this
- using hyphens for lists
- cause asterisks got overloaded"""
        example_seven = """1. this is
2. an ordered list
3. so it should count"""
        example_eight = """this is just a normal block of text
so it should show up as a paragraph block."""
        self.assertEqual(block_to_block_type(example_one), BlockType.HEADING)
        self.assertEqual(block_to_block_type(example_two), BlockType.HEADING)
        self.assertEqual(block_to_block_type(example_three), BlockType.CODE)
        self.assertEqual(block_to_block_type(example_four), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(example_five), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(example_six), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(example_seven), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(example_eight), BlockType.PARAGRAPH)

    def test_markdown_to_html_node(self):
        example_one = """
This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# This is a heading

- This is a list item
- This is another list item

1. This is an ordered list item
2. This is another list item with [a link](https://www.example.com)

> This is a quote block
> It has multiple lines

## This is a subheading

```
def foo():
    print("hello world!")
```
"""

        res = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(
                            None, "This is a paragraph of text. It has some ", None
                        ),
                        LeafNode("b", "bold", None),
                        LeafNode(None, " and ", None),
                        LeafNode("i", "italic", None),
                        LeafNode(None, " words inside of it.", None),
                    ],
                    None,
                ),
                ParentNode("h1", [LeafNode(None, "This is a heading", None)], None),
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li", [LeafNode(None, "This is a list item", None)], None
                        ),
                        ParentNode(
                            "li",
                            [LeafNode(None, "This is another list item", None)],
                            None,
                        ),
                    ],
                    None,
                ),
                ParentNode(
                    "ol",
                    [
                        ParentNode(
                            "li",
                            [LeafNode(None, "This is an ordered list item", None)],
                            None,
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "This is another list item with ", None),
                                LeafNode(
                                    "a", "a link", {"href": "https://www.example.com"}
                                ),
                            ],
                            None,
                        ),
                    ],
                    None,
                ),
                ParentNode(
                    "blockquote",
                    [
                        LeafNode(
                            None, "This is a quote block\nIt has multiple lines", None
                        )
                    ],
                    None,
                ),
                ParentNode("h2", [LeafNode(None, "This is a subheading", None)], None),
                ParentNode(
                    "pre",
                    [
                        ParentNode(
                            "code",
                            [
                                LeafNode(
                                    None, 'def foo():\n    print("hello world!")', None
                                )
                            ],
                            None,
                        )
                    ],
                    None,
                ),
            ],
            None,
        )
        self.assertEqual(markdown_to_html_node(example_one), res)


if __name__ == "__main__":
    unittest.main()
