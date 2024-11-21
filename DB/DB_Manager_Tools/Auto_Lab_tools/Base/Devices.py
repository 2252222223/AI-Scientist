import uuid

def uuid_genrate():
    # 生成一个新的 GUID
    guid = uuid.uuid4()
    return str(guid)



def get_WLDWT_all_parameters():
    data = {"id": uuid_genrate(),
   "name": "物料定位台",
   "workingHours": "1",
   "data": {"workingHours": 1,      #工作时长
    "robotJob": 1,      #机器人任务：1：取料 2：放料
    "selContainer": 1,  # 选择的实验容器或耗材种类  1: 反应釜 2: 坩锅/球磨罐 3: 试管 4: 高通量料架 5: 封装料架 6: 烧杯 7: 镍片 8: 球磨罐
    "container1Position": 1,    #反应釜位置,都默认从1号位拿
    "container2Position": 1,    #坩锅位置
    "container3Position": 1,    #试管位置
    "container4Position": 1,    #高通量料架位置
    "container5Position": 1,    #封装料架位置
    "container6Position": 1,    #烧杯位置
    "container7Position": 1,    #镍片位置
    "container8Position": 1,    #球磨罐位置
    "demandAmount": 0}}
    return data


def get_GTLPF_all_parameters():
    data = {"id": uuid_genrate(),
                   "name": "高通量配粉系统",
                   "workingHours": "1",
                   "data": {"workingHours": 1,
                            "materialCup1_Status": True,    #1号料杯 是否启用
                            "materialCup1_Tank1_Status": True,  #1号料杯1号罐是否启用
                            "materialCup1_Tank1_Weight": "300", #1号料杯-1号料罐 加多少mg的药品
                            "materialCup1_Tank2_Status": True,  #1号料杯2号罐是否启用
                            "materialCup1_Tank2_Weight": "300", #1号料杯-2号料罐 加多少mg的药品
                            "materialCup1_Tank3_Status": False,
                            "materialCup1_Tank3_Weight": 0,
                            "materialCup1_Tank4_Status": False,
                            "materialCup1_Tank4_Weight": 0,
                            "materialCup1_Tank5_Status": False,
                            "materialCup1_Tank5_Weight": 0,
                            'materialCup2_Status': False,   #2号料杯 是否启用（用于高通量粉，一次配多个）
                            "materialCup2_Tank1_Status": False,
                            "materialCup2_Tank1_Weight": 0,
                            "materialCup2_Tank2_Status": False,
                            "materialCup2_Tank2_Weight": 0,
                            "materialCup2_Tank3_Status": False,
                            "materialCup2_Tank3_Weight": 0,
                            "materialCup2_Tank4_Status": False,
                            "materialCup2_Tank4_Weight": 0,
                            "materialCup2_Tank5_Status": False,
                            "materialCup2_Tank5_Weight": 0,
                            "materialCup3_Status": False,
                            "materialCup3_Tank1_Status": False,
                            "materialCup3_Tank1_Weight": 0,
                            "materialCup3_Tank2_Status": False,
                            "materialCup3_Tank2_Weight": 0,
                            "materialCup3_Tank3_Status": False,
                            "materialCup3_Tank3_Weight": 0,
                            "materialCup3_Tank4_Status": False,
                            "materialCup3_Tank4_Weight": 0,
                            "materialCup3_Tank5_Status": False,
                            "materialCup3_Tank5_Weight": 0,
                            "materialCup4_Status": False,
                            "materialCup4_Tank1_Status": False,
                            "materialCup4_Tank1_Weight": 0,
                            "materialCup4_Tank2_Status": False,
                            "materialCup4_Tank2_Weight": 0,
                            "materialCup4_Tank3_Status": False,
                            "materialCup4_Tank3_Weight": 0,
                            "materialCup4_Tank4_Status": False,
                            "materialCup4_Tank4_Weight": 0,
                            "materialCup4_Tank5_Status": False,
                            "materialCup4_Tank5_Weight": 0,
                            "materialCup5_Status": False,
                            "materialCup5_Tank1_Status": False,
                            "materialCup5_Tank1_Weight": 0,
                            "materialCup5_Tank2_Status": False,
                            "materialCup5_Tank2_Weight": 0,
                            "materialCup5_Tank3_Status": False,
                            "materialCup5_Tank3_Weight": 0,
                            "materialCup5_Tank4_Status": False,
                            "materialCup5_Tank4_Weight": 0,
                            "materialCup5_Tank5_Status": False,
                            "materialCup5_Tank5_Weight": 0,
                            "materialCup6_Status": False,
                            "materialCup6_Tank1_Status": False,
                            "materialCup6_Tank1_Weight": 0,
                            "materialCup6_Tank2_Status": False,
                            "materialCup6_Tank2_Weight": 0,
                            "materialCup6_Tank3_Status": False,
                            "materialCup6_Tank3_Weight": 0,
                            "materialCup6_Tank4_Status": False,
                            "materialCup6_Tank4_Weight": 0,
                            "materialCup6_Tank5_Status": False,
                            "materialCup6_Tank5_Weight": 0}}
    return data


