from pydantic import BaseModel, ValidationError, EmailStr, Field

class Question(BaseModel):
    id: int 
    text: str
    options: list[str]

class Player(BaseModel):
    username: str
    email: EmailStr
    score: int | None = Field(ge = 0, le = 100)
    correct_answers: int | None = Field(ge = 0)
    wrong_answers: int | None = Field(ge = 0)

class Test(BaseModel):
    '''Тест со всеми вопросами по определенной теме'''
    id: int
    name: str = Field(description="Name of test")
    questions: list[Question]

class Answer(BaseModel):
    '''Правильный Ответ на вопрос'''
    question_id: int
    text: str

# создать класс UserAnswer(question_id, answer), SubmitQuizRequest(имя пользователя, его имейл, список ответов)

class UserAnswer(BaseModel):
    user: str
    emeil: EmailStr
    answers: list[Question]


user = Player(username="Kirill", email="kirill@gmail.com", score=100, correct_answers=5, wrong_answers=4)
print(user)
# class Question_not_pydantic:
#     def __init__(self, id, text, options):
#         self.id = id
#         self.text = text
#         self.options = options
    
#     def __str__(self):
#         return f"id={self.id} text={self.text} options={self.options}"

# try:
#     q = Question(id = 10, text = "Столица России", options=["Москва", 10])
#     print(q)
# except ValidationError:
#     print("Введите корректные данные")


# q2 = Question_not_pydantic(id = "10A", text = "Столица России", options=["Москва", 10])

# print(q2)
