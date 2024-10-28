from typing import Annotated
from fastapi import FastAPI, File, UploadFile, Body
from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Body, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer



app = FastAPI()


SECRET_KEY = "secret_key_here"  # Substitua por uma chave secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Classes para autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Funções auxiliares para gerenciar usuários
fake_users_db = {
    "user1": {
        "username": "user1",
        # Use a pre-hashed password for testing purposes
        "hashed_password": "$2b$12$KIXsP2G9HVHsjFlSLIh3lu.f3/WJxwI3gTa6Zub6eKuul7/6.eVhy",  # Hash for 'password1'
        "disabled": False,
    }
}


class Schedule(BaseModel):
    startTime: datetime
    endTime: datetime
    user: str

class Tool(BaseModel):
    toolName: str
    sapCode: str
    schedule: List[Schedule]

class Issue(BaseModel):
    number: int
    issue: str
    toolsCode: List[str]

class Machine(BaseModel):
    machineName: str
    machineId: int
    issues: List[Issue]

class EquipmentData(BaseModel):
    tools: List[Tool]
    machines: List[Machine]

class ServiceOrderData(BaseModel):
    orderText: str

class ToolUsage(BaseModel):
    toolCode: str
    startTime: datetime
    endTime: datetime
    username: str



"""


retorna
{
    tools: [
        {toolName: "", sapCode: "", schedule: [
            {
                startTime: datetime,
                endTime: datetime,
                user: ""
            }
        ]}
    ]


    machines: [
        {
            machineName: "aaaa",
            machineId: 123,
            issues: [
                {number: 1, issue: "aaaaa", toolsCode: ["", ""]},
                {number: 2, issue: "aaaaa", toolsCode: ["", ""]},
            ]
        }
    ]

}
"""
def listIssuesAndMachines(orderText) -> EquipmentData:
    # chama a llm para colocar o nome, id e problemas (sem codigo de ferramenta)
    return

def listTools(equipmentData: EquipmentData) -> EquipmentData:
    #coloca a lista de ferramentas com o schedule
    return


def findTools(equipmentData: EquipmentData) -> EquipmentData:
    # llm adiciona ferramentas necessarias para cada problema (apenas o sapCode)
    return 



def fillServiceOrder(orderText: str) -> EquipmentData:
    equipmentData = listIssuesAndMachines(orderText)
    equipmentData = listTools(equipmentData)
    equipmentData = findTools(equipmentData)
    return equipmentData



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependência para verificar o token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Rotas protegidas com autenticação
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}





@app.post("/serviceOrder/audio")
async def serviceOrderAudio(
    file: UploadFile, current_user: User = Depends(get_current_user)
):
    orderText = ""  # Logic to process the audio
    return fillServiceOrder(orderText)

@app.post("/serviceOrder/text")
async def serviceOrderText(
    data: ServiceOrderData = Body(...), current_user: User = Depends(get_current_user)
):
    return fillServiceOrder(data.orderText)


"""
[
    {order: EquipmentData, done: bool}
]

"""
@app.get("/userOrders")
async def userOrders(
    current_user: User = Depends(get_current_user)
):
    # pega no db todas as ordens antigas
    return 



"""
[
    {
        toolCode: "",
        startTime: datetime,
        endTime: datetime
        username: ""
    }
]
"""
@app.post("/toolUsage")
async def toolUsage(
    data: List[ToolUsage] = Body(...), current_user: User = Depends(get_current_user)
):
    # alterar no servidor a disponibilidade das ferramentas e adicionar nas ordens
    return 


"""
query: {
    machineId: 123
}
retorno:

{
    manuals: [
        {name: "", link: ""},
        {name: "", link: ""}
    ],
    videos: [
        {name: "", link: ""},
        {name: "", link: ""}
    ],
    summaries: "",
    suggestions: [
        {name: "", link: ""},
        {name: "", link: ""}
    ]
}


"""
@app.get("/manual")
async def manual(
    current_user: User = Depends(get_current_user)
):
    # pega no db a ordem atual
    # manda para a llm com o id da maquina para sumarizar os manuais dessa maquina
    return 



"""
MongoDB:

EquipmentData:
{
    date: datetime,
    tools: [
        {toolName: "", sapCode: "", schedule: [
            {
                startTime: datetime,
                endTime: datetime,
                user: ""
            }
        ]}
    ]


    machines: [
        {
            machineName: "aaaa",
            machineId: 123,
            issues: [
                {number: 1, issue: "aaaaa", toolsCode: ["", ""]},
                {number: 2, issue: "aaaaa", toolsCode: ["", ""]},
            ]
        }
    ]

}


collection: users
{
    username: "",
    hashed_password: "",
    disabled: bool
}
collection: orders
{
    username: "",
    orders: [
        {
            order: EquipmentData, #sem campo tools
            done: bool
        }
    ]
}

collection: tools
{
    toolName: "",
    sapCode: "",
    category: "",
    schedule: [
        {
            startTime: datetime,
            endTime: datetime,
            user: ""
        }
    ]
    
}

collection: manuals
[
    {
        name: "",
        path: ""
    }
]



"""



"""

POST /serviceOrder
headers:
 - ContentType
body: texto/audio
retorna:
ferramentas (da llm) -> mandar codigo sap
lista das maquinas
lista de problemas

POST /toolUsage
body: ferramentas que serao utilizadas e horario de utilizacao




GET /manual
query: nome da maquina
query: problemas da maquina
manuais oficiais
videos
resumos dos manuais oficiais e videos oficiais

lista de sugestoes (links) para mais informacoes (internet)





"""