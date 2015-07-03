#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

# Frank Zalkow

import argparse
import subprocess
import glob
import os
import os.path
import tempfile
import shutil

def convert(infile, outfile):
	tmp_dir = tempfile.mkdtemp()
	
	call("convert %s -deconstruct %s/test%%d.tif" % (infile, tmp_dir))
	deconstructed_files = glob.glob(tmp_dir + "/*")
	
	maxsize = 0
	maxidx = 0
	for i, file in enumerate(deconstructed_files):
		size = os.path.getsize(file)
		if size > maxsize:
			maxsize = size
			maxidx = i
			
	tmpfile = deconstructed_files[maxidx]

	identify = call("sips -g pixelHeight -g pixelWidth %s" % (tmpfile, ))
	identify = identify.split("\n")
	x = identify[2].split(" ")[-1]
	y = identify[1].split(" ")[-1]
	
	call("convert %s -flatten -alpha off %s" % (tmpfile, outfile))
	call('exiv2 -M\"set Exif.Photo.PixelXDimension Long %s\" -M\"set Exif.Photo.PixelYDimension Long %s\" %s' % (x, y, outfile))
	
	shutil.rmtree(tmp_dir)
	
	print "%s\t->\t%s\t->\t%s" % (infile, tmpfile, outfile)

def call(cmd):
	return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]



def main():
	# get command line arguments
	parser = argparse.ArgumentParser(prog="\033[1mready-for-bridge.py\033[0m", description="Convertes images to to be ready for Camera Raw:\n\t1. Deconstructes all layers and chooses the one with biggest file size (so preview layers will be ignored)\n\t2. removes all layers aka flatten the image\n\t3. removes the alpha cannel\n\t4. writes Exif.Photo Dimension metadata to the image)", formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument("-i", "--input", help="input file/folder to be converted", required=True)
	parser.add_argument("-o", "--output", help="output file/folder to be written", required=True)
	parser.add_argument("-b", "--batch", help="input and output are folders -- batch convert all files (default: convert single file)", action='store_true')

	args = parser.parse_args()

	# check everything is ok
	if call("which convert") == "":
		raise RuntimeError("convert from ImageMagick must be installed... (http://www.imagemagick.org/)")
	if call("which exiv2") == "":
		raise RuntimeError("exiv2 must be installed... (http://www.exiv2.org/)")
	if call("which exiv2") == "":
		raise RuntimeError("sips must be installed... (https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/sips.1.html)")
	if args.output == args.input:
		raise RuntimeError("infolder must be different from outfolder...")

	if args.batch:
		# run over all files
		for file in glob.glob(args.input + "/*"):
			newfile = args.output + "/" + os.path.split(file)[1]
			convert(os.path.abspath(file), os.path.abspath(newfile))
	else:
		convert(args.input, args.output)

if __name__ == "__main__":
    main()