from optparse import OptionParser

from reportlab.lib.styles import StyleSheet1, ParagraphStyle
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

styles = StyleSheet1()
styles.add(ParagraphStyle("std", fontName=FONT_NAME, fontSize=FONT_SIZE))

document = SimpleDocTemplate(FILENAME + ".pdf", title=TITLE)
flowables = []

with open(FILENAME) as f:
    pass

document.build(flowables)
