from .crud_user import user
from .crud_role import role
from .crud_domain import domain
from .crud_domain_user import domain_user
from .crud_feedback import feedback
from .crud_tags import tags
from .crud_upgrade_requests import upgrade_requests
from .crud_data_requests import data_requests
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
