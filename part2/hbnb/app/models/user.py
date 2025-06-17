from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def max_lenght(self):
        if len(self.first_name) <= 50 or len(self.last_name) <= 50 :
            pass
        else:
            raise ValueError("The number of characters must not exceed 50.")

    def is_required(self):
        if self.first_name == "":
            raise ValueError("This field is required.")

        if self.last_name == "":
            raise ValueError("This field is required.")

        if self.email == "":
            raise ValueError("This field is required.")

    def is_unique(self):
        pass

    def is_admin(self, username, boolean = False):
        admins = ["Guarick", "StrawberSam"]
        if username == admins:
            boolean = True
