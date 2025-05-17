from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont
import textwrap
import logging

from litkitchen_server.domain.models import PrintJobStatus


class ReceiptPrinterService:
    def __init__(self):
        self.status = PrintJobStatus.ready
        self.vendor_id = 0x04B8
        self.product_id = 0x0202
        self.font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
        self.font_size = 28
        self.chars_per_line = 13
        self.line_height = 36
        self.img_width = 384

    def print_text(self, text: str) -> bool:
        try:
            self.status = PrintJobStatus.printing
            font = ImageFont.truetype(self.font_path, self.font_size)
            wrapped_lines = textwrap.wrap(text, width=self.chars_per_line)
            img_height = self.line_height * len(wrapped_lines)
            img = Image.new("L", (self.img_width, img_height), color=255)
            draw = ImageDraw.Draw(img)
            for i, line in enumerate(wrapped_lines):
                draw.text((10, i * self.line_height), line, font=font, fill=0)
            p = Usb(self.vendor_id, self.product_id, 0)
            p.image(img)
            p.cut()
            self.status = PrintJobStatus.ready
            return True
        except Exception as e:
            logging.error(f"Printer error: {e}")
            # TODO: 根據例外訊息可進一步細分狀態
            if "out of paper" in str(e).lower():
                self.status = PrintJobStatus.out_of_paper
            else:
                self.status = PrintJobStatus.error
            return False

    def get_status(self) -> str:
        return self.status.value


printer = ReceiptPrinterService()
