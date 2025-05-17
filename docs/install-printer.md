# Epson TM-T88VI 熱感應收據列印整合（Raspberry Pi）

本文件說明如何於 Raspberry Pi 上整合 Epson TM-T88VI 熱感應收據印表機，實現繁體中文收據列印，並提供安裝、設定、程式範例。



## 🖨️ 硬體設備資訊

| 項目           | 規格                       |
|----------------|----------------------------|
| 印表機型號     | Epson TM-T88VI             |
| 連接方式       | USB type-B interface         |
| Vendor ID      | 0x04b8                     |
| Product ID     | 0x0202                     |
| 作業系統       | Raspberry Pi OS / Debian   |


## 系統安裝步驟

### 安裝系統套件

```bash
sudo apt update
sudo apt install \
    fonts-noto-cjk \
    imagemagick \
    libusb-1.0-0-dev \
    cups
```

### 專案需要安裝的 Python 套件

```bash
poetry add python-escpos pillow pyusb
```

### 設定 USB 權限（udev 規則）

建立權限規則讓非 root 使用者能列印：

```bash
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0202", MODE="0666", GROUP="plugdev"' \
  | sudo tee /etc/udev/rules.d/99-escpos.rules > /dev/null
sudo udevadm control --reload
sudo udevadm trigger
# 重新啟動 Raspberry Pi
sudo reboot
```

## 中文收據列印範例

以下為將中文轉為圖片再列印的 Python 範例：

```python
from escpos.printer import Usb
import textwrap
from PIL import Image, ImageDraw, ImageFont

# 1. 設定中文字體（使用系統 Noto Sans）
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
font = ImageFont.truetype(font_path, 28)

# 2. 建立影像並寫入中文
text = '''
她出生在雨夜，母親是個不受寵的妾，屋外是黃泥巴的院子，屋內是閨秀的香氛混著煤油燈的焦味。當她第一聲啼哭落下時，整個宅子裡的老鼠都停止了咀嚼。產婆說她的左眼有一層銀灰的薄膜，像是沒剝乾淨的鴿子蛋。

她長大以後，人們說她是個「不乾淨的女孩」，不是因為她做了什麼，只因為她從來不看人正眼。她說她看得見另一個世界。人間不過是一口翻蓋的銅鍋，鍋蓋底下是另一城，裡頭的太陽是死的，夜晚卻像活的。

她十六歲那年，嫁給了一個遠房堂哥。新郎是個好人，只是心思太正經，看不見她眼裡那些浮來浮去的影子。她穿一件紅緞子的鳳仙裝，手指尖一抖，便能從袖子裡放出一隻金色的蟬來，在花廳裡繞三圈，最後停在香案上，吐出一縷白煙，像她的叛逆心思，也像她未出口的話。

「我不是你的人，」她在洞房裡說，語氣比床幔還輕，「我是那鍋底的城裡逃出來的。」

新郎以為她發燒胡言。她卻笑得溫婉，手指輕抹他的眉骨，那一瞬間，他彷彿看見自己眉心開了一隻眼，望見那鍋底世界的倒影——飛鳥倒著飛，水從地上流上天。

她走的時候沒有聲音。只留下一雙繡著錦鯉的鞋，和一本無字的簿冊。那本書，他日復一日翻閱，書頁空空如也，只有他在眼淚滴落之後，看見書頁裡寫著她的名字，像是銀針繡成的，針口還亮著一絲絲光。
'''
# 每行能放幾個中文字？
chars_per_line = 13
wrapped_lines = textwrap.wrap(text, width=chars_per_line)
line_height = 36
img_height = line_height * len(wrapped_lines)

# 建立圖片
img = Image.new('L', (384, img_height), color=255)
draw = ImageDraw.Draw(img)

for i, line in enumerate(wrapped_lines):
    draw.text((10, i * line_height), line, font=font, fill=0)

# 3. 初始化印表機
p = Usb(0x04b8, 0x0202, 0)  # Epson TM-T88VI
p.image(img)
p.cut()
```

## USB 連線驗證

確認 USB 是否正確連接：

```bash
lsusb

# Bus 001 Device 002: ID 04b8:0202 Seiko Epson Corp. Interface Card UB-U05 for Thermal Receipt Printers [M129C/TM-T70/TM-T88IV]
# Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

## 備用方案：CUPS 列印 PNG 測試圖

若需直接列印圖片，可使用 CUPS 官方驅動：

```bash
convert -size 384x80 xc:white -gravity center -pointsize 24 -annotate 0 "Hello TM-T88VI!" hello.png
lpr -o PageSize=RP80x200 -P TM-T88VI hello.png
```
> 須先安裝 Epson 官方 raster 驅動並註冊佇列。

## 技術決策總結

| 列印方式             | 優點                        | 適合場景         |
|----------------------|-----------------------------|------------------|
| CUPS raster          | 可列印 PNG、PDF、報表等     | 圖像輸出需求高者 |
| ESC/POS raw + image  | 控制靈活、支援中文、直接切紙 | 收據、POS 自動列印 |


## TODO

- 整合 webhook，將接收到的訂單自動列印
- 封裝為 infra service
- infra service 需要提供系統層級的狀態查詢
- 排版套件：自動加入時間戳、店名、總計欄位
