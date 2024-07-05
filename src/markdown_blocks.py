from enum import Enum, auto
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import extract_children_from_text


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


def convert_paragraph_block(block: str) -> HTMLNode:
    return HTMLNode("p", children=extract_children_from_text(block))


def convert_heading_block(block: str) -> HTMLNode:
    starting_length = len(block)
    contents = block.lstrip("#").strip()
    tag = f"h{starting_length - len(contents)}"
    return HTMLNode(tag, children=extract_children_from_text(contents))


def convert_code_block(block: str) -> HTMLNode:
    contents = block.lstrip("`").rstrip("`").strip()
    return HTMLNode("pre", HTMLNode("code", extract_children_from_text(contents)))


def convert_quote_block(block: str) -> HTMLNode:
    raise NotImplementedError
    return HTMLNode("", children=extract_children_from_text(contents))


def convert_unordered_list_block(block: str) -> HTMLNode:
    raise NotImplementedError


def convert_ordered_list_block(block: str) -> HTMLNode:
    raise NotImplementedError


def markdown_to_html_node(markdown: str) -> HTMLNode:
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
