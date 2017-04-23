'''
All icons in this directory will be added to a
resources.qrc file.
'''

import os

iconsdir = './icons'
out_qrc  = 'resources.qrc'
out_py   = 'resources_rc.py'
icons = [f for f in os.listdir(iconsdir) if f[-4:] in ('.svg', '.png', '.jpg')]
icons.sort()

fout = open(out_qrc, 'w')
fout.write('\
<!DOCTYPE RCC><RCC version="1.0">\n\
<qresource>\n')
for icon in icons:
    fout.write('<file alias="{}">{}</file>\n'.\
            format(icon, iconsdir+os.sep+icon))
fout.write(\
'</qresource>\n\
</RCC>')
fout.close()

# Then run:
# pyrcc4 resources.qrc -o resources_rc.py
#command = "pyrcc4 {} -o {}".format(out_qrc, out_py)
#command = "pyrcc4 -py3 {} -o {}".format(out_qrc, out_py)
command = "pyrcc5 {} -o {}".format(out_qrc, out_py)
os.system(command)
