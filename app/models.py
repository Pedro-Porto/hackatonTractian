from dataclasses import dataclass, field

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional



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


class Schedule(BaseModel):
    startTime: datetime
    endTime: datetime
    user: str

class Tool(BaseModel):
    toolName: str
    sapCode: str
    schedule: List[Schedule]

class ToolList(BaseModel):
    list_of_tools: List[str]

class Issue(BaseModel):
    number: int
    issue: str
    toolsCode: List[str]

class Machine(BaseModel):
    machineName: str
    machineId: int
    issues: List[Issue]

class MachineList(BaseModel):
    machine_list: List[Machine]

class EquipmentData(BaseModel):
    tools: List[Tool]
    #machines: List[Machine]
    machines: MachineList

class ServiceOrderData(BaseModel):
    orderText: str

class ToolUsage(BaseModel):
    toolCode: str
    startTime: datetime
    endTime: datetime
    username: str
