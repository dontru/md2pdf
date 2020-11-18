from optparse import OptionParser
import re

from reportlab.lib.styles import StyleSheet1, ParagraphStyle, ListStyle
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, ListFlowable, PageBreak, Paragraph

parser = OptionParser()
parser.add_option("-t", "--title")
(options, args) = parser.parse_args()

FILENAME = args[0]
TITLE = options.title

registerFont(TTFont("DejaVuSans", "fonts/DejaVuSans.ttf"))
registerFont(TTFont("DejaVuSans-Bold", "fonts/DejaVuSans-Bold.ttf"))
registerFont(TTFont("DejaVuSans-Oblique", "fonts/DejaVuSans-Oblique.ttf"))
registerFont(TTFont("DejaVuSans-BoldOblique", "fonts/DejaVuSans-BoldOblique.ttf"))
registerFontFamily("", "DejaVuSans", "DejaVuSans-Bold", "DejaVuSans-Oblique", "DejaVuSans-BoldOblique")

FONT_NAME = "DejaVuSans"
FONT_SIZE = 12
BORDER_COLOR = "#bbbbbb"

styles = StyleSheet1()
styles.add(ParagraphStyle("std", fontName=FONT_NAME, fontSize=FONT_SIZE))
styles.add(ParagraphStyle("h3", fontName=f"{FONT_NAME}-Bold", fontSize=14))
styles.add(ListStyle(
    "list", fontName=FONT_NAME, fontSize=FONT_SIZE,
    bulletType="bullet", bulletFontName=FONT_NAME, bulletFontSize=FONT_SIZE,
))
table_style_base = [
    ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
    ('FONTSIZE', (0, 0), (-1, -1), FONT_SIZE),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.1, BORDER_COLOR)
]

T_LIST = "list"
T_LIST_ITEM = "list_item"
T_TABLE = "table"
T_TABLE_ROW = "table_row"
T_PAGE_BREAK = "page_break"
T_H3 = "h3"
T_PARAGRAPH = "paragraph"

MATCHES = [
    (T_LIST_ITEM, re.compile("^- (.*)$")),
    (T_TABLE_ROW, re.compile("(^\\|(.*)\\|)$")),
    (T_PAGE_BREAK, re.compile("^<!-- (PAGE_BREAK) -->$")),
    (T_H3, re.compile("^### (.+)$")),
    (T_PARAGRAPH, re.compile("^(.*)$")),
]

TABLE_MATCHES = [
    ("LEFT", re.compile("^:?-+$")),
    ("CENTER", re.compile("^:-+:$")),
    ("RIGHT", re.compile("^-+:$")),
]


def main():
    document = SimpleDocTemplate(FILENAME + ".pdf", title=TITLE)
    flowables = []

    with open(FILENAME) as f:
        read_data = f.read()
    tokens = text2tokens(read_data)

    flowables = [token2flowable(token) for token in tokens]
    flowables = [f for f in flowables if f is not None]
    document.build(flowables)


def text2tokens(text):
    lines = text.strip().splitlines()
    tokens = [line2token(line) for line in lines]
    tokens = group_tokens(tokens, T_TABLE, T_TABLE_ROW)
    tokens = group_tokens(tokens, T_LIST, T_LIST_ITEM)
    return tokens


def line2token(line):
    for token_type, pattern in MATCHES:
        search = re.search(pattern, line)
        if search:
            return token_type, search.group(1)
    else:
        raise


def group_tokens(tokens, key, old_key):
    ranges = get_ranges(tokens, old_key)

    offset = 0
    for a, b in ranges:
        left = tokens[:a-offset]
        center = tokens[a-offset:b+1-offset]
        right = tokens[b+1-offset:]

        tokens = left + [(key, [value for _, value in center])] + right
        offset += b - a

    return tokens


def get_ranges(tokens, token):
    ranges = []
    indices = [i for i, x in enumerate(tokens) if x[0] == token]
    pairs = zip(indices[:-1], indices[1:])

    for a, b in pairs:
        if a == b - 1:
            if len(ranges) == 0:
                ranges.append((a, b))
            else:
                (previous_a, previous_b) = ranges.pop()
                if a == previous_b:
                    ranges.append((previous_a, b))
                else:
                    ranges.append((previous_a, previous_b))
                    ranges.append((a, b))

    return ranges


def token2flowable(token):
    key, value = token

    if key == T_LIST:
        return ListFlowable([paragraph(item) for item in value], style=styles["list"])
    elif key == T_TABLE:
        pass
    elif key == T_PAGE_BREAK:
        return PageBreak()
    elif key == T_H3:
        return paragraph(value, "h3")
    elif key == T_PARAGRAPH or key == T_LIST_ITEM or key == T_TABLE_ROW:
        return paragraph(value)


def paragraph(text, style="std"):
    text = re.sub("__([^_]+)__", r"<b>\1</b>", text)
    text = re.sub("_([^_]+)_", r"<u>\1</u>", text)
    return Paragraph(text, styles[style])


if __name__ == '__main__':
    main()