def get_FYFKG_all_parameters():
    data ={"id": uuid_genrate(),
                                         "name": "反应釜开盖机",
                                         "workingHours": "1",
                                         "data": {
            "workingHours": 1,                      # 工作时长
            "operate": 0,                           # 执行操作 0: 开盖 1: 锁盖
          }}
    return data


def get_SGKGJ_all_parameters():
    data= {"id": uuid_genrate(),
                                         "name": "试管开盖机",
                                         "workingHours": "1",
                                         "data": {
                                            "workingHours": 1,                      # 工作时长
                                            "operate": 0,                           # 进行操作 0: 开盖 1: 锁盖
                                            "selectContainer": 1,                   # 选择容器 1：试管 2：球磨罐
                                            "tubeLidOperate": 0,                    # 盖处理 0：丢盖 1：留盖
                                             }
                                         }
    return data


def get_YYPBXT_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "移液配比系统",
                                         "workingHours": "1",
                                         "data": {
                                                "workingHours": 1,                      # 工作时长

                                                "crucible1_Status": False,              # 1号坩埚 是否启用
                                                "crucible1_Aspiration_Weight_A": 0,     # 1号坩埚-A溶剂吸液量
                                                "crucible1_Aspiration_Weight_B": 0,     # 1号料杯-B溶剂吸液量
                                                "crucible1_Aspiration_Weight_C": 0,     # 1号料杯-C溶剂吸液量
                                                "crucible1_Aspiration_Weight_D": 0,     # 1号料杯-D溶剂吸液量

                                                "crucible2_Status": False,              # 2号坩埚 是否启用
                                                "crucible2_Aspiration_Weight_A": 0,     # 2号坩埚-A溶剂吸液量
                                                "crucible2_Aspiration_Weight_B": 0,     # 2号料杯-B溶剂吸液量
                                                "crucible2_Aspiration_Weight_C": 0,     # 2号料杯-C溶剂吸液量
                                                "crucible2_Aspiration_Weight_D": 0,     # 2号料杯-D溶剂吸液量

                                                "crucible3_Status": False,              # 3号坩埚 是否启用
                                                "crucible3_Aspiration_Weight_A": 0,     # 3号坩埚-A溶剂吸液量
                                                "crucible3_Aspiration_Weight_B": 0,     # 3号料杯-B溶剂吸液量
                                                "crucible3_Aspiration_Weight_C": 0,     # 3号料杯-C溶剂吸液量
                                                "crucible3_Aspiration_Weight_D": 0,     # 3号料杯-D溶剂吸液量

                                                "crucible4_Status": False,              # 4号坩埚 是否启用
                                                "crucible4_Aspiration_Weight_A": 0,     # 4号坩埚-A溶剂吸液量
                                                "crucible4_Aspiration_Weight_B": 0,     # 4号料杯-B溶剂吸液量
                                                "crucible4_Aspiration_Weight_C": 0,     # 4号料杯-C溶剂吸液量
                                                "crucible4_Aspiration_Weight_D": 0,     # 4号料杯-D溶剂吸液量
                                             }

                                         }
    return data


