from enum import Enum
from htmlnode import LeafNode, ParentNode
import re


class TextType(Enum):
    NORMAL_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        
        return (
            self.text == other.text and
            self.text_type == other.text_type and 
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.NORMAL_TEXT:
                return LeafNode(None, text_node.text)
             
            case TextType.BOLD_TEXT:
                return LeafNode("b", text_node.text)
            
            case TextType.ITALIC_TEXT:
                return LeafNode("i", text_node.text)
            
            case TextType.CODE_TEXT:
                return LeafNode("code", text_node.text)
            
            case TextType.LINKS:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            
            case TextType.IMAGES:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            
            case _:
                raise ValueError(f"Invalid text type: {text_node.text_type}")
            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in ["**", "*", "`", "_"]:
        raise ValueError(f"{delimiter} is not a valid markdown delimiter")
    result = []
    for node in old_nodes:
        
        if node.text_type != TextType.NORMAL_TEXT:
            result.append(node)
            continue
        split_nodes = []
        node_text_content = node.text.split(delimiter)
        if len(node_text_content) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(node_text_content)):
            if node_text_content[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(node_text_content[i], TextType.NORMAL_TEXT))
            else:
                split_nodes.append(TextNode(node_text_content[i], text_type))

        result.extend(split_nodes)       

    return result

def extract_markdown_images(text):
    found_result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found_result

def extract_markdown_links(text):
    found_result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found_result

def split_nodes_image(old_nodes):    
    new_nodes = []
    for old_node in old_nodes:
        if len(extract_markdown_images(old_node.text)) == 0:
            new_nodes.append(old_node)
            continue
        if len(old_node.text) == 0:
            continue
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        image_markdown_list = extract_markdown_images(old_node.text)
        node_text = old_node.text
        for image_markdown in image_markdown_list:
            image_text = image_markdown[0]
            image_url = image_markdown[1]
            node_text_list = node_text.split(f"![{image_text}]({image_url})", 1)
            if len(node_text_list) != 2:
                raise ValueError("Invalid markdown, formatted section not closed")
            if node_text_list[0]:
                split_nodes.append(TextNode(node_text_list[0], TextType.NORMAL_TEXT))
            split_nodes.append(TextNode(image_text, TextType.IMAGES, image_url))
            node_text = node_text_list[1] if len(node_text_list) > 1 else ""
        if node_text:
            split_nodes.append(TextNode(node_text, TextType.NORMAL_TEXT))
            
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):  
    new_nodes = []
    for old_node in old_nodes:
        if len(extract_markdown_links(old_node.text)) == 0:
            new_nodes.append(old_node)
            continue
        if len(old_node.text) == 0:
            continue
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        link_markdown_list = extract_markdown_links(old_node.text)
        node_text = old_node.text
        for link_markdown in link_markdown_list:
            link_text = link_markdown[0]
            link_url = link_markdown[1]
            parts = node_text.split(f"[{link_text}]({link_url})", 1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown, formatted section not closed")
            if parts[0]:
                split_nodes.append(TextNode(parts[0], TextType.NORMAL_TEXT))
            split_nodes.append(TextNode(link_text, TextType.LINKS, link_url))
            node_text = parts[1] if len(parts) > 1 else ""
        if node_text:
            split_nodes.append(TextNode(node_text, TextType.NORMAL_TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    # Process underscores for italics after other delimiters
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    result_array = []
    current_block = []

    for line in markdown.split("\n"):
        stripped_line = line.strip()
        if stripped_line:
            current_block.append(stripped_line)
        else:
            if current_block:
                result_array.append("\n".join(current_block))
                current_block = []
    if current_block:
        result_array.append("\n".join(current_block))
        
    return result_array

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"   

def block_to_block_type(block):
    # if block.startswith("# "):
    #     return block_type_heading
    # if block.startswith("* ") or block.startswith("- "):
    #     return block_type_ulist
    # if block.startswith("1. "):
    #     return block_type_olist
    # if block.startswith(">"):
    #     return block_type_quote
    # if block.startswith("```"):
    #     return block_type_code
    
    # return block_type_paragraph
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:    
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)                     
