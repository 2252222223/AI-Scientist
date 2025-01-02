from CEO.Base.COB_intervention import COBInputRun, InteractionManager

expertise_save = True
interaction_manager = InteractionManager(expertise_save)
# interaction_manager = COBInputRun()
# 配置字典，封装所有相关参数
CONFIG = {
    "interaction_manager": interaction_manager,
    "model_name": "gpt-4o",
    "COB_in_the_loop": True,
    "Expert_experience_switch": True,
    "expertise_save": expertise_save,
}


