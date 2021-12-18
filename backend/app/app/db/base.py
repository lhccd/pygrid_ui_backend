# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.pdf import PDFObject # noqa
from app.models.roles import Role # noqa
from app.models.feedback import Feedback # noqa
