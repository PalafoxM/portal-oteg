import os
from web.models import BarometroTuristico
from back.models import Reportes_Mensuales
from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd

source_folder = "C:/Users/rogel/OneDrive/Escritorio/CEDOC/Boletines"  # Replace with the actual path to your source folder
excel_file_path = "C:/Users/rogel/OneDrive/Escritorio/CEDOC/boletines_keys.xlsx"  # Replace with the actual path to your Excel file

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

        if year :
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
    
def load_files_to_model_boletines():

    df = pd.read_excel(excel_file_path)
    df['Mes'] = df['Mes'].map(month_to_number)
    df['Mes'] = df['Mes'].fillna("1")


    for file_name in os.listdir(source_folder):

        source_path = os.path.join(source_folder, file_name)

        try:
            # Create a BarometroTuristico instance and set its attributes
            reporte = Reportes_Mensuales()
            reporte.titulo = str(get_name_by_file_name(df,file_name)) + " " + str(get_year_by_file_name(df,file_name))
            reporte.ano =  get_year_by_file_name(df,file_name)
            reporte.mes = get_monty_by_file_name(df,file_name)

            # Assuming you are using the S3 storage backend for the doc field
            # Set the doc field to the S3 URL of the uploaded file
            with open(source_path, "rb") as f:
                reporte.doc.save(file_name, f)

            reporte.save()
            
            print(f"Loaded '{file_name}' into the model.")

        except Exception as e:
            print(f"Error loading '{file_name}': {e}")




class Command(BaseCommand):
    help = 'Load files from a folder into a model'

    def handle(self, *args, **kwargs):
        load_files_to_model_boletines()