from CEO.CEO_Manager_Tools.CEO_ML_Tools import CustomMLTool
from CEO.CEO_Manager_Tools.CEO_KA_Tools import CustomKATool
from CEO.CEO_Manager_Tools.CEO_QA_Tools import CustomKQATool
from CEO.CEO_Manager_Tools.CEO_Data_Collect_Tools import CustomDataCollectTool
from CEO.CEO_Manager_Tools.CEO_Open_Model_Tools import CustomOpenModelTool
from CEO.CEO_Manager_Tools.CEO_Auto_Lab_Tools import CustomAutoLabTool

CEO_tools_list = [
    CustomMLTool(),
    CustomKQATool(),
    CustomKATool(),
    CustomDataCollectTool(),
    CustomAutoLabTool()
]


available_departments = {"Material intelligence reasoning": CustomMLTool(),
                         "Self-driven learning": CustomKATool(),
                         "Memory expression": CustomKQATool(),
                         "Data acquisition": CustomDataCollectTool(),
                         "Auto Lab": CustomAutoLabTool()
                         }


def CEO_departments_huamn_choice(tools_list):

    CEO_tools_list = [available_departments[tool] for tool in tools_list]


    return CEO_tools_list