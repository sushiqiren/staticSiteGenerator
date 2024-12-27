import os
import shutil

def copy_directory_contents(src, dest):
    # Ensure the destination directory is clean
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    # Recursive function to copy contents
    def copy_contents(src_dir, dest_dir):
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dest_path = os.path.join(dest_dir, item)
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
                print(f"Copied file: {src_path} to {dest_path}")
            elif os.path.isdir(src_path):
                os.mkdir(dest_path)
                print(f"Created directory: {dest_path}")
                copy_contents(src_path, dest_path)

    copy_contents(src, dest)