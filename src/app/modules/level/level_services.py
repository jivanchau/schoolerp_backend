from fastcrud import FastCRUD

from .level_model import LevelModel
from .level_schema import LevelCreate, LevelUpdate, LevelCreateInternal, LevelUpdateInternal, LevelDelete

CRUDLevel = FastCRUD[LevelModel, LevelCreateInternal, LevelUpdate, LevelUpdateInternal, LevelDelete]
levelServices = CRUDLevel(LevelModel)