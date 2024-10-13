import os

class Config:
    """
    Base configuration class with default settings.
    Inherit this class to define environment-specific configurations.
    """
    # Flask settings
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

    # Google Cloud Project settings
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-default-gcp-project-id")
    
    # BigQuery settings
    DATASET_NAME = os.getenv("DATASET_NAME", "geotech_dataset")
    TABLE_NAME = os.getenv("TABLE_NAME", "geospatial_data")

    # Flask App settings
    JSONIFY_PRETTYPRINT_REGULAR = True

class DevelopmentConfig(Config):
    """
    Development environment-specific configuration.
    """
    DEBUG = True
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-dev-gcp-project-id")

class TestingConfig(Config):
    """
    Testing environment-specific configuration.
    """
    TESTING = True
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-test-gcp-project-id")

class ProductionConfig(Config):
    """
    Production environment-specific configuration.
    """
    DEBUG = False
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-prod-gcp-project-id")
    
def get_config():
    """
    Retrieves the configuration class based on the FLASK_ENV environment variable.
    If not set, defaults to 'development'.
    """
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
