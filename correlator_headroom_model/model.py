
class MaxException(Exception):
    pass


class Cell:

    DEFAULT_MAX = 1e20
    DIFF_CHK = 1e-10

    def __init__(self, ratio=None, max=None, label=None):
        assert sum([x is not None for x in [ratio, max]])==1
        max = None if max is not None and max < 0 else max
        self.ratio = ratio
        self.max = max
        self.label = label

    def vin(self, vout):
        """Backward run, get input from output."""
        res = vout
        if self.ratio is not None:
            res = vout/self.ratio
        elif self.max is not None:
            if vout > self.max:
                if abs(vout-self.max) > self.DIFF_CHK:
                    raise MaxException
                res = self.max
        return res

    def vout(self, vin):
        """Forward run, get output from input."""
        res = vin
        if self.ratio is not None:
            res = vin*self.ratio
        elif self.max is not None:
            res = min(vin, self.max)
        return res


class Scale(Cell):

    def __init__(self, ratio):
        super().__init__(ratio=ratio)

    def __repr__(self):
        return "|{}>".format(self.ratio)


class Limit(Cell):

    def __init__(self, max, label=None):
        super().__init__(max=max, label=label)

    def __repr__(self):
        return "[{}]{}".format(self.max if self.max else "-", " '{}'".format(self.label) if self.label else "")


class HeadroomModel:

    values = None

    def __init__(self, cells, filter_limit=None):
        assert filter_limit is None or isinstance(filter_limit, str)
        self.cells = cells
        assert len(self.cells)>=3, "The model needs at least three cells"
        assert self.cells[0].max is not None, "The first cell must be a limit"
        assert self.cells[-1].max is not None, "The last cell must be a limit"
        if filter_limit:
            f = lambda x: x if x.ratio is not None or (x.max is not None and x.label and filter_limit in x.label) else Limit(-1)
            self.cells = [f(x) for x in self.cells ]

    def _propagate_model(self):
        vin = self.cells[0].max

        # In case filter_limit is applied
        if not vin:
            vin = Cell.DEFAULT_MAX

        # Forward iteration
        for cell in self.cells:
            vin = cell.vout(vin)

        # Backward iteration
        values = [vin]
        for cell in self.cells[::-1]:
            vin = cell.vin(vin)
            values.append(vin)
        self.values = values[::-1]

        # Check
        if any([x>=(Cell.DEFAULT_MAX-Cell.DIFF_CHK) for x in self.values]):
            raise MaxException

    def cached_values(self, reload=False):
        if reload or not self.values:
            self._propagate_model()
        return self.values

    def get_limits(self):
        return [None]+[cell.max for cell in self.cells]

    def get_r_in_max(self):
        return self.cached_values()[0]

    def get_r_out_max(self):
        return self.cached_values()[-1]

    def __repr__(self):
        return "-".join([str(x) for x in self.cells])

    @property
    def R(self):
        return self.get_r_in_max()
