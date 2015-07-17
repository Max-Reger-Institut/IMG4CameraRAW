# IMG4CameraRAW

## Description

Some images cannot be opened with Adobe Camera Raw (Adobe CS3). For those cases this small script prepares the images to be opened with Camera Raw. See *usage* for some details what is done.

## Usage

    usage: ready-for-bridge.py [-h] -i INPUT -o OUTPUT [-b]

    Convertes images to to be ready for Camera Raw:
        1. Deconstructes all layers and chooses the one with biggest file size (so preview layers will be ignored)
        2. removes all layers aka flatten the image
        3. removes the alpha cannel
        4. writes Exif.Photo Dimension metadata to the image)

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            input file/folder to be converted
      -o OUTPUT, --output OUTPUT
                            output file/folder to be written
      -b, --batch           input and output are folders -- batch convert all files (default: convert single file)

## Dependencies

* [Python 2](https://www.python.org/)
* [ImageMagick](http://www.imagemagick.org)
* [exiv2](http://www.exiv2.org)

## License

This is MIT license so you can do what you want with the code, just give proper attribution. Anyway, if you make any improvements to the code we are happy if you share it with us or even contribute directly to our project. Please contact rwa@max-reger-institut.de.