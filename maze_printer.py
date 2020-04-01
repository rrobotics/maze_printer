"""Saves a series of mazes to a PDF."""

from fpdf import FPDF
import math
from PIL import Image
import requests
import sys

__author__ = 'rrobotics'
__version__ = '0.1'

USAGE = '\n\tUsage: python maze_printer.py\
 [total_images] [images_per_row] [images_per_column] [output_name]\n'

# Defaults
NUM_IMAGES = 4
IMAGRS_PER_ROW = 2
IMAGES_PER_COL = 2

LTR_width = 215.9
LTR_height = 279.4
H_BORDER = 10.0
V_BORDER = 10.0
PADDING = 5.0


class MazePDF(FPDF):

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 12)
        self.cell(w=LTR_width,
                  h=20,
                  txt='Mazes by makeamaze.com    Page %s' % self.page_no(),
                  align='C')


def download_maze(url, filename):
    data = requests.get(url, stream=True)
    Image.open(data.raw).save(filename)
    return filename


def create_pdf(images, num_images, images_per_row, images_per_col):
    pdf = MazePDF('P', 'mm', (LTR_width, LTR_height))

    # Page parameters
    images_per_page = images_per_row * images_per_col
    image_width = (LTR_width - (2.0 * H_BORDER) -
                   (images_per_row * PADDING)) / (images_per_row)
    image_height = (LTR_height - (2.0 * V_BORDER) -
                    (images_per_col * PADDING)) / (images_per_col)

    # Add first page
    pdf.add_page()

    # Add images
    img_num = 0
    pre_page = 0
    for image in images:
        if image is not None:
            page = math.floor(img_num / images_per_page)
            y = math.floor((img_num - page * images_per_page) / images_per_row)
            x = math.floor((img_num - page * images_per_page) % images_per_row)

            if page > pre_page:
                pdf.add_page()

            cur_maze = Image.open(image)
            x_dim, y_dim = cur_maze.size
            cur_maze.close()

            x = H_BORDER + x * (image_width + PADDING) + PADDING / 2.0
            y = V_BORDER + y * (image_height + PADDING) + PADDING / 2.0

            # Is the image wider than tall?
            ratio = float(x_dim) / float(y_dim)
            if ratio > (float(image_width) / float(image_height)):
                pdf.image(image,
                          x=x,
                          y=y,
                          w=image_width,
                          h=image_width / ratio
                          )
            else:
                pdf.image(image,
                          x=x,
                          y=y,
                          h=image_height,
                          w=image_height * ratio
                          )
            img_num += 1
            pre_page = page

    return pdf


if __name__ == '__main__':
    # Defaults
    args = [NUM_IMAGES, IMAGRS_PER_ROW, IMAGES_PER_COL, 'maze']

    # Look for 'h' in 'help' or '?'
    if len(sys.argv) > 1:
        if 'h' in str(sys.argv[1]).lower() or '?' in str(sys.argv[1]).lower():
            print(USAGE)
            exit()

    # Too many arguments given
    if len(sys.argv) > 5:
        print(USAGE)
        exit()

    # Use as many CLI args as are given
    for i in range(1, len(sys.argv)):
        if i < 5:
            args[i - 1] = int(sys.argv[i])
        else:
            args[i - 1] = str(sys.argv[i])

    # Download an images from mazemaker
    images = []
    for i in range(args[0]):
        filename = 'maze_{}.png'.format(i)
        images.append(download_maze('https://www.makeamaze.com/image',
                                    filename))

    pdf = create_pdf(images, args[0], args[1], args[2])
    pdf.output(str(args[3]) + '.pdf', 'F')
    print("\tSaved to {}.pdf".format(str(args[3])))
