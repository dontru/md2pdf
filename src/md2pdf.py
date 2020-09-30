from optparse import OptionParser
import re

from reportlab.lib.styles import StyleSheet1, ParagraphStyle, ListStyle
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate

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
        pass

    document.build(flowables)


def line2token(line):
    for token_type, pattern in MATCHES:
        search = re.search(pattern, line)
        if search:
            return token_type, search.group(1)
    else:
        raise


if __name__ == '__main__':
    main()
