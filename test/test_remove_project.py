from model.project import Project
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits * 5
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_remove_random_project(app):
    app.session.login("administrator", "root")
    old_project_list = app.project.get_projects_list()
    if len(old_project_list) == 0:
        app.project.create(Project(name=random_string("test", 10), description="test_description"))
        old_project_list = app.project.get_projects_list()
    project = random.choice(old_project_list)
    app.project.remove_project_by_id(project.id)
    old_project_list.remove(project)
    new_project_list = app.project.get_projects_list()
#     assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)
