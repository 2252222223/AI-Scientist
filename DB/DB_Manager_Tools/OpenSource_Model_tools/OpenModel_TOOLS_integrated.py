
from DB.DB_Manager_Tools.OpenSource_Model_tools.Query_CSV_tool import Query_CSV
from DB.DB_Manager_Tools.OpenSource_Model_tools.Py_tool import Py_shell
from DB.DB_Manager_Tools.OpenSource_Model_tools.OpenModelPre import Open_Model_Pre
from DB.DB_Manager_Tools.OpenSource_Model_tools.OpenModelTransf import Open_Model_Tra


Open_Model_Pre_tool = Open_Model_Pre()
Open_Model_Tra_tool = Open_Model_Tra()
Query_CSV_tool = Query_CSV()
PY_tool = Py_shell()

singal_Open_model_tools_list = [Open_Model_Pre_tool, Open_Model_Tra_tool]
Open_model_tools_list =[Open_Model_Pre_tool, Open_Model_Tra_tool, Query_CSV_tool, PY_tool]