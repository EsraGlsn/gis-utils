import sys
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib as mpl; mpl.use('TkAgg')

print('matplotlib version: {}\npython version: {}'.format(mpl.__version__, sys.version))

mpl.get_cachedir()

#check for Univers in the system fonts
univers_fonts = [f for f in fm.findSystemFonts(fontpaths=None, fontext='ttf') if 'univers' in f.lower()]
univers_fonts


#get the univers names

univers_names = [fm.FontProperties(fname=f).get_name() for f in univers_fonts]
univers_names

#verify that matplotlib can find them
fm.findfont('Univers 67 Condensed')
plt.rcParams['pdf.fonttype']

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['pdf.fonttype']


fig, ax = plt.subplots()
plt.plot(range(10), range(10))

plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.it'] = 'Univers 67 Condensed:italic'

ax.set_title('$\it{someitalicstuff}$ not italic', fontname='Univers 67 Condensed' , loc='left')
plt.savefig('junk.pdf')