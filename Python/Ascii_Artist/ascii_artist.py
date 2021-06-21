from PIL import Image, ImageDraw, ImageFont
from numpy import interp

class FontSetup:

    def __init__(self, font="/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", symbols=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"):
        self.__used_symbols = symbols
        self.__font_path = font
        self.__font = ImageFont.truetype(font, 30)
        self.__process_font()
        self.__map_values_to_rgb_range()


    def __process_font(self):
        
        for i in self.__used_symbols:
            img = Image.new("RGB", (15,30), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((0,-1), i,font=self.__font, fill=(0,0,0))
            black = 0
            for k in range(0,15):
                for m in range(0,30):
                    r, g, b = img.getpixel((k,m))
                    if(r!=255 or g!=255 or b!=255):
                        black+=1
            self.__symbols[ord(i)] = round(black / (15*30) * 100)
               
    def __map_values_to_rgb_range(self):
        max_value = max(self.__symbols.values())
        min_value = min(self.__symbols.values())
        for (key,value) in self.__symbols.items():
            self.__symbols[key] = round(interp(value,[min_value,max_value],[0,255]))
    
    def get_font_info(self):
        return dict((v,k) for k,v in self.__symbols.items()), self.__font_path

    __font = ""
    __symbols = {}
    __font_path = ""
    __used_symbols = ""


class Artist:
    
    def __init__(self, font_information):
        self.__font_info, self.__font_path = font_information.get_font_info()

    def __get_closest_symbol_for_pixel(self, pix_val):
        return chr(self.__font_info.get(pix_val, self.__font_info[min(self.__font_info.keys(), key=lambda k: abs(k-pix_val))]))

    def create_art(self,path_to_img, output_filename,desired_width=400, font_size=5):
        self.__font_size = font_size
        self.__desired_width = desired_width
        self.__path_to_image = path_to_img
        self.__image_setup()
        self.__convert_pixels_to_ascii()
        self.__output_image_setup()
        self.__print_ascii_strings_to_image()
        self.__output_image.save(output_filename)

    def __print_ascii_strings_to_image(self):
        marginx = 0
        marginy = -self.__y_coordinate_compress
        for line in self.__ascii_strings_list:
            width, height = self.__font.getsize(line)
            self.__draw.text((marginx, marginy), line, font=self.__font, fill=(0,0,0))
            marginy += height-self.__y_coordinate_compress

    def __convert_pixels_to_ascii(self):
        for x in range(self.__img_height):
            curr_line = ""
            for y in range(self.__img_width):
                curr_line += self.__get_closest_symbol_for_pixel(255-self.__get_mean_of_pixel(self.__pixels[y,x]))
            self.__ascii_strings_list.append(curr_line)

    def __get_mean_of_pixel(self, pixel):
        return (pixel[0] + pixel[1] + pixel[2]) // 3

    def __output_image_setup(self):
        self.__font = ImageFont.truetype(self.__font_path, self.__font_size)
        width, height = self.__font.getsize(self.__ascii_strings_list[100])
        self.__output_image = Image.new("RGB", (width,height*self.__img_height-(self.__img_height*self.__y_coordinate_compress)), color = (255, 255, 255))
        
        self.__draw = ImageDraw.Draw(self.__output_image)

    def __image_setup(self):
        image = Image.open(self.__path_to_image)
        old_width = image.size[0]
        old_height = image.size[1]
        ratio = self.__desired_width/old_width
        image = image.resize((round(ratio*old_width), round(ratio*old_height)))
        self.__img_width  = image.size[0]
        self.__img_height = image.size[1]

        self.__pixels = image.load()

    __font_info = {}
    __path_to_image = ""
    __pixels = 0
    __img_width = 0
    __img_height = 0
    __ascii_strings_list = []
    __font_path = ""
    __font = ""
    __output_image = 0
    __draw = 0
    __y_coordinate_compress = 3
    __desired_width = 0
    __font_size = 0



