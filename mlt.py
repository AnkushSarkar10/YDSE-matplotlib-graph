import numpy as np
import math as m
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider, Button

from w2rgb import wavelength_to_rgb


def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)
    
def w2hex(wav):
    return str(rgb2hex(wavelength_to_rgb(wav)[0], wavelength_to_rgb(wav)[1], wavelength_to_rgb(wav)[2]))

plt.style.use('seaborn')

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)


wavelenghth_slider_val = 700 #wav_l in nm
wavelenghth_light = wavelenghth_slider_val*(10**-9) #wav_l in m

color_hex = w2hex(wavelenghth_slider_val)

# wavelenghth_red = 700*(10**-9)
# wavelenghth_green = 550*(10**-9)
# wavelenghth_blue = 450*(10**-9)

i_max = 0.2 #intenisity in watt/m2
s = 0.000002 #slit sepr in metres
d = 50 #screen distance in metres
y_lim = 150
y = np.arange(-y_lim,y_lim,0.075)

intensities_light = []
# intensities_red = []
# intensities_green = []
# intensities_blue = []

def create_y_axis():
    global wavelenghth_light, wavelenghth_slider_val

    wavelenghth_light = wavelenghth_slider_val*(10**-9)
    
    for x in y:
        d1 = m.sqrt(d**2 + abs(x-s/2)**2)
        d2 = m.sqrt(d**2 + abs(x+s/2)**2)
        pathdif = abs(d1-d2)

        phi_red = 2*(np.pi)*pathdif/wavelenghth_light

        intensities_light.append(4*i_max*(np.cos(phi_red/2)**2))

        # ax.add_patch(Rectangle((x,-0.3),0.075,0.2,color=(intensities_light[-1]/0.8,0,0)))


create_y_axis()

l, = ax.plot(y,intensities_light ,color_hex, label="Red")

# Slider Shit

wav_slider_ax = plt.axes([0.15, 0.15, 0.7, 0.035], facecolor='lightgoldenrodyellow')
wav_slider = Slider(wav_slider_ax, 'Wavelengths', valmin=380 , valmax=700, valfmt='%1.0f', valstep=2, color=color_hex)

wav_slider.set_val(wavelenghth_slider_val)

def update(val):
    global intensities_light, wavelenghth_slider_val, color_hex
    wavelenghth_slider_val = wav_slider.val
    color_hex = w2hex(wavelenghth_slider_val)
    l.set_color(color_hex) 
    intensities_light.clear()
    create_y_axis()
    l.set_ydata(intensities_light)

    fig.canvas.draw()


wav_slider.on_changed(update)

ax.legend()

plt.show()