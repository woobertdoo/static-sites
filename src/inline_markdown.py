import re

from htmlnode import (
    ParentNode,
    LeafNode
)

from textnode import (
    TextNode,
    text_type_italic,
    text_type_bold,
    text_type_text,
    text_type_code,
    text_type_image,
    text_type_link
)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        node_images = extract_markdown_images(text)
        next_segment = text
        curr_segment = ""
        final_segment = ""
        if len(node_images) == 0:
            new_nodes.append(old_node)
        for image in node_images:
            split = next_segment.split(f"![{image[0]}]({image[1]})", 1)
            curr_segment = split[0]
            if len(split) > 1:
                next_segment = split[1]
            if curr_segment != "":
                new_nodes.append(TextNode(curr_segment, text_type_text))
            image_node = TextNode(image[0], text_type_image, image[1])
            new_nodes.append(image_node)
        if len(node_images) != 0:
            final_segment = next_segment.split(f"![{node_images[-1][0]}]({node_images[-1][1]})", 1)
            if final_segment[0] != "":
                final_node = TextNode(final_segment[0], text_type_text)
                if final_node not in new_nodes:
                    new_nodes.append(final_node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        node_links = extract_markdown_links(text)
        next_segment = text
        curr_segment = ""
        final_segment = []
        if len(node_links) == 0:
            new_nodes.append(old_node)
        for link in node_links:
            split = next_segment.split(f"[{link[0]}]({link[1]})", 1)
            curr_segment = split[0]
            if len(split) > 1:
                next_segment = split[1]
            if curr_segment != "":
                new_nodes.append(TextNode(curr_segment, text_type_text))
            link_node = TextNode(link[0], text_type_link, link[1])
            new_nodes.append(link_node)
        if len(node_links) != 0:
            final_segment = next_segment.split(f"[{node_links[-1][0]}]({node_links[-1][1]})", 1)
            if final_segment[0] != '':
                final_node = TextNode(final_segment[0], text_type_text)
                if final_node not in new_nodes:
                    new_nodes.append(final_node)
    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, text_type_text)
    bold_split = split_nodes_delimiter([text_node], '**', text_type_bold)
    italic_split = split_nodes_delimiter(bold_split, '*', text_type_italic)
    code_split = split_nodes_delimiter(italic_split, '`', text_type_code)
    image_split = split_nodes_image(code_split)
    final_split = split_nodes_link(image_split)
    return final_split


def markdown_to_blocks(markdown):
    blocks = []
    curr_block = ""
    lines = markdown.split("\n")
    for line in lines:
        if line.strip(' \n') == "":
            if curr_block != "":
                blocks.append(curr_block)
                curr_block = ""
        else:
            curr_block += f"{line.strip()}\n"
    return blocks


def block_to_block_type(block):
    heading_match = re.findall(r"^#{1,6}\s.*", block)
    code_match = re.findall(r"^`{3}[\s\S]*`{3}$", block)
    quote_match = re.findall(r"(?m)^>.*$", block)
    unordered_match = re.findall(r"(?m)^[\*|-].*$", block)
    ordered_match = re.findall(r"(?m)^\d\..*$", block)

    block_lines = block.split("\n")
    block_lines.pop()

    if heading_match != []:
        return block_type_heading
    elif code_match != []:
        return block_type_code
    elif quote_match != []:
        if len(quote_match) == len(block_lines):
            return block_type_quote
    elif unordered_match != []:
        if len(unordered_match) == len(block_lines):
            return block_type_unordered_list
    elif ordered_match != []:
        if len(ordered_match) == len(block_lines):
            cur_line = 0
            for line in block_lines:
                if int(line[0]) == cur_line + 1:
                    cur_line = int(line[0])
            if cur_line == len(block_lines):
                return block_type_ordered_list
    return block_type_paragraph


def heading_to_html(heading):
    heading_num = 0
    for char in heading:
        if char == "#":
            heading_num += 1
        else:
            break

    tag = f'h{heading_num}'
    content = heading.split('# ', 1)[1]
    return LeafNode(tag=tag, value=content)


def quote_to_html(quote):
    lines = []
    for line in quote.split("\n"):
        if len(line) > 1:
            lines.append(line.split("> ", 1)[1])
    children = []
    for line in lines:
        children.append(LeafNode(tag="p", value=line))
    return ParentNode(tag="blockquote", children=children)


def code_to_html(code):
    content = code.split('```')[1]
    block_node = LeafNode(tag="code", value=content)
    return ParentNode(tag="pre", children=[block_node])


def unordered_list_to_html(ul):
    lines = []
    for line in ul.split("\n"):
        if len(line) > 1:
            split_char = line[0]
            lines.append(line.split(f"{split_char} ", 1)[1])
    items = []
    for item in lines:
        items.append(LeafNode(tag="li", value=item))
    return ParentNode(tag="ul", children=items)


def ordered_list_to_html(ol):
    lines = []
    for line in ol.split("\n"):
        if len(line) > 1:
            split_char = line[0]
            lines.append(line.split(f"{split_char}. ", 1)[1])
    items = []
    for item in lines:
        items.append(LeafNode(tag="li", value=item))
    return ParentNode(tag="ol", children=items)


def paragraph_to_html(paragraph):
    return LeafNode(tag="p", value=paragraph)


def markdown_to_html(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            nodes.append(heading_to_html(block))
        elif block_type == block_type_quote:
            nodes.append(quote_to_html(block))
        elif block_type == block_type_code:
            nodes.append(code_to_html(block))
        elif block_type == block_type_unordered_list:
            nodes.append(unordered_list_to_html(block))
        elif block_type == block_type_ordered_list:
            nodes.append(ordered_list_to_html(block))
        elif block_type == block_type_paragraph:
            nodes.append(paragraph_to_html(block))
    return ParentNode(tag="div", children=nodes)
