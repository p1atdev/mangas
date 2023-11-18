import humps
from pydantic import BaseModel, ConfigDict


# JSON のキーをすべてキャメルケースにキャストするモデル
class ForceCamelCaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(alias_generator=humps.camelize)
