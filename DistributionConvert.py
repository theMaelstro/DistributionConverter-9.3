# ==================================================================================
#   Made by MAEL
#   Script designed to convert distribution table from old format to 9.3 compliant.
#   Output is formatted in CSV.
# ==================================================================================

# Importing pandas library
import pandas as pd
import time
from module_mael import *

import os
import glob
import argparse

# Convert CSV
def convert():
    # Start Timer.
    start_time = time.time()
    
    # Find files and store in list filenames.
    file_location = os.path.join(args.file_path)
    filenames = glob.glob(file_location)
    
    message("Looking for files. Filter: {}".format(file_location), "warning")
    message("Found {} files: {}".format(len(filenames), [file for file in filenames]), "info")
    
    
    # Set output CSV name.
    output_filename = "distribution_items.csv"
    
    # Define CSV column headers and NULL type.
    cols = ["distribution_id", "item_type", "item_id", "quantity"]
    rows = []
    empty = ""
    data_set = pd.DataFrame(rows, columns=cols)

    # Open csv file
    file = filenames[0]
    message("{} Reading CSV".format(file))
    
    # Read distributions .csv file.
    df = pd.read_csv(file,
        # Define headers for distributions.csv if it has none after export.
        header=None,    
        names=["id", "character_id", "type", "deadline", "event_name", "description", "times_acceptable", "min_hr", "max_hr", "min_sr", "max_sr", "min_gr", "max_gr", "data"],)
    # Sort table by id.
    df.sort_values(by=['id'])

    # Iterate all rows.
    for index, row in df.iterrows():
        # Set id which is the distribution_id in new .csv file.
        col_id = row['id']
        # Clean raw string.
        col_data = row['data'].replace('\\x','')
        if len(col_data) == 0:
            col_data = None
        # Define number of items in string and remove that information from data.
        if col_data != None:
            number_of_items = int(col_data[0:4], 16)
            col_data = col_data[4:]
        else:
            number_of_items = None
        
        # If set, prepare data.
        if col_data != None:
            # For number of items extract single item string.
            for i in range(number_of_items):
                item_string = col_data[26*i:26*(i+1)]
                # Extract item info from string.
                item_type = int(item_string[0:2], 16)
                item_unk1 = item_string[2:6]
                item_id = int(item_string[6:10], 16)
                item_unk2 = item_string[10:14]
                item_quantity = int(item_string[14:18], 16)
                item_unk3 = item_string[18:]
                
                # Append row to output table.
                message("Appending Rows")
                rows.append({
                        "distribution_id": col_id,
                        "item_type": item_type,
                        "item_id": item_id,
                        "quantity": item_quantity
                        })
    
    # Writing dataframe to csv
    df = pd.DataFrame(rows, columns=cols)
    message("Writing to: {}".format(output_filename), "warning")
    df.index.name = 'id'
    df.to_csv(output_filename, header=None)
    message(df)
    message("Finished %.2f seconds" % (time.time() - start_time), "info")

# Main function body.
def main():
    # Initialize parser
    parser = argparse.ArgumentParser()
     
    # Adding optional argument    
    parser.add_argument('file_path', metavar='Path', help = "Define filter for input files. Use asterisk (*) for wildcard.")
    parser.add_argument("-p", "--Prefix", default = "", help = "Define prefix for output filename. Default None.")
     
    # Read arguments from command line
    args = parser.parse_args()

    convert()

# Call main function.
if __name__ == "__main__":
    main()