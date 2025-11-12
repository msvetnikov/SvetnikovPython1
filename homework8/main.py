# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date, datetime
from pathlib import Path
import re, json

# Сервис сбора обращений абонентов
app = FastAPI(title="Сервис абонентов — Задание 1")

# ==== МОДЕЛЬ ====
class Subscriber(BaseModel):
    last_name: str = Field(..., description="Фамилия: кириллица, с заглавной")
    first_name: str = Field(..., description="Имя: кириллица, с заглавной")
    birth_date: date = Field(..., description="Дата рождения YYYY-MM-DD")
    phone: str = Field(..., description="Телефон: +7XXXXXXXXXX или 8XXXXXXXXXX")
    email: EmailStr = Field(..., description="E-mail")

    # Фамилия/имя: кириллица, первая буква заглавная; допускается дефис
    @field_validator("last_name", "first_name")
    @classmethod
    def cyrillic_capital(cls, v: str) -> str:
        if not re.fullmatch(r"[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?", v):
            raise ValueError("Только кириллица, первая буква заглавная (допустим дефис).")
        return v

    # Дата рождения: не в будущем и не старше 120 лет
    @field_validator("birth_date")
    @classmethod
    def birth_not_future(cls, v: date) -> date:
        today = date.today()
        if v > today:
            raise ValueError("Дата рождения не может быть в будущем.")
        if today.year - v.year > 120:
            raise ValueError("Нереалистичный возраст.")
        return v

    # Телефон: нормализуем к виду +7XXXXXXXXXX
    @field_validator("phone")
    @classmethod
    def phone_ru(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)
        if len(digits) != 11 or digits[0] not in {"7", "8"}:
            raise ValueError("Ожидается 11 цифр и код страны 7/8. Пример: +7XXXXXXXXXX.")
        return "+7" + digits[1:]


# Папка для сохранения
DATA_DIR = Path("submissions")
DATA_DIR.mkdir(exist_ok=True)

# ==== ЭНДПОИНТ ====
@app.post("/subscribe")
def create_subscriber(item: Subscriber):
    # Сохраняем JSON на диск
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{item.last_name}_{item.first_name}_{ts}.json".replace(" ", "_")
    path = DATA_DIR / fname
    with path.open("w", encoding="utf-8") as f:
        json.dump(item.model_dump(), f, ensure_ascii=False, indent=2)
    return {"status": "ok", "file": str(path)}

@app.get("/")
def root():
    return {"message": "Сервис абонентов запущен", "endpoint": "/subscribe"}

# Локальный запуск: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)