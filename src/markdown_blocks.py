from enum import Enum, auto


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
        if segment != "":
            res.append(segment.strip())
    return res


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        pass
    return BlockType.PARAGRAPH