def get_SGQMJ_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "试管球磨机",
                                         "workingHours": "1",
                                         "data": {
                                                "workingHours": 1,                      # 工作时长
                                                "intervalTime": 0,                      # 间隔时间
                                                "burialTime": 0,                        # 冷却时间
                                                "loopNumber": 1,                        # 循环次数
                                                "speed_1": 0,                           # 第1段：转速
                                                "rotationTime_1": 0,                    # 第1段：旋转时间
                                                "coolingTime_1": 0,                     # 第1段：冷却时间
                                                "speed_2": 0,                           # 第2段：转速
                                                "rotationTime_2": 0,                    # 第2段：旋转时间
                                                "coolingTime_2": 0,                     # 第2段：冷却时间
                                                "speed_3": 0,                           # 第3段：转速
                                                "rotationTime_3": 0,                    # 第3段：旋转时间
                                                "coolingTime_3": 0,                     # 第3段：冷却时间
                                              }
                                         }
    return data


def get_QMGQMJ_all_parameters():
    data= {"id": uuid_genrate(),
                                         "name": "球磨罐球磨机",
                                         "workingHours": "1",
                                         "data": {
                                                "workingHours": 1,                      # 工作时长

                                                "intervalTime": 30,                      # 间隔时间
                                                "burialTime": 30,                        # 冷却时间
                                                "loopNumber": 1,                        # 循环次数

                                                "speed_1": 1200,                           # 第1段：转速
                                                "rotationTime_1": 120,                    # 第1段：旋转时间
                                                "coolingTime_1": 30,                     # 第1段：冷却时间

                                                "speed_2": 1200,                           # 第2段：转速
                                                "rotationTime_2": 120,                    # 第2段：旋转时间
                                                "coolingTime_2": 30,                     # 第2段：冷却时间

                                                "speed_3": 1200,                           # 第3段：转速
                                                "rotationTime_3": 120,                    # 第3段：旋转时间
                                                "coolingTime_3": 30,                     # 第3段：冷却时间
                                              }
                                         }
    return data


def get_ESPSJ_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "颚式破碎机",
                                         "workingHours": "1",
                                         "data": {
                                                "workingHours": 1,                      # 工作时长
                                                "crushTime": 60,                         # 振动时间
                                                "coolingTime": 20,                       # 冷却时间
                                                "crushFrequency": 1000,                    # 振动频率
                                                "cycleTime": 1,                         # 循环次数
                                              }
                                         }
    return data


