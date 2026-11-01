import os
from PIL import Image, ImageDraw, ImageFont

images_dir = os.path.join(os.path.dirname(__file__), 'jobs', 'static', 'images')
os.makedirs(images_dir, exist_ok=True)

# -------------------------------------------------------------------------
# Load Fonts with graceful fallbacks
# -------------------------------------------------------------------------
try:
    font_logo_bold = ImageFont.truetype("arialbd.ttf", 34)
    font_logo_sub = ImageFont.truetype("arial.ttf", 11)
    
    font_title_bold = ImageFont.truetype("arialbd.ttf", 15)
    font_salary_bold = ImageFont.truetype("arialbd.ttf", 13)
    font_body = ImageFont.truetype("arial.ttf", 12)
    font_badge = ImageFont.truetype("arialbd.ttf", 11)
    font_sm = ImageFont.truetype("arial.ttf", 11)
    
    font_banner_bold = ImageFont.truetype("arialbd.ttf", 15)
    font_banner_sub = ImageFont.truetype("arial.ttf", 12)
    font_btn_sm = ImageFont.truetype("arialbd.ttf", 12)
    font_url = ImageFont.truetype("arial.ttf", 11)
except Exception:
    font_logo_bold = ImageFont.load_default()
    font_logo_sub = font_logo_bold
    font_title_bold = font_logo_bold
    font_salary_bold = font_logo_bold
    font_body = font_logo_bold
    font_badge = font_logo_bold
    font_sm = font_logo_bold
    font_banner_bold = font_logo_bold
    font_banner_sub = font_logo_bold
    font_btn_sm = font_logo_bold
    font_url = font_logo_bold

# -------------------------------------------------------------------------
# 1. Logo (360 x 90 PNG, transparent)
# -------------------------------------------------------------------------
logo_img = Image.new('RGBA', (360, 90), (0, 0, 0, 0))
draw = ImageDraw.Draw(logo_img)

# Logo icon box
draw.rounded_rectangle([(10, 15), (70, 75)], radius=14, fill=(16, 42, 67, 255), outline=(6, 182, 212, 255), width=2)
draw.ellipse([(28, 30), (52, 54)], outline=(6, 182, 212, 255), width=4)
draw.ellipse([(35, 37), (45, 47)], fill=(255, 255, 255, 255))
draw.line([(45, 42), (58, 42)], fill=(6, 182, 212, 255), width=3)

# Logo Text: "Career" (Navy 900) + "Connect" (Cyan 500)
draw.text((85, 22), "Career", fill=(10, 25, 47, 255), font=font_logo_bold)
draw.text((195, 22), "Connect", fill=(6, 182, 212, 255), font=font_logo_bold)
draw.text((87, 58), "JOB & TALENT PLATFORM", fill=(98, 125, 152, 255), font=font_logo_sub)

logo_path = os.path.join(images_dir, 'logo.png')
logo_img.save(logo_path)
print(f"Saved: {logo_path}")

# -------------------------------------------------------------------------
# 2. Hero Image (800 x 520 PNG) - Pixel-perfect layout with ZERO overlap
# -------------------------------------------------------------------------
hero_img = Image.new('RGBA', (800, 520), (248, 250, 252, 255))
h_draw = ImageDraw.Draw(hero_img)

# Main Mockup Window Box (30, 20) to (770, 500)
h_draw.rounded_rectangle([(30, 20), (770, 500)], radius=20, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)

# Top Bar of Mockup (Navy 900)
h_draw.rounded_rectangle([(30, 20), (770, 68)], radius=20, fill=(10, 25, 47, 255))
h_draw.rectangle([(30, 50), (770, 68)], fill=(10, 25, 47, 255))

# Window Controls (macOS style dots)
h_draw.ellipse([(52, 38), (64, 50)], fill=(244, 63, 94, 255))
h_draw.ellipse([(72, 38), (84, 50)], fill=(245, 158, 11, 255))
h_draw.ellipse([(92, 38), (104, 50)], fill=(16, 185, 129, 255))

