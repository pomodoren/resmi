from ... import dict_admins, db, models

from .issues import IssueView

admin = dict_admins["m6_feedback"]

admin.add_view(IssueView(models.Issue, db.session, name="Issues"))
