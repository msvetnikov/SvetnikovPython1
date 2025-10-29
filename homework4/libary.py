from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


# ЗАДАЧА 1: базовые модели

class Book(BaseModel):
    title: str
    author: str
    year: int = Field(ge=0, le=9999)
    available: bool = True
    categories: List[str] = Field(default_factory=list)

    @field_validator("title", "author")
    @classmethod
    def _strip_nonempty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Пустое значение")
        return v

    @field_validator("categories")
    @classmethod
    def _clean_categories(cls, cats: List[str]) -> List[str]:
        # нормализация и уникальность
        out, seen = [], set()
        for c in cats:
            c = c.strip()
            if c and c not in seen:
                seen.add(c)
                out.append(c)
        return out


class User(BaseModel):
    name: str
    email: EmailStr
    membership_id: str

    @field_validator("name", "membership_id")
    @classmethod
    def _strip_nonempty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Пустое значение")
        return v


# ЗАДАЧА 3: модель Library и метод

class Library(BaseModel):
    books: List[Book] = Field(default_factory=list)
    users: List[User] = Field(default_factory=list)

    def total_books(self) -> int:
        return len(self.books)

    def _find_book_index(self, title: str) -> Optional[int]:
        t = title.lower().strip()
        for i, b in enumerate(self.books):
            if b.title.lower().strip() == t:
                return i
        return None


# ЗАДАЧА 2: функции

def add_book(library: Library, book: Book) -> None:
    # защита от дублей по title+author
    key = (book.title.lower().strip(), book.author.lower().strip())
    for b in library.books:
        if (b.title.lower().strip(), b.author.lower().strip()) == key:
            raise ValueError("Книга уже есть")
    library.books.append(book)


def find_book(library: Library, title: str) -> Optional[Book]:
    idx = library._find_book_index(title)
    return library.books[idx] if idx is not None else None


def is_book_borrow(library: Library, title: str, user: User) -> bool:
    # только флаг доступности
    book = find_book(library, title)
    if not book or not book.available:
        return False
    book.available = False
    return True


def return_book(library: Library, title: str) -> bool:
    book = find_book(library, title)
    if not book or book.available:
        return False
    book.available = True
    return True


# демонстрация

if __name__ == "__main__":
    lib = Library()
    user = User(name="Ivan Petrov", email="ivan@example.com", membership_id="M-001")

    add_book(lib, Book(title="Три мушкетёра", author="А. Дюма", year=1844,
                       categories=["Роман", "Приключения"]))
    add_book(lib, Book(title="Чистый Python", author="Д. Бальцевич", year=2019,
                       categories=["Программирование"]))

    print("Всего книг:", lib.total_books())
    print("Есть ли 'Чистый Python':", find_book(lib, "чистый python") is not None)
    print("Взять 'Три мушкетёра':", is_book_borrow(lib, "Три мушкетёра", user))
    print("Доступна ли книга:", find_book(lib, "Три мушкетёра").available)
    print("Вернуть книгу:", return_book(lib, "Три мушкетёра"))