def get_ZDHDCFZJ_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "自动化电池封装机",
                                         "workingHours": "1",
                                         "data": {
                                                "workingHours": 1,                      # 工作时长
                                                "solidity_PackageValue": 0,             # 固态封装数量
                                                "liquid_PackageValue": 0,               # 液态封装数量
                                                "solidity_PressureValue_1": 0,          # 第1段：固态目标压力值
                                                "solidity_PressurizeTime_1": 0,         # 第1段：固态保压时间
                                                "liquid_PressureValue_1": 0,            # 第1段：液态目标压力值
                                                "liquid_PressurizeTime_1": 0,           # 第1段：液态保压时间
                                                "solidity_PressureValue_2": 0,          # 第2段：固态目标压力值
                                                "solidity_PressurizeTime_2": 0,         # 第2段：固态保压时间
                                                "liquid_PressureValue_2": 0,            # 第2段：液态目标压力值
                                                "liquid_PressurizeTime_2": 0,           # 第2段：液态保压时间
                                                "solidity_PressureValue_3": 0,          # 第3段：固态目标压力值
                                                "solidity_PressurizeTime_3": 0,         # 第3段：固态保压时间
                                                "liquid_PressureValue_3": 0,            # 第3段：液态目标压力值
                                                "liquid_PressurizeTime_3": 0,           # 第3段：液态保压时间
                                                "solidity_PressureValue_4": 0,          # 第4段：固态目标压力值
                                                "solidity_PressurizeTime_4": 0,         # 第4段：固态保压时间
                                                "liquid_PressureValue_4": 0,            # 第4段：液态目标压力值
                                                "liquid_PressurizeTime_4": 0,           # 第4段：液态保压时间
                                                "solidity_PressureValue_5": 0,          # 第5段：固态目标压力值
                                                "solidity_PressurizeTime_5": 0,         # 第5段：固态保压时间
                                                "liquid_PressureValue_5": 0,            # 第5段：液态目标压力值
                                                "liquid_PressurizeTime_5": 0,           # 第5段：液态保压时间
                                                "solidity_PressureValue_6": 0,          # 第6段：固态目标压力值
                                                "solidity_PressurizeTime_6": 0,         # 第6段：固态保压时间
                                                "liquid_PressureValue_6": 0,            # 第6段：液态目标压力值
                                                "liquid_PressurizeTime_6": 0,           # 第6段：液态保压时间
                                                "solidity_PressureValue_7": 0,          # 第7段：固态目标压力值
                                                "solidity_PressurizeTime_7": 0,         # 第7段：固态保压时间
                                                "liquid_PressureValue_7": 0,            # 第7段：液态目标压力值
                                                "liquid_PressurizeTime_7": 0,           # 第7段：液态保压时间
                                                "solidity_PressureValue_8": 0,          # 第8段：固态目标压力值
                                                "solidity_PressurizeTime_8": 0,         # 第8段：固态保压时间
                                                "liquid_PressureValue_8": 0,            # 第8段：液态目标压力值
                                                "liquid_PressurizeTime_8": 0,           # 第8段：液态保压时间
                                                }
                                         }
    return data


def get_TCYPJ_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "陶瓷压片机",
                                         "workingHours": "1",
                                         "data": {
                                                "workingHours": 1,                      # 工作时长
                                                "startPressureValue": 0,                # 起始压力值
                                                "targetPressureValue_1": 20,             # 目标压力值1
                                                "targetPressureValue_2": 0,             # 目标压力值2
                                                "upperPressureValue": 25,                # 压力上限值
                                                "programRunningTime": 120,                # 升压时间
                                                "pressureHoldTime": 120,                  # 保压时长
                                              }
                                         }
    return data


def get_SLJ_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "刷料机",
                                         "workingHours": "1",
                                         "data":  {
                                                "workingHours": 1,                      # 工作时长
                                                "operate": 0,                           # 进行操作  0: 刷料 1: 剪镍板
                                                "scrapingTime": 0,                      # 刷料时间 (s)
                                                }

                                         }
    return data


def get_RQZH_all_parameters():
    data= {"id": uuid_genrate(),
                                         "name": "容器转换",
                                         "workingHours": "1",
                                         "data":  {
                                                "workingHours": 1,                      # 工作时长
                                                "operate": 0,                           # 进行操作  0: 球磨罐转试管 1: 试管转球磨罐 2：球磨罐转球磨罐 3：粉末装载
                                                }
                                    }
    return data


