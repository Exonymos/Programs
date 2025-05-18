import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = """
This is **bolded** paragraph
This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is bolded paragraph",
                "This is another paragraph with italic text and code here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_no_blocks(self):
        md = "Just a single line of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single line of text."])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_leading_trailing_spaces_in_blocks(self):
        md = "  block1  \n\n  block2  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["block1", "block2"])

    def test_markdown_to_blocks_excessive_newlines_between_blocks(self):
        md = "block1\n\n\n\nblock2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["block1", "block2"])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(
            block_to_block_type("####### Not a Heading"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("#NoSpace"), BlockType.PARAGRAPH
        )

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("```code```"), BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("```\ncode"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("code\n```"), BlockType.PARAGRAPH
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> quote line 1\n> quote line 2"), BlockType.QUOTE
        )
        self.assertEqual(block_to_block_type("> single line quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("> quote line 1\nnot a quote line"), BlockType.PARAGRAPH
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("* item 1\n* item 2"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- item 1\n* item 2"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("- item1\n not a list item"), BlockType.PARAGRAPH
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. item 1\n2. item 2\n3. item 3"),
            BlockType.ORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("1. single item list"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. item 1\n3. item 3"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("0. item 1\n1. item 2"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. item1\n not a list item"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. item1\n2.item2"), BlockType.PARAGRAPH
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("Another paragraph\non multiple lines."),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type(" leading space paragraph"), BlockType.PARAGRAPH
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- item 1
- item 2
- item 3 **bold**

1. first
2. second _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3 <b>bold</b></li></ul><ol><li>first</li><li>second <i>italic</i></li></ol></div>"
        )

    def test_headings_and_quotes(self):
        md = """
# Big Heading

> This is a quote.
> With **bold** text.

## Smaller Heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Big Heading</h1><blockquote>This is a quote.\nWith <b>bold</b> text.</blockquote><h2>Smaller Heading</h2></div>"
        )


    def test_codeblock(self):
        md = """
This is text that *should* remain
the **same** even with inline stuff
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            
            expected_html_code_block = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
            self.assertEqual(html, expected_html_code_block)
        )


    def test_empty_markdown(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_markdown_with_only_newlines(self):
        md = "\n\n\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
        
    def test_full_mix(self):
        md = """
# Welcome

This is a **paragraph** with _some_ `code`.

> A wise quote.
> Spread over two lines.

## List Section

- Item A
- Item B: with an ![image](img.png)

1. Number One
2. Number Two: with a [link](https://example.com)
verbatim code
preserved spacing
end code
Another paragraph.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>Welcome</h1><p>This is a <b>paragraph</b> with <i>some</i> <code>code</code>.</p><blockquote>A wise quote.\nSpread over two lines.</blockquote><h2>List Section</h2><ul><li>Item A</li><li>Item B: with an <img src=\"img.png\" alt=\"image\"></img></li></ul><ol><li>Number One</li><li>Number Two: with a <a href=\"https://example.com\">link</a></li></ol><pre><code>verbatim code\n  preserved spacing\nend code</code></pre><p>Another paragraph.</p></div>"
        self.assertEqual(html, expected_html)

if __name__ == "__main__":
    unittest.main()
