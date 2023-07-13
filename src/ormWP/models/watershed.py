from mongoengine import Document, StringField, ReferenceField, ListField ,FloatField
from .adm3 import Adm3

class Watershed(Document):

    """
    Represents a watershed in the database.

    Attributes:
    ----------
    name: str
        Name of the watershed.
    area: float
        Crop object that the group belongs to. Mandatory.
    adm3: Adm3
        Adm3 reference.
    traced: array
        array with created time, updated and a active 

    Methods:
    -------
    save()
        Saves the Group object to the database.
    delete()
        Deletes the Group object from the database.
    """

    meta = {
        'collection': 'watershed'
    }
    area=FloatField(max_length=100,required=True)
    name=StringField(max_length=100,required=True)
    traced=ListField(required=True)
    adm3=ReferenceField(Adm3,required=True)