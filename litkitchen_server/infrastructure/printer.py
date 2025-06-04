import os
from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont
import textwrap
import logging

from litkitchen_server.domain.models import PrintJobStatus


import queue
import threading
import time
from functools import lru_cache

from litkitchen_server.settings import REPO_ROOT

from dataclasses import dataclass


@dataclass
class PrintJobParams:
    result_text: str
    option_a_label: str
    option_b_label: str
    option_c_label: str


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
        self.img_width = 498
        self.header_image_path = os.path.join(REPO_ROOT, "header.png")
        self.footer_image_path = os.path.join(REPO_ROOT, "footer.png")

    def print_text(self, params: PrintJobParams) -> bool:
        p = Usb(self.vendor_id, self.product_id, 0)
        try:
            self.status = PrintJobStatus.printing
            font = ImageFont.truetype(self.font_path, self.font_size)

            # 產生 options_text_img
            options_text = "\n".join(
                [
                    "—" * 20,
                    "・主食材區・",
                    params.option_a_label,
                    f"・配菜區・{params.option_b_label}",
                    f"・飲品區・{params.option_c_label}",
                    "—" * 20,
                ]
            )
            options_lines = options_text.split("\n")
            options_img_height = self.line_height * len(options_lines)
            options_img = Image.new(
                "L", (self.img_width, options_img_height), color=255
            )
            options_draw = ImageDraw.Draw(options_img)
            for i, line in enumerate(options_lines):
                bbox = options_draw.textbbox((0, 0), line, font=font)
                w = bbox[2] - bbox[0]
                x = (self.img_width - w) // 2
                options_draw.text((x, i * self.line_height), line, font=font, fill=0)

            # 列印 header 圖片
            try:
                header_img = Image.open(self.header_image_path)
                p.image(header_img, center=True)
            except Exception as e:
                logging.warning(f"Header image error: {e}")

            # 列印 options_text_img
            p.image(options_img)

            # 列印文字圖片
            wrapped_lines = textwrap.wrap(params.result_text, width=self.chars_per_line)
            img_height = self.line_height * len(wrapped_lines)
            img = Image.new("L", (self.img_width, img_height), color=255)
            draw = ImageDraw.Draw(img)
            w_list = []
            bbox_list = []
            for i, line in enumerate(wrapped_lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                w = bbox[2] - bbox[0]
                w_list.append(w)
                bbox_list.append(bbox)

            # img 水平置中
            max_w = max(w_list)
            for i, bbox in enumerate(bbox_list):
                x = (self.img_width - max_w) // 2
                draw.text(
                    (x, i * self.line_height), wrapped_lines[i], font=font, fill=0
                )

            p.image(img)

            # 這裡希望多一點空白大約 20px
            p.text("\n")

            # 列印 footer 圖片
            try:
                footer_img = Image.open(self.footer_image_path)
                p.image(footer_img, center=True)
            except Exception as e:
                logging.warning(f"Footer image error: {e}")

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
        finally:
            try:
                p.close()
            except Exception as e:
                logging.warning(f"Printer close error: {e}")


class PrinterWorker:
    """
    負責印表機任務 queue 與背景 worker。
    外部只需呼叫 submit_print(text) 送列印任務，狀態查詢用 get_status。
    """

    _queue = queue.Queue(maxsize=1)

    def __init__(self, printer: ReceiptPrinterService):
        self.printer = printer
        threading.Thread(target=self._worker, daemon=True).start()

    def submit_print(self, params: PrintJobParams) -> bool:
        try:
            self._queue.put(params, block=False)
            return True
        except queue.Full:
            logging.warning("Printer queue is full. Rejecting new print job.")
            return False

    def _worker(self):
        while True:
            params = self._queue.get()
            try:
                self.printer.print_text(params)
            finally:
                self._queue.task_done()
                time.sleep(0.1)

    def get_status(self) -> PrintJobStatus:
        return self.printer.status


@lru_cache()
def get_printer_worker() -> PrinterWorker:
    return PrinterWorker(printer=ReceiptPrinterService())


printer_worker = get_printer_worker()
