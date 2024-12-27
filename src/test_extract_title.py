import unittest
from extract_title import extract_title

# class TestExtractTitle(unittest.TestCase):
#     def test_extract_title_with_title(self):
#         markdown = "# This is a title\nThis is some content."
#         self.assertEqual(extract_title(markdown), "This is a title")

#     def test_extract_title_with_no_title(self):
#         markdown = "This is some content without a title."
#         self.assertEqual(extract_title(markdown), "")

#     def test_extract_title_with_multiple_titles(self):
#         markdown = "# First title\nSome content\n# Second title"
#         self.assertEqual(extract_title(markdown), "First title")

#     def test_extract_title_with_whitespace(self):
#         markdown = "#    Title with leading whitespace\nSome content"
#         self.assertEqual(extract_title(markdown), "Title with leading whitespace")

#     def test_extract_title_with_empty_string(self):
#         markdown = ""
#         self.assertEqual(extract_title(markdown), "")

#     def test_extract_title_with_no_hash(self):
#         markdown = "This is a line without a hash\n# This is a title"
#         self.assertEqual(extract_title(markdown), "This is a title")

# if __name__ == "__main__":
#     unittest.main()
class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

* and
* a
* list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass


if __name__ == "__main__":
    unittest.main()