import re
from enum import Enum, auto
from htmlnode import ParentNode
from inline_markdown import extract_children_from_text


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = "#"
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "*/-"
    ORDERED_LIST = "[0-9]+. "


def markdown_to_blocks(markdown: str) -> list:
    res = []
    segments = markdown.split("\n\n")
    for segment in segments:
        if segment == "":
            continue
        res.append(segment.strip())
    return res


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if False not in [line.startswith(">") for line in block.split("\n")]:
        return BlockType.QUOTE
    if False not in [
        line.startswith("* ") or line.startswith("- ") for line in block.split("\n")
    ]:
        return BlockType.UNORDERED_LIST
    if False not in [
        line.startswith(f"{i + 1}. ") for i, line in enumerate(block.split("\n"))
    ]:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def convert_paragraph_block(block: str) -> ParentNode:
    return ParentNode(
        "p", children=extract_children_from_text(" ".join(block.split("\n")))
    )


def convert_heading_block(block: str) -> ParentNode:
    starting_length = len(block)
    contents = block.lstrip("#").strip()
    # the strip messes up the length so we remove 1 from the result
    tag = f"h{starting_length - len(contents) - 1}"
    return ParentNode(tag, children=extract_children_from_text(contents))


def convert_code_block(block: str) -> ParentNode:
    contents = block.lstrip("`").rstrip("`").strip()
    return ParentNode("pre", [ParentNode("code", extract_children_from_text(contents))])


def convert_quote_block(block: str) -> ParentNode:
    contents = " ".join(block.replace("> ", "").split("\n")).strip()
    return ParentNode("blockquote", children=extract_children_from_text(contents))


def convert_unordered_list_block(block: str) -> ParentNode:
    delimiter = "* " if block.startswith("* ") else "- "
    contents = block.split(delimiter)
    children = [
        ParentNode("li", children=extract_children_from_text(content.strip()))
        for content in contents
        if content != ""
    ]
    return ParentNode("ul", children=children)


def convert_ordered_list_block(block: str) -> ParentNode:
    contents = re.split("[0-9]+.", block)
    children = [
        ParentNode("li", children=extract_children_from_text(content.strip()))
        for content in contents
        if content != ""
    ]
    return ParentNode("ol", children=children)


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                children.append(convert_paragraph_block(block))
            case BlockType.HEADING:
                children.append(convert_heading_block(block))
            case BlockType.CODE:
                children.append(convert_code_block(block))
            case BlockType.QUOTE:
                children.append(convert_quote_block(block))
            case BlockType.UNORDERED_LIST:
                children.append(convert_unordered_list_block(block))
            case BlockType.ORDERED_LIST:
                children.append(convert_ordered_list_block(block))
            case _:
                raise Exception("how'd you find a missing blocktype???")
    top_node = ParentNode("div", children)
    return top_node


if __name__ == "__main__":
    md = """
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
    print('hello world!')
```
"""
    print(markdown_to_html_node(md))
