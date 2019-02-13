#!/usr/bin/env python3

import datetime, xlrd
import sys

import os
import urllib.request

VERBOSE=False

HTML_PAGE=False
HTML_PAGE=True

IMAGE_DIR="./images"

if not os.path.exists(IMAGE_DIR):
    os.mkdir( IMAGE_DIR, 0o755 )
    print("Creating dir <{}>".format( IMAGE_DIR ))

# Choose colour method for colouring cells:
PROCESS_COLOR=True
USE_IMAGE_SVG=True
USE_IMAGE_MAGICK=False
USE_IMAGE_ONLINE=False

USE_IMAGE = USE_IMAGE_SVG or USE_IMAGE_MAGICK or USE_IMAGE_ONLINE
USE_STYLE=False

SVG_TEXTBOX_TEMPLATE='''
<?xml version="1.0" encoding="utf-8"  standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg 
    width="{}" height="{}"
    viewBox="0 0 {} {}"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
>
  <rect id="rec" x="0" y="0" width="{}" height="{}" style="fill:{}" />
  <text id="TextElement" x="0" y="{}" style="font-family:{};font-size:{};fill:{}"> {} </text> 
</svg>'''

SVG_TEXT2BOX_TEMPLATE='''
<?xml version="1.0" encoding="utf-8"  standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg 
    width="{}" height="{}"
    viewBox="0 0 {} {}"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
>
  <rect id="rec" x="0" y="0" width="{}" height="{}" style="fill:{}" />
  <text id="TextElement" x="0" y="{}" style="font-family:{};font-size:{};fill:{}"> {} </text> 
  <text id="TextElement" x="0" y="{}" style="font-family:{};font-size:{};fill:{}"> {} </text> 
</svg>'''



if len(sys.argv) > 1 and sys.argv[1] == '-v':
    VERBOSE=True

def die(msg):
    print("die: " + msg)
    sys.exit(1)

COLOR_TABLE={}

TABLE_HEADER=''' <table> <tbody> '''

TABLE_FOOTER=''' </tbody> </table> '''

'''
    convertDate(isoDate): Concert string in iso format YYYY-MM-DD to DD-Mon-YYYY
'''
def convertDate(isoDate):
    bits=isoDate.split("-")
    mth=int(bits[1])-1
    if mth < 0 or mth > 11:
        die("Failed to parse month[{}] in date[{}]".format(bits[1], isoDate))

    month=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][mth]

    return bits[2]+" "+month+" "+bits[0]

'''
    csv_from_excel(wb, worksheet, txt_opfile): Export Worksheet as a CSV file
'''
def csv_from_excel(wb, worksheet, txt_opfile):

    sheet = wb.sheet_by_name(worksheet)
    op = open(txt_opfile, "w")

    #print("Sheet: " + worksheet)
    rownum=0
    op.write(", ".join(sheet.row_values(rownum)))

    for rownum in range(1,sheet.nrows):
        op.write(", ".join(sheet.row_values(rownum)))

    op.close()

'''
    Calculate brightness as %age based on RGB tuple (r,g,b)
'''
def brightnessPC(fgbg, tple):
    if tple == None:
        return 0.0

    #print("{}: TPLE={}".format(fgbg, tple))
    brightness=100.0*( (tple[0]*tple[0]) + (tple[1]*tple[1]) + (tple[2]*tple[2]) ) / (3.0 * 255 * 255)

    #print("brightness=" + str(brightness))
    return brightness


'''
    Convert RGB tuple (r,g,b) to hex string: e.g. #ffffff for white
'''
def To0xRGB(tple):
    if tple == None:
        return ''

    return "#%02x%02x%02x" % tple

'''
    dump_style_rules(color_dict): Dump color table as <STYLE> ... </STYLE> section
'''
def dump_style_rules(color_dict, default_color='#ffffff'):
    style='<STYLE>\n'

    for idx in color_dict:
        color = color_dict[idx]
        if color == None or color == '':
            color=default_color

        style += '.cellstyle{} {}\n'.format(idx, color)

    style += '</STYLE>\n'
    return style

