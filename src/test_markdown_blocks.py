import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownToHtml(unittest.TestCase):
    def test_markdown_to_blocks(self):
        example_one = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        answer_two = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]
        self.assertEqual(markdown_to_blocks(example_one), answer_two)
        example_two = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        answer_two = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(markdown_to_blocks(example_two), answer_two)


if __name__ == "__main__":
    unittest.main()
