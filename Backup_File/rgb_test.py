import sys
from time import sleep

from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW



def main():
    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    original_colors = lifx.get_color_all_lights()
    original_powers = lifx.get_power_all_lights()

    print("Turning on all lights...")
    lifx.set_power_all_lights(True)
    sleep(1)
    
    lan.set_color_all_lights(0, 0, True)

if __name__=="__main__":
    main()
