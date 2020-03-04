import os

def insert_font_into_xml(openbox_file_string, font):
    font = font.split()
    file = openbox_file_string.replace('"', "'")
    file = file.split('\n')

    for index in range(len(file)):
        if 'font' in file[index]:
            file[index+1] = '\t\t<name>' + font[0] + '</name>'
            file[index + 2] = '\t\t<size>' + font[-1] + '</size>'
            
            if 'Bold' in font:
                file[index + 4] = '\t\t<weight>' + 'Bold' + '</weight>'
            else:
                file[index + 4] = '\t\t<weight>' + 'Normal' + '</weight>'
                
            if 'Italic' in font:
                file[index + 6] = '\t\t<slant>' + "Italic" + '</slant>'
            else:
                file[index + 6] = '\t\t<slant>' + "Normal" + '</slant>'

    return '\n'.join(file)
    
def insert_color_in_xml(openbox_file_string, typ, color):
    file = openbox_file_string.replace('"', "'")
    file = file.split('\n')
    if typ == 'bg':
        for index in range(len(file)):
            if 'titleColor' in file[index]:
                file[index] = '<titleColor>' + color + '</titleColor>'
    elif typ == 'fg':
        for index in range(len(file)):
            if 'textColor' in file[index]:
                file[index] = '<textColor>' + color + '</textColor>'
    return '\n'.join(file)
    
# METHOD TO CONVERT COLOR TO HEX
# ---------------------------------------------------------------------------------------
def color_to_short_hex(color):
    color = color.split(',')
    for index in range(len(color)):
        color[index] = int(color[index])
    return '#%02x%02x%02x' % tuple(color)

def color_to_hex(color):
        color = color.split(',')
        color_string = '#'
        for index in range(len(color)):
            hex_temp_color = hex(int(color[index]))[2:] * 2
            if len(hex_temp_color) < 4:
                hex_temp_color += hex_temp_color
            color_string += hex_temp_color
        return color_string
    

