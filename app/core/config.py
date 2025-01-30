from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET : str
    TITLE: str = Field(default = "Fast Api", title = "Title of Api")
    DESCRIPTION : str = Field(default = "Vehicles Api to Register Vehicle", description = "description of api" )
    VERSION : str = Field ( default = "0.0.1", version = "version of Api")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
# Creating object of Setting class
settings = Settings() 
 



