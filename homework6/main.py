from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

# Простой калькулятор на FastAPI: базовые операции и вычисление строковых выражений

app = FastAPI(title="Простой калькулятор API", version="1.0.0")

# ==== МОДЕЛИ ====
class BinOpBody(BaseModel):
    a: float = Field(..., description="Левый операнд")
    b: float = Field(..., description="Правый операнд")

class BuildExprBody(BaseModel):
    a: float
    op: Literal['+','-','*','/']
    b: float
    as_group: bool = Field(True, description="Оборачивать кусок в скобки")

class AppendRawBody(BaseModel):
    expr: str = Field(..., description="Фрагмент выражения для добавления")

class EvalBody(BaseModel):
    expr: str  # выражение целиком

# ==== СОСТОЯНИЕ (демо) ====
_current_expression: str = ""

def _get_current_expression() -> str:
    return _current_expression or "0"

def _append_to_expression(part: str) -> str:
    global _current_expression
    _current_expression = (_current_expression + part).strip()
    return _current_expression

def _reset_expression():
    global _current_expression
    _current_expression = ""

# ==== ПАРСЕР (шунтирующий двор) ====
class ParseError(ValueError):
    pass

_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}


def _tokenize(expr: str):
    """Разбиваем строку на токены; поддерживаем унарный минус."""
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1; continue
        if ch in '+-*/()':
            if ch == '-':  # унарный минус -> вставляем 0
                prev = tokens[-1] if tokens else None
                if prev in (None, '+', '-', '*', '/', '('):
                    tokens.append('0')
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == '.':
            j = i; dots = 0
            while j < n and (expr[j].isdigit() or expr[j] == '.'):
                if expr[j] == '.':
                    dots += 1
                    if dots > 1:
                        raise ParseError("Некорректное число")
                j += 1
            tokens.append(expr[i:j])
            i = j
        else:
            raise ParseError(f"Неизвестный символ: {ch}")
    return tokens


def _to_rpn(tokens):
    """Инфикс -> ОПН (RPN)."""
    out, stack = [], []
    for tok in tokens:
        if tok.replace('.', '', 1).isdigit():
            out.append(tok)
        elif tok in _PRECEDENCE:
            while stack and stack[-1] in _PRECEDENCE and _PRECEDENCE[stack[-1]] >= _PRECEDENCE[tok]:
                out.append(stack.pop())
            stack.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(':
                out.append(stack.pop())
            if not stack:
                raise ParseError("Несогласованные скобки")
            stack.pop()
        else:
            raise ParseError(f"Неожиданный токен: {tok}")
    while stack:
        top = stack.pop()
        if top in ('(', ')'):
            raise ParseError("Несогласованные скобки")
        out.append(top)
    return out


def _eval_rpn(rpn):
    """Вычисляем ОПН."""
    stack = []
    for tok in rpn:
        if tok in _PRECEDENCE:
            try:
                b = stack.pop(); a = stack.pop()
            except IndexError:
                raise ParseError("Неверное выражение")
            if tok == '+': stack.append(a + b)
            elif tok == '-': stack.append(a - b)
            elif tok == '*': stack.append(a * b)
            elif tok == '/':
                if b == 0: raise ZeroDivisionError("Деление на ноль")
                stack.append(a / b)
        else:
            stack.append(float(tok))
    if len(stack) != 1:
        raise ParseError("Неверное выражение")
    return stack[0]


def evaluate_expression(expr: str) -> float:
    tokens = _tokenize(expr)
    rpn = _to_rpn(tokens)
    return _eval_rpn(rpn)

# ==== БАЗОВЫЕ ОПЕРАЦИИ ====
@app.post("/add")
def add(body: BinOpBody):
    return {"result": body.a + body.b}

@app.post("/subtract")
def subtract(body: BinOpBody):
    return {"result": body.a - body.b}

@app.post("/multiply")
def multiply(body: BinOpBody):
    return {"result": body.a * body.b}

@app.post("/divide")
def divide(body: BinOpBody):
    if body.b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль")
    return {"result": body.a / body.b}

# ==== КОНСТРУКТОР ВЫРАЖЕНИЯ ====
@app.post("/expression/append")
def append_raw(body: AppendRawBody):
    expr = body.expr.strip()
    if not expr:
        raise HTTPException(status_code=400, detail="Пустой фрагмент")
    return {"current_expression": _append_to_expression(expr)}

@app.post("/expression/build")
def build_from_parts(body: BuildExprBody):
    part = f"({body.a}{body.op}{body.b})" if body.as_group else f"{body.a}{body.op}{body.b}"
    return {"current_expression": _append_to_expression(part)}

@app.get("/expression")
def get_expression():
    return {"current_expression": _get_current_expression()}

@app.post("/expression/reset")
def reset_expression():
    _reset_expression()
    return {"current_expression": _get_current_expression()}

@app.post("/expression/eval")
def eval_current():
    try:
        result = evaluate_expression(_get_current_expression())
        return {"expression": _get_current_expression(), "result": result}
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ParseError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга: {e}")

# ==== РАЗОВОЕ ВЫЧИСЛЕНИЕ ====
@app.post("/eval")
def eval_expr(body: EvalBody):
    try:
        result = evaluate_expression(body.expr)
        return {"expression": body.expr, "result": result}
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ParseError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга: {e}")

# ==== ПРОВЕРКА ЖИВЫ ЛИ ====
@app.get("/")
def root():
    return {
        "message": "Калькулятор запущен",
        "endpoints": [
            "/add", "/subtract", "/multiply", "/divide",
            "/expression/append", "/expression/build", "/expression", "/expression/reset", "/expression/eval",
            "/eval"
        ]
    }
