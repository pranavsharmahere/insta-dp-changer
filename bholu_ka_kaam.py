from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from instagrapi import Client
import os
import sys # Error aane par script band karne ke liye

# --- Image banane ka kaam ---
def create_date_image():
    print("🎨 Bholu apni upgraded drawing class mein hai...")
    CANVAS_SIZE = 512
    MARGIN = 100
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"Bholu aaj ki taarikh likhne wala hai: {today_str}")

    img = Image.new('RGB', (CANVAS_SIZE, CANVAS_SIZE), color = 'black')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("LiberationSans-Regular.ttf", 90)
        print("Bholu ko 'Liberation Sans' font mil gaya!")
    except IOError:
        print("Oops! Bholu ko koi accha font nahi mila, woh default font use kar raha hai.")
        font = ImageFont.load_default()
        
    max_text_width = CANVAS_SIZE - (2 * MARGIN)
    bbox = font.getbbox(today_str)
    text_width = bbox[2] - bbox[0]
    
    current_font_size = 90
    while text_width > max_text_width:
        print(f"Font thoda bada hai ({text_width} > {max_text_width}), chhota kar raha hoon...")
        current_font_size -= 5
        font = ImageFont.truetype("LiberationSans-Regular.ttf", current_font_size)
        bbox = font.getbbox(today_str)
        text_width = bbox[2] - bbox[0]
    
    text_height = bbox[3] - bbox[1]
    position = ((CANVAS_SIZE - text_width) / 2, (CANVAS_SIZE - text_height) / 2)
    draw.text(position, today_str, font=font, fill='white')
    
    image_path = "daily_dp_512.jpg"
    img.save(image_path)
    
    print("-" * 30)
    print(f"✅ Bholu ne image bana di hai!")
    print(f"File ka naam hai: {image_path}")
    print("-" * 30)
    return image_path

# --- Instagram par upload karne ka kaam ---
def upload_dp(image_path):
    print("📸 Bholu ab Instagram mission ki taiyaari kar raha hai...")
    insta_user = os.getenv("INSTA_USER")
    insta_pass = os.getenv("INSTA_PASS")

    if not insta_user or not insta_pass:
        print("❌ FATAL ERROR: Bholu ko username ya password nahi mila! Mission Abort.")
        sys.exit(1) # Script ko fail kar do

    cl = Client()
    try:
        print(f"Bholu '{insta_user}' se login karne ki koshish kar raha hai...")
        cl.login(insta_user, insta_pass)
        print("✅ Bholu login ho gaya! Ab DP badal raha hai...")
        cl.account_change_profile_picture(image_path)
        print("🎉 MISSION SUCCESSFUL! Bholu ne DP badal di! Party time! 😎")
        cl.logout()
    except Exception as e:
        print(f"❌ MISSION FAILED: Oh no! Bholu pakda gaya ya koi gadbad ho gayi: {e}")
        sys.exit(1) # Script ko fail kar do taaki Action mein error dikhe

# --- Poora Mission Ek Saath ---
if __name__ == "__main__":
    dp_path = create_date_image()
    upload_dp(dp_path)
