class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html_str = ""
        for prop in self.props:
            html_str += f' {prop}=\"{self.props[prop]}\"'
        return html_str

    def __repr__(self):
        return f'HTMLNode(tag={self.tag},value={self.value},children={self.children},props={self.props})'


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None,  props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes require a value")
        if self.tag is None:
            return self.value

        html_string = f'<{self.tag}'
        if self.props is not None:
            for prop in self.props:
                html_string += f' {prop}="{self.props[prop]}"'
        html_string += f'>{self.value}</{self.tag}>'
        return html_string


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node requires a tag")
        if self.children is None:
            raise ValueError("Parent node requires children")

        html_str = f'<{self.tag}'
        if self.props is not None:
            for prop in self.props:
                html_str += f' {prop}="{self.props[prop]}'
        html_str += '>'

        for child in self.children:
            html_str += child.to_html()
        html_str += f'</{self.tag}>'
        return html_str
