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

        attributes = ""
        for key, val in self.props.items():
            attributes += f' {key}="{val}"'
        return attributes

    def __repr__(self):
        return f"HTMLNode({repr(self.tag)}, {repr(self.value)}, children: {repr(self.children)}, {repr(self.props)})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if value is None:
            raise ValueError("LeafNode requires a value")

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value to render to HTML")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        if self.children is None:
            raise ValueError("ParentNode requires a list of children (can be empty)")

    def to_html(self):
        children_html_content = ""
        for child_node in self.children:
            children_html_content += child_node.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html_content}</{self.tag}>"
