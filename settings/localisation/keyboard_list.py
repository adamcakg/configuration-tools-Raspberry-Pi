    
def get_keyboard_stuff():    
    models = []
    layouts = []
    variants = {}

    load = ''
    lang_code = ''
    with open('/usr/share/console-setup/KeyboardNames.pl','r') as file:
        line = file.readline()
        while line:
            
            if load == 'models':
                if '=>' in line:
                    line = line.replace(',', '').replace("'", "").lstrip().rstrip().split('=>')
                    models.append(line)
            if load == 'layouts':
                if '=>' in line:
                    line = line.replace(',', '').replace("'", "").lstrip().rstrip().split('=>')
                    layouts.append(line)
            if load == 'variants':
                if '{' in line:
                    lang_code = line.lstrip()[:5].replace("'", "").replace(' ', '')
                    variants[lang_code] = []
                    
                elif '=>' in line:
                    line = line.replace(',', '').replace("'", "").lstrip().rstrip().split('=>')
                    variants[lang_code].append(line)
            
            if '%models' in line:
                load = 'models'
                
            if '%layouts' in line:
                load = 'layouts'
            
            if '%variants' in line:
                load = 'variants'
            
            line = file.readline()
    return models, layouts, variants
