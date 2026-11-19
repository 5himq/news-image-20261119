import os
import datetime
from PIL import Image, ImageDraw, ImageFont

# Constants
WIDTH, HEIGHT = 1024, 1024
BG_COLOR = (0, 0, 128)
TEXT_COLOR = (255, 255, 255)
PANEL_COLOR = (255, 255, 255)
PANEL_RADIUS = 25
PADDING = 20

# Fonts
font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
font_big = ImageFont.truetype(font_path, 60)
font_small = ImageFont.truetype(font_path, 36)
font_region = ImageFont.truetype(font_path, 28)

# Headlines data (region, headline, detail)
headlines = [
    ("China", "TRUMP, XI, PUTIN HOLD TRILATERAL SUMMIT", "First-ever three-way meeting in Shenzhen; nuclear arms and the Ukraine war on the table."),
    ("Netherlands", "WORLD COURT RULES ON ROHINGYA GENOCIDE", "ICJ judgment in Gambia's case against Myanmar over the Rohingya."),
    ("Saudi Arabia", "RIYADH SKYSCRAPER DAMAGED IN HOUTHI ATTACK", "Tower housing the sovereign wealth fund hit amid new reported attacks."),
    ("Bangladesh", "EX-LEADER YUNUS'S FAMILY HOME TORCHED", "Unrest and protests spread; security forces deployed across districts."),
    ("Strait of Hormuz", "THREE OIL TANKERS BURN AFTER MINE STRIKES", "Iran says tankers hit mines east of the strait."),
    ("World", "MUSLIMS PROJECTED LARGEST FAITH BY 2035", "Pew Research: Islam's population to overtake Christianity's.")
]

# Helper to wrap text by pixel width

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ''
    for w in words:
        test = current + (' ' if current else '') + w
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

# Create image
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Top band
draw.text((PADDING, PADDING), "WORLD NEWS", font=font_big, fill=TEXT_COLOR)
now = datetime.datetime.now()
date_str = now.strftime("%A, %d %B %Y")
world_news_height = font_big.getbbox("WORLD NEWS")[3] - font_big.getbbox("WORLD NEWS")[1]
date_height = font_small.getbbox(date_str)[3] - font_small.getbbox(date_str)[1]
draw.text((PADDING, PADDING + world_news_height + 10), date_str, font=font_small, fill=TEXT_COLOR)

# Panel layout
panel_width = (WIDTH - 3 * PADDING) // 2
panel_height = (HEIGHT - 3 * PADDING - world_news_height - date_height - 20) // 3
x_offset = PADDING

y_offset = PADDING + world_news_height + date_height + 30

for idx, (region, headline, detail) in enumerate(headlines):
    col = idx % 2
    row = idx // 2
    x = x_offset + col * (panel_width + PADDING)
    y = y_offset + row * (panel_height + PADDING)

    # Panel
    draw.rounded_rectangle([x, y, x + panel_width, y + panel_height], radius=PANEL_RADIUS, fill=PANEL_COLOR)

    # Pin pictogram
    # small pin in top-right corner
    pc_x = x + panel_width - 20
    pc_y = y + 20
    draw.ellipse([pc_x - 14, pc_y - 14, pc_x + 14, pc_y + 14], fill=(200, 0, 0))
    draw.line([pc_x, pc_y + 14, pc_x + 20, pc_y + 34], fill=(200, 0, 0), width=3)

    # Region title
    draw.text((x + 10, y + 10), region, font=font_region, fill=(0, 0, 0))

    # Headline – adjust font size to fit upper 55% of panel
    max_headline_height = int(panel_height * 0.55)
    head_font_size = 48
    while head_font_size > 20:
        head_font = ImageFont.truetype(font_path, head_font_size)
        max_text_width = panel_width - 2 * PADDING
        lines = wrap_text(headline, head_font, max_text_width, draw)
        line_height = head_font.getbbox("Ay")
        total_height = sum(line_height[3] - line_height[1] for _ in lines) + (len(lines) - 1) * 4
        if total_height <= max_headline_height:
            break
        head_font_size -= 1
    # Draw headline
    text_y = y + 10 + 28 + 5
    for line in lines:
        draw.text((x + 10, text_y), line, font=head_font, fill=(0, 0, 0))
        text_y += (head_font.getbbox(line)[3] - head_font.getbbox(line)[1]) + 4

    # Detail – up to 26px
    detail_font = ImageFont.truetype(font_path, 26)
    detail_max_width = panel_width - 2 * PADDING
    detail_lines = wrap_text(detail, detail_font, detail_max_width, draw)
    detail_y = text_y + 10
    for line in detail_lines:
        draw.text((x + 10, detail_y), line, font=detail_font, fill=(0, 0, 0))
        detail_y += (detail_font.getbbox(line)[3] - detail_font.getbbox(line)[1]) + 4

# Save image
out_path = os.path.join(os.getcwd(), "entry.png")
img.save(out_path)
size_bytes = os.path.getsize(out_path)
print(f"Saved {out_path}: {size_bytes} bytes, {img.size}")
