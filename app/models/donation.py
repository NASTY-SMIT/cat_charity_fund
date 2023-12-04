from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import Parent


class Donation(Parent):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
