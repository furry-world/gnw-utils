#!/bin/python

# png2cbi
# utility to convert 1-bit PNG into CBI (Commander Bitmap Image)
# Part of furry-world project
# Written by qRea, 2025

import imageio as iio
import sys
import os

def printUsage():
    print("png2charrom v0.1 (alpha)")
    print(f"usage: {sys.argv[0]} <INPUT FILE> [SWITCHES]")
    print()
    print("valid switches:")
    print("   -h          print help")
    print("   -o=<FILE>   specify output file name")


fileNameIn = ""
fileNameOut = ""


arguments = sys.argv[1:]
for arg in arguments:
    if arg.startswith("-h"):
        printUsage()
        sys.exit()

    elif arg.startswith("-o="):
        fileNameOut = arg[3:]


    else: fileNameIn = arg

if fileNameIn == "":
    printUsage()
    sys.exit()

if fileNameOut == "":
    fileNameOut = "char.rom"


try:
    img = iio.imread(fileNameIn)
except:
    print(f'ERROR: file "{fileNameIn}" is not a valid image or does not exist')
    sys.exit(1)
height, width, dummy = img.shape

if width != 128 or height != 128:
    print("ERROR: image must be 128x128 (16x16 characters)!")
    sys.exit(1)

pixels = []

for y in img:
    for x in y:
        averageBrightness = int(x[0]) + int(x[1]) + int(x[2])
        if averageBrightness < 384:
            pixels.append(0)
        else:
            pixels.append(1)

bytes = []

for y in range(16):
    for x in range(16):
        for line in range(8):
            byte = 0
            for bit in range(8):
                currentX = x * 8 + bit
                currentY = y * 8 + line

                byte <<= 1
                byte += pixels[currentY * 128 + currentX]
            bytes.append(byte)

with open(fileNameOut, "wb") as file:
    for byte in bytes:
        file.write(byte.to_bytes(1))
