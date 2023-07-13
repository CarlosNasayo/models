from mongoengine import Document, StringField, ReferenceField, ListField ,FloatField
from .waterpoint import Waterpoint
from .type_content import Typecontent

class Wpcontent(Document):

    """
    Represents a waterpoint content in the database.

    Attributes:
    ----------
    content: array
        array with the content.
    type: Typecontent
        reference of the typecontent id.
    watershed: Watershed
        reference of the Watershed id.
   
    Methods:
    -------
    save()
        Saves the Group object to the database.
    delete()
        Deletes the Group object from the database.
    """

    meta = {
        'collection': 'wpcontent'
    }
    content=ListField(required=True)
    watershed=ReferenceField(Waterpoint)
    type= ReferenceField(Typecontent)