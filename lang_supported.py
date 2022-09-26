import json
import rich
from rich.console import Console
import pathlib
from rich.table import Table

console = Console()

def langs():
    # get the path of the json file
    my_path = pathlib.Path(__file__).parent.resolve() / "assets"
    lang_path = str(my_path) + "\\languages.json"

    # create a table
    table = Table(title="Languages Supported") 

    table.add_column("Language Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Code", style="bold green", justify="middle")

    # read the json file
    with open(lang_path, 'r') as json_file:
            json_load = json.load(json_file)
            
    data = json_load['supported_languages']

    # add the data to the table
    for key, value in data.items():
        table.add_row(key, value)
                
    console.print(table)