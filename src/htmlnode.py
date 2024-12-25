
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    
    def __repr__(self):
        # object = HTMLNode(self.tag, self.value, self.children, self.props)
        # tag_name = object.tag
        # text_value = object.value
        # children_list = object.children
        # attributes_dict = object.props
        # return (
        #     f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, "
        #     f"children={repr(self.children)}, props={repr(self.props)})"
        # )
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)        
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return f"{self.value}"
        
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node should have tags")
        
        if not self.children:
            raise ValueError("Parent node must have children nodes")
        
        props_str = self.props_to_html()
        
        html_str = ""
        for child in self.children:
            html_str += child.to_html()

        html_start = f"<{self.tag}{props_str}>"
        html_end = f"</{self.tag}>"
        html_str = html_start + html_str + html_end
        return html_str
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"   

