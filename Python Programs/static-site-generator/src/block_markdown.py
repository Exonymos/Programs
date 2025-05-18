from enum import Enum
import re
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode, LeafNode


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        stripped_block = block.strip()
        if stripped_block:
            filtered_blocks.append(stripped_block)
    return filtered_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block_string):
    lines = block_string.split("\n")

    if re.match(r"#{1,6} ", block_string):
        return BlockType.HEADING

    if block_string.startswith("```") and block_string.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith("* ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    expected_number = 1
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            is_ordered_list = False
            break
        expected_number += 1
    if is_ordered_list and len(lines) > 0:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    """Converts a string of text with inline markdown to a list of HTMLNode children."""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block_string):
    processed_block_string = block_string.replace("\n", " ")
    children = text_to_children(processed_block_string)
    return ParentNode("p", children)


def heading_to_html_node(block_string):
    level = 0
    for char in block_string:
        if char == "#":
            level += 1
        else:
            break

    if level == 0 or level > 6 or not block_string[level:].startswith(" "):
        return paragraph_to_html_node(block_string)

    content = block_string[level + 1 :]
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block_string):
    if not block_string.startswith("```") or not block_string.endswith("```"):
        raise ValueError("Invalid code block: missing ``` delimiters")

    lines = block_string.split("\n")
    if len(lines) < 2:
        content = block_string[3:-3]
    else:
        content = "\n".join(lines[1:-1])

    code_leaf_node = LeafNode("code", content)
    return ParentNode("pre", [code_leaf_node])


def quote_to_html_node(block_string):
    lines = block_string.split("\n")
    cleaned_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block: line does not start with '>'")
        cleaned_line = line.lstrip(">").lstrip(" ")
        cleaned_lines.append(cleaned_line)

    content = "\n".join(cleaned_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block_string):
    lines = block_string.split("\n")
    list_item_nodes = []
    for line in lines:
        if line.startswith("- "):
            content = line[2:]
        elif line.startswith("* "):
            content = line[2:]
        else:
            raise ValueError(f"Invalid unordered list item: {line}")

        children = text_to_children(content)
        list_item_nodes.append(ParentNode("li", children))

    return ParentNode("ul", list_item_nodes)


def ordered_list_to_html_node(block_string):
    lines = block_string.split("\n")
    list_item_nodes = []
    expected_number = 1
    for line in lines:
        prefix = f"{expected_number}. "
        if not line.startswith(prefix):
            raise ValueError(f"Invalid ordered list item (expected {prefix}): {line}")

        content = line[len(prefix) :]
        children = text_to_children(content)
        list_item_nodes.append(ParentNode("li", children))
        expected_number += 1

    return ParentNode("ol", list_item_nodes)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_html_nodes = []

    for block_string in blocks:
        block_type = block_to_block_type(block_string)

        if block_type == BlockType.PARAGRAPH:
            children_html_nodes.append(paragraph_to_html_node(block_string))
        elif block_type == BlockType.HEADING:
            children_html_nodes.append(heading_to_html_node(block_string))
        elif block_type == BlockType.CODE:
            children_html_nodes.append(code_to_html_node(block_string))
        elif block_type == BlockType.QUOTE:
            children_html_nodes.append(quote_to_html_node(block_string))
        elif block_type == BlockType.UNORDERED_LIST:
            children_html_nodes.append(unordered_list_to_html_node(block_string))
        elif block_type == BlockType.ORDERED_LIST:
            children_html_nodes.append(ordered_list_to_html_node(block_string))
        else:
            raise ValueError(
                f"Unknown block type: {block_type} for block: {block_string}"
            )

    return ParentNode("div", children_html_nodes)
