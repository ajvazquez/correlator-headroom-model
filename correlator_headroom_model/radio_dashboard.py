from radio_model import RIModel
from representation import dashboard


# Parameter, default, step, min, max, type
parameters = [
    ["S", 4,1, 2,256, int],
    ["Nc", 8,1, 1,128, int],
    ["kc", 16,1, 1,128, int],
    ["RH", 1,.1, .1,10, float],
    ["RHw", 1,.1, .1,10, float],
    ["RN", 1,.1, .1,10, float],
    ["RFT", RIModel.DEFAULT_RFT,1e-3, 1e-3, .5, float],
    ["RXA", RIModel.DEFAULT_RXA,1e-3, 1e-3, 5, float],
    ["Fe", RIModel.DEFAULT_Fe,.1, .1,1000, float],
    ["Fc", RIModel.DEFAULT_Fc,.1, .1,10000, float],
    ["P", RIModel.DEFAULT_P,1, 1,100, int],
]


def start():
    dashboard(model=RIModel, parameters=parameters)
