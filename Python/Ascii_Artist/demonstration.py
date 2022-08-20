from ascii_artist import *
import cProfile, pstats

if __name__ == "__main__":
    
    # By default loads Ubuntu font. 
    # If you want to use any other one, you should specify path to .ttf file

    font = FontSetup() 
    print(font.get_font_info())
    artist = Artist(font)
    # why diffecence
    # picture streches in y-axis when font_size changes

    profiler = cProfile.Profile()
    profiler.enable()
    artist.create_art("/home/windy-stairs/Resume/Python/Ascii_Artist/marguerite.jpg",
                        "ascii_marguerite_1.jpg", font_size=50)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()