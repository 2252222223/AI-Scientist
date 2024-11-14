
from DB.DB_Manager_Tools.MIR_tools.Pearson import HotMaPDraw
from DB.DB_Manager_Tools.MIR_tools.RandomForest_tool import RF_Regression
from DB.DB_Manager_Tools.MIR_tools.NN_tool import NN_Regression
from DB.DB_Manager_Tools.MIR_tools.XGB_tool import XGB_Regression
from DB.DB_Manager_Tools.MIR_tools.GP_tool import GP_Regression
from DB.DB_Manager_Tools.MIR_tools.SHAP_tool import SHAP
from DB.DB_Manager_Tools.MIR_tools.Query_CSV_tool import Query_CSV
from DB.DB_Manager_Tools.MIR_tools.python_agent_tools.Py_tool import Py_shell
from CEO.CEO_Manager_Tools.CEO_Open_Model_Tools import CustomOpenModelTool
Query_CSV_tool = Query_CSV()
NN_tool = NN_Regression()
Pearson_tool = HotMaPDraw()
Rf_tool = RF_Regression()
XGB_tool = XGB_Regression()
GP_tool = GP_Regression()
Shap_tool = SHAP()
PY_tool = Py_shell()
open_model = CustomOpenModelTool()
ml_tools_list = [GP_tool, Pearson_tool, Rf_tool, NN_tool, XGB_tool, Query_CSV_tool, Shap_tool, PY_tool, open_model]

# NN_tool.run({"task":"Train_only","f_path":"CO2吸附.xlsx"})