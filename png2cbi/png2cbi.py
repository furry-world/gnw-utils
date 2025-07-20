#!/bin/python

# png2cbi
# utility to convert 1-bit PNG into CBI (Commander Bitmap Image)
# Part of furry-world project
# Written by qRea, 2025

import imageio as iio
import sys
import os

def printUsage():
    print("png2cbi v0.1 (alpha)")
    print(f"usage: {sys.argv[0]} <INPUT FILE> [SWITCHES]")
    print()
    print("valid switches:")
    print("   -h          print help")
    print("   -o=<FILE>   specify output file name")
    print("   -c          compress the image using RLE compression")


fileNameIn = ""
fileNameOut = ""
compress = False


arguments = sys.argv[1:]
for arg in arguments:
    if arg.startswith("-h"):
        printUsage()
        sys.exit()

    elif arg.startswith("-o="):
        fileNameOut = arg[3:]

    elif arg.startswith("-c"):
        compress = True

    else: fileNameIn = arg

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
        averageBrightness = int(x[0]) + int(x[1]) + int(x[2])
        if averageBrightness < 384:
            pixels.append(1)
        else:
            pixels.append(0)

hytes = []
if compress:
    currentColor = 0
    currentRun = 0

    for i in range(len(pixels)):
        if pixels[i] == currentColor:
            currentRun += 1
        else:
            if currentRun == 0:
                hytes.append(0)
                continue

            while currentRun > 0:
                hytes.append(currentRun % 64)
                currentRun //= 64
                if currentRun > 0: hytes.append(0)

            if currentColor == 0: currentColor = 1
            else: currentColor = 0

else:
    for i in range(len(pixels) // 6):
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

print(f"Wrote {len(hytes)} bytes.")
