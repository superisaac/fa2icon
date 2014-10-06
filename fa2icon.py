#!/usr/bin/env python

import os, sys
import re
import urllib
import math
import getopt

import ImageFont, ImageDraw, Image
import tinycss

TTF_URL = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/fonts/fontawesome-webfont.ttf'
TTF_FILENAME = 'fontawesome-webfont.ttf'

CSS_URL = 'https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/css/font-awesome.min.css'
CSS_FILENAME = 'font-awesome.min.css'

class Options(object):
    verbose = False
    update = False
    canvas_size = 100
    file_tmpl = '%s.png'
    dest_dir = 'icons'
    color = 'white'
    whitelist = None

options = Options()

def update(force=False):
    if force or not os.path.exists(TTF_FILENAME):
        if options.verbose:
            print 'downloading ttf file ...'
        urllib.urlretrieve(TTF_URL, TTF_FILENAME)

    if force or not os.path.exists(CSS_FILENAME):
        if options.verbose:
            print 'downloading css file ...'
        urllib.urlretrieve(CSS_URL, CSS_FILENAME)

def parse_css():
    parser = tinycss.make_parser('page3')
    stylesheet = parser.parse_stylesheet_file(CSS_FILENAME)
    for rule in stylesheet.rules:
        if isinstance(rule, tinycss.css21.RuleSet):
            names = re.findall(r'\.(fa\-[\w\-]+):before\b', rule.selector.as_css())
            for decl in rule.declarations:
                if decl.name == 'content':
                    content_ord = int(decl.value.as_css()[2:-1], 16)
                    for iconname in names:
                        yield iconname, content_ord
    
def draw_text(faname, content, canvas_size):
    font_size = canvas_size
    font = ImageFont.truetype(TTF_FILENAME, font_size)
    w, h = font.getsize(content)
    if w > canvas_size or h > canvas_size:
        font_size = int(math.floor(font_size * float(font_size) / float(max(w, h))))
        font = ImageFont.truetype(TTF_FILENAME, font_size)
        w, h = font.getsize(content)

    im = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    draw.text(((canvas_size - w)/2, (canvas_size-h)/2), content, font=font, fill=options.color)
    
    imagename = os.path.join(options.dest_dir, options.file_tmpl % faname)
    im.save(imagename)

def usage():
    print 'Usage:', sys.argv[0], '[options]'
    print ' -h|--help\t\tPrint this message'
    print ' -v|--verbose\t\tPrint debug info'
    print ' --update\t\tUpdate the latest ttf and css files from github'
    print ' -c|--color=<color>\tThe color used to fill texts, can be #rrggbb or color names, default "white"'
    print ' --size=<size>\t\tThe canvas size of generated images, default 100'
    print ' -d|--dir=<dir>\t\tThe directory where generated images stores, default ./icons'
    print ' --filetmpl=<tmpl>\tThe filename template, default %s.png'
    print ' -w|--whitelist=<falist>\tA comma separated fa name list to generate'

def parse_command_line():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], 'hvd:c:w:',
            ['help', 'update', 'verbose',
             'size=', 'filetmpl=', 'dir=',
             'color=', 'whitelist='])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for o, v in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o in ('--update',):
            options.update = True
        elif o in ('-v', '--verbose',):
            options.verbose = True
        elif o in ('--size',):
            options.canvas_size = int(v)
        elif o in ('--filetmpl',):
            options.file_tmpl = v
        elif o in ('--dir', '-d'):
            options.dest_dir = v
        elif o in ('-c', '--color'):
            options.color = v
        elif o in ('-w', '--whitelist'):
            options.whitelist = set(v.split(','))

def main():
    parse_command_line()
    print options.whitelist
    update(options.update)
    if not os.path.isdir(options.dest_dir):
        if options.verbose:
            print 'prepare data dir', options.dest_dir
        os.makedirs(options.dest_dir)

    for faname, content_ord in parse_css():
        if options.whitelist is not None and (faname not in options.whitelist):
            continue
            
        u = unichr(content_ord)
        if options.verbose:
            print 'generating', faname
        draw_text(faname, u, options.canvas_size)

if __name__ == '__main__':
    main()
