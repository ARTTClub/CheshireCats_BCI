import sys
from time import sleep
from copy import copy

from lifxlan import BLUE, CYAN, GREEN, LifxLAN, ORANGE, PINK, PURPLE, RED, YELLOW



def main():
    num_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        num_lights = int(sys.argv[1])

    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    original_colors = lifx.get_color_all_lights()
    original_powers = lifx.get_power_all_lights()

    print("Turning on all lights...")
    lifx.set_power_all_lights(True)
    sleep(1)
    print("Discovering lights...")

    half_period_ms = 2500
    duration_mins = 20
    duration_secs = duration_mins*60
 
 #60000 =red
    for bulb in original_colors:
        color = original_colors[bulb]
        dim = list(copy(color))
        i = 0
        dim[0] = 38000
        bulb.set_color(dim, 0, rapid=True)
        while True:
            text = raw_input("Color = ")
            dim[0] = int(text)
            bulb.set_color(dim, 0, rapid=True)
#        while i < 62000:
#            dim[0] = i
        #print "changing bulb to %s" % dim[2]
#            bulb.set_color(dim, 0, rapid=True)
#            print i
#            i +=2000
#            sleep(1)

 
 
    #lifx.set_color_all_lights(0, 0, True)
#    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]
#    transition_time_ms = 0
#    rapid = True
#    for color in colors:
#        lifx.set_color_all_lights(color, transition_time_ms, rapid)
#        sleep(1)

if __name__=="__main__":
    main()
