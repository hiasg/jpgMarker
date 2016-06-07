#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, sys
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ExifTags import TAGS,GPSTAGS

def get_exif(image):
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data =  {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t,t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data

def gps_convert(value):
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",75)

img = Image.open(sys.argv[1])
logo = Image.open(sys.argv[2]).resize((300,370))

lat = str(gps_convert(get_exif(img)["GPSInfo"]["GPSLatitude"]))
lon = str(gps_convert(get_exif(img)["GPSInfo"]["GPSLongitude"]))
alt = str("%.2f" % (get_exif(img)["GPSInfo"]["GPSAltitude"][0]/get_exif(img)["GPSInfo"]["GPSAltitude"][1]))
date = get_exif(img)["DateTime"]

draw = ImageDraw.Draw(img)
color = (0,0,0)
draw.rectangle(((300,0),(1800,370)), fill="white", outline="black")

draw.text((350,20),"LKLD - Penzberg "+sys.argv[1],color,font=font)
draw.text((350,100),"Aufgenommen : "+date,color,font=font)
draw.text((350,180),"GPS : "+lat+" "+lon,color,font=font)
draw.text((350,260),"Hoehe NN : "+alt+" m",color,font=font)

img.paste(logo,(0,0))
save_name = "BW-LKLD_" + sys.argv[1]
img.save(save_name)
