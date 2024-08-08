from pydantic import BaseModel


# Handle the token data schema later

# class TokenData(BaseModel):

class Token(BaseModel):
    access_token: str
    token_type: str
