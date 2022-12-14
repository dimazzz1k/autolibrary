from sqlalchemy import update, select
from sqlalchemy.orm import Session
from pydantic import BaseModel as Schema

from db.models import (
    Base as Model, 
    Book, 
    BookType, 
    BookGenre, 
    Publisher, 
    Department, 
    BookDecommision, 
    Student, 
    BookState
)
from db.schemas import (
    BookCreate, 
    BookPatch, 
    BookTypeCreate, 
    BookGenreCreate, 
    PublisherCreate, 
    DepartmentCreate, 
    BookDecommisionCreate, 
    StudentCreate, 
    BookStateCreate
)
from db.password import get_hashed_password


class RepoBase:
    def __init__(self, session: Session, model: Model):
        self._session = session
        self._model = model

    def create(self, item: Schema) -> Model:
        session = self._session
        
        db_item = self._model(**item.dict())
        
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        
        return db_item
    
    def read_by_id(self, item_id: int) -> Model | None:
        session = self._session
        
        db_item = session.get(self._model, item_id)
        
        return db_item
        
    def update(self, item: Schema, item_id: int) -> bool:
        session = self._session

        db_item = self.read_by_id(item_id)
        
        if not db_item:
            return False

        stmt = (
            update(self._model)
            .where(self._model.id == item_id)
            .values(item.dict())
        )
        
        session.execute(stmt)
        session.commit()
        
        return True
        
    def delete(self, item_id: int) -> bool:
        session = self._session
        
        db_item = self.read_by_id(item_id)
        
        if not db_item:
            return False
        
        session.delete(db_item)
        session.commit()
        
        return True


class BookRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Book)
    
    def create(self, item: BookCreate) -> Book:
        book = super().create(item=item)
        
        return book
    
    def read_pending(self) -> list[Book | None]:
        session = self._session
        
        stmt = (
            select(Book)
            .join(Book.state)
            .where(BookState.name == "?? ??????????????????")
        )
    
        books = session.scalars(stmt).all()
        
        return books
    
    def read_by_id(self, item_id: int) -> Book | None:
        book = super().read_by_id(item_id=item_id)
        
        return book
  
    def read(self) -> list[Book | None]:
        session = self._session
        
        stmt = select(Book)
        
        books = session.scalars(stmt).all()
        
        return books
    
    
    def patch(self, item: BookPatch, item_id: int) -> bool:
        session = self._session
        
        db_item = self.read_by_id(item_id)
        
        if not db_item:
            return False
        
        stmt = (
            update(Book)
            .where(Book.id == item_id)
            .values(item.dict())
        )
    
        session.execute(stmt)
        session.commit()
        
        return True
    
    def update(self):
        pass
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response
        

class BookTypeRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=BookType)
    
    def create(self, item: BookTypeCreate) -> BookType:
        book_type = super().create(item=item)
        
        return book_type
    
    def read_by_id(self, item_id: int) -> BookType | None:
        book_type = super().read_by_id(item_id=item_id)
        
        return book_type
  
    def read(self, name: str | None = None) -> list[BookType | None]:
        session = self._session
        
        stmt = select(BookType)
        
        if name:
            stmt = stmt.where(BookType.name == name)
        
        book_types = session.scalars(stmt).all()
        
        return book_types

    def update(self, item: BookTypeCreate, item_id: int) -> bool:
        response = super().update(item=item, item_id=item_id)
        
        return response
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response


class BookGenreRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=BookGenre)
    
    def create(self, item: BookGenreCreate) -> BookGenre:
        book_genre = super().create(item=item)
        
        return book_genre
    
    def read_by_id(self, item_id: int) -> BookGenre | None:
        book_genre = super().read_by_id(item_id=item_id)
        
        return book_genre
  
    def read(self, name: str | None = None) -> list[BookGenre | None]:
        session = self._session
        
        stmt = select(BookGenre)
        
        if name:
            stmt = stmt.where(BookGenre.name == name)
        
        book_genres = session.scalars(stmt).all()
        
        return book_genres

    def update(self, item: BookGenreCreate, item_id: int) -> bool:
        response = super().update(item=item, item_id=item_id)
        
        return response
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response


class PublisherRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Publisher)
    
    def create(self, item: PublisherCreate) -> Publisher:
        publisher = super().create(item=item)
        
        return publisher
    
    def read_by_id(self, item_id: int) -> Publisher | None:
        publisher = super().read_by_id(item_id=item_id)
        
        return publisher
  
    def read(self, name: str | None = None, city: str | None = None) -> list[Publisher | None]:
        session = self._session
        
        stmt = select(Publisher)
        
        if name:
            stmt = stmt.where(Publisher.name == name)
        if city:
            stmt = stmt.where(Publisher.city == city)
        
        publishers = session.scalars(stmt).all()
        
        return publishers

    def update(self, item: PublisherCreate, item_id: int) -> bool:
        response = super().update(item=item, item_id=item_id)
        
        return response
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response
        
        
class DepartmentRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Department)
    
    def create(self, item: DepartmentCreate) -> Department:
        department = super().create(item=item)
        
        return department
    
    def read_by_id(self, item_id: int) -> Department | None:
        department = super().read_by_id(item_id=item_id)
        
        return department
  
    def read(self, name: str | None = None) -> list[Department | None]:
        session = self._session
        
        stmt = select(Department)
        
        if name:
            stmt = stmt.where(Department.name == name)
        
        departments = session.scalars(stmt).all()
        
        return departments

    def update(self, item: DepartmentCreate, item_id: int) -> bool:
        response = super().update(item=item, item_id=item_id)
        
        return response
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response       
        
        
class BookDecommisionRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=BookDecommision)
    
    def create(self, item: BookDecommisionCreate) -> BookDecommision:
        book_decommision = super().create(item=item)
        
        return book_decommision
    
    def read_by_id(self, item_id: int) -> BookDecommision | None:
        book_decommision = super().read_by_id(item_id=item_id)
        
        return book_decommision
  
    def read(self, books_total: int | None = None) -> list[BookDecommision | None]:
        session = self._session
        
        stmt = select(BookDecommision)
        
        if books_total:
            stmt = stmt.where(BookDecommision.books_total == books_total)
        
        book_decommisions = session.scalars(stmt).all()
        
        return book_decommisions

    def update(self, item: BookDecommisionCreate, item_id: int) -> bool:
        response = super().update(item=item, item_id=item_id)
        
        return response
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response
        

class StudentRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=Student)
    
    def create(self, item: StudentCreate) -> Student:
        session = self._session
        
        hashed_password = get_hashed_password(item.password)
        
        student = Student(
            first_name=item.first_name,
            last_name=item.last_name,
            login=item.login,
            hashed_password=hashed_password
        )
        
        session.add(student)
        session.commit()
        session.refresh(student)
        
        return student
    
    def read_by_id(self, item_id: int) -> Student | None:
        student = super().read_by_id(item_id=item_id)
        
        return student
  
    def read(
        self, 
        first_name: str | None = None, 
        last_name: str | None = None, 
        login: str | None = None
    ) -> list[Student | None]:
        session = self._session
        
        stmt = select(Student)
        
        if first_name:
            stmt = stmt.where(Student.first_name == first_name)
        if last_name:
            stmt = stmt.where(Student.last_name == last_name)
        if login:
            stmt = stmt.where(Student.login == login)
        
        students = session.scalars(stmt).all()
        
        return students

    def update(self, item: StudentCreate, item_id: int) -> bool:
        session = self._session
        
        student = self.read_by_id(item_id)
        
        if not student:
            return False
        
        hashed_password = get_hashed_password(item.password)
        
        stmt = (
            update(Student)
            .where(Student.id == item_id)
            .values(
                first_name=item.first_name,
                last_name=item.last_name,
                login=item.login,
                hashed_password=hashed_password
            )
        )
        
        session.execute(stmt)
        session.commit()
        
        return True
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response


class BookStateRepo(RepoBase):
    def __init__(self, session: Session):
        super().__init__(session=session, model=BookState)
    
    def create(self, item: BookStateCreate) -> BookState:
        book_state = super().create(item=item)
        
        return book_state
    
    def read_by_id(self, item_id: int) -> BookState | None:
        book_state = super().read_by_id(item_id=item_id)
        
        return book_state
  
    def read(self, name: str | None = None) -> list[BookState | None]:
        session = self._session
        
        stmt = select(BookState)
        
        if name:
            stmt = stmt.where(BookState.name == name)
        
        book_states = session.scalars(stmt).all()
        
        return book_states

    def update(self, item: BookStateCreate, item_id: int) -> bool:
        response = super().update(item=item, item_id=item_id)
        
        return response
    
    def delete(self, item_id: int) -> bool:
        response = super().delete(item_id=item_id)
        
        return response