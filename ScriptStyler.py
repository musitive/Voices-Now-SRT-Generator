from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.shared import OxmlElement,qn
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

LOOP = 0
IN = 1
OUT = 2
ROLE = 3
ENGLISH = 4
TRANSLATION = 5

LOOP_WIDTH = Inches(0.25)
INTIME_WIDTH = Inches(1)
OUTTIME_WIDTH = Inches(1)
ROLE_WIDTH = Inches(1)
ENGLISH_WIDTH = Inches(2.8)
TRANSLATION_WIDTH = Inches(2.8)

def color_cell(cell) -> None:
    shading_elm_1 = parse_xml(r'<w:shd {} w:fill="F6CC9E"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading_elm_1)

def set_repeat_table_header(header_row):
    """ set repeat table row on every new page
    """
    tr = header_row._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), "true")
    trPr.append(tblHeader)
    return header_row

def set_widths(row):
    row.cells[LOOP].width = LOOP_WIDTH
    row.cells[IN].width = INTIME_WIDTH
    row.cells[OUT].width = OUTTIME_WIDTH
    row.cells[ROLE].width = ROLE_WIDTH
    row.cells[ENGLISH].width = ENGLISH_WIDTH
    row.cells[TRANSLATION].width = TRANSLATION_WIDTH

class ScriptStyler:
    def initialize_tables(self) -> None:
        self.remove_metadata()

        self.old_table = self.document.tables[0]
        self.new_table = self.document.add_table(1, 6)
        self.new_table.style = 'Table Grid'
        set_repeat_table_header(self.new_table.rows[0])

        self.initialize_table_headers()

    def __init__(self, document: Document):
        self.document = document

    def remove_table(self, index: int) -> None:
        table = self.document.tables[index]
        table._element.getparent().remove(table._element)

    def remove_metadata(self) -> None:
        self.remove_table(2)
        self.remove_table(0)

    def change_orientation(self) -> None:
        sections = self.document.sections

        for section in sections:
            # change orientation to landscape
            section.orientation = WD_ORIENT.LANDSCAPE

            new_width, new_height = section.page_height, section.page_width
            section.page_width = new_width
            section.page_height = new_height

    def prevent_document_break(self) -> None:
        """
        https://github.com/python-openxml/python-docx/issues/245#event-621236139
        Globally prevent table cells from splitting across pages.
        """
        tags = self.document.element.xpath('//w:tr')
        rows = len(tags)
        for row in range(0, rows):
            tag = tags[row]                     # Specify which <w:r> tag you want
            child = OxmlElement('w:cantSplit')  # Create arbitrary tag
            tag.append(child)                   # Append in the new tag

    def save_as_new_script(self, new_filename) -> None:
        self.document.save(new_filename)

    def set_styles(self) -> None:
        style = self.document.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(11)

    def initialize_table_headers(self) -> None:
        old_row = self.old_table.rows[0]
        new_row = self.new_table.rows[0]

        self.shift_translation(old_row, new_row, "IN", "OUT", bold=True, loop="#")
        for cell in new_row.cells:
            color_cell(cell)

    def add_row_to_new_table(self, translation_index: int, in_time: str, out_time: str) -> None:
        old_row = self.old_table.rows[translation_index]
        new_row = self.new_table.add_row()
        self.shift_translation(old_row, new_row, in_time, out_time, loop=str(translation_index))

    def shift_translation(self, old_row, new_row, in_time: str, out_time: str, bold: bool = False, style: str = 'Normal', loop: str = "") -> None:
        if loop == "":
            loop = old_row.cells[self.old_start].text
        self.update_text(new_row, loop, LOOP, bold, style)
        self.update_text(new_row, in_time, IN, bold, style)
        self.update_text(new_row, out_time, OUT, bold, style)
        
        for i in range(1, len(old_row.cells)-self.old_start):
            contents = old_row.cells[i+self.old_start].text
            self.update_text(new_row, contents, i+2, bold, style)

        set_widths(new_row)
        return

    def update_text(self, new_row, text: str, cell: int, bold: bool = False, style: str = 'Normal'):
        run = new_row.cells[cell].paragraphs[0].add_run(text)
        new_row.cells[cell].paragraphs[0].style = self.document.styles[style]
        run.bold = bold