from sys import maxsize


class Project:
    def __init__(self, name=None, status='development', inherit=True, view_status='public', description=None, id=None):
        self.name = name
        self.status = status
        self.inherit = inherit
        self.view_status = view_status
        self.description = description
        self.id = id

    # def __eq__(self, other):
    #     return self.name == other.name
    #
    # def __repr__(self):
    #     return "Project:name=%s" % self.name
    #
    # def key_by_name(self):
    #     return self.name
    #
    # def key(self):
    #     return self.name
    def __repr__(self):
        return "%s:%s:%s:%s:%s:%s" % (
            self.id, self.name, self.status, self.inherit, self.view_status, self.description)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
