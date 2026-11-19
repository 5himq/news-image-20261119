import os
import datetime
from PIL import Image, ImageDraw, ImageFont

# Constants
WIDTH, HEIGHT = 1024, 1024
PADDING = 20
PANEL_RADIUS = 25
SHADOW_OFFSET = 6
ACCENT_HEIGHT = 6
BG_START = (8, 18, 54)
BG_END = (16, 42, 102)
ACCENT_COLOR = (195, 180, 120)
SHADOW_COLOR = (10, 10, 30)

# Fonts
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_big = ImageFont.truetype(font_path, 60)
font_small = ImageFont.truetype(font_path, 36)
font_region = ImageFont.truetype(font_path, 28)

# Headlines data (region, headline, detail)
headlines = [
    ("China", "TRUMP, XI, PUTIN HOLD TRILATERAL SUMMIT", "First three-way summit in Shenzhen; nuclear arms, Ukraine war on the table."),
    ("The Hague", "WORLD COURT FINDS MYANMAR GUILTY OF GENOCIDE", "ICJ judgment in Gambia's case against Myanmar over the Rohingya."),
    ("Saudi Arabia", "RIYADH SKYSCRAPER DAMAGED IN HOUTHI ATTACK", "Tower housing the sovereign wealth fund hit in renewed attacks."),
    ("Bangladesh", "EX-LEADER YUNUS'S FAMILY HOME TORCHED", "Unrest and protests spread; security forces deployed to seven districts."),
    ("Strait of Hormuz", "THREE OIL TANKERS BURN AFTER MINE STRIKES", "Iran says tankers hit mines east of the strait."),
    ("World", "ISLAM PROJECTED AS LARGEST FAITH BY 2035", "Pew Research: Muslim population set to overtake Christians worldwide.")
]

# Helper to wrap text by pixel width

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

# Create image with vertical gradient background
img = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)
for y in range(HEIGHT):
    ratio = y / (HEIGHT - 1)
    r = int(BG_START[0] + ratio * (BG_END[0] - BG_START[0]))
    g = int(BG_START[1] + ratio * (BG_END[1] - BG_START[1]))
    b = int(BG_START[2] + ratio * (BG_END[2] - BG_START[2]))
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Top band
text_color = (255, 255, 255)
world_news_y = PADDING
draw.text((PADDING, world_news_y), "WORLD NEWS", font=font_big, fill=text_color)
now = datetime.datetime.now()
# Fixed literal date
date_str = "Thursday, 19 November 2026"
world_news_height = font_big.getbbox("WORLD NEWS")[3] - font_big.getbbox("WORLD NEWS")[1]
# Gap of 20 pixels
date_y = world_news_y + world_news_height + 20
draw.text((PADDING, date_y), date_str, font=font_small, fill=text_color)

# Panel layout calculations
panel_width = (WIDTH - 3 * PADDING) // 2
panel_height = (HEIGHT - 3 * PADDING - world_news_height - (date_y - world_news_y) - 30) // 3
x_offset = PADDING
panel_x_offsets = [x_offset, x_offset + panel_width + PADDING]

# Start drawing panels
for idx, (region, headline, detail) in enumerate(headlines):
    col = idx % 2
    row = idx // 2
    x = panel_x_offsets[col]
    y = date_y + 30 + row * (panel_height + PADDING)

    # Shadow rectangle
    shadow_rect = [x + SHADOW_OFFSET, y + SHADOW_OFFSET, x + panel_width + SHADOW_OFFSET, y + panel_height + SHADOW_OFFSET]
    draw.rounded_rectangle(shadow_rect, radius=PANEL_RADIUS, fill=SHADOW_COLOR)

    # Card rectangle
    card_rect = [x, y, x + panel_width, y + panel_height]
    draw.rounded_rectangle(card_rect, radius=PANEL_RADIUS, fill=(255, 255, 255))

    # Accent bar inside card
    accent_rect = [x + PADDING, y + PADDING, x + panel_width - PADDING, y + PADDING + ACCENT_HEIGHT]
    draw.rectangle(accent_rect, fill=ACCENT_COLOR)

    # Region title
    region_y = y + PADDING + ACCENT_HEIGHT + 10
    draw.text((x + PADDING, region_y), region, font=font_region, fill=(0, 0, 0))

    # Headline – adjust font size to fit upper 55% of panel
    max_headline_height = int(panel_height * 0.55)
    head_font_size = 48
    while head_font_size > 20:
        head_font = ImageFont.truetype(font_path, head_font_size)
        max_text_width = panel_width - 2 * PADDING
        lines = wrap_text(headline, head_font, max_text_width, draw)
        line_height_px = int(head_font.getbbox("Ay")[3] - head_font.getbbox("Ay")[1])
        total_height = sum(line_height_px for _ in lines) + int((len(lines) - 1) * line_height_px * 0.15)
        if total_height <= max_headline_height:
            break
        head_font_size -= 1
    # Draw headline
    text_y = region_y + line_height_px + 10
    for line in lines:
        draw.text((x + PADDING, text_y), line, font=head_font, fill=(0, 0, 0))
        text_y += int(head_font.getbbox(line)[3] - head_font.getbbox(line)[1]) + int(line_height_px * 0.15)

    # Detail – up to 26px
    detail_font = ImageFont.truetype(font_path, 20)
    detail_max_width = panel_width - 2 * PADDING
    detail_lines = wrap_text(detail, detail_font, detail_max_width, draw)
    detail_y = text_y + 10
    for line in detail_lines:
        draw.text((x + PADDING, detail_y), line, font=detail_font, fill=(0, 0, 0))
        detail_y += int(detail_font.getbbox(line)[3] - detail_font.getbbox(line)[1]) + 4

# Save image
out_path = os.path.join(os.getcwd(), "entry.png")
img.save(out_path)
print(f"Saved {out_path}: {os.path.getsize(out_path)} bytes, {img.size}")