import pandas as pd # type: ignore
import sys
import utils

# Get input filename from command line
if len(sys.argv) <= 1:
    print('input file not defined')
    sys.exit(1)
elif len(sys.argv) <= 2:
    print('Missing trip distance column name')
    sys.exit(1)

file_path = sys.argv[1]

# Read the Parquet file into a DataFrame
df = pd.read_parquet(file_path)

# Check if we have trip distance column
column_name = str(sys.argv[2])
if column_name not in df.columns:
    print('No trip distance column found in file: ' + column_name)
    sys.exit(1)

# Calculate 90th percentile value
# Many trips can have the same distance, need to get the unique distances
unique_distances = df[column_name].unique()

# Sort trip distance in ascending order
sorted_distances = sorted(unique_distances)

# Determine number of distances in column
n = len(sorted_distances)

# Determine 90th percentile index
index_90th_percentile = int(0.9 * (n - 1))

# Get the distance from the column at the 90th percentile index
ninetieth_percentile = sorted_distances[index_90th_percentile]

# Get all rows with a trip distance greater than or equal to 90 percentile value
rows_in_90th_percentile = df[df[column_name] > ninetieth_percentile]

# Write out results to new parquet file
rows_in_90th_percentile.to_parquet(utils.insert_string(file_path, '-ninetieth_percentile'))

# Print results of execution
print("90th percentile value: " + str(ninetieth_percentile) + " miles")
print("Total number of trips: " + str(len(df)))
print ("Total number of trips in 90th percentile: " + str(len(rows_in_90th_percentile)))