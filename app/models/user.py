from pydantic import BaseModel



class RegistrationUser(BaseModel):
    userID: int 
    username: str
    password: str
    
