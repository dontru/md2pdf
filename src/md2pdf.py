from optparse import OptionParser

from reportlab.platypus import SimpleDocTemplate

parser = OptionParser()
parser.add_option("-t", "--title")
(options, args) = parser.parse_args()

FILENAME = args[0]
TITLE = options.title

document = SimpleDocTemplate(FILENAME + ".pdf", title=TITLE)
flowables = []

with open(FILENAME) as f:
    pass

document.build(flowables)
