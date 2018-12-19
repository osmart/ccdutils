#!/usr/bin/env python
# software from PDBe: Protein Data Bank in Europe; https://pdbe.org
#
# Copyright 2018 EMBL - European Bioinformatics Institute
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import os
from sys import platform

from PIL import Image, ImageDraw, ImageFont


def supply_font():
    """
    Platform non-specific function to locate sans-serif font in the environment.

    Returns:
        str: path to the font
    """
    font = ''
    if platform == "linux" or platform == "linux2":
        font = '/usr/share/fonts/gnu-free/FreeSans.ttf'
    elif platform == "darwin":
        font = '/Library/Fonts/arial.ttf'
    elif platform == "win32":
        font = 'c:\\windows\\font\\arial.ttf'

    if os.path.isfile(font):
        return font
    else:
        return None


def save_no_image(path_to_image, width=200):
    """
    Generate pretty image with 'No image available' message in case
    the 2D depiction cannot be created.

    Args:
        path_to_image (str): path to the image
        width (int, optional): Defaults to 200. width of the image
    """
    if path_to_image.split('.')[-1] == "svg":
        svg = _svg_no_image(width)
        with open(path_to_image, 'w') as f:
            f.write(svg)
    else:
        _png_no_image(path_to_image, width)


def _png_no_image(path_to_image, width):
    """
    Save image with the text 'No image available' as a png.

    Args:
        path_to_image (str): path to save the image
        width (int): Width of an image
    """

    font = None
    font_path = supply_font()

    if font is not None:
        font_path = ImageFont.truetype(font_path, size=(int(width / 8)))
    else:
        font = ImageFont.load_default()

    white = (255, 255, 255)
    black = (0, 0, 0)
    img = Image.new("RGBA", (width, width), white)
    draw = ImageDraw.Draw(img)
    draw.multiline_text((width / 4, width / 3), "No image\n available",
                        font=font, align='center', fill=black)
    draw = ImageDraw.Draw(img)
    img.save(path_to_image)


def _svg_no_image(width=200):
    """Get svg representation
        width (int, optional): Defaults to 200. width of the image

    Returns:
        str: string representation of an svg image.
    """

    svg = """<?xml version='1.0' encoding='iso-8859-1'?>
<svg version='1.1' baseProfile='full'
              xmlns='http://www.w3.org/2000/svg'
                      xmlns:rdkit='http://www.rdkit.org/xml'
                      xmlns:xlink='http://www.w3.org/1999/xlink'
                  xml:space='preserve' width='{width}px' height='{width}px' >
            <rect style='opacity:1.0;fill:#FFFFFF;stroke:none' width='{width}' height='{width}' x='0' y='0'> </rect>
            <text alignment-baseline="middle" text-anchor="middle" x="25%" y="25%" style='font-size:{font}px;font-family:sans-serif;text-anchor:start;fill:#000000'>
                Image not
            </text>
            <text alignment-baseline="middle" text-anchor="middle" x="30%" y="50%" style='font-size:{font}px;font-family:sans-serif;text-anchor:start;fill:#000000'>
                available
            </text>
            </svg>
          """
    return svg.format(width=width, font=width / 8)
