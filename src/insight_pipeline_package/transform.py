from pyspark.sql.functions import col, when


def process_data(raw_data):
    # Remove duplicates
    processed_data = raw_data.dropDuplicates()

    # Replace empty values with Null
    for column in processed_data.columns:
        processed_data = processed_data.withColumn(column, \
            when(col(column) == "", None).otherwise(col(column)))

    # Drop rows with mostly Null values
    processed_data = processed_data.na.drop()

    return processed_data


def agg_data(raw_data):
    # Aggregation
    agg_data = raw_data.groupBy("Country", "City", "Product") \
                       .agg(sum("UnitsSold").alias("TotalUnitsSold"), sum("Revenue").alias("TotalRevenue"))

    return agg_data
