def extract_title(markdown):
    markdown_list = markdown.split('\n')
    
    for line in markdown_list:
        if line.startswith('# '):
            return line[2:].strip()
            
    raise ValueError("No title found in markdown")
