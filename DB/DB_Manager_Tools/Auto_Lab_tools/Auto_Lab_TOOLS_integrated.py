
from DB.DB_Manager_Tools.Auto_Lab_tools.XRD_tool import XRD_tool
from DB.DB_Manager_Tools.Auto_Lab_tools.soild_phase_synthesis_tool import Solid_synthesis_tool
from DB.DB_Manager_Tools.Auto_Lab_tools.recipes_parse_tool import Recipes_tool
from DB.DB_Manager_Tools.Auto_Lab_tools.auto_lab_universal_task_submission_tool import Universal_task_tool
XRD_tool = XRD_tool()
Solid_synthesis_tool = Solid_synthesis_tool()
recipes_tool = Recipes_tool()
auto_lab_task = Universal_task_tool()
Auto_lab_tools_list = [recipes_tool, auto_lab_task]
