import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type


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


if __name__ == "__main__":
    unittest.main()
