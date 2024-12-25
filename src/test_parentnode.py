import unittest

from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_parent_node_with_single_child(self):
        leaf = LeafNode(value="This is a paragraph.", tag="p")
        parent = ParentNode(tag="div", children=[leaf])
        expected_html = "<div><p>This is a paragraph.</p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_multiple_children(self):
        leaf1 = LeafNode(value="First paragraph.", tag="p")
        leaf2 = LeafNode(value="Second paragraph.", tag="p")
        parent = ParentNode(tag="div", children=[leaf1, leaf2])
        expected_html = "<div><p>First paragraph.</p><p>Second paragraph.</p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_no_children(self):
        parent = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Parent node must have children nodes")

    def test_parent_node_with_props(self):
        leaf = LeafNode(value="This is a paragraph.", tag="p")
        parent = ParentNode(tag="div", children=[leaf], props={"class": "container", "id": "main"})
        expected_html = '<div class="container" id="main"><p>This is a paragraph.</p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_nested_parent_nodes(self):
        inner_leaf = LeafNode(value="Nested paragraph.", tag="p")
        inner_parent = ParentNode(tag="section", children=[inner_leaf])
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        expected_html = "<div><section><p>Nested paragraph.</p></section></div>"
        self.assertEqual(outer_parent.to_html(), expected_html)

    def test_parent_node_with_missing_tag(self):
        leaf = LeafNode(value="This is a paragraph.", tag="p")
        parent = ParentNode(tag=None, children=[leaf])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Parent node should have tags")

    def test_parent_node_with_leaf_with_props(self):
        leaf = LeafNode(value="Click here", tag="a", props={"href": "https://example.com"})
        parent = ParentNode(tag="div", children=[leaf])
        expected_html = '<div><a href="https://example.com">Click here</a></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_leaf_without_tag(self):
        leaf = LeafNode(value="Raw text", tag=None)
        parent = ParentNode(tag="div", children=[leaf])
        expected_html = "<div>Raw text</div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_empty_parent_node(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(tag="div", children=None).to_html()
        self.assertEqual(str(context.exception), "Parent node must have children nodes")

    def test_nested_parent_with_props(self):
        leaf = LeafNode(value="Nested content", tag="span")
        inner_parent = ParentNode(tag="section", children=[leaf], props={"class": "inner"})
        outer_parent = ParentNode(tag="div", children=[inner_parent], props={"class": "outer"})
        expected_html = '<div class="outer"><section class="inner"><span>Nested content</span></section></div>'
        self.assertEqual(outer_parent.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()