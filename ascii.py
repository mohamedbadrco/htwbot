# Python code to convert an image to ASCII image.
from email.mime import image
import sys, random, argparse
import numpy as np
import math
import time
 
from PIL import Image, ImageDraw, ImageFont
import os

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@@ '

def getAverageL(image):

	"""
	Given PIL Image, return average value of grayscale value
	"""
	# get image as numpy array
	im = np.array(image)

	# get shape
	w,h = im.shape

	# get average
	return np.average(im.reshape(w*h))

def covertImageToAscii(fileName, scale, moreLevels):
	"""
	Given Image and dims (rows, cols) returns an m*n list of Images
	"""
	# declare globals
	global gscale1, gscale2

	# open image and convert to grayscale
	image = Image.open(fileName).convert('L')

	# store dimensions
	W, H = image.size[0], image.size[1]
	print("input image dims: %d x %d" % (W, H))
	cols = round(W*scale)
    # compute width of tile
	w = W/cols
 
    # compute tile height based on aspect ratio and scale
	rows = round(H*scale)

	h = H/rows
 
	print("cols: %d, rows: %d" % (cols, rows))
	print("tile dims: %d x %d" % (w, h))

	# check if image size is too small
	if cols > W or rows > H:
		print("Image too small for specified cols!")
		exit(0)

	# ascii image is a list of character strings
	aimg = []
	# generate list of dimensions
	for j in range(rows):
		y1 = int(j*h)
		y2 = int((j+1)*h)

		# correct last tile
		if j == rows-1:
			y2 = H

		# append an empty string
		aimg.append("")

		for i in range(cols):

			# crop image to tile
			x1 = int(i*w)
			x2 = int((i+1)*w)

			# correct last tile
			if i == cols-1:
				x2 = W

			# crop image to extract tile
			img = image.crop((x1, y1, x2, y2))

			# get average luminance
			avg = int(getAverageL(img))

			# look up ascii char
			if moreLevels:
				gsval = gscale1[int((avg*69)/255)]
			else:
				gsval = gscale2[int((avg*2)/255)]

			# append ascii char to string
			aimg[j] += gsval
	
	# return txt image
	return aimg

# main() function
def main():
	# create parser
	descStr = "This program converts an image into ASCII art."
	parser = argparse.ArgumentParser(description=descStr)
	# add expected arguments
	parser.add_argument('--file', dest='imgFile', required=True)
	parser.add_argument('--scale', dest='scale', required=False)
	parser.add_argument('--out', dest='outFile', required=False)
	parser.add_argument('--morelevels',dest='moreLevels',action='store_true')

	# parse args
	args = parser.parse_args()

	imgFile = args.imgFile

	# set output file
	outFile = 'out.txt'
	if args.outFile:
		outFile = args.outFile

	# set scale default as 0.43 which suits
	# a Courier font
	scale = 0.5
	if args.scale:
		scale = float(args.scale)

	print('generating ASCII art...')
	# convert image to ascii txt
	aimg = covertImageToAscii(imgFile, scale, args.moreLevels)

	image = Image.open(imgFile)

	# store dimensions
	W, H = image.size[0], image.size[1]

	f = open(outFile, 'w')
	cols = round(W*scale)
    # compute width of tiles
 
    # compute tile height based on aspect ratio and scale
	rows = round(H*scale)
	intfont = 20

	image = Image.new(mode = "RGB", size = ( round(cols*intfont*0.65) , round(rows*intfont*0.65) ), color = "white")
	print(f" out img {round(cols*8)} {round(rows*8) }")
	
	font =  ImageFont.truetype( r"fonts/CourierPrime-Regular.ttf" , size = intfont  , encoding="unic")
	
	draw = ImageDraw.Draw(image)

    # write to file
	index_row = -2
	indexcol = 14
	cola = ["red","green","blue","black"]
	for row in aimg:
		f.write(row + '\n')
		indexcol = 14
		for char in row:
			draw.text((indexcol,index_row),char,fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),random.randint(0,255)),font = font)
			indexcol += intfont*0.6
			# print(char)
		index_row += intfont*0.6

    # index_row = -2
	# indexcol = 0
	# for row in aimg:
	# 	f.write(row + '\n')
	# 	indexcol = 0
	# 	for char in row:
	# 		draw.text((indexcol,index_row),char,fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),random.randint(0,255)),font = font)
	# 		indexcol += intfont*0.6+5
	# 		# print(char)
	# 	index_row += intfont*0.6+5
		
	
	
	f = open("out.txt", "r")


   # now = time.Now()
    # name of the file to save
	filename = "img0.png"
    # create new image
	image.save(filename)

	# open file
	f = open(outFile, 'w')

	# write to file
	for row in aimg:
		f.write(row + '\n')

	# cleanup
	f.close()
	print("ASCII art written to %s" % outFile)


# call main
if __name__ == '__main__':
	main()