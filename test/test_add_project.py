from model.project import Project
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits *5
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_add_project(app):
    app.session.login("administrator", "root")
    # app.project.open_project_page()
    old_project_list = app.project.get_projects_list()
    for x in old_project_list:
        print(x)
    project = Project(name=(random_string("test", 10)), status="stable", inherit=True,
                      view_status="public", description="test description")
    app.project.create(project)
    new_project_list = app.project.get_projects_list()
    old_project_list.append(project)
    # assert sorted(new_project_list, key=Project.key) == sorted(old_project_list, key=Project.key)
    assert sorted(old_project_list, key=Project.id_or_max) == sorted(new_project_list, key=Project.id_or_max)