import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_path) and src_path.endswith('.md'):
            dest_path = os.path.splitext(dest_path)[0] + '.html'
            generate_page(src_path, template_path, dest_path)
            print(f"Generated page: {dest_path}")
        elif os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            print(f"Created directory: {dest_path}")
            generate_pages_recursive(src_path, template_path, dest_path)