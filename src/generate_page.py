import os
from textnode import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page: from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        content = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    title = extract_title(content)
    content = markdown_to_html_node(content).to_html()
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(template)
    print(f"Generated page: {dest_path}")