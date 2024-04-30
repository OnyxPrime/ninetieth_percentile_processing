# 90th Percentile Trip Finder
The 90th percentile trip finder will find all trips in the 90th percentile distance traveled from a given `parquet` file containing a series of trip information. It will then output the results to a new file.

## USAGE:

### Prerequisites
Install the following packages, if not already installed: `pandas` and `pyarrow`
```bash
pip install pandas pyarrow
```

### Program Execution
Run the trip finder with the following command, replacing the necessary placeholders.
```bash
python trip_percentile `<FILE_LOCATION_TO_BE_PROCESSED>` `<COLUMN_NAME_FOR_TRIP_DISTANCE>`
```

ex.
```bash
python trip_percentile .sample_data/green_tripdata_2024-01.parquet trip_distance
```

### Sample Data
A set of `parquet` files, obtained from the [NYC Taxi and Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) trip record data site, is provided in the root directory. The column containing each trips distance is `trip_distance`.

## How it works
The trip finder relies on 2 python packages, `pandas` and `pyarrow`, to consume the data from the `parquet` file. `pandas` will load the `parquet` object from the file and convert it to a `DataFrame`. `DataFrame` is a 2 dimensional data structure, similar to a table with rows and columns. 

```python
import pandas as pd 

df = pd.read_parquet(filename)
```

Once the data is loaded, we need to determine what trip distance falls at the 90th percentile.

Since some, or many, trip distances could have the same values, we need to start by getting only the unique distances and sorting them in ascending order.
```python
unique_distances = df[column_name].unique()

sorted_distances = sorted(df[column_name])
```

Next, calculate the index at the 90th percentile
```python
n = len(sorted_distances)

index_90th_percentile = int(0.9 * (n - 1))
```

Lastly, get the distance at the 90th percentile
```python
ninetieth_percentile = sorted_distances[index_90th_percentile]
```

With the 90th percentile value, the program will grab all the trips from the `DataFrame` where the trip distance is greater than the 90th percentile value determined above.
```python
rows_in_90th_percentile = df[df[column_name] >= ninetieth_percentile]
```

Finally, output the data to a new file.
```python
rows_in_90th_percentile.to_parquet(utils.insert_string(filename, '-ninetieth_percentile'))
```