import re

from selenium.webdriver.support.select import Select

from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    project_cache = None

    def create(self, project):
        wd = self.app.wd
        if wd.current_url.endswith("/manage_proj_create_page.php"):
            self.create_page(project)
        else:
            self.open_project_page()
            wd.find_element_by_xpath("//input[@value='Create New Project']").click()
            wd.implicitly_wait(2)
            self.create_page(project)
            wd.implicitly_wait(20)

    def create_page(self, project):
        wd = self.app.wd
        self.fill_project_from("name", project.name)
        self.select_dropdown_field("status", project.status)
        self.select_dropdown_field("view_state", project.view_status)
        self.fill_project_from("description", project.description)
        if not (wd.find_element_by_name("inherit_global").is_selected() == project.inherit):
            wd.find_element_by_name("inherit_global").click()
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        wd.implicitly_wait(10)

    def remove_project_by_id(self, proj_id):
        wd = self.app.wd
        self.open_project_page()
        self.select_project(proj_id)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.implicitly_wait(2)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()

    def fill_project_from(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def select_dropdown_field(self, field_name, text):
        wd = self.app.wd
        wd.find_element_by_name(field_name).click()
        Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)

    def open_project_page(self):
        wd = self.app.wd
        if wd.current_url.endswith("/manage_proj_page.php"):
            return
        wd.find_element_by_link_text("Manage").click()
        wd.implicitly_wait(2)
        wd.find_element_by_link_text("Manage Projects").click()

    def select_project(self, proj_id):
        wd = self.app.wd
        wd.find_element_by_css_selector('[href="manage_proj_edit_page.php?project_id=%s"]' % proj_id).click()

    def get_projects_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            wd.implicitly_wait(20)
            self.open_project_page()
            self.project_cache = []
            for element in wd.find_elements_by_css_selector(
                          "table.width100 tbody [class='row-1'], table.width100 tbody [class='row-2']"):
                proj_id = int(element.find_element_by_tag_name("a").get_attribute("href")[-2:].replace('=', '0'))
                name = element.find_element_by_css_selector('td:nth-of-type(1)').text
                status = element.find_element_by_css_selector('td:nth-of-type(2)').text
                description = element.find_element_by_css_selector('td:nth-of-type(5)').text
                if description == "":
                    description = None
                self.project_cache.append(
                    Project(id=proj_id, name=self.clear(name), status=self.clear(status),
                            description=self.clear(description)))
            return list(self.project_cache)

    def clear(self, s):
        if s is None:
            pass
        else:
            return re.sub("[() -]", "", s)

#    def get_projects_list(self):
#     if self.project_cache is None:
#         wd = self.app.wd
#         self.open_project_page()
#         self.project_cache = []
#         for element in wd.find_elements_by_css_selector(
#                 "table.width100 tbody [class='row-1'], table.width100 tbody [class='row-2']"):
#             project_id = int(element.find_element_by_css_selector('[href*="manage_proj_edit_page.php?project_id="]')
#                              .get_attribute('href')[-2:].replace('=', '0'))
#             name = element.find_element_by_css_selector('td:nth-of-type(1)').text
#             description = element.find_element_by_css_selector('td:nth-of-type(5)').text
#             if description == "":
#                 description = None
#             self.project_cache.append(
#                 Project(id=project_id, name=self.clear(name), description=self.clear(description)))
#         return list(self.project_cache)
