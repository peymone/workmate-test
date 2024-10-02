from pydantic import BaseModel


class AddCat(BaseModel):

    name: str
    age: int
    color: str
    breed: str


class AddCatSucess(BaseModel):

    message: str = "New cat successfully added to database"


class UpdateCatSucess(BaseModel):

    message: str = "Cat successfully updated"


class DeleteCatSucess(BaseModel):

    message: str = "Cat successfully deleted"
