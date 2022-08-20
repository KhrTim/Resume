from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (15,30), color=(255, 255, 255))
d = ImageDraw.Draw(img)
fnt = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", 30)
print(fnt.getsize('-'))
d.text((0,0), 'q',font=fnt, fill=(0,0,0))
img.save("font_font.png")
