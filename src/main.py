import inline_markdown as imd

from textnode import (
    TextNode,
    text_type_image,
    text_type_link,
    text_type_code,
    text_type_text
)


def main():
    text = """# This is a heading

    ```This is a 
    Code Block```

    > This is a block quote
    > Someone really said this

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is an
    * unordered list
    
    1. This is an
    2. Ordered List
    """
    print(imd.markdown_to_html(text))


main()
