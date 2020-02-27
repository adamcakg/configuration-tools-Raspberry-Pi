from xml.etree import ElementTree 



def insert_font_into_xml(openbox_file_string, font):
        tree = ElementTree.fromstring(openbox_file_string)
        
        font = font.split()
        tree[0][0][0].text = font[0]
        tree[0][1][0].text = font[0]
        
        tree[0][0][1].text = font[-1]
        tree[0][1][1].text = font[-1]
        
        if 'Bold' in font:
            tree[0][0][2].text = 'Bold'
            tree[0][1][2].text = 'Bold'
        else:
            tree[0][0][2].text = 'Normal'
            tree[0][1][2].text = 'Normal'
            
        if 'Italic' in font:
            tree[0][0][3].text = 'Italic'
            tree[0][1][3].text = 'Italic'
        else:
            tree[0][0][3].text = 'Normal'
            tree[0][1][3].text = 'Normal'
            
        return '<?xml version="1.0"?>\n' + ElementTree.tostring(tree).decode()
    
# METHOD TO CONVERT COLOR TO HEX
# ---------------------------------------------------------------------------------------
def color_to_hex(color):
        color = color.split(',')
        color_string = '#'
        for index in range(len(color)):
            hex_temp_color = hex(int(color[index]))[2:] * 2
            if len(hex_temp_color) < 4:
                hex_temp_color += hex_temp_color
            color_string += hex_temp_color
        return color_string
    

