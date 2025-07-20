#!/bin/python

# png2cbi
# utility to convert 1-bit PNG into CBI (Commander Bitmap Image)
# Part of furry-world project
# Written by qRea, 2025

import imageio as iio
import sys
import os

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b
    def __format__(self, dummy):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)


def printUsage():
    print("png2cbi v0.1 (alpha)")
    print(f"usage: {sys.argv[0]} <INPUT FILE> [SWITCHES]")
    print()
    print("valid switches:")
    print("   -h          print help")
    print("   -o=<FILE>   specify output file name")


fileNameIn = ""
fileNameOut = ""

arguments = sys.argv[1:]
for arg in arguments:

    if arg.startswith("-o="):
        fileNameOut = arg[3:]

    fileNameIn = arg

if fileNameIn == "":
    printUsage()
    sys.exit()

if fileNameOut == "":
    fileNameOut = os.path.basename(fileNameIn).split(".")[0] + ".cbi"


try:
    img = iio.imread(fileNameIn)
except:
    print(f'ERROR: file "{fileNameIn}" is not a valid image or does not exist')
    sys.exit(1)
height, width, dummy = img.shape

if width % 6 != 0:
    print("ERROR: image width not divisible by 6!")
    sys.exit(1)

pixels = []

for y in img:
    for x in y:
        color = Color(x[0], x[1], x[2])
        if color == Color(0, 0, 0):
            pixels.append(1)
        else:
            pixels.append(0)

hytes = []
for i in range(int(len(pixels) / 6)):
    offset = i * 6
    hyte = 0
    for j in range(6):
        hyte <<= 1
        hyte += pixels[offset + j]
    hytes.append(hyte)

with open(fileNameOut, "wb") as file:
    for hyte in hytes:
        byte = hyte.to_bytes(1)
        file.write(byte)
