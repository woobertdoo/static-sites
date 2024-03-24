import re

from textnode import (
    TextNode,
    text_type_italic,
    text_type_bold,
    text_type_text,
    text_type_code,
    text_type_image,
    text_type_link
)


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
