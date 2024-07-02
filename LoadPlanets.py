factor_aumento = 2

planets = {
    'sun': {
                'image_path':'./Planets_INFO/sun/sun.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':70.0*factor_aumento,
                'rotation_ratio_relative_to_earth': 0.0,
                'revolution_ratio_relative_to_earth': 0.0,
                'distance_from_sun':0.0,
                'Material_ambient': [ 0.5, 0.5, 0.5, 1.0],
                'Material_diffuse': [ 0.17, 0.17, 0.17, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.95],
                },
    'mercury': {
                'image_path':'./Planets_INFO/mercury/mercury.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':8.38*factor_aumento, #Aqui se modifica el tamaño con respecto al sol
                'rotation_ratio_relative_to_earth': 0.58,
                'revolution_ratio_relative_to_earth': 0.5,
                'distance_from_sun':150.98*factor_aumento,             # modifique Distancia con respecto al sol
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.15, 0.15, 0.15, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.98],
                },
    'venus': {
                'image_path':'./Planets_INFO/venus/venus.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':8.95*factor_aumento, #Modifique el tamaño
                'rotation_ratio_relative_to_earth': 0.23,
                'revolution_ratio_relative_to_earth': 0.3,
                'distance_from_sun':200.24*factor_aumento,             # modifique Distancia con respecto al sol
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.18, 0.18, 0.18, 1.0],
                'Material_specular': [ 0.9, 0.9, 0.9, 1.0],
                'Material_shininess': [0.98],
                },
    'earth': {
                'image_path':'./Planets_INFO/earth/earth.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':8.0*factor_aumento, #Modifique el tamaño
                'rotation_ratio_relative_to_earth': 1,
                'revolution_ratio_relative_to_earth': 0.01,
                'distance_from_sun':250.96*factor_aumento,         # modifique Distancia con respecto al sol
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.4, 0.5, 0.4, 1.0],
                'Material_specular': [ 0.9, 1.0, 0.9, 1.0],
                'Material_shininess': [0.95],
                },
    'mars': {
                'image_path':'./Planets_INFO/mars/mars.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':8.53*factor_aumento, #Modifique el tamaño
                'rotation_ratio_relative_to_earth': 0.9,
                'revolution_ratio_relative_to_earth': 0.13,
                'distance_from_sun':350.6*factor_aumento,                  # modifique Distancia con respecto al sol
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.15, 0.15, 0.15, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.95],
                },
    'jupiter': {
                'image_path':'./Planets_INFO/jupiter/jupiter.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':11.2*factor_aumento, #moddifique el tamaño
                'rotation_ratio_relative_to_earth': 1.4,
                'revolution_ratio_relative_to_earth': 0.005,
                'distance_from_sun':590.8*factor_aumento,                  # modifique Distancia con respecto al sol
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.15, 0.15, 0.15, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.95],
                },
    'saturn': {
                'image_path':'./Planets_INFO/saturn/saturn.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':9.45*factor_aumento,
                'rotation_ratio_relative_to_earth': 1.6,
                'revolution_ratio_relative_to_earth': 0.003,
                'distance_from_sun':890.8*factor_aumento,
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.15, 0.15, 0.15, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.95],
                },
    'uranus': {
                'image_path':'./Planets_INFO/uranus/uranus.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':10.0*factor_aumento,
                'rotation_ratio_relative_to_earth': 1.3,
                'revolution_ratio_relative_to_earth': 0.002,
                'distance_from_sun':1784.0*factor_aumento,
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.15, 0.15, 0.15, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.95],
                },
    'neptune': {
                'image_path':'./Planets_INFO/neptune/neptune.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':10.88*factor_aumento,
                'rotation_ratio_relative_to_earth': 1.2,
                'revolution_ratio_relative_to_earth': 0.001,
                'distance_from_sun':2193*factor_aumento,
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.15, 0.15, 0.15, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.95],
                },
    'stars': {
                'image_path':'./Planets_INFO/StarsMap.jpg',
                'texture':'',
                'size_ratio_relative_to_earth':2000*factor_aumento,
                'rotation_ratio_relative_to_earth': 0.0,
                'revolution_ratio_relative_to_earth': 0.0,
                'distance_from_sun':0,
                'Material_ambient': [ 0.4, 0.4, 0.4, 1.0],
                'Material_diffuse': [ 0.15, 0.15, 0.15, 1.0],
                'Material_specular': [ 1.0, 1.0, 1.0, 1.0],
                'Material_shininess': [0.95],
                }
}                