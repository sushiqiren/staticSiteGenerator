import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        # Test when a tag and value are provided
        node = LeafNode(value="This is a paragraph.", tag="p")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_to_html_with_tag_value_and_props(self):
        # Test when a tag, value, and properties are provided
        node = LeafNode(value="Click here", tag="a", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">Click here</a>')

    

    def test_to_html_missing_value(self):
        # Test when the value is None (should raise ValueError)
        with self.assertRaises(ValueError):
            node = LeafNode(value=None, tag="p")
            node.to_html()

    def test_to_html_empty_props(self):
        # Test when props is an empty dictionary
        node = LeafNode(value="No props here", tag="div", props={})
        self.assertEqual(node.to_html(), "<div>No props here</div>")

    def test_to_html_special_characters_in_props(self):
        # Test props with special characters
        node = LeafNode(value="Special props", tag="meta", props={"charset": "UTF-8"})
        self.assertEqual(node.to_html(), '<meta charset="UTF-8">Special props</meta>')

    def test_to_html_with_numeric_value(self):
        # Test when value is numeric
        node = LeafNode(value="12345", tag="span")
        self.assertEqual(node.to_html(), "<span>12345</span>")

    

    def test_repr(self):
        # Test the __repr__ method
        node = LeafNode(value="Example", tag="em", props={"class": "highlight"})
        self.assertEqual(repr(node), "LeafNode(em, Example, {'class': 'highlight'})")


if __name__ == "__main__":
    unittest.main()