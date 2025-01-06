from fastcrud import FastCRUD

from .faculty_model import FacultyModel
from .faculty_schema import FacultyCreateInternal, FacultyDelete, FacultyUpdate, FacultyUpdateInternal

CRUDFaculty = FastCRUD[FacultyModel, FacultyCreateInternal, FacultyUpdate, FacultyUpdateInternal, FacultyDelete]
facultyServices = CRUDFaculty(FacultyModel)