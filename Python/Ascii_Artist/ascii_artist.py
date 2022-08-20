from PIL import Image, ImageDraw, ImageFont, ImageOps
from numpy import interp
import numpy as np

class FontSetup:

    def __init__(self, 
                font="/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", 
                symbols=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"):
        self._symbols = {}
        self._used_symbols = symbols
        self._font_path = font
        self._font = ImageFont.truetype(font, 30)
        self._process_font()
        self._map_values_to_rgb_range()


    def _process_font(self):
        
        for i in self._used_symbols:
            img = Image.new("RGB", (15,30), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((0,-1), i,font=self._font, fill=(0,0,0))
            black = 0
            for k in range(0,15):
                for m in range(0,30):
                    r, g, b = img.getpixel((k,m))
                    if(r!=255 or g!=255 or b!=255):
                        black+=1
            self._symbols[ord(i)] = round(black / (15*30) * 100)
               
    def _map_values_to_rgb_range(self):
        max_value = max(self._symbols.values())
        min_value = min(self._symbols.values())
        for (key,value) in self._symbols.items():
            self._symbols[key] = round(interp(value,[min_value,max_value],[0,255]))
    
    def get_font_info(self):
        return dict((v,k) for k,v in self._symbols.items()), self._font_path



class Artist:
    
    def __init__(self, font_information):
        self._font_info, self._font_path = font_information.get_font_info()
        self._font_info = dict(sorted(self._font_info.items()))
        self._pixel_map = self._make_pixel_map()
        print(self._pixel_map)

    def _make_pixel_map(self):
        p_map = {}
        for i in range(256):
            p_map[i] = self._font_info[self._find_position(list(self._font_info.keys()), i)]
        return p_map


    def _find_position(self, key_list, item):
        # make into binary search, dumbass!
        to_return = key_list[0]

        for i in key_list:
            if i <= item:
                to_return = i
            else:
                break
        return to_return

    
    def __get_closest_symbol_for_pixel(self, pix_val):
        return chr(self._pixel_map[pix_val])


    def create_art(self,path_to_img, output_filename,desired_width=400, font_size=5):
        self._font_size = font_size
        self.__desired_width = desired_width
        self.__path_to_image = path_to_img
        self.__image_setup()
        self.__convert_pixels_to_ascii()
        self.__output_image_setup()
        self.__print_ascii_strings_to_image()
        self.__output_image.save(output_filename)

    
    def __print_ascii_strings_to_image(self):
        x_margin = 0
        y_margin = -self.__y_coordinate_compress
        for line in self.__ascii_strings_list:
            width, height = self._font.getsize(line)
            # TODO try multiline
            
            self.__draw.text((x_margin, y_margin), line, font=self._font, fill=(0,0,0))
            y_margin += height-self.__y_coordinate_compress

    def __convert_pixels_to_ascii(self):
        for x in range(self.__img_height):
            curr_line = ""
            for y in range(self.__img_width):
                curr_line += self.__get_closest_symbol_for_pixel(255-self.__pixels[y,x]) #255-self.__get_mean_of_pixel(self.__pixels[y,x]))
            self.__ascii_strings_list.append(curr_line)

    def __get_mean_of_pixel(self, pixel):
        return (pixel[0] + pixel[1] + pixel[2]) // 3

    def __output_image_setup(self):
        self._font = ImageFont.truetype(self._font_path, self._font_size)
        width, height = self._font.getsize(self.__ascii_strings_list[100])
        self.__output_image = Image.new(
            "RGB", 
            (
            width,height*self.__img_height-(self.__img_height*self.__y_coordinate_compress)
            ),
            color = (255, 255, 255)
        )
        
        self.__draw = ImageDraw.Draw(self.__output_image)

    def __image_setup(self):
        image = Image.open(self.__path_to_image)
        image = ImageOps.grayscale(image)
        old_width = image.size[0]
        old_height = image.size[1]
        ratio = self.__desired_width/old_width
        image = image.resize((round(ratio*old_width), round(ratio*old_height)))
        self.__img_width  = image.size[0]
        self.__img_height = image.size[1]

        self.__pixels = image.load()

    _font_info = {}
    __path_to_image = ""
    __pixels = 0
    __img_width = 0
    __img_height = 0
    __ascii_strings_list = []
    _font_path = ""
    _font = ""
    __output_image = 0
    __draw = 0
    __y_coordinate_compress = 3
    __desired_width = 0
    _font_size = 0