'''
    getCellStyle(wb, sheet_name, sheet, row, col): Get foreground/background colours for Cell:
'''
def getCellStyle(wb, sheet_name, sheet, row, col):
    (fontcolor, background) = getCellColors(wb, sheet_name, sheet, row, col)

    print("style_index={}: background={} font_color={}".format(style_index, background,font_color))
    json_style='{\n  ' + 'background-color: {};\n  color: {};\n'.format(background,font_color) + '}'

    if style_index in COLOR_TABLE:
        if COLOR_TABLE[style_index] != json_style:
            die("BUG-json_style")
    else:
        COLOR_TABLE[style_index]   = json_style

    if USE_STYLE:
        style = " class='cellstyle{}'".format(style_index)

    if cell_info != "":
        cell_info = sheet_name + ": " + pos + " " + cell_info
        print(cell_info)
        #xf.dump()
        #font.dump()

    return style


'''
    getCellTextImage(wb, sheet_name, sheet, row, col, col_width, text): Get foreground/background colours and text for Cell:
'''
def getCellTextImage(wb, sheet_name, sheet, row, rect_height, col, col_width, text, link=False):
    (fgcolor, bgcolor) = getCellColors(wb, sheet_name, sheet, row, col)
    width=100
    height=30

    if USE_IMAGE_SVG:
        img_path = createColouredTextImage_SVG(fgcolor, bgcolor, rect_height, col_width, height, text, link, dir=IMAGE_DIR)
        return img_path

    if USE_IMAGE_ONLINE:
        img_path = createColouredTextImage_online(fgcolor, bgcolor, width, height, text, link, dir=IMAGE_DIR)
        return img_path

    if USE_IMAGE_MAGICK:
        img_path = createColouredTextImage_magick(fgcolor, bgcolor, width, height, text, link, dir=IMAGE_DIR)
        return img_path

    return text



'''
    getCellColors(wb, sheet_name, sheet, row, col): Get foreground/background colours for Cell:
'''
def getCellColors(wb, sheet_name, sheet, row, col):
    xfx = sheet.cell_xf_index(row, col)
    xf  = wb.xf_list[xfx]
    bgx = xf.background.pattern_colour_index
    #print("bgx=" + str(bgx))
    #bgx = xf.background.background_colour_index

    font = wb.font_list[xf.font_index]
    #font.dump()
    fgx  = font.colour_index
    #print("fgx=" + str(fgx))

    pos="(%s,%s)" % (row,col)
    background = ""
    obg = ""
    cell_info=""
    SHOW_ALL=False

    if bgx in wb.colour_map:
        background_tpl = wb.colour_map[bgx]
        background = To0xRGB(background_tpl)
    else:
        print("colour_map keys=<{}>".format(join(",", wb.colour_map.keys())))
        die("Not found bgx={}".format(bgx))

    font_color = ""
    ofg = ""

    if fgx in wb.colour_map:
        font_color_tpl = wb.colour_map[fgx]
        font_color = To0xRGB(font_color_tpl)
        color  = wb.colour_map.get(fgx)
    else:
        print("colour_map keys=<{}>".format(join(",", wb.colour_map.keys())))
        die("Not found fgx={}".format(fgx))

    style_index = "{}_{}".format(bgx, fgx)

    if background == '' and font_color == '':
        background = '#ffffff'
        font_color = '#000000'

    if background == '':
        if brightnessPC('font', font_color_tpl) < 50.0:
            background = '#ffffff'
        else:
            background = '#000000'

    if font_color == '':
        if brightnessPC('background', background_tpl) < 50:
            font_color = '#000000'
        else:
            font_color = '#ffffff'

    return (font_color, background)


def findFirstDelimitedPosWidth(text):
    pos = findFirstDelimiterPos(text)
    length = len(text)

    width = length
    if pos != -1:
        if pos > (length-pos):
            width=pos
        else:
            width=length-pos
    #print("width={} TEXT=<{}>".format(width, text))
    return (pos, width)

def findFirstDelimiterPos(text):
    marker=999999
    pos=marker

    #delimiters=[ "(", " - ", ":" ]
    #delimiters=[ "(", " - ", ":" ]
    delimiters=[ "\n" ]

    for delimiter in delimiters:
        if delimiter in text:
            dpos = text.find(delimiter)
            if dpos < pos:
                pos = dpos

    if pos == marker:
        return -1

    return pos