# Mockup URL bar
h_draw.rounded_rectangle([(125, 34), (460, 54)], radius=6, fill=(24, 43, 73, 255))
h_draw.text((140, 38), "https://careerconnect.com/explore-jobs", fill=(165, 243, 252, 255), font=font_url)

# Status Pill in top bar
h_draw.rounded_rectangle([(670, 34), (748, 54)], radius=10, fill=(16, 42, 67, 255), outline=(6, 182, 212, 255), width=1)
h_draw.ellipse([(678, 41), (684, 47)], fill=(16, 185, 129, 255))
h_draw.text((692, 38), "LIVE", fill=(255, 255, 255, 255), font=font_badge)

# Search Bar inside Mockup
h_draw.rounded_rectangle([(55, 85), (745, 135)], radius=12, fill=(248, 250, 252, 255), outline=(203, 213, 225, 255), width=1)
h_draw.text((75, 102), "Search 250+ verified roles, tech stacks & companies...", fill=(100, 116, 139, 255), font=font_body)
h_draw.rounded_rectangle([(635, 93), (735, 127)], radius=8, fill=(6, 182, 212, 255))
h_draw.text((658, 102), "Search", fill=(10, 25, 47, 255), font=font_btn_sm)

# -------------------------------------------------------------------------
# Job Card 1: Senior Python Engineer (X: 55 to 385, Width: 330px)
# -------------------------------------------------------------------------
h_draw.rounded_rectangle([(55, 155), (385, 335)], radius=14, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)

# Company Icon Box
h_draw.rounded_rectangle([(75, 172), (115, 212)], radius=10, fill=(16, 42, 67, 255))
h_draw.text((90, 182), "C", fill=(6, 182, 212, 255), font=font_title_bold)

# Job Title & Subtitle (fits cleanly within 330px width)
h_draw.text((125, 175), "Senior Python Engineer", fill=(10, 25, 47, 255), font=font_title_bold)
h_draw.text((125, 198), "CloudScale • Remote • Full-time", fill=(100, 116, 139, 255), font=font_body)

# Tags Row
h_draw.rounded_rectangle([(75, 230), (145, 254)], radius=6, fill=(240, 244, 248, 255), outline=(188, 204, 220, 255), width=1)
h_draw.text((88, 235), "Django", fill=(36, 59, 83, 255), font=font_badge)

h_draw.rounded_rectangle([(155, 230), (245, 254)], radius=6, fill=(236, 254, 255, 255), outline=(165, 243, 252, 255), width=1)
h_draw.text((166, 235), "Tailwind CSS", fill=(8, 145, 178, 255), font=font_badge)

h_draw.rounded_rectangle([(255, 230), (335, 254)], radius=6, fill=(240, 244, 248, 255), outline=(188, 204, 220, 255), width=1)
h_draw.text((267, 235), "PostgreSQL", fill=(36, 59, 83, 255), font=font_badge)

# Bottom Divider & Salary / CTA
h_draw.line([(75, 272), (365, 272)], fill=(241, 245, 249, 255), width=1)
h_draw.text((75, 292), "$125k - $160k / yr", fill=(16, 185, 129, 255), font=font_salary_bold)

h_draw.rounded_rectangle([(285, 283), (365, 315)], radius=6, fill=(16, 42, 67, 255))
h_draw.text((308, 292), "Apply", fill=(255, 255, 255, 255), font=font_btn_sm)

# -------------------------------------------------------------------------
# Job Card 2: Lead Product Designer (X: 415 to 745, Width: 330px)
# -------------------------------------------------------------------------
h_draw.rounded_rectangle([(415, 155), (745, 335)], radius=14, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)

# Company Icon Box
h_draw.rounded_rectangle([(435, 172), (475, 212)], radius=10, fill=(8, 145, 178, 255))
h_draw.text((450, 182), "F", fill=(255, 255, 255, 255), font=font_title_bold)

# Job Title & Subtitle (fits cleanly within 330px width)
h_draw.text((485, 175), "Lead Product Designer", fill=(10, 25, 47, 255), font=font_title_bold)
h_draw.text((485, 198), "Finova Global • Hybrid • Full-time", fill=(100, 116, 139, 255), font=font_body)

