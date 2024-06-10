from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode


def main() -> None:
    node = TextNode("This is a text node", "bold", "https://boot.dev")
    print(node)


if __name__ == "__main__":
    main()