'''
    def html_from_excel(wb, sheet_name, html_opfile, HTML_PAGE=False):
        Write out Excel table spreadsheet as an HTML table, with coloured cells
'''
def html_from_excel(wb, sheet_name, html_opfile, HTML_PAGE=False):

    sheet = wb.sheet_by_name(sheet_name)
    op = open(html_opfile, "w")

    table_html = "\n<H1>Sheet: " + sheet_name + "</H1>\n\n"
    table_html += "<!-- ### {} -->\n".format(sheet_name)
    table_html += TABLE_HEADER

    rownum=0
    table_html += "<tr>\n  "

    note_map = sheet.cell_note_map
    print("note_map = " + str(sheet.cell_note_map))
    #die("OK")

    # Determine column widths:
    col_widths=[]
    rect_heights=[]
    for col in range( len( sheet.row_values(0) ) ):
        col_widths.append(0)

    # Determine rect_heights:
    for rownum in range(0,sheet.nrows):
        rect_heights.append(1)

        for col in range( len( sheet.row_values(rownum) ) ):
            text = sheet.row_values(rownum)[col]
            (pos, width) = findFirstDelimitedPosWidth(text)

            if width > col_widths[col]:
                col_widths[col]=width
            if pos != -1:
                rect_heights[rownum]=2

    rownum=0
    for col in range( len( sheet.row_values(rownum) ) ):
        if col > 0:
            table_html += "</th>  "

        if PROCESS_COLOR and USE_STYLE:
            table_html += "<th{}>".format( getCellStyle(wb, sheet_name, sheet, rownum, col) )
        else:
            table_html += "<th>"

        text = sheet.row_values(rownum)[col]
        if PROCESS_COLOR and USE_IMAGE:
            table_html += getCellTextImage(wb, sheet_name, sheet, rownum, rect_heights[rownum], col, col_widths[col], text)
        else:
            table_html += text

    table_html += "</th>\n</tr>\n"

    for rownum in range(1,sheet.nrows):
        table_html += "<tr>\n  "

        for col in range( len( sheet.row_values(rownum) ) ):
            if col > 0:
                table_html += "</td>  "

            if PROCESS_COLOR and USE_STYLE:
                table_html += "<td{}>".format( getCellStyle(wb, sheet_name, sheet, rownum, col) )
            else:
                table_html += "<td>"

            LINK=''
            #if ( note_map = sheet.cell_note_map
            if (rownum,col) in note_map:
                note_text = note_map[(rownum,col)].text
                if "LINK" in note_text:
                    LINK=note_text[ 5+note_text.find("LINK("): ]
                    if LINK[0] == '"' or LINK[0] == "'":
                        LINK = LINK[1: LINK.find(")")-1]
                    else:
                        LINK = LINK[: LINK.find(")")]

                    print("<{}>".format(LINK))

            text = sheet.row_values(rownum)[col]
            if PROCESS_COLOR and USE_IMAGE:
                if LINK == '':
                    table_html += getCellTextImage(wb, sheet_name, sheet, rownum, rect_heights[rownum], col, col_widths[col], text)
                else:
                    table_html += "<a href={}> {} </a>".format(LINK,
                        getCellTextImage(wb, sheet_name, sheet, rownum, rect_heights[rownum], col, col_widths[col], text, link=True))
            else:
                table_html += text

        table_html += "</td>\n</tr>\n"

    table_html += TABLE_FOOTER

    HEADER_HTML='!<DOCTYPE HTML>\n<HTML>\n'
    page_html = HEADER_HTML

    if PROCESS_COLOR:
        page_html += dump_style_rules( COLOR_TABLE )
    page_html += "<BODY>\n\n"
    page_html += table_html
    page_html += "\n\n</BODY>\n</HTML>"

    if HTML_PAGE:
        op.write(page_html)
    else:
        op.write(table_html)

    op.close()

'''
    write_color_index_table(wb, html_opfile):
            Write out Workbook colour_map as a coloured HTML table
 '''
