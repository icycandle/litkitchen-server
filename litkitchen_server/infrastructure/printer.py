from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont
import textwrap
import logging

from litkitchen_server.domain.models import PrintJobStatus


import queue
import threading
import time
from functools import lru_cache


class ReceiptPrinterService:
    """
    印表機硬體操作服務，僅負責與實體印表機溝通，不處理 queue 或 worker。
    """

    def __init__(self):
        self.status = PrintJobStatus.ready
        self.vendor_id = 0x04B8
        self.product_id = 0x0202
        self.font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
        self.font_size = 28
        self.chars_per_line = 16
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
            self.status = PrintJobStatus.done
            return True
        except Exception as e:
            logging.error(f"Printer error: {e}")
            if "out of paper" in str(e).lower():
                self.status = PrintJobStatus.out_of_paper
            else:
                self.status = PrintJobStatus.error
            return False


class PrinterWorker:
    """
    負責印表機任務 queue 與背景 worker。
    外部只需呼叫 submit_print(text) 送列印任務，狀態查詢用 get_status。
    """

    _queue = queue.Queue(maxsize=1)

    def __init__(self, printer: ReceiptPrinterService):
        self.printer = printer
        threading.Thread(target=self._worker, daemon=True).start()

    def submit_print(self, text: str) -> bool:
        try:
            self._queue.put(text, block=False)
            return True
        except queue.Full:
            logging.warning("Printer queue is full. Rejecting new print job.")
            return False

    def _worker(self):
        while True:
            text = self._queue.get()
            try:
                self.printer.print_text(text)
            finally:
                self._queue.task_done()
                time.sleep(0.1)

    def get_status(self) -> PrintJobStatus:
        return self.printer.status


@lru_cache()
def get_printer_worker() -> PrinterWorker:
    return PrinterWorker(printer=ReceiptPrinterService())


printer_worker = get_printer_worker()
