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

class UserAnswer(BaseModel):
    '''Ответ пользователя'''
    question_id: int
    answer: str = Field(description="Строка с ответом пользователя")

# создать класс UserAnswer(question_id, answer), SubmitQuizRequest(имя пользователя, его имейл, id теста, список ответов)  
# создать по 2 объетка классов 1 с правильными параметрами 1 с неправильными

try:
    q = Question(id = 10, text = "Столица России", options=["Москва", "Ярославль"])
    print(q)
except ValidationError:
    print("Введите корректные данные")
user = Player(username="Kirill", email="kirill@gmail.com", score=100, correct_answers=5, wrong_answers=4)
test = Test(id = 10, name = " test", questions = [q])
print(user)
# class Question_not_pydantic:
#     def __init__(self, id, text, options):
#         self.id = id
#         self.text = text
#         self.options = options
    
#     def __str__(self):
#         return f"id={self.id} text={self.text} options={self.options}"




# q2 = Question_not_pydantic(id = "10A", text = "Столица России", options=["Москва", 10])

# print(q2)
