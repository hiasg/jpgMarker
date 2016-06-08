#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, sys
from PIL import Image,ImageEnhance,ImageDraw,ImageFont
from PIL.ExifTags import TAGS,GPSTAGS

def get_exif(image):
    """Extraxt Exif data"""
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
    """ GPSInfo is a nested dig """
    exif_data.update(exif_data['GPSInfo'])
    return exif_data

def gps_convert(value):
    """ Convert lat and lon """
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])

    return d + (m / 60.0) + (s / 3600.0)

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",75)
dirname, filename = os.path.split(os.path.abspath(__file__))
print dirname
print filename
#for jpg in os.listdir(os.getcwd()):
for jpg in os.listdir('/home/hias/original'):
    print jpg
    name, ext = os.path.splitext(jpg.lower())
    if name.startswith('dsc'):
        print 'IMAGE'
        img = Image.open(jpg)
    if name.startswith('logo'):
        print 'LOGO'
        logo = Image.open(jpg).resize((300,370))
        continue


    lat = str(gps_convert(get_exif(img)["GPSLatitude"]))
    lon = str(gps_convert(get_exif(img)["GPSLongitude"]))
    alt = str("%.2f" % (get_exif(img)["GPSAltitude"][0]/get_exif(img)["GPSAltitude"][1]))
    date = get_exif(img)["DateTime"]

    draw = ImageDraw.Draw(img)
    color = (0,0,0)
    draw.rectangle(((320,20),(1820,390)), fill="white", outline="black")

    draw.text((370,40),"LKLD - Penzberg "+jpg,color,font=font)
    draw.text((370,120),"Aufgenommen : "+date,color,font=font)
    draw.text((370,200),"GPS : "+lat+" "+lon,color,font=font)
    draw.text((370,280),"Hoehe NN : "+alt+" m",color,font=font)

    img.paste(logo,(20,20))
    save_name = "BW-LKLD_" + jpg
    img.save(save_name)
