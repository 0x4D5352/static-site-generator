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
