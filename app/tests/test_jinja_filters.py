import pytest

from app import (
    clean_tags_and_replace_highlight_tag,
    format_date_iso,
    format_number_with_commas,
    format_opensearch_field_name,
    null_to_dash,
)


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        # input is string "null"
        ("null", "-"),
        # input is None
        (None, "-"),
        # input is an empty string
        ("", ""),
        # input is an integer zero
        (0, 0),
        # input is a string zero
        ("0", "0"),
        # input is a non-zero integer
        (123, 123),
        # input is just a string and not "null"
        ("hello", "hello"),
        # input is a more complex type
        (["null", None], ["null", None]),
        # input is a boolean False
        (False, False),
        # input is a boolean True
        (True, True),
    ],
)
def test_null_to_dash(input_value, expected_output):
    assert null_to_dash(input_value) == expected_output


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        # input with non-test_highlight_key HTML tags
        (
            "<div>Test</div> <span>Text</span>",
            "&lt;div&gt;Test&lt;/div&gt; &lt;span&gt;Text&lt;/span&gt;",
        ),
        # input with ALLOWED <test_highlight_key> tag
        (
            "<test_highlight_key>Highlight</test_highlight_key>",
            "<mark>Highlight</mark>",
        ),
        # mixed tags with <test_highlight_key> and other tags
        (
            "<test_highlight_key>Keep</test_highlight_key> <div>Remove</div>",
            "<mark>Keep</mark> &lt;div&gt;Remove&lt;/div&gt;",
        ),
        # nested tags including <test_highlight_key>
        (
            "<div><test_highlight_key>Inside</test_highlight_key> Div</div>",
            "&lt;div&gt;<mark>Inside</mark> Div&lt;/div&gt;",
        ),
        # self-closing tag (e.g., <img>)
        (
            "<img src='image.png'/>Picture",
            "&lt;img src='image.png'/&gt;Picture",
        ),
        # no tags in input
        ("Just plain text", "Just plain text"),
        # tags with attributes
        (
            "<p class='text'>Paragraph</p>",
            "&lt;p class='text'&gt;Paragraph&lt;/p&gt;",
        ),
        # mixed case-sensitive tags (e.g., <test_highlight_key> vs <test_highlight_key>) - tags are not case sensitive
        (
            "<test_highlight_key>Upper</test_highlight_key> <test_highlight_key>Lower</test_highlight_key>",
            "<mark>Upper</mark> <mark>Lower</mark>",
        ),
        # empty tag pairs
        ("<div></div>", "&lt;div&gt;&lt;/div&gt;"),
        # unclosed tag
        ("<span>Open tag", "&lt;span&gt;Open tag"),
        # EXTREMELY IMPORTANT: removed stript tags (even if we have CSP)
        (
            "<script>This is a script tag</script>",
            "&lt;script&gt;This is a script tag&lt;/script&gt;",
        ),
        # EXTREMELY IMPORTANT: self closing script tags
        (
            "<script/>This is a self closing script tag",
            "&lt;script/&gt;This is a self closing script tag",
        ),
        # EXTREMELY IMPORTANT: script tags with attributes
        (
            "<script src='myscript.js'>This is a script tag with attrs</script>",
            "&lt;script src='myscript.js'&gt;This is a script tag with attrs&lt;/script&gt;",
        ),
        # removes onclick attributes from test_highlight_key elements
        (
            "<test_highlight_key onclick='alert('XSS')'>Should remove onclick</test_highlight_key>",
            "<mark>Should remove onclick</mark>",
        ),
    ],
)
def test_clean_tags(input_text, expected_output):
    assert (
        clean_tags_and_replace_highlight_tag(input_text, "test_highlight_key")
        == expected_output
    )


@pytest.mark.parametrize(
    "field, expected",
    [
        # fields directly mapped
        ("file_name", "File name"),
        ("description", "Description"),
        ("transferring_body", "Transferring body"),
        ("foi_exemption_code", "FOI code"),
        ("content", "Content"),
        ("closure_start_date", "Closure start date"),
        ("end_date", "Record date"),
        ("date_last_modified", "Record date"),
        ("citeable_reference", "Citeable reference"),
        ("series_name", "Series name"),
        ("transferring_body_description", "Transferring body description"),
        ("consignment_reference", "Consignment ref"),
    ],
)
def test_format_opensearch_field_name(field, expected):
    assert format_opensearch_field_name(field) == expected


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        (1000, "1,000"),
        (33000, "33,000"),
        (123456789, "123,456,789"),
        (0, "0"),
        (-1000, "-1,000"),
        (-9876543, "-9,876,543"),
        (1000000.50, "1,000,000.5"),
        (99999.999, "99,999.999"),
    ],
)
def test_format_number_with_commas(input_value, expected_output):
    assert format_number_with_commas(input_value) == expected_output


@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        # Valid date
        ("13/03/2025", "2025-03-13"),
        # Leading zeros
        ("01/01/2000", "2000-01-01"),
        # End of year
        ("31/12/1999", "1999-12-31"),
        # Invalid format: wrong order
        ("2025/03/13", "2025/03/13"),
        # Invalid separator
        ("13-03-2025", "13-03-2025"),
        # Completely invalid string
        ("not a date", "not a date"),
        # Empty string
        ("", ""),
        # None input
        (None, None),
        # Integer input
        (12345, 12345),
        # List input
        (["13/03/2025"], ["13/03/2025"]),
    ],
)
def test_format_date_iso(input_value, expected_output):
    assert format_date_iso(input_value) == expected_output
