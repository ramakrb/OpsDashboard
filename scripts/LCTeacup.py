# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import division, print_function
from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime, date
import sys
from reservoirsa import res_attrib
import os


colors = {
                  'white' : (255, 255, 255),
                  'blue' : (100, 100, 255),
                  'n1blue' : (8, 82, 150),
                  'nblue' : (0, 0, 140),
                  'red' : (255, 0, 0),
                  'green' : (0, 220, 0),
                  'black' : (0, 0, 0),
				  'Recblue' : (0,130,164)
                 }


imgPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'Basin8.png')
img = Image.open(imgPath).convert('RGBA')
img2 = img.copy()

for res in res_attrib:
    x,y = res['upper_left']
    size = res['size']
    current_fill = res['current_fill']
    max_fill = res['max_fill']
    label = res['label']
    date1 = datetime.strptime(res['date'], '%m/%d/%Y')
    pfull = current_fill*100.0/max_fill
   
        # upperleft, upperright, lowerright, lowerleft
    cup = [(x, y), (x+30*size, y), (x+20*size, y+20*size), (x+10*size, y+20*size)]
   
    if label == 'Lake Mohave':
        percent_full = pfull - 10 #current_fill*100.0/max_fill
    elif label == 'Lake Havasu':
        percent_full = pfull - 15
    else:
        percent_full = pfull - 3
       
    area_full = 400*size**2 + (3200*(size**2)*percent_full)/100.0
    area_full = (math.sqrt(area_full) - 20*size)/(40*size)

    if area_full > 1.0:
        area_full = 1.0
    elif area_full < 0.0:
        area_full = 0.0

    x, y = cup[3] # Lower left
    filled_cup = cup[:]
    filled_cup[0] = (x - 10*size*area_full, y - 20*size*area_full) # Upper left
    filled_cup[1] = (x + 10*size + 10*size*area_full, y - 20*size*area_full)

    draw = ImageDraw.Draw(img2)
    draw.polygon(cup, fill=colors['white'])
    if label == 'Lake Powell':
        fill1 = colors['Recblue']
        draw.polygon(filled_cup, fill=fill1, outline=fill1)
    else:
        draw.polygon(filled_cup, fill=colors['n1blue'], outline=colors['n1blue'])
        fill1 = colors['black']
   
    draw.line(cup+[cup[0]], fill=fill1) # Add width=2 if desired


    font_size = 28
    #font_face = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_face = '/usr/share/fonts/truetype/freefont/FreeSans.ttf'
    width, height = draw.textsize(label, font=ImageFont.truetype(font_face, font_size))
    label_box = [(x, y+3), (x + width, y+3 + height)]
    draw.rectangle(label_box, fill=colors['white'])
   
    #font_size = 11

    fraction = '{:,.0f} / {:,.0f} ac.ft.'.format(current_fill,max_fill)
    width, height = draw.textsize(fraction, font=ImageFont.truetype(font_face, font_size))
    fraction_box = [(x, y+3+font_size), (x + width, y+3 + font_size + height)]
    draw.rectangle(fraction_box,fill=colors['white'])
   
    qualifier = (' as of {}'.format(date1.strftime("%m/%d/%y")))
    percent_string = '{:.0f}% full{}'.format(pfull, qualifier)
    width, height = draw.textsize(percent_string, font=ImageFont.truetype(font_face, font_size))
    percent_box = [(x, y+3 + font_size*2), (x+width, y+3 + font_size*2 + height)]
    #draw.rectangle(percent_box, fill=colors['white'])
   
   
   
    draw.text(label_box[0], fraction, fill=fill1, font=ImageFont.truetype(font_face, font_size))
    #font_size = 11
    draw.text(fraction_box[0], percent_string, fill=fill1, font=ImageFont.truetype(font_face, font_size))
    #draw.text(percent_box[0], percent_string, fill=colors['black'], font=ImageFont.truetype(font_face, font_size))
   
#full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'Basin8TC.png')
#full_path = os.path.join('scripts/Basin8TC.png')
img2.save('Basin8TC.png')
