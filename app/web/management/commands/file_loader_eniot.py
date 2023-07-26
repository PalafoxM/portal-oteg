import os
from web.models import BarometroTuristico
from back.models import Eniot
from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd

source_folder = "C:/Users/rogel/OneDrive/Escritorio/CEDOC/Eniot"  # Replace with the actual path to your source folder
destination_folder = "barometro-turistico"  # Destination folder in S3 (if applicable)
excel_file_path = "C:/Users/rogel/OneDrive/Escritorio/CEDOC/eniot_keys.xlsx"  # Replace with the actual path to your Excel file

def get_year_by_file_name(df, file_name):

    # Filter the DataFrame based on the provided file_name
    filtered_df = df[df['Nombre del archivo'] == file_name]

    # Check if there is any match for the given file_name
    if filtered_df.empty:
        return None  # Return None if no match is found
    else:
        # Retrieve the year value from the filtered DataFrame
        year = filtered_df['Subsección'].iloc[0]
        return year
    
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
    
def load_files_to_model():

    df = pd.read_excel(excel_file_path)


    for file_name in os.listdir(source_folder):

        source_path = os.path.join(source_folder, file_name)
        
        try:
            # Create a BarometroTuristico instance and set its attributes
            eniot = Eniot()
            eniot.nombrePDF = str(get_name_by_file_name(df,file_name)) + " " + str(get_year_by_file_name(df,file_name))
            eniot.anio =  get_year_by_file_name(df,file_name)
            eniot.seccion = "ponencia-eventos"

            
            with open(source_path, "rb") as f:
                eniot.doc_url.save(file_name, f)

            eniot.save()
            
            print(f"Loaded '{file_name}' into the model.")

        except Exception as e:
            print(f"Error loading '{file_name}': {e}")


class Command(BaseCommand):
    help = 'Load files from a folder into a model'

    def handle(self, *args, **kwargs):
        load_files_to_model()