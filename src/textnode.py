from enum import Enum
from htmlnode import LeafNode

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
    if delimiter not in ["**", "*", "`"]:
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