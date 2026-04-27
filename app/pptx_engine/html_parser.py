import html.parser
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from app.pptx_engine.themes import Theme, rgb

class PPTXHTMLParser(html.parser.HTMLParser):
    def __init__(self, slide, theme: Theme):
        super().__init__()
        self.slide = slide
        self.theme = theme
        self.current_tag = None
        self.current_y = 1.0 # start at 1 inch from top
        self.margin_left = 1.0
        self.width = 11.33
        
        # Add background
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(theme.colors.bg_dark)
        shape.line.fill.background()

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return

        if self.current_tag in ['h1', 'h2']:
            self._add_text(text, self.theme.fonts.heading, 44, self.theme.colors.text_light, True)
            self.current_y += 1.2
        elif self.current_tag == 'h3':
            self._add_text(text, self.theme.fonts.heading, 32, self.theme.colors.accent, True)
            self.current_y += 0.8
        elif self.current_tag == 'p':
            self._add_text(text, self.theme.fonts.body, 20, self.theme.colors.text_light, False)
            self.current_y += 1.0
        elif self.current_tag == 'li':
            self._add_text(f"• {text}", self.theme.fonts.body, 18, self.theme.colors.text_light, False, margin_left=1.5)
            self.current_y += 0.6

    def _add_text(self, text, font_name, font_size, color, bold, margin_left=None):
        left = Inches(margin_left if margin_left else self.margin_left)
        top = Inches(self.current_y)
        width = Inches(self.width)
        height = Inches(1.0)
        
        txBox = self.slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = font_name
        p.font.size = Pt(font_size)
        p.font.color.rgb = rgb(color)
        p.font.bold = bold


def parse_html_to_slide(slide, html_str: str, theme: Theme):
    parser = PPTXHTMLParser(slide, theme)
    parser.feed(html_str)
