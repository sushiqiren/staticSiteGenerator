import os, shutil, sys
from copy_directory_content import copy_directory_contents
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive

source_directory = "/home/zhx/staticSiteGenerator/static"
destination_directory = "/home/zhx/staticSiteGenerator/docs"
root_directory = "/home/zhx/staticSiteGenerator"

def main():
    # Get basepath from command line argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print("Deleting existing docs directory...")
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)
    
    print("Copying static files to docs directory...")    
    copy_directory_contents(source_directory, destination_directory)

    print("Generating pages...")
    # Generate pages from content directory using template.html and write them to docs directory
    generate_pages_recursive(
        os.path.join(root_directory, "content/"),
        os.path.join(root_directory, "template.html"),
        destination_directory,
        basepath
    )


if __name__ == "__main__":
    main()