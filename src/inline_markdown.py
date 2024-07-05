import re
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_textnodes(text: str) -> list:
    input_text = TextNode(text, TextType.TEXT)
    res = [input_text]
    for text_type in TextType:
        delimiter = ""
        match text_type:
            case TextType.TEXT:
                res = res
            case TextType.BOLD:
                delimiter = "**"
            case TextType.ITALIC:
                delimiter = "*"
            case TextType.CODE:
                delimiter = "`"
            case TextType.IMAGE:
                res = split_nodes_image(res)
            case TextType.LINK:
                res = split_nodes_link(res)
        if delimiter != "":
            res = split_nodes_delimiter(res, delimiter, text_type)
    return res


def extract_children_from_text(block: str) -> list:
    text_nodes = text_to_textnodes(block)
    return [text_node_to_html_node(node) for node in text_nodes]


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    res = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
        else:
            sub_node = []
            split_nodes = old_node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception(
                    f"Invalid markdown detected: missing a matching {delimiter} in {old_node.text}"
                )
            for i, node in enumerate(split_nodes):
                # how do i get this without enumerate... maybe i just should enumerate
                if i % 2 == 0:
                    # we're a non-code block word
                    sub_node.append(TextNode(node, TextType.TEXT))
                else:
                    # we're in a delimited block!
                    sub_node.append(TextNode(node, text_type))
            res.extend(sub_node)
    return res


def split_nodes_image(old_nodes: list) -> list:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for match in matches:
            splitter = f"![{match[0]}]({match[1]})"
            split_nodes = node_text.split(splitter, 1)
            if len(split_nodes) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if split_nodes[0] != "":
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            node_text = split_nodes[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list) -> list:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for match in matches:
            splitter = f"[{match[0]}]({match[1]})"
            split_nodes = node_text.split(splitter, 1)
            if len(split_nodes) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if split_nodes[0] != "":
                new_nodes.append(TextNode(split_nodes[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            node_text = split_nodes[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text: str) -> list:
    image_regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(image_regex, text)
    return matches


def extract_markdown_links(text: str) -> list:
    image_regex = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(image_regex, text)
    return matches
