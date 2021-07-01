from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, String


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __repr__(self, input_str=None):
        """
        Model representation on the admin panel
        """
        res_string = f"<{self.__tablename__}: "

        if input_str:
            res_string += f"{input_str}>"
            return res_string

        res_string += f"id: {self.id}; "

        try:
            name = self.name
            res_string += f"name: {name}; "
        except AttributeError:
            pass

        try:
            cake_id = self.cake_id
            res_string += f"cake_id: {cake_id}"
        except AttributeError:
            pass

        res_string += ">"

        return res_string


class UserBase(Base):
    __tablename__ = "user"
    search_id = Column(String)
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    job_title = Column(String)

    def __repr__(self, input_str=None):
        return super().__repr__(f"{self.email} {self.id}")