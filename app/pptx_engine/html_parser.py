import html.parser
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from app.pptx_engine.themes import Theme, rgb

class PPTXHTMLParser(html.parser.HTMLParser):
    def __init__(self, slide, theme: Theme, is_title_slide: bool = False):
        super().__init__()
        self.slide = slide
        self.theme = theme
        self.is_title_slide = is_title_slide
        self.current_tag = None
        
        # Slide Dimensions
        self.slide_width = Inches(13.33)
        self.slide_height = Inches(7.5)
        
        # Add background
        shape = slide.shapes.add_shape(1, Inches(0), Inches(0), self.slide_width, self.slide_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(theme.colors.bg_dark)
        shape.line.fill.background()

        # Create a single robust text frame for the entire slide content
        # This prevents overlapping because paragraphs will naturally flow one after another
        margin_x = Inches(1.0)
        
        if self.is_title_slide:
            # Center title slide content vertically
            top = Inches(2.5)
            height = Inches(3.0)
        else:
            top = Inches(0.8)
            height = Inches(6.0)
            
        self.txBox = self.slide.shapes.add_textbox(
            margin_x, top, self.slide_width - (2 * margin_x), height
        )
        self.tf = self.txBox.text_frame
        self.tf.word_wrap = True
        
        if self.is_title_slide:
            self.tf.vertical_anchor = 1 # Top anchor for consistent starting point, but we'll center text

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return

        if self.current_tag == 'h1':
            # Main Slide Title
            p = self._get_new_paragraph()
            p.text = text
            p.font.name = self.theme.fonts.heading
            p.font.size = Pt(60 if self.is_title_slide else 44)
            p.font.color.rgb = rgb(self.theme.colors.text_light)
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER if self.is_title_slide else PP_ALIGN.LEFT
            p.space_after = Pt(20)
            
        elif self.current_tag == 'h2':
            # Subtitle or Tagline
            p = self._get_new_paragraph()
            p.text = text
            p.font.name = self.theme.fonts.heading
            p.font.size = Pt(32 if self.is_title_slide else 28)
            p.font.color.rgb = rgb(self.theme.colors.accent)
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER if self.is_title_slide else PP_ALIGN.LEFT
            p.space_after = Pt(15)
            
        elif self.current_tag == 'h3':
            p = self._get_new_paragraph()
            p.text = text
            p.font.name = self.theme.fonts.heading
            p.font.size = Pt(24)
            p.font.color.rgb = rgb(self.theme.colors.text_light)
            p.font.bold = True
            p.space_before = Pt(10)
            p.space_after = Pt(5)
            
        elif self.current_tag == 'p':
            p = self._get_new_paragraph()
            p.text = text
            p.font.name = self.theme.fonts.body
            p.font.size = Pt(18)
            p.font.color.rgb = rgb(self.theme.colors.text_light)
            p.space_before = Pt(10)
            p.alignment = PP_ALIGN.CENTER if self.is_title_slide else PP_ALIGN.LEFT
            
        elif self.current_tag == 'li':
            p = self._get_new_paragraph()
            p.text = f"• {text}"
            p.font.name = self.theme.fonts.body
            p.font.size = Pt(18)
            p.font.color.rgb = rgb(self.theme.colors.text_light)
            p.level = 0
            p.space_before = Pt(5)

    def _get_new_paragraph(self):
        # Use the first empty paragraph if it exists, otherwise add a new one
        if len(self.tf.paragraphs) == 1 and not self.tf.paragraphs[0].text:
            return self.tf.paragraphs[0]
        return self.tf.add_paragraph()

def parse_html_to_slide(slide, html_str: str, theme: Theme, is_title_slide: bool = False):
    parser = PPTXHTMLParser(slide, theme, is_title_slide)
    parser.feed(html_str)
