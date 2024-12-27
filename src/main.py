import os, shutil
from copy_directory_content import copy_directory_contents
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive

source_directory = "/home/zhx/staticSiteGenerator/static"
destination_directory = "/home/zhx/staticSiteGenerator/public"
root_directory = "/home/zhx/staticSiteGenerator"

def main():
    print("Deleting existing public directory...")
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    
    print("Copying static files to public directory...")    
    copy_directory_contents(source_directory, destination_directory)

    print("Generating pages...")
    # Generate a page from content/index.md using template.html and write it to public/index.html
    generate_pages_recursive(
        os.path.join(root_directory, "content/"),
        os.path.join(root_directory, "template.html"),
        destination_directory
    )


if __name__ == "__main__":
    main()