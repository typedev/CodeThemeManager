from mojo.UI import getDefault, setDefault, preferencesChanged
from pygments.lexer import RegexLexer, bygroups
from pygments.token import *
from pygments.styles import get_style_by_name, get_all_styles
from fontParts.world import *
#import matplotlib.colors as colors
   # # Output window background color
   # "DebuggerBackgroundColor": [0.0854, 0.0733, 0.2221, 1],
   # # Output window text color
   # "DebuggerTextColor": [1, 1, 1, 1],
   # # Editor background color
   # "PyDEBackgroundColor": [0.1028, 0.1473, 0.2947, 0],
   # # Editor hightlight color
   # "PyDEHightLightColor": [0.8866, 0.6455, 0.9994, 1],
   # # Editor hightlight text Colors
   # "PyDETokenColors": {}
def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(round((1.0*int(value[i:i + lv // 3], 16)/255),4) for i in range(0, lv, lv // 3))

def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

# get current value
currentStyle = getDefault("PyDETokenColors")
style = get_style_by_name('material')
print(style.background_color, hex_to_rgb(style.background_color))
styledic = {}
for (k,v) in style:
    styledic[k] = v
    
for k, v in currentStyle.items():
    # print(k)
    if string_to_tokentype(k) in styledic and k != 'Token':
        print (k, v) # ,'\n', styledic[string_to_tokentype(k)]

# style = get_style_by_name('material')
# for k in style:
#     print(k)
    # print(v)