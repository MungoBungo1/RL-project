import arcade
from RacerView import RacerView

WIDTH = 1400    
HEIGHT = 800

def main():
    window = arcade.Window(WIDTH, HEIGHT, "Racer")
    view = RacerView()
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()