from CNN_CLASSIFIER.constants import *
from CNN_CLASSIFIER.utils.common import read_yaml,create_directories
from CNN_CLASSIFIER.entity.config_entity import DataIngstionConfig,PrepareBaseModelConfig,TrainingConfig
import os

class ConfigurationManager:
    def __init__(self,
                 config_file_path=CONFIG_FILE_PATH,
                 params_file_path=PARAMS_FILE_PATH):
        
        self.config=read_yaml(config_file_path)
        self.params=read_yaml(params_file_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngstionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngstionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config
    
    
    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config=self.config.prepare_base_model

        create_directories([config.root_dir])

        prepare_base_model_config=PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_img_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weight=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )
        return prepare_base_model_config
    
    def get_training_config(self) -> TrainingConfig:
        training=self.config.training
        prepare_base_model=self.config.prepare_base_model
        params=self.params

        training_data=os.path.join(self.config.data_ingestion.unzip_dir,"Dataset")
        create_directories([
            Path(training.root_dir)
        ])

        training_config=TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            update_base_model_path=Path(prepare_base_model.updated_base_model_path),
            training_data=Path(training_data),
            params_epoch=params.Epochs,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_img_size=params.IMAGE_SIZE
        )

        return training_config
