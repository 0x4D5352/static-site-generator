from os import path, listdir, mkdir
from shutil import copy, rmtree


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


def main() -> None:
    print(listdir("public"))
    print("deleting the above files and directories")
    rmtree("public")
    mkdir("public")
    copy_files("static", "public")


if __name__ == "__main__":
    main()