def get_GSL_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "管式炉",
                                         "workingHours": "1",
                                         "data":   {
                                                "workingHours": 1,                      # 工作时长
                                                "intakeFlowRate": 100,                    # 进气流量
                                                "programMaxTemperatureValue": 1100,        # 程序最高温度值
                                                "scrubbingCirculateCount": 3,           # 洗气循环次数
                                                "autoInletFlowValue": 100,                # 自动进气流量值
                                                "autoLoopCount": 3,                     # 自动循环次数
                                                "doorOpenTemperatureValue": 60,          # 舱门开启温度值
                                                "heatLoopProgramNumber": 1,             # 加热循环程序段号
                                                "washingGasTimeoutTime": 30,             # 洗气超时时间
                                                "vacuumLowerLimitValue": 200,             # 真空下限值
                                                "hatchOpenPressureLowerLimit": 90000,       # 舱门开启压力下限
                                                "hatchOpenPressureUpperLimit": 110000,       # 舱门开启压力上限
                                                "furnaceTubePressureAlarmValue": 130000,     # 炉管压力报警值
                                                "constantVoltageEnable": True,         #是否使用恒压功能
                                                "constantVoltageRangeLowerLimit": 105000,    # 恒压范围下限
                                                "constantVoltageRangeUpperLimit": 109000,    # 恒压范围上限
                                                "selectThroughput": False,              #选择通量 false=单通量，true=高通量
                                                "param": [], #输入格式为一个list，里面为字典 {key: Date.now(), time: 0, temperature: 0}
                                              }
                                    }
    return data


def get_XZL_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "下装炉",
                                         "workingHours": "1",
                                         "data":  {
                                                "workingHours": 1,                      # 工作时长
                                                "doorVelocity": 0,                      # 舱门升降速度
                                                "temperaturePeakValue": 0,              # 程序最高温度值
                                                "doorOpenTemperature": 0,               # 舱门开启温度值
                                                "selectThroughput": False,              #选择通量 false=单通量，true=高通量
                                                "param": [], #输入格式为一个list，里面为字典 {key: Date.now(), time: 0, temperature: 0}
                                                }

                                    }
    return data


def get_XRD_all_parameters():
    data = {"id": uuid_genrate(),
             "name": "XRD测试仪",
             "workingHours": "1",
             "data":  {
                    "workingHours": 1,                      # 工作时长
                    "testSampleType":2,                    #测试样件类型
                    "sampleName": 'TEST',                       # 样本名称
                    "sampleCode": '1',                       # 样本编号
                    "highVoltageKV": 30,                     # 设定高压 (千伏)
                    "highVoltagemA": 20,                     # 设定高压 (毫安)
                    "startAngle": 10,                        # 起始角度
                    "endAngle": 85,                          # 终止角度
                    "measureVelocity": 5,                   # 测量速度
                    "measureStep": 0.02,                       # 测量步宽
                  }
             }
    return data


def get_ZDHGJ_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "自动化烘干机",
                                         "workingHours": "1",
                                         "data": {
                                                "workingHours": 1,                      # 工作时长
                                                "selMaterial": 0,                       # 物料选择
                                                "settingTemperature": 0,                # 设定温度
                                                "settingRotateSpeed": 0,                # 设定转速
                                                "settingTime": 0,                       # 设定时间
                                                "doorOpenTemperature": 0,              # 设定开门温度
                                                "selectThroughput": False,              #选择通量 false=单通量，true=高通量
                                                "param": [], #{key: Date.now(), time: 0, temperature: 0, speed: 0}
                                              }
                                         }
    return data


def get_QMGYW_all_parameters():
    data = {"id": uuid_genrate(),
             "name": "球磨罐移位",
             "workingHours": "1",
             "data": {
                    "workingHours": 1,                      # 工作时长
                    "settingPosition": 1,                # 提篮坩埚位置
                  }
             }
    return data


def get_GTLHCGW_all_parameters():
    data = {"id": uuid_genrate(),
                                         "name": "高通量缓存工位",
                                         "workingHours": "1",
                                         "data":  {
                                                    "workingHours": 1,                      # 工作时长
                                                    "selectContainer": 0,                   # 选择容器 1: 反应釜 2：球磨罐 3：坩埚
                                                    "robotTaskType": 0,                     # 机器人任务类型
                                                    "selectPosition": 0,                    # 取放位置
                                                  }
                                            }
    return data


