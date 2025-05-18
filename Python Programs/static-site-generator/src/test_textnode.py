import unittest

from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node3)

    def test_eq_false_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", TextType.LINK, "https://www.wagslane.dev"
        )
        self.assertNotEqual(node, node2)

    def test_repr_method(self):
        node = TextNode("This is text", TextType.TEXT, "https://example.com/image.png")
        expected_repr = (
            "TextNode('This is text', 'text', 'https://example.com/image.png')"
        )
        self.assertEqual(repr(node), expected_repr)

        node_no_url = TextNode("Another text", TextType.BOLD)
        expected_repr_no_url = "TextNode('Another text', 'bold', None)"
        self.assertEqual(repr(node_no_url), expected_repr_no_url)

    def test_text_node_to_html_text(self):
        tn = TextNode("This is plain text", TextType.TEXT)
        hn = text_node_to_html_node(tn)
        self.assertIsInstance(hn, LeafNode)
        self.assertEqual(hn.tag, None)
        self.assertEqual(hn.value, "This is plain text")

    def test_text_node_to_html_bold(self):
        tn = TextNode("This is bold text", TextType.BOLD)
        hn = text_node_to_html_node(tn)
        self.assertIsInstance(hn, LeafNode)
        self.assertEqual(hn.tag, "b")
        self.assertEqual(hn.value, "This is bold text")

    def test_text_node_to_html_italic(self):
        tn = TextNode("This is italic text", TextType.ITALIC)
        hn = text_node_to_html_node(tn)
        self.assertIsInstance(hn, LeafNode)
        self.assertEqual(hn.tag, "i")
        self.assertEqual(hn.value, "This is italic text")

    def test_text_node_to_html_code(self):
        tn = TextNode("self.value = None", TextType.CODE)
        hn = text_node_to_html_node(tn)
        self.assertIsInstance(hn, LeafNode)
        self.assertEqual(hn.tag, "code")
        self.assertEqual(hn.value, "self.value = None")

    def test_text_node_to_html_link(self):
        tn = TextNode("Click here", TextType.LINK, "https://example.com")
        hn = text_node_to_html_node(tn)
        self.assertIsInstance(hn, LeafNode)
        self.assertEqual(hn.tag, "a")
        self.assertEqual(hn.value, "Click here")
        self.assertEqual(hn.props, {"href": "https://example.com"})

    def test_text_node_to_html_image(self):
        tn = TextNode("Alt text for image", TextType.IMAGE, "/images/pic.png")
        hn = text_node_to_html_node(tn)
        self.assertIsInstance(hn, LeafNode)
        self.assertEqual(hn.tag, "img")
        self.assertEqual(hn.value, "")
        self.assertEqual(
            hn.props, {"src": "/images/pic.png", "alt": "Alt text for image"}
        )

    def test_text_node_to_html_invalid_type(self):
        class MockTextType(Enum):
            UNKNOWN = "unknown"

        tn_invalid = TextNode("test", MockTextType.UNKNOWN)
        tn_non_enum_type = TextNode("test", "not_an_enum_member")
        with self.assertRaisesRegex(ValueError, "Invalid TextType: not_an_enum_member"):
            text_node_to_html_node(tn_non_enum_type)


if __name__ == "__main__":
    unittest.main()
