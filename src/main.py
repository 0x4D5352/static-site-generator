from os import path, listdir, mkdir
from shutil import copy, rmtree
from markdown_blocks import markdown_to_html_node


def copy_files(source: str, destination: str) -> None:
    print(f"Copying files from {source} to {destination}")
    for item in listdir(source):
        print(f"Item found: {item}")
        item_path = path.join(source, item)
        if path.isfile(item_path):
            print(f"Copying file: {item}")
            copy(item_path, destination)
        else:
            print(f"Creating subdirectory: {item}")
            subdirectory = path.join(destination, item)
            mkdir(subdirectory)
            source_subdirectory = path.join(source, item)
            copy_files(source_subdirectory, subdirectory)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path}, using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown)
    content = content.to_html()
    generated = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest_path, "w") as file:
        file.write(generated)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path
) -> None:
    for item in listdir(dir_path_content):
        item_path = path.join(dir_path_content, item)
        if path.isfile(item_path):
            if item.endswith(".md"):
                item_name = item[:-3]
                dest_path = path.join(dest_dir_path, item_name + ".html")
                generate_page(item_path, template_path, dest_path)
        else:
            subdirectory = path.join(dest_dir_path, item)
            mkdir(subdirectory)
            generate_pages_recursive(item_path, template_path, subdirectory)


def main() -> None:
    print(listdir("public"))
    print("deleting the above files and directories")
    rmtree("public")
    mkdir("public")
    copy_files("static", "public")
    print("generating pages")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