def write_color_index_table(wb, html_opfile):

    op = open(html_opfile, "w")

    op.write("<HTML>\n<BODY>")
    op.write(TABLE_HEADER)

    for idx in wb.colour_map:
        background_tpl = wb.colour_map[idx]
        if background_tpl:
            background_tpl = wb.colour_map[idx]
            background = To0xRGB( background_tpl )

            if brightnessPC('background', background_tpl) < 50.0:
                #font_color = '#ffffff'
                font_color = '#0000ff'
            else:
                font_color = '#000000'
        else:
            #print("tpl={} bg={}".format( background_tpl, background))
            background = '#ffffff'
            font_color = '#000000'

        style='background-color: {}; color: {};'.format(background, font_color)
        op.write("<tr><td> {}: </td><td style='{}'> {} == {} </td></tr>\n".format(idx, style, background_tpl, style))

    op.write(TABLE_FOOTER)
    op.write("</BODY>\n</HTML>")
    op.close()


'''
    write_color_table(wb, html_opfile):
        Write out COLOR_TABLE as a coloured HTML table
'''
def write_color_table(wb, html_opfile):

    op = open(html_opfile, "w")

    op.write("<HTML>\n" + dump_style_rules( COLOR_TABLE ) + "\n<BODY>")

    op.write(TABLE_HEADER)

    #for idx in wb.colour_map:
    for style_index in COLOR_TABLE:
        style = COLOR_TABLE[style_index].replace("\n","")
        #op.write("<tr><td> {}: </td><td style='{}'> {} SOME TEXT </td></tr>\n".format(style_index, style, style))
        op.write("<tr><td> cellstyle{}: </td><td class='cellstyle{}'> {} </td></tr>\n".format(style_index, style_index, style))

    op.write(TABLE_FOOTER)

    op.write("</BODY>\n</HTML>")
    op.close()

'''
    def createColouredTextImage_SVG(fgcolor, bgcolor, rect_height, col_width, height, text):
        fgcolor: in dddddd form, e.g. 7F7FFF
        bgcolor: in dddddd form, e.g. 7F0000
'''
def createColouredTextImage_SVG(fgcolor, bgcolor, rect_height, col_width, height, text, link=False, dir="."):

    REP_SPACE="+"
    fn_text=text
    fn_text=fn_text.replace(" ", REP_SPACE)
    fn_text=fn_text.replace("\n", REP_SPACE)
    fn_text=fn_text.replace("-", "BR-")
    fn_text=fn_text.replace(":", "BRcn-")
    fn_text=fn_text.replace("(", "BRpa-")
    fn_text=fn_text.replace(")", "-")

    texts=[]
    texts.append(text)

    (pos, width) = findFirstDelimitedPosWidth(text)
    if pos != -1:
        texts[0]=text[:pos+1] # +"\\"
        texts.append( text[pos:] )

    #if text == "":
        #text="__"

    font_size=24
    #rect_width=int(width*font_size/1.8)
    rect_width=int(col_width*font_size/1.6) # ??
    #rect_width=int(width*font_size)

    if len(texts) == 1:
        rect_height = height * rect_height
        svg = SVG_TEXTBOX_TEMPLATE.format( rect_width, rect_height, rect_width, rect_height, rect_width, rect_height,
                bgcolor,
                rect_height-5, 'verdana', font_size, fgcolor, text)
    else:
        rect_height = height * rect_height
        svg = SVG_TEXT2BOX_TEMPLATE.format( rect_width, rect_height, rect_width, rect_height, rect_width, rect_height,
                bgcolor,
                height, 'verdana', font_size, fgcolor, texts[0],
                height+20, 'verdana', font_size, fgcolor, texts[1],
                )
  #<text id="TextElement" x="0" y="{}" style="font-family:{};font-size:{};fill:{}"> {} </text> 

    # Advance until '<'
    svg = svg[ svg.find("<"): ]
    #print(svg[0]); print(svg[1]); print(svg[2]); die("SVG")


    size=str(rect_width) + "x" + str(height)
    bgcolor = bgcolor[1:] # Remove #
    fgcolor = fgcolor[1:] # Remove #
    file = dir + "/" + fn_text + "_" + size + "_" + bgcolor + "_" + fgcolor + ".svg"

    #if not os.path.exists(file):
    # Create svg file
    if VERBOSE:
        print("file=" + file)
    with open(file, 'w') as f:
        f.write(svg)

    return "<img src='" + file + "'/>"

