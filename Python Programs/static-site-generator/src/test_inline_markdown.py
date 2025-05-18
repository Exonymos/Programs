import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_simple_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_bold(self):
        node = TextNode("This has **bold text** in it.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_italic(self):
        node = TextNode("An _italic_ word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_multiple_delimiters(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_starts_and_ends_with_delimiter(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_no_delimiter(self):
        node = TextNode("Just plain text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("Just plain text.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_non_text_node(self):
        node = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_mixed_nodes(self):
        nodes = [
            TextNode("Text before, then ", TextType.TEXT),
            TextNode("`code here`", TextType.TEXT),
            TextNode(" and some more text.", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("Text before, then ", TextType.TEXT),
            TextNode("code here", TextType.CODE),
            TextNode(" and some more text.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_double_delimiter_in_row(self):
        node = TextNode("Text with **bold1****bold2** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold1", TextType.BOLD),
            TextNode("bold2", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("This is `unclosed code", TextType.TEXT)
        with self.assertRaisesRegex(
            ValueError, "Invalid markdown: unclosed delimiter '`'"
        ):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_empty_input_node_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_delimiter_only_text(self):
        node = TextNode("``", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

        node2 = TextNode("` `", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "`", TextType.CODE)
        expected2 = [TextNode(" ", TextType.CODE)]
        self.assertEqual(new_nodes2, expected2)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt_or_url(self):
        text = "![alt text]() and ![](/url.png)"
        matches = extract_markdown_images(text)
        expected = [("alt text", ""), ("", "/url.png")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_single(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "Link1 [L1](url1) and Link2 [L2](url2)."
        matches = extract_markdown_links(text)
        expected = [("L1", "url1"), ("L2", "url2")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links, but maybe an ![image](img.png)."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_mixed_content(self):
        text = "A [link](link.com) and an ![image](image.com) and another [link2](link2.com)."
        matches = extract_markdown_links(text)
        expected = [("link", "link.com"), ("link2", "link2.com")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_empty_anchor_or_url(self):
        text = "[anchor text]() and [](/url.com)"
        matches = extract_markdown_links(text)
        expected = [("anchor text", ""), ("", "/url.com")]
        self.assertListEqual(expected, matches)


class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_multiple(self):
        node = TextNode(
            "![image1](url1.png) and ![image2](url2.png) surrounding text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image1", TextType.IMAGE, "url1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2.png"),
            TextNode(" surrounding text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_at_start_and_end(self):
        node = TextNode(
            "![image1](url1.png)text between![image2](url2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image1", TextType.IMAGE, "url1.png"),
            TextNode("text between", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_no_images(self):
        node = TextNode("Just plain text, no images here.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Just plain text, no images here.", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_only_image(self):
        node = TextNode("![onlyimage](only.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("onlyimage", TextType.IMAGE, "only.png")]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)

    def test_split_image_non_text_node_passthrough(self):
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("This has an ![image](img.png)", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("This has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode("Italic text", TextType.ITALIC),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_single(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) antd text after.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" antd text after.", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_multiple(self):
        node = TextNode(
            "Link [L1](url1) and link [L2](url2) and text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Link ", TextType.TEXT),
            TextNode("L1", TextType.LINK, "url1"),
            TextNode(" and link ", TextType.TEXT),
            TextNode("L2", TextType.LINK, "url2"),
            TextNode(" and text.", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_start_and_end(self):
        node = TextNode(
            "[L1](url1)text between[L2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("L1", TextType.LINK, "url1"),
            TextNode("text between", TextType.TEXT),
            TextNode("L2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_no_links(self):
        node = TextNode("Just plain text, no links here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("Just plain text, no links here.", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_only_link(self):
        node = TextNode("[onlylink](only.url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("onlylink", TextType.LINK, "only.url")]
        self.assertListEqual(expected, new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_full_conversion_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_simple_text(self):
        text = "Just plain text."
        nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("Just plain text.", TextType.TEXT)]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_bold_and_italic(self):
        text = "**Bold** and _italic_."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_code_and_link(self):
        text = "`code here` and [a link](url.com)."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("code here", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "url.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_image_at_start(self):
        text = "![alt text](img.url) followed by text."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("alt text", TextType.IMAGE, "img.url"),
            TextNode(" followed by text.", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected_nodes)

    def test_text_to_textnodes_interspersed(self):
        text = "Text, then `code`, then _italic_, then **bold**, then ![img](url), then [link](url2)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text, then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", then ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", then ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(", then ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url2"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [])


if __name__ == "__main__":
    unittest.main()
