from PIL import Image, ImageDraw, ImageFont, ImageOps
from numpy import interp
import numpy as np
import os.path


class FontSetup:
    def __init__(
        self,
        font="./assets/UbuntuMono-B.ttf",
        symbols=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
    ):
        self.symbol_darkness = {}
        self.used_symbols = symbols
        self.font_path = font
        self.font = ImageFont.truetype(font, 30)
        if(not self.font_info_file_found()):
            self.calculate_symbols_darkness()
            self.map_darkness_to_rgb_range()
            self._make_pixel_map()
            self.save_font_info()



    def font_info_file_found(self):
        if(os.path.isfile("font_info.txt")):
            return True
        else:
            return False

    def save_font_info(self):
        with open("font_info.txt", "w") as font_config:
            for key, val in self.p_map.items():
                font_config.write(f"{key} {ord(val)}\n")

    def calculate_symbols_darkness(self):
        for i in self.used_symbols:
            img = Image.new("RGB", (15, 30), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((0, -1), i, font=self.font, fill=(0, 0, 0))
            black = 0
            for k in range(0, 15):
                for m in range(0, 30):
                    r, g, b = img.getpixel((k, m))
                    if r != 255 or g != 255 or b != 255:
                        black += 1
            self.symbol_darkness[i] = round(black / (15 * 30) * 100)

    def map_darkness_to_rgb_range(self):
        max_value = max(self.symbol_darkness.values())
        min_value = min(self.symbol_darkness.values())
        for (key, value) in self.symbol_darkness.items():
            round_val = round(interp(value, [min_value, max_value], [0, 255]))
            self.symbol_darkness[key] = round_val

    # Filling up the missed values for future convenience
    def _make_pixel_map(self):
        self.p_map = {}
        revert_symbols_dict = dict((v,k) for k, v in self.symbol_darkness.items())
        symbols_darkness = sorted(list(revert_symbols_dict.keys()))
        symbols_darkness.insert(0, -1)
        for i in range(256):
            if symbols_darkness[1] > i:
                self.p_map[i] = revert_symbols_dict[symbols_darkness[0]]
            else:
                self.p_map[i] = revert_symbols_dict[symbols_darkness[1]]
                symbols_darkness.remove(symbols_darkness[0])

    def load_font_info(self):
        font_info = {}
        with open("font_info.txt", "r") as font_info_file:
            for line in font_info_file.readlines():
                k, v = list(map(int, line.split()))
                font_info[k] = v
        return font_info, self.font_path

class Artist:
    def __init__(self, font_information):
        self._pixel_map, self.font_path = font_information.load_font_info()

    def __get_closest_symbol_for_pixel(self, pix_val):
        return chr(self._pixel_map[pix_val])

    def create_art(self, path_to_img, output_filename, desired_width=400, font_size=5):
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
            _, height = self.font.getsize(line)

            self.__draw.text(
                (x_margin, y_margin), line, font=self.font, fill=(0, 0, 0)
            )
            y_margin += height - self.__y_coordinate_compress

    def __convert_pixels_to_ascii(self):
        self.__ascii_strings_list = [""] * self.__img_height
        for y in range(self.__img_height):
            curr_line_chars = [0] * self.__img_width
            for x in range(self.__img_width):
                curr_line_chars[x] = self.__get_closest_symbol_for_pixel(
                    255 - self.__pixels[x, y]
                )
            self.__ascii_strings_list[y] = ''.join(curr_line_chars)

    def __output_image_setup(self):
        self.font = ImageFont.truetype(self.font_path, self._font_size)
        width, height = self.font.getsize(self.__ascii_strings_list[0])
        self.__output_image = Image.new(
            "RGB",
            (width,
                height * self.__img_height - (self.__img_height * self.__y_coordinate_compress),
            ),
            color=(255, 255, 255),
        )

        self.__draw = ImageDraw.Draw(self.__output_image)

    def __image_setup(self):
        image = Image.open(self.__path_to_image)
        old_width = image.size[0]
        old_height = image.size[1]
        ratio = self.__desired_width/old_width
        image.thumbnail((round(ratio*old_width), round(ratio*old_height)), Image.Resampling.LANCZOS)
        grayscale_image = ImageOps.grayscale(image)
        self.__img_width = grayscale_image.size[0]
        self.__img_height = grayscale_image.size[1]
        self.__pixels = grayscale_image.load()


    __y_coordinate_compress = 3