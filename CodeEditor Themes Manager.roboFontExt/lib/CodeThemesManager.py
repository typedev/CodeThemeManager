# import os
# import AppKit
import vanilla
from mojo.UI import CodeEditor, getDefault, setDefault, preferencesChanged
from pygments.token import *
from pygments.styles import get_style_by_name, get_all_styles

# # Output window background color
# "DebuggerBackgroundColor": [r, g, b, 1],
# # Output window text color
# "DebuggerTextColor": [r, g, b, 1],
# # Editor background color
# "PyDEBackgroundColor": [r, g, b, 0],
# # Editor hightlight color
# "PyDEHightLightColor": [r, g, b, 1],
# # Editor hightlight text Colors
# "PyDETokenColors": { token:'value' ...}

SAMPLECODE = """
from typing import Iterator

# This is an example
class Math:
    @staticmethod
    def fib(n: int) -> Iterator[int]:
        \"\"\" Fibonacci series up to n \"\"\"
        a, b = 0, 1
        while a < n:
            yield a
            a, b = b, a + b

result = sum(Math.fib(42))
print(\"The answer is {}\".format(result))

\"\"\"
The Extension uses built-in Themes from the <pygments> modules. 
More information on the link: https://pygments.org/styles/
\"\"\"

"""

def hex_to_rgb (value):
	"""Return (red, green, blue) for the color given as #rrggbb."""
	try:
		value = value.lstrip('#')
		lv = len(value)
		return tuple(round((1.0 * int(value[i:i + lv // 3], 16) / 255), 4) for i in range(0, lv, lv // 3))
	except:
		return (0,0,0)

def rgb_to_hex (red, green, blue):
	"""Return color as #rrggbb for the given color values."""
	return '#%02x%02x%02x' % (red, green, blue)

def getPyDEtoken (token):
	bold, italic, underline = '', '', ''
	if token['bold']:
		bold = ' bold'
	if token['italic']:
		italic = ' italic'
	if token['underline']:
		underline = ' underline'
	return '%s%s%s%s' % (token['color'], bold, italic, underline)

def getStyleTokensDict (style):
	stylesdic = {}
	for (k, v) in style:
		stylesdic[k] = v
	return stylesdic

def applyTheme (applyPrefs = False, styleName = None):
	if not applyPrefs or not styleName: return
	PyDETokenColors = getDefault('PyDETokenColors')
	# PyDEBackgroundColor = getDefault('PyDEBackgroundColor')
	# PyDEHightLightColor = getDefault('PyDEHightLightColor')
	# print(PyDETokenColors)

	style = get_style_by_name(styleName)
	styleTokens = getStyleTokensDict(style)
	newPyDETokenColors = {'Token': 'FFFFFF'}
	for PyDEtokenName, v in PyDETokenColors.items():
		token = string_to_tokentype(PyDEtokenName)
		if token in styleTokens:
			newPyDETokenColors[PyDEtokenName] = getPyDEtoken(styleTokens[token])
		else:
			print(token, 'not founded')
	debuggerTextColor = hex_to_rgb('#%s' % styleTokens[string_to_tokentype('Token.Text')]['color'])

	for k, v in newPyDETokenColors.items():
		if v == 'None' or v == None or 'None' in v:
			newPyDETokenColors[k] = '000000'

	if applyPrefs:
		r, g, b = hex_to_rgb(style.background_color)
		setDefault('PyDEBackgroundColor', (r, g, b, 1), validate = True)
		setDefault('DebuggerBackgroundColor', (r, g, b, 1), validate = True)
		r, g, b = hex_to_rgb(style.highlight_color)
		setDefault('PyDEHightLightColor', (r, g, b, 1), validate = True)
		r, g, b = debuggerTextColor
		setDefault('DebuggerTextColor', (r, g, b, 1), validate = True)
		setDefault('PyDETokenColors', newPyDETokenColors, validate = True)
		preferencesChanged()


class TDCodeThemeManagerWindow:
	def __init__ (self, parent = None):
		_version = '0.2'
		self.parent = parent

		self.stylesList = []
		for style in list(get_all_styles()):
			self.stylesList.append(style)
		self.styleName = 'default'

		self.w = vanilla.FloatingWindow((500, 600), minSize = (300, 300), title = 'CodeEditor Theme Manager v%s' % _version)

		self.w.label1 = vanilla.TextBox('auto', 'Choose Theme:')
		self.w.chooseStyles = vanilla.PopUpButton('auto', self.stylesList, sizeStyle = "regular", callback = self.optionsChanged)

		self.w.btnRun = vanilla.Button('auto', title = 'Apply', callback = self.btnRunCallback)  # ,
		self.w.textBox = CodeEditor('auto', text = '', readOnly = True, showLineNumbers = True, checksSpelling = False)
		self.w.textBox.setHighlightStyle(get_style_by_name(self.styleName))

		rules = [
			# Horizontal
			"H:|-border-[label1]-border-|",
			"H:|-border-[chooseStyles]-border-|",
			"H:|-border-[btnRun]-border-|",
			"H:|-0-[textBox]-0-|",
			# Vertical
			"V:|-border-[label1]-space-[chooseStyles]-border-[btnRun]-border-[textBox]-0-|"
		]
		metrics = {
			"border": 15,
			"space": 8
		}
		self.w.addAutoPosSizeRules(rules, metrics)
		self.w.textBox.set(SAMPLECODE)
		self.w.open()

	def optionsChanged(self, sender):
		self.styleName = self.stylesList[sender.get()]
		self.w.textBox.setHighlightStyle(get_style_by_name(self.styleName))

	def btnRunCallback (self, sender):
		applyTheme(applyPrefs = True, styleName = self.styleName)


def main ():
	TDCodeThemeManagerWindow()

if __name__ == "__main__":
	main()
