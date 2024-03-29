from insight_pipeline.pipeline_config import PipelineConfig
from insight_pipeline.ingest import read_data
from insight_pipeline.load import write_data
from insight_pipeline.transform import process_raw_data, process_odl_data
from insight_pipeline.utils import get_spark_session

def run_pipeline(config: PipelineConfig):
       """
    All stages of the pipeline execution 
    
    Args:
      PipelineConfig  :  class with all the pipeline settings
    """
       spark = get_spark_session(config.session_name)

       print(f'Start reading data from: {config.input_data_file} ...')
       raw_data = read_data(config.input_data_file, spark)
       print('Data loaded')

       print('Start processing RAW data...')
       ods_data = process_raw_data(raw_data)
       print('RAW Data processed')
       
       print(f'Start uploading ODS data to {config.output_ods_path}...')
       write_data(ods_data, config.output_ods_path)
       print('ODS Data uploaded')

       print('Start processing DML data...')
       dml_data = process_odl_data(ods_data, config.grb_column, config.agg_column)
       print('DML Data processed')
       
       print(f'Start uploading DML data to {config.output_dml_path}...')
       write_data(dml_data, config.output_dml_path)
       print('DML Data uploaded')

