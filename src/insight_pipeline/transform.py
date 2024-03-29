from pyspark.sql.functions import col, when, sum

def filter_dublicates_na(data):
    # Remove duplicates
    filtered_data = data.dropDuplicates()

    # Replace empty values with None 
    for column in filtered_data.columns:
        filtered_data = filtered_data.withColumn(column, \
            when(col(column) == "", None).otherwise(col(column)))

    # Drop rows with Null, NaN values
    filtered_data = filtered_data.na.drop()
    return filtered_data

def aggregate_data(data, grb_column: str, agg_column: str):
    #Converts the data in a column to type integer
    data = data.withColumn(agg_column , data[agg_column].cast('int'))
    
    # Aggregation
    agg_data = data.groupBy(grb_column).agg(sum(agg_column).alias(agg_column))

    return agg_data

def process_raw_data(raw_data):
    """
    Function for treatment raw data
    """
    filtered_data = filter_dublicates_na(raw_data)

    return filtered_data


def process_odl_data(odl_data, grb_column: str, agg_column: str):
    """
    Function for aggregation data from ods layer
    """
    aggregated_data = aggregate_data(odl_data, grb_column, agg_column)

    return aggregated_data