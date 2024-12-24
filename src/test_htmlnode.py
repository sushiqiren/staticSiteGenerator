import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        """Test props_to_html when no props are set."""
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        """Test props_to_html with multiple properties."""
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://example.com", "class": "btn"})
        expected = ' href="https://example.com" class="btn"'
        self.assertEqual(node.props_to_html(), expected)

    # def test_repr_method(self):
    #     """Test the __repr__ method for an HTMLNode."""
    #     node = HTMLNode(tag="div", value="Test", props={"id": "test-id"}, children=[
    #         HTMLNode(tag="span", value="Child")
    #     ])
    #     expected = (
    #         "HTMLNode(tag='div', value='Test', children=[HTMLNode(tag='span', value='Child', children=[], props={})], props={'id': 'test-id'})"
    #     )
    #     self.assertEqual(node.__repr__(), expected)
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()