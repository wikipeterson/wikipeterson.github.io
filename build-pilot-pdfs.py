"""Update the recipe PDFs and rebuild cookbook collections from recipe PDFs."""
from pathlib import Path
from io import BytesIO
from html import escape
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).parent
RECIPES = json.loads((ROOT / 'recipes/recipes.json').read_text())
COLORS = {'a': '#657344', 'b': '#a0503b', 'c': '#886522', 'd': '#526b7a', 'separate': '#35413b'}
FORMATS = {'kindle': ((446.4, 595.44), 12), 'paperwhite': ((303.12, 403.2), 11), 'letter': ((612, 792), 11)}

def clean(text):
    import re
    fractions = {'¼':'1/4','½':'1/2','¾':'3/4','⅓':'1/3','⅔':'2/3','⅛':'1/8','⅜':'3/8','⅝':'5/8','⅞':'7/8','⅙':'1/6','⅚':'5/6'}
    text = re.sub(r'(\d)([¼½¾⅓⅔⅛⅜⅝⅞⅙⅚])', r'\1 \2', text)
    for glyph, plain in fractions.items(): text = text.replace(glyph, plain)
    return escape(text.replace('⁄','/').replace('×','x').replace('–', '-').replace('—', '-').replace('↗', '').replace('’', "'"))

def styles(size):
    return {
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=size, leading=size*1.3, spaceAfter=5),
        'small': ParagraphStyle('small', fontName='Helvetica', fontSize=size-2, leading=size*1.2, spaceAfter=7),
        'title': ParagraphStyle('title', fontName='Times-Roman', fontSize=size*2.2, leading=size*2.4, spaceAfter=12),
        'heading': ParagraphStyle('heading', fontName='Times-Roman', fontSize=size*1.5, leading=size*1.7, spaceBefore=10, spaceAfter=7, keepWithNext=True),
    }

def footer(canvas, doc):
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(HexColor('#68726b'))
    canvas.drawString(doc.leftMargin, 15, 'WIKIPETERSON / RECIPES')
    canvas.drawRightString(doc.pagesize[0]-doc.rightMargin, 15, str(doc.page))

