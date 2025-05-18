import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        html_props = node.props_to_html()
        self.assertIn(' href="https://www.google.com"', html_props)
        self.assertIn(' target="_blank"', html_props)
        self.assertTrue(html_props.startswith(" "))
        self.assertEqual(len(html_props.split(" ")) - 1, 2)

    def test_repr_method(self):
        node = HTMLNode("p", "Hello", None, {"class": "my-paragraph"})
        expected_repr = (
            "HTMLNode('p', 'Hello', children: None, {'class': 'my-paragraph'})"
        )
        self.assertEqual(repr(node), expected_repr)

        node_no_props = HTMLNode("div", "Content")
        expected_repr_no_props = "HTMLNode('div', 'Content', children: None, None)"
        self.assertEqual(repr(node_no_props), expected_repr_no_props)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leaf_to_html_no_props(self):
        node = LeafNode("span", "Simple span")
        self.assertEqual(node.to_html(), "<span>Simple span</span>")

    def test_leaf_value_required(self):
        with self.assertRaisesRegex(ValueError, "LeafNode requires a value"):
            LeafNode("p", None)

    def test_repr_method(self):
        node = LeafNode("a", "Link", {"href": "#"})
        expected_repr = "HTMLNode('a', 'Link', children: None, {'href': '#'})"
        self.assertEqual(repr(node), expected_repr)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode(None, "Nested text with "), LeafNode("b", "bold part")],
                ),
                LeafNode("span", "Sibling span"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>Nested text with <b>bold part</b></p><span>Sibling span</span></div>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div", [LeafNode("span", "child")], {"class": "container", "id": "main"}
        )
        html_output = node.to_html()
        self.assertTrue(html_output.startswith("<div"))
        self.assertTrue(html_output.endswith("><span>child</span></div>"))
        self.assertIn(' class="container"', html_output)
        self.assertIn(' id="main"', html_output)

    def test_to_html_no_children_empty_list(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_constructor_errors(self):
        with self.assertRaisesRegex(ValueError, "ParentNode requires a tag"):
            ParentNode(None, [LeafNode("p", "text")])

        with self.assertRaisesRegex(
            ValueError, "ParentNode requires a list of children"
        ):
            ParentNode("div", None)

    def test_repr_method(self):
        child = LeafNode("b", "Bold")
        node = ParentNode("p", [child], {"class": "text"})
        expected_child_repr = "HTMLNode('b', 'Bold', children: None, None)"
        expected_repr = f"HTMLNode('p', None, children: [{expected_child_repr}], {{'class': 'text'}})"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
