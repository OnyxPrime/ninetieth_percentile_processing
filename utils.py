def insert_string(filename, string_to_insert):
    # Find the index of ".parquet" in the filename
    index = filename.find(".parquet")
    
    # If ".parquet" is found, insert the string before it
    if index != -1:
        modified_filename = filename[:index] + string_to_insert + filename[index:]
        return modified_filename
    else:
        # If ".parquet" is not found, return the original filename
        return filename