def build_recipe(recipe, fmt, page, size):
    dest = ROOT / 'recipes/pdf' / fmt / (recipe['id']+'.pdf')
    doc = SimpleDocTemplate(str(dest), pagesize=page, rightMargin=25, leftMargin=25,
                            topMargin=28, bottomMargin=30, title=recipe['title'], author='Wikipeterson')
    st = styles(size)
    p = lambda text, style='body': Paragraph(clean(text), st[style])
    flow = [p(recipe['title'], 'title'), p(recipe['category']+' | '+recipe['method'], 'small'),
            p('Before you start', 'heading'), p(recipe['overview']), p('Ingredients', 'heading'),
            p('Matching letters and colors = one prep bowl. Charcoal = keep separate.' if recipe['prepGroups'] else 'Keep these ingredients separate; follow the order in the directions.', 'small')]
    for group, name in recipe['prepGroups'].items():
        flow.append(p('Bowl '+group.upper()+' - '+name, 'small'))
    for ingredient in recipe['ingredients']:
        if ingredient['heading']:
            flow.append(p(ingredient['text'], 'heading')); continue
        if ingredient.get('informational'):
            flow.append(p(ingredient['text'], 'small')); continue
        group = ingredient['prepGroup']; color = COLORS[group]
        # A vector checkbox avoids font-dependent square glyphs, and letters survive grayscale printing.
        from reportlab.graphics.shapes import Drawing, Rect
        box = Drawing(13, 16); box.add(Rect(1, 3, 10, 10, strokeColor=HexColor(color), strokeWidth=1.5, fillColor=None))
        suffix = '  [Bowl '+group.upper()+']' if group!='separate' else ''
        table = Table([[box, p(ingredient['text']+suffix)]], colWidths=[19, page[0]-69])
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
                                   ('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        flow.append(table)
    stage_blocks = []
    for i, stage in enumerate(recipe['stages'],1):
        block = [p(str(i)+'. '+stage['title'], 'heading')]
        for j, step in enumerate(stage['steps'],1): block.append(p(str(j)+'. '+step))
        if i == len(recipe['stages']) and recipe['notes']:
            block.append(p('Notes', 'heading'))
            block += [p(n) for n in recipe['notes']]
        stage_blocks.append(block)
    if len(stage_blocks) > 1 and sum(len(item.text) for item in stage_blocks[-1]) < 200:
        stage_blocks[-2].extend(stage_blocks.pop())
    flow.extend(KeepTogether(block) for block in stage_blocks)
    def recipe_footer(canvas, document):
        footer(canvas, document)
        canvas.setFont('Helvetica', 7)
        canvas.drawString(document.leftMargin, 27, 'Original recipe | Google Doc')
        canvas.linkURL(recipe['source'], (document.leftMargin, 25, document.leftMargin+48, 34), relative=0)
        canvas.linkURL(recipe['docUrl'], (document.leftMargin+51, 25, document.leftMargin+95, 34), relative=0)
    doc.build(flow, onFirstPage=recipe_footer, onLaterPages=recipe_footer)

def cookbook(fmt, page, size):
    ordered = sorted(RECIPES, key=lambda r:r['title'].casefold())
    front = BytesIO(); st=styles(size)
    flow = [Paragraph('The Wikipeterson Cookbook',st['title']), Paragraph(f'{len(RECIPES)} recipes to keep.',st['body']),
            Paragraph('Recipe collection updated October 19, 2026',st['small']),
            Paragraph('Contents',st['heading'])]
    for r in ordered:
        flow.append(Paragraph('<link href="#'+r['id']+'">'+clean(r['title'])+'</link>',st['small']))
    # Build the contents with external page links after the final front-matter page count is known.
    # ReportLab cannot resolve destinations in PDFs appended later, so use plain contents text and add links with pypdf.
    plain=[]
    for f in flow:
        if isinstance(f,Paragraph):
            import re
            f=Paragraph(re.sub(r'<link[^>]*>|</link>','',f.text),f.style)
        plain.append(f)
    SimpleDocTemplate(front,pagesize=page,leftMargin=25,rightMargin=25,topMargin=28,bottomMargin=30).build(plain,onFirstPage=footer,onLaterPages=footer)
    front.seek(0); writer=PdfWriter(); writer.append(PdfReader(front))
    starts={}
    for r in ordered:
        starts[r['id']]=len(writer.pages)
        writer.append(str(ROOT/'recipes/pdf'/fmt/(r['id']+'.pdf')),outline_item=r['title'], import_outline=False)
    # Find contents entries by rendered text coordinates and attach native GoTo links.
    import pdfplumber
    front.seek(0)
    with pdfplumber.open(front) as pdf:
        for page_index,pg in enumerate(pdf.pages):
            for r in ordered:
                matches=pg.search(clean(r['title']).replace('&amp;','&'),regex=False)
                for match in matches:
                    if match['top']<100 and page_index==0: continue
                    from pypdf.annotations import Link
                    writer.add_annotation(page_index,Link(rect=(match['x0'],page[1]-match['bottom'],match['x1'],page[1]-match['top']),target_page_index=starts[r['id']]))
    writer.add_metadata({'/Title':'The Wikipeterson Cookbook','/Author':'Wikipeterson'})
    with open(ROOT/'recipes/pdf'/fmt/'wikipeterson-cookbook.pdf','wb') as out: writer.write(out)

if __name__ == '__main__':
    for fmt,(page,size) in FORMATS.items():
        for r in RECIPES:
            if 'prepGroups' in r: build_recipe(r,fmt,page,size)
        cookbook(fmt,page,size)
        print('Updated',fmt)
