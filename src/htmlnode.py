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
    

        