# Tags Row
h_draw.rounded_rectangle([(435, 230), (500, 254)], radius=6, fill=(240, 244, 248, 255), outline=(188, 204, 220, 255), width=1)
h_draw.text((448, 235), "Figma", fill=(36, 59, 83, 255), font=font_badge)

h_draw.rounded_rectangle([(510, 230), (610, 254)], radius=6, fill=(236, 254, 255, 255), outline=(165, 243, 252, 255), width=1)
h_draw.text((522, 235), "Design Systems", fill=(8, 145, 178, 255), font=font_badge)

h_draw.rounded_rectangle([(620, 230), (710, 254)], radius=6, fill=(240, 244, 248, 255), outline=(188, 204, 220, 255), width=1)
h_draw.text((634, 235), "Prototypes", fill=(36, 59, 83, 255), font=font_badge)

# Bottom Divider & Salary / CTA
h_draw.line([(435, 272), (725, 272)], fill=(241, 245, 249, 255), width=1)
h_draw.text((435, 292), "$115k - $150k / yr", fill=(16, 185, 129, 255), font=font_salary_bold)

h_draw.rounded_rectangle([(645, 283), (725, 315)], radius=6, fill=(16, 42, 67, 255))
h_draw.text((668, 292), "Apply", fill=(255, 255, 255, 255), font=font_btn_sm)

# -------------------------------------------------------------------------
# Bottom Floating Status Banner (X: 75 to 725, Width: 650px)
# -------------------------------------------------------------------------
h_draw.rounded_rectangle([(75, 360), (725, 465)], radius=16, fill=(10, 25, 47, 255), outline=(6, 182, 212, 255), width=2)

# Checkmark Circle
h_draw.ellipse([(100, 392), (140, 432)], fill=(16, 185, 129, 255))
h_draw.text((113, 398), "v", fill=(255, 255, 255, 255), font=font_title_bold)

# Banner Title
h_draw.text((155, 388), "Direct Candidate Application Flow • 100% Verified", fill=(255, 255, 255, 255), font=font_banner_bold)

# Status Stepper Badges
h_draw.rounded_rectangle([(155, 420), (225, 444)], radius=6, fill=(255, 251, 235, 255))
h_draw.text((166, 425), "Pending", fill=(146, 64, 14, 255), font=font_badge)

h_draw.text((235, 424), "->", fill=(165, 243, 252, 255), font=font_badge)

h_draw.rounded_rectangle([(255, 420), (345, 444)], radius=6, fill=(236, 254, 255, 255))
h_draw.text((267, 425), "Shortlisted", fill=(8, 145, 178, 255), font=font_badge)

h_draw.text((355, 424), "->", fill=(165, 243, 252, 255), font=font_badge)

h_draw.rounded_rectangle([(375, 420), (455, 444)], radius=6, fill=(236, 253, 245, 255))
h_draw.text((387, 425), "Accepted", fill=(4, 120, 87, 255), font=font_badge)

h_draw.text((475, 425), "Instant employer feedback", fill=(148, 163, 184, 255), font=font_sm)

hero_path = os.path.join(images_dir, 'hero-image.png')
hero_img.save(hero_path)
print(f"Saved: {hero_path}")

# -------------------------------------------------------------------------
# 3. Default Company Logo (200 x 200 PNG)
# -------------------------------------------------------------------------
comp_img = Image.new('RGBA', (200, 200), (240, 244, 248, 255))
c_draw = ImageDraw.Draw(comp_img)
c_draw.rounded_rectangle([(10, 10), (190, 190)], radius=30, fill=(16, 42, 67, 255), outline=(6, 182, 212, 255), width=3)
c_draw.rectangle([(55, 60), (145, 150)], fill=(36, 59, 83, 255), outline=(6, 182, 212, 255), width=2)
for x in (70, 95, 120):
    for y in (75, 95, 115):
        c_draw.rectangle([(x, y), (x+10, y+10)], fill=(6, 182, 212, 255))
c_draw.rectangle([(90, 130), (110, 150)], fill=(255, 255, 255, 255))

comp_path = os.path.join(images_dir, 'default-company.png')
comp_img.save(comp_path)
print(f"Saved: {comp_path}")
