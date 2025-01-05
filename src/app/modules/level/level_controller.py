from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_superuser, get_current_user
from app.core.db.database import async_get_db
from app.core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from app.core.utils.cache import cache
from app.modules.level.level_services import levelServices
from app.crud.crud_users import crud_users
from app.modules.level.level_schema import LevelCreate, LevelRead, LevelUpdate, LevelCreateInternal


router = APIRouter(tags=["levels"])

@router.get('/levels', response_model=PaginatedListResponse[LevelRead])
# @cache(
#     key_prefix="levels:page_{page}:items_per_page:{items_per_page}",
#     expiration=60,
#     resource_id_type=str,
#     resource_id_name="all",
# )
async def read_levels(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    db_levels = await levelServices.get(db=db, schema_to_select=LevelRead)
    if not db_levels:
        raise NotFoundException("Levels not found")
    
    levels_data = await levelServices.get_multi(
        db=db,
        offset=compute_offset(page=page, items_per_page=items_per_page),
        limit=items_per_page,
        schema_to_select=LevelRead,
    )

    response: dict[str, Any] = paginated_response(crud_data=levels_data, page=page, items_per_page=items_per_page)
    return response


@router.post('/level', response_model=LevelRead, status_code=201)
async def write_level(
    request: Request,
    level: LevelCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> LevelRead:
    
    level_internal_dict = level.model_dump()
    level_internal = LevelCreateInternal(**level_internal_dict)

    created_level: LevelRead = await levelServices.create(db=db, object=level_internal)
    return created_level


@router.get('/level/{level_id}', response_model=LevelRead)
@cache(key_prefix="{level_id}_single_level", expiration=60, resource_id_name="level_id")
async def read_level(
    request: Request,
    level_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> LevelRead:
    db_level: LevelRead | None = await levelServices.get(db=db, levelID=level_id, schema_to_select=LevelRead)
    if not db_level:
        raise NotFoundException("Level not found")
    
    return db_level


@router.patch('/level/{level_id}', response_model=LevelRead)
async def patch_level(
    request: Request,
    level_id: int,
    level: LevelUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> LevelRead:
    db_level: LevelRead | None = await levelServices.get(db=db, levelID=level_id, schema_to_select=LevelRead)
    
    if not db_level:
        raise NotFoundException("Level not found")
    
    db_level['level_name'] = level.level_name
    await levelServices.update(db=db, object=level, levelID=level_id)
    return db_level
