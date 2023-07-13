from mongoengine import Document, StringField, ReferenceField, ListField ,FloatField
from .watershed import Watershed

class Typecontent(Document):

    """
    Represents the tipe of content.

    Attributes:
    ----------
    name: string
        name of the content.
        
    Methods:
    -------
    save()
        Saves the Group object to the database.
    delete()
        Deletes the Group object from the database.
    """

    meta = {
        'collection': 'typcontent'
    }
    name=StringField(max_length=100,required=True)