import os 
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation,DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig, ModelTriner

@dataclass
class DataIngestionConfig:
  raw_data_path:str= os.path.join('artifacts', 'data.csv')
  train_data_path:str = os.path.join('artifacts', 'train.csv')
  test_data_path:str = os.path.join('artifacts', 'test.csv')

class DataIngestion:
  def __init__(self):
    self.ingestion_config = DataIngestionConfig()

  def initiate_data_ingestion(self):
    try:
      df= pd.read_csv('notebook/data/stud.csv')
      logging.info("Entered the Data Ingestion Method")

      os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
      df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

      logging.info("Train Test Split Initiated")
      train_set, test_set = train_test_split(df, train_size=0.2, random_state=42)

      train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
      test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

      logging.info("Train Test Split completed")

      return (
        self.ingestion_config.train_data_path,
        self.ingestion_config.test_data_path
      )

    except Exception as e:
      raise CustomException(e,sys)

if __name__ == "__main__":
  data_obj = DataIngestion()
  train_path, test_path = data_obj.initiate_data_ingestion()

  data_transformation = DataTransformation()
  train_arr, test_arr, _= data_transformation.initiate_data_transformation(train_path, test_path)

  model_trainer = ModelTriner()
  print(model_trainer.initiate_model_trainer(train_array=train_arr, test_array=test_arr))

