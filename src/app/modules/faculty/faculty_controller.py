from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_superuser, get_current_user
from app.core.db.database import async_get_db
from app.core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from app.core.utils.cache import cache
from app.modules.faculty.faculty_services import facultyServices
from app.crud.crud_users import crud_users
from app.modules.faculty.faculty_schema import FacultyCreate, FacultyRead, FacultyUpdate, FacultyCreateInternal

router = APIRouter(tags=["faculties"])

@router.get('/faculties', response_model=PaginatedListResponse[FacultyRead])
async def read_faculties(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    db_faculties = await facultyServices.get(db=db, schema_to_select=FacultyRead)
    if not db_faculties:
        raise NotFoundException("Faculties not found")
    
    faculties_data = await facultyServices.get_multi(
        db=db,
        offset=compute_offset(page=page, items_per_page=items_per_page),
        limit=items_per_page,
        schema_to_select=FacultyRead,
    )
    
    response: dict[str, Any] = paginated_response(crud_data=faculties_data, page=page, items_per_page=items_per_page)
    return response

