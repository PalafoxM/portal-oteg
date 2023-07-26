import os
from web.models import BarometroTuristico
from back.models import Reportes_Mensuales, Publications ,SeccionesCentroDocumental , Categorias
from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd
import datetime


# Replace with the actual path to your source folder
source_folder = "C:/Users/rogel/OneDrive/Escritorio/CEDOC/Pub"
# Replace with the actual path to your Excel file
excel_file_path = "C:/Users/rogel/OneDrive/Escritorio/CEDOC/publicaciones_keys_clean.xlsx"

month_to_number = {
    'ENERO': "1",
    'FEBRERO': "2",
    'MARZO': "3",
    'ABRIL': "4",
    'MAYO': "5",
    'JUNIO': "6",
    'JULIO': "7",
    'AGOSTO': "8",
    'SEPTIEMBRE': "9",
    'OCTUBRE': "10",
    'NOVIEMBRE': "11",
    'DICIEMBRE': "12"
}


def get_year_by_file_name(df, file_name):

    # Filter the DataFrame based on the provided file_name
    filtered_df = df[df['Nombre del archivo'] == file_name]

    # Check if there is any match for the given file_name
    if filtered_df.empty:
        return None  # Return None if no match is found
    else:
        # Retrieve the year value from the filtered DataFrame
        year = filtered_df['Año'].iloc[0]

        if year:
            return int(year)
        else:
            return 0


def get_monty_by_file_name(df, file_name):

    # Filter the DataFrame based on the provided file_name
    filtered_df = df[df['Nombre del archivo'] == file_name]

    # Check if there is any match for the given file_name
    if filtered_df.empty:
        return None  # Return None if no match is found
    else:
        # Retrieve the year value from the filtered DataFrame
        monty = filtered_df['Mes'].iloc[0]
        return monty


def get_name_by_file_name(df, file_name):

    # Filter the DataFrame based on the provided file_name
    filtered_df = df[df['Nombre del archivo'] == file_name]

    # Check if there is any match for the given file_name
    if filtered_df.empty:
        return None  # Return None if no match is found
    else:
        # Retrieve the name value from the filtered DataFrame
        name = filtered_df['Título del documento'].iloc[0]
        return name


def get_type_by_file_name(df, file_name):

    # Filter the DataFrame based on the provided file_name
    filtered_df = df[df['Nombre del archivo'] == file_name]

    # Check if there is any match for the given file_name
    if filtered_df.empty:
        return None  # Return None if no match is found
    else:
        # Retrieve the type value from the filtered DataFrame
        type_doc = filtered_df['Tipo de archivo'].iloc[0]
        return type_doc


def get_section_by_file_name(df, file_name):
    # Assuming the 'section' field in the DataFrame is named 'SectionName'.
    section_name = df[df['Nombre del archivo'] == file_name]['Sección'].iloc[0]   

    # Look for the 'section' instance in the database using the extracted name.

    print('Seccion_pub:',section_name)
    try:
        section = SeccionesCentroDocumental.objects.get(seccion=section_name)
        return section
    except SeccionesCentroDocumental.DoesNotExist:
        return None
    
def get_category_by_file_name(df, file_name ,seccion):

    # Assuming the 'category' field in the DataFrame is named 'CategoryName'.
    category_name = df[df['Nombre del archivo'] == file_name]['Subsección'].iloc[0]

    # Look for the 'category' instance in the database using the extracted name.
    # Look for the 'category' instance in the database using the extracted name and section.
    try:
        category = Categorias.objects.get(nombre_categoria=category_name, seccion=seccion)
    except Categorias.DoesNotExist:
        # If the category does not exist, create a new one and save it to the database.
        category = Categorias(nombre_categoria=category_name, fecha_creacion=datetime.date.today(), seccion=seccion)
        category.save()

    return category



def load_files_to_model_pub():

    df = pd.read_excel(excel_file_path)

    for file_name in os.listdir(source_folder):

        source_path = os.path.join(source_folder, file_name)

        try:
            # Create a BarometroTuristico instance and set its attributes

            publication = Publications()
            publication.name = str(get_name_by_file_name(df, file_name))

            # Assuming you have a function to get the type from the file name.

            publication.type = get_type_by_file_name(df, file_name)

            publication.visible = True  # Defaulting to True.

            # Set the section and category fields based on the corresponding values from the DataFrame.
            publication.section = get_section_by_file_name(df, file_name)
            publication.category = get_category_by_file_name(df, file_name , publication.section)

            # Assuming you are using the S3 storage backend for the doc field
            # Set the doc field to the S3 URL of the uploaded file

            with open(source_path, "rb") as f:
                publication.doc.save(file_name, f)

            publication.save()

            print(f"Loaded '{file_name}' into the model.")

        except Exception as e:
            print(f"Error loading '{file_name}': {e}")


class Command(BaseCommand):
    help = 'Load files from a folder into a model'

    def handle(self, *args, **kwargs):
        load_files_to_model_pub()
