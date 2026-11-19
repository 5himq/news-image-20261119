import os
import datetime
import textwrap
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
BG_COLOR = (0, 0, 128)
TEXT_COLOR = (255, 255, 255)
PANEL_COLOR = (255, 255, 255)
PANEL_RADIUS = 25
PADDING = 20

# Load font
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_big = ImageFont.truetype(font_path, 60)
font_small = ImageFont.truetype(font_path, 36)
font_headline = ImageFont.truetype(font_path, 48)
font_region = ImageFont.truetype(font_path, 28)

# Headlines data
headlines = [
    ("H1 China — TRUMP, XI, PUTIN HOLD TRILATERAL SUMMIT — First‑ever three‑way meeting in Shenzhen; nuclear arms and the Ukraine war on the table.", "China"),
    ("H2 Netherlands — WORLD COURT RULES ON ROHINGYA GENOCIDE — ICJ judgment in Gambia's case against Myanmar over the Rohingya.", "Netherlands"),
    ("H3 Saudi Arabia — RIYADH SKYSCRAPER DAMAGED IN HOUTHI ATTACK — Tower housing the sovereign wealth fund hit amid new reported attacks.", "Saudi Arabia"),
    ("H4 Bangladesh — EX‑LEADER YUNUS'S FAMILY HOME TORCHED — Unrest and protests spread; security forces deployed across districts.", "Bangladesh"),
    ("H5 Strait of Hormuz — THREE OIL TANKERS BURN AFTER MINE STRIKES — Iran says tankers hit mines east of the strait.", "Strait of Hormuz"),
    ("H6 World — MUSLIMS PROJECTED LARGEST FAITH BY 2035 — Pew Research: Islam's population to overtake Christianity's.", "World"),
]

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Top band
draw.text((PADDING, PADDING), "WORLD NEWS", font=font_big, fill=TEXT_COLOR)
now = datetime.datetime.now()
date_str = now.strftime("%A, %d %B %Y")
# compute height of world news
world_news_height = font_big.getbbox("WORLD NEWS")[3] - font_big.getbbox("WORLD NEWS")[1]
draw.text((PADDING, PADDING + world_news_height + 10), date_str, font=font_small, fill=TEXT_COLOR)
# panel layout
panel_width = (WIDTH - 3 * PADDING) // 2
# estimate panel height
panel_height = (HEIGHT - 3 * PADDING - world_news_height - (font_small.getbbox(date_str)[3] - font_small.getbbox(date_str)[1]) - 20) // 3
x_offset = PADDING
# y_offset after top band
date_height = font_small.getbbox(date_str)[3] - font_small.getbbox(date_str)[1]
y_offset = PADDING + world_news_height + date_height + 30

for idx, (headline, region) in enumerate(headlines):
    col = idx % 2
    row = idx // 2
    x = x_offset + col * (panel_width + PADDING)
    y = y_offset + row * (panel_height + PADDING)
    # panel
    draw.rounded_rectangle([x, y, x + panel_width, y + panel_height], radius=PANEL_RADIUS, fill=PANEL_COLOR)
    # pictogram: circle + line
    pc_x = x + panel_width // 4
    pc_y = y + panel_height // 3
    draw.ellipse([pc_x - 15, pc_y - 15, pc_x + 15, pc_y + 15], fill=(200, 0, 0))
    draw.line([pc_x, pc_y + 15, pc_x + 20, pc_y + 35], fill=(200, 0, 0), width=3)
    # region title
    region_size = draw.textbbox((0,0), region, font=font_region)[2:]
    draw.text((x + 10, y + 10), region, font=font_region, fill=(0, 0, 0))
    # headline wrapped
    wrapped = textwrap.fill(headline, width=35)
    lines = wrapped.splitlines()
    text_y = y + 10 + region_size[1] + 5
    for line in lines:
        draw.text((x + 10, text_y), line, font=font_headline, fill=(0, 0, 0))
        text_y += font_headline.getbbox(line)[3] - font_headline.getbbox(line)[1] + 4

# save
out_path = os.path.join(os.getcwd(), "entry.png")
img.save(out_path)
# print size and dimensions
size_bytes = os.path.getsize(out_path)
print(f"Saved {out_path}: {size_bytes} bytes, {img.size}")
