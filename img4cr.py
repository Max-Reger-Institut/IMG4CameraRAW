#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

# Frank Zalkow, 2014

import argparse
import subprocess
import glob
import os
import os.path
import tempfile
import shutil

def convert(infile, outfile):
	tmp_dir = tempfile.mkdtemp()
	
	subprocess.call("convert %s -deconstruct %s/test%%d.tif" % (infile, tmp_dir), shell=True)
	deconstructed_files = glob.glob(tmp_dir + "/*")
	
	maxsize = 0
	maxidx = 0
	for i, file in enumerate(deconstructed_files):
		size = os.path.getsize(file)
		if size > maxsize:
			maxsize = size
			maxidx = i
			
	tmpfile = deconstructed_files[maxidx]

	identify = subprocess.check_output("sips -g pixelHeight -g pixelWidth %s" % (tmpfile, ), shell=True)
	identify = identify.split("\n")
	x = identify[2].split(" ")[-1]
	y = identify[1].split(" ")[-1]
	
	subprocess.call("convert %s -flatten -alpha off %s" % (tmpfile, outfile), shell=True)
	subprocess.call('exiv2 -M\"set Exif.Photo.PixelXDimension Long %s\" -M\"set Exif.Photo.PixelYDimension Long %s\" %s' % (x, y, outfile), shell=True)
	
	shutil.rmtree(tmp_dir)
	
	print "%s\t->\t%s\t->\t%s" % (infile, tmpfile, outfile)



# get command line arguments
parser = argparse.ArgumentParser(prog="\033[1mready-for-bridge.py\033[0m", description="Convertes a folder with images to another folder to be ready for Camera Raw:\n\t1. Deconstructes all layers and chooses the one with biggest file size (so preview layers will be ignored)\n\t2. removes all layers aka flatten the image\n\t3. removes the alpha cannel\n\t4. writes Exif.Photo Dimension metadata to the image)", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-i", "--infolder", help="input folder with image files to be converted", required=True)
parser.add_argument("-o", "--outfolder", help="output folder to put the converted files in", required=True)

args = parser.parse_args()

# check everything is ok
if subprocess.check_output("which convert", shell=True) == "":
	raise Error("convert from ImageMagick must be installed... (http://www.imagemagick.org/)")
if subprocess.check_output("which exiv2", shell=True) == "":
	raise Error("exiv2 must be installed... (http://www.exiv2.org/)")
if subprocess.check_output("which exiv2", shell=True) == "":
	raise Error("sips must be installed... (https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/sips.1.html)")
if args.outfolder == args.infolder:
	raise Error("infolder must be different from outfolder...")

# run over all files
for file in glob.glob(args.infolder + "/*"):
	newfile = args.outfolder + "/" + os.path.split(file)[1]
	convert(os.path.abspath(file), os.path.abspath(newfile))