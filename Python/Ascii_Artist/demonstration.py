from ascii_artist import *

if __name__ == "__main__":

    font = FontSetup() #by default loads Ubuntu font. If you want to use any other one, you should specify path to .ttf file
    artist = Artist(font)
    artist.create_art("train.jpg", "ascii_train.jpg")
