from ascii_artist import *

if __name__ == "__main__":

    font = FontSetup()
    artist = Artist(font)
    artist.create_art("train.jpg", "ascii_train.jpg")