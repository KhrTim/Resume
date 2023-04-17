from ascii_artist import *


if __name__ == "__main__":
    font = FontSetup()
    artist = Artist(font)
    file_name = input("Please, input the image file name: ")
    output_file_name = input(
        "Please, input the output image file name (without extension): ")
    output_file_name += ".jpg"
    desired_width = int(input("Please, enter desired output image width: "))
    desired_font_size = int(input("Please, enter desired desired font size: "))

    artist.create_art(path_to_img=file_name, output_filename=output_file_name,
                      font_size=desired_font_size, desired_width=desired_width)
