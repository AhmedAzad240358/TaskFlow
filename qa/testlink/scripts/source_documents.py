"""Render the committed README and code test basis as readable source PDFs.

Requires reportlab (available in the Codex bundled runtime). This is source material,
not a replacement for either TestLink-generated deliverable.
"""
from html import escape
from pathlib import Path
import subprocess
import sys
import textwrap
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import ROOT, SOURCE_COMMIT, REPO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted

OUT = ROOT / 'qa/project1/Source_Documents'
OUT.mkdir(parents=True, exist_ok=True)
font = Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
if font.exists():
    pdfmetrics.registerFont(TTFont('Source', str(font)))
else:
    raise SystemExit('Install a Unicode TrueType font and configure source_documents.py')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='SourceBody',fontName='Source',fontSize=9,leading=13,spaceAfter=7))
styles.add(ParagraphStyle(name='SourceCode',fontName='Source',fontSize=7.5,leading=10))

def committed(path):
    return subprocess.run(['git','show',f'{SOURCE_COMMIT}:{path}'],cwd=ROOT,check=True,capture_output=True,text=True).stdout

def footer(canvas, doc):
    canvas.setFont('Helvetica',8)
    canvas.setFillColor(colors.HexColor('#455568'))
    canvas.drawString(40,26,f'TaskFlow source basis | main@{SOURCE_COMMIT}')
    canvas.drawRightString(A4[0]-40,26,str(doc.page))

def build(name, title, files):
    story=[Paragraph(escape(title),styles['Title']),
           Paragraph(f'SECJ3343 Project 1 - Group TaskFlow. Committed source baseline main@{SOURCE_COMMIT}.',styles['SourceBody']),
           Paragraph(escape(REPO),styles['SourceBody']),
           Paragraph('This is a faithful text snapshot of the named repository files used to derive acceptance requirements. '
                     'Line numbers refer to the committed source. Wrapped continuation lines retain indentation. '
                     'Source behavior is distinguished from independently documented requirements in each member\'s test basis.',styles['SourceBody'])]
    for path in files:
        story += [PageBreak(),Paragraph(escape(path),styles['Heading1'])]
        for number,line in enumerate(committed(path).splitlines(),1):
            # Display Unicode emoji in source as an explicit code-point notation if
            # the selected source font lacks supplementary-plane glyphs.
            line=''.join(c if ord(c)<=65535 else f'[U+{ord(c):X}]' for c in line)
            wrapped=textwrap.wrap(line.expandtabs(4),width=104,replace_whitespace=False,drop_whitespace=False) or ['']
            for i,part in enumerate(wrapped):
                story.append(Preformatted((f'{number:4d}  ' if i==0 else '      ')+part,styles['SourceCode']))
    path=OUT/name
    SimpleDocTemplate(str(path),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=42,bottomMargin=42,
                      title=title,author='Group TaskFlow').build(story,onFirstPage=footer,onLaterPages=footer)
    print(path)

if __name__=='__main__':
    build('TaskFlow_README_Baseline.pdf','TaskFlow documented requirements - README baseline',['README.md'])
    files=subprocess.run(['git','ls-tree','-r','--name-only',SOURCE_COMMIT,'src'],cwd=ROOT,check=True,capture_output=True,text=True).stdout.splitlines()
    files=[p for p in files if p.endswith(('.js','.jsx','.css')) and not p.endswith('.test.js')]
    build('TaskFlow_Code_Baseline.pdf','TaskFlow implementation - code test basis',files)
