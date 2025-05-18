import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) == 1:
            if old_node.text:
                new_nodes.append(old_node)
            continue

        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: unclosed delimiter '{delimiter}' in text: '{old_node.text}'"
            )

        for i, part_text in enumerate(parts):
            if not part_text:
                continue

            current_text_type = TextType.TEXT if i % 2 == 0 else text_type
            new_nodes.append(TextNode(part_text, current_text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if not images:
            if original_text:
                new_nodes.append(TextNode(original_text, TextType.TEXT))
            continue

        remaining_text = original_text
        for alt_text, url in images:
            parts = remaining_text.split(f"![{alt_text}]({url})", 1)
            if len(parts) < 2:
                continue

            text_before = parts[0]
            text_after = parts[1]

            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = text_after

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if not links:
            if original_text:
                new_nodes.append(TextNode(original_text, TextType.TEXT))
            continue

        remaining_text = original_text
        for anchor_text, url in links:
            parts = remaining_text.split(f"[{anchor_text}]({url})", 1)
            if len(parts) < 2:
                continue

            text_before = parts[0]
            text_after = parts[1]

            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))

            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            remaining_text = text_after

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes
