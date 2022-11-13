from .model import HeadroomModel, Scale, Limit
from .representation import ReprMixin


class RIModel(ReprMixin, HeadroomModel):

    DEFAULT_RFT = 0.08
    DEFAULT_Fe = 1
    DEFAULT_RXA = 1.112
    DEFAULT_Fc = 1000
    DEFAULT_P = 1
    DEFAULT_UNITS = "Gbps"

    def __init__(self, S, Nc, kc, RH, RN, RHw=None, Fe=None, RFT=None, RXA=None, P=None, ST=None, Fc=None, units=None, filter_limit=None):

        # Defaults
        if Fe is None:
            Fe = self.DEFAULT_Fe
        if RFT is None:
            RFT = self.DEFAULT_RFT
        if RXA is None:
            RXA = self.DEFAULT_RXA
        if P is None:
            P = self.DEFAULT_P
        if ST is None:
            ST = S
        if Fc is None:
            Fc = self.DEFAULT_Fc
        if RHw is None:
            RHw = RH
        if units is None:
            units = self.DEFAULT_UNITS
        self.units = units
        GT = (S-1)/(ST-1)

        # Cells
        cells = [
            Limit(RH),
            Scale(1/P),
            Limit(RH, "Data read limit"),
            Scale(GT),
            Limit(RN, "Data streaming limit"),
            Scale(S*P/Nc),
            Limit(RN, "Data distribution limit"),
            Scale(Fe/kc),
            Limit(RFT, "Station-based processing limit"),
            Scale(ST-1),
            Limit(RXA, "Baseline-based processing limit"),
            Scale(kc/Fc),
            Limit(RN),
            Scale(Nc),
            Limit(RN),
            Limit(RHw, "Collection limit")
        ]
        super().__init__(cells=cells, filter_limit=filter_limit)
