# destinos
destinos={'abasolo' : 'abasolo',
    'acambao' : 'acambaro',
    'acambaro' : 'acambaro',
    'acámbaro' : 'acambaro',
    'apaseo el alto' : 'apaseo el alto',
    'apaseo el grande' : 'apaseo el grande',
    'apaseo el grande, comonfort, san miguel allende,dolores hidalgo cin, san felipe, ocampo' : 'estado de guanajuato',
    'atarjea' : 'atarjea',
    'celaya' : 'celaya',
    'comonfort' : 'comonfort',
    'coroneo' : 'coroneo',
    'cortazar' : 'cortazar',
    'cueramaro' : 'cueramaro',
    'cuerámaro' : 'cueramaro',
    'doctor mora' : 'doctor mora',
    'dolores hidalgo' : 'dolores hidalgo cin',
    'dolores hidalgo cin' : 'dolores hidalgo cin',
    'dolores hidalgo cuna de la independencia nacional' : 'dolores hidalgo cin',
    'estado' : 'estado de guanajuato',
    'estado de guanajuato' : 'estado de guanajuato',
    'estatal' : 'estado de guanajuato',
    'guanajuato' : 'guanajuato',
    'huanímaro' : 'huanímaro',
    'irapuato' : 'irapuato',
    'jaral del progreso' : 'jaral del progreso',
    'jerecuaro' : 'jerecuaro',
    'jerécuaro' : 'jerecuaro',
    'juventino rosas' : 'juventino rosas',
    'leon' : 'león',
    'león' : 'león',
    'manuel doblado' : 'manuel doblado',
    'mineral de pozos / san luis de la paz' : 'mineral de pozos',
    'moroleón' : 'moroleón',
    'ocampo' : 'ocampo',
    'penjamo' : 'penjamo',
    'pénjamo' : 'penjamo',
    'pueblo nuevo' : 'pueblo nuevo',
    'purisima del rincon' : 'purisima del rincon',
    'purísima del rincón' : 'purisima del rincon',
    'purisima del rincón' : 'purisima del rincon',
    'resto de estado' : 'estado de guanajuato',
    'romita' : 'romita',
    'salamanca' : 'salamanca',
    'salvatierra' : 'salvatierra',
    'san diego de la union' : 'san diego de la union',
    'san diego de la unión' : 'san diego de la union',
    'san felipe' : 'san felipe',
    'san franccisco del rincón' : 'san francisco del rincón',
    'san francisco del  rincon' : 'san francisco del rincón',
    'san francisco del rincon' : 'san francisco del rincón',
    'san francisco del rincón' : 'san francisco del rincón',
    'san josé iturbide' : 'san josé iturbide',
    'san luis de la paz' : 'san luis de la paz',
    'san miguel de allende' : 'san miguel de allende',
    'san migue de allende' : 'san miguel de allende',
    'san miguel de allende / comonfort' : 'san miguel de allende',
    'santa catarina' : 'santa catarina',
    'santa cruz de juventino rosas' : 'santa cruz de juventino rosas',
    'santiago maravatio' : 'santiago maravatio',
    'santiago maravatío' : 'santiago maravatio',
    'silao' : 'silao',
    'silao de la victoria' : 'silao',
    'tarandacuao' : 'tarandacuao',
    'tarimoro' : 'tarimoro',
    'tierra blanca' : 'tierra blanca',
    'uriangato' : 'uriangato',
    'valle de santiago' : 'valle de santiago',
    'varios municipios' : 'estado de guanajuato',
    'victoria' : 'victoria',
    'villagran' : 'villagran',
    'villagrán' : 'villagran',
    'xichu' : 'xichu',
    'xichú' : 'xichu',
    'yuriria' : 'yuriria'
    }

# Categorías
categorias={'5 estrellas' : '5 estrellas',
            '5 etrellas' : '5 estrellas',
            '5 e' : '5 estrellas',
            '5' : '5 estrellas',
            '4 estrellas' : '4 estrellas',
            '4 etrellas' : '4 estrellas',
            '4 e' : '4 estrellas',
            '4' : '4 estrellas',
            '3 estrellas' : '3 estrellas',
            '3 etrellas' : '3 estrellas',
            '3 e' : '3 estrellas',
            '3' : '3 estrellas',
            '2 estrellas' : '2 estrellas',
            '2 etrellas' : '2 estrellas',
            '2 e' : '2 estrellas',
            '2' : '2 estrellas',
            '1 estrellas' : '1 estrella',
            '1 etrellas' : '1 estrella',
            '1 e' : '1 estrella',
            '1' : '1 estrella',
            '1 estrella':'1 estrella',
            'sc' : 'sc',
            'sin calsinficar' : 'sc',
            'sin clasificacion' : 'sc',
            'sin clasificación' : 'sc',
            'sin categoría': 'sc'}

# Limpiar columnas de tipo str
def clean_str_col(value):
    # Convierte a string
    value = str(value)
    # Limpia espacios al principio y al final
    value = value.strip()
    # Reemplaza \n por espacios
    value = value.replace("\n"," ")
    # Convierte a minúsculas
    value = value.lower()
    # Limpia espacios al principio y al final de nuevo
    value = value.strip()
    return value

def homologar_columna_destino(destino):
    if destino in destinos:
        return destinos[destino]
    else:
        return destino
    
def homologar_columna_categoria(categoria):
    if categoria in categorias:
        return categorias[categoria]
    else:
        return categoria
