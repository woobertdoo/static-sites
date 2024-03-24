import inline_markdown as imd

from textnode import (
    TextNode,
    text_type_image,
    text_type_link,
    text_type_code,
    text_type_text
)


def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    print(imd.text_to_textnodes(text))


main()
