# observatory API parser

This module contains functions for parsing responses received from API's, and in particular those recieved from Observatory API's. The aim is to format the responses into the same structure making the outputs more usable in applications combining datasets from different observatories.

# Functions
#### convert_csv_to_json:
   <br/>Definition: This takes a csv response the Sheffield urban observatory API and transforms into JSON of the same format of that returned from the Newcastle Urban Observatory API.
   <br/>
   <br/>Accepts: API response string
   <br/>Return: JSON
  
#### convert_api_json_to_geojson:
   <br/>This function takes a JSON string and converts it to GeoJSON.
   <br/>
   <br/>Accepts: JSON string
   <br/>Returns: GeoJSON
   
# Requirements
python3 (any version)
    