'''
    def createColouredTextImage_online(fgcolor, bgcolor, width, height, text):
        fgcolor: in dddddd form, e.g. 7F7FFF
        bgcolor: in dddddd form, e.g. 7F0000
'''
def createColouredTextImage_online(fgcolor, bgcolor, width, height, text, link=False, dir="."):
    ''' 'http://placehold.it/360x65/7F7FFF/7F0000.png&text=Some+text'  '''

    bgcolor = bgcolor[1:] # Remove #
    fgcolor = fgcolor[1:] # Remove #
    text=text.replace(" ", "+")
    text=text.replace("\n", "+")
    text=text.replace(":", "-")
    text=text.replace("(", "-")
    text=text.replace(")", "-")
    if text == "":
        text="__"
    size=str(width) + "x" + str(height)
    url = "http://placehold.it/" + size + "/" + bgcolor + "/" + fgcolor + \
          ".png&text=" + text
    file = dir + "/" + text + "_" + size + "_" + bgcolor + "_" + fgcolor + ".png"

    if not os.path.exists(file):
        # Download the file from `url` and save it locally under `file_name`:
        if VERBOSE:
            print("url=" + url)
            print("file=" + file)
        urllib.request.urlretrieve(url, file)

    return "<img src='" + file + "'/>"


'''
    def createColouredTextImage_magick(fgcolor, bgcolor, width, height, text):
        fgcolor: in #dddddd form, e.g. #7F7FFF
        bgcolor: in #dddddd form, e.g. #7F0000
'''
def createColouredTextImage_magick(fgcolor, bgcolor, width, height, text, link=False, dir="."):
    ''' 'http://placehold.it/360x65/7F7FFF/7F0000.png&text=Some+text'  '''

    REP_SPACE="+"
    fn_text=text
    fn_text=fn_text.replace(" ", REP_SPACE)
    fn_text=fn_text.replace("\n", REP_SPACE)
    fn_text=fn_text.replace(":", "-")
    fn_text=fn_text.replace("(", "-")
    fn_text=fn_text.replace(")", "-")

    if text=='':
        return ''

    '''
    convert -background '#ff8888' -fill '#0000ff' -font Candice -pointsize 72 label:"Some Text"           label.gif
    '''

    ''' list available fonts using convert -list font'''
    font_size=24
    font='DejaVu-Serif'

    rgb_bgcolor = bgcolor[1:] # Remove #
    rgb_fgcolor = fgcolor[1:] # Remove #
    file = dir + "/magick_{}_{}fs_{}_{}.png".format( fn_text, font_size, rgb_bgcolor, rgb_fgcolor)

    COMMAND="convert -background '{}' -fill '{}' -font {} -pointsize {} label:'{}' {}".format(bgcolor, fgcolor, font, font_size, text, file)

    if not os.path.exists(file):
        if VERBOSE:
            print("file=" + file)
            print(COMMAND)
        output = os.popen(COMMAND).read()

    if not os.path.exists(file):
        die("Failed to create file: <{}>".format(file))
   

    img_src= "<img src='" + file + "'/>"
    img_src = img_src.replace("#", "%23")
    return img_src


################################################################################
# Main:

xls_file = sys.argv[1]

if xls_file == "-table":
    HTML_PAGE=False
    xls_file = sys.argv[2]

if xls_file == "-page":
    HTML_PAGE=True
    xls_file = sys.argv[2]


'''
    formatting_info option only works on .xls not on .xlsx:

    NOTE: colouring will not work without formatting_info, so not on .xlsx files
'''

if ".xlsx" in xls_file:
    PROCESS_COLOR=False
    wb = xlrd.open_workbook(xls_file)
else:
    wb = xlrd.open_workbook(xls_file, formatting_info=True)

sheet_names = wb.sheet_names()
print(sheet_names)

for sheet_name in sheet_names:
    html_from_excel(wb, sheet_name, sheet_name+".html", HTML_PAGE)
    #csv_from_excel(wb, sheet_name, sheet_name+".csv")

if PROCESS_COLOR:
    write_color_index_table(wb, "COLORS_INDEX.html")
    write_color_table(wb, "COLORS.html")

