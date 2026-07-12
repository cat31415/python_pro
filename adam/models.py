from pydantic import BaseModel, ValidationError, EmailStr, Field

class Question(BaseModel):
    id: int 
    text: str
    options: list[str]

class Player(BaseModel):
    username: str
    email: EmailStr
    score: int | None = Field(default=None, ge=0, le=99)
    correct_answers: int | None = Field(default=None, ge=0)
    wrong_answers: int | None = Field(default=None, ge=0)

class Test(BaseModel):
    '''Тест со всеми вопросами по определенной теме'''
    id: int
    name: str = Field(description="Name of test")
    questions: list[Question]

class Answer(BaseModel):
    '''Правильный Ответ на вопрос'''
    question_id: int
    text: str

class UserAnswer(BaseModel):
    question_id: int
    answer: str

class SubmitQuizRequest(BaseModel):
    username: str
    email: EmailStr
    answers: list[UserAnswer]

user = Player(username="Kirill", email="kirill@gmail.com", score=99, correct_answers=6, wrong_answers=0)
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

class Question_not_pydantic:
    def __init__(self, id, text, options):
        self.id = id
        self.text = text
        self.options = options
    
    def __str__(self):
        return f"id={self.id} text={self.text} options={self.options}"

try:
    q = Question(id=10, text="Столица России", options=["Москва", 10])
    print(q)
except ValidationError:
    print("")

q2 = Question_not_pydantic(id="10A", text="Столица России", options=["Москва", 10])
print(q2)
