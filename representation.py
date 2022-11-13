import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


class ReprMixin:

    units = None

    def xticks(self):
        values = self.cached_values()
        return [chr(97 + x).upper() for x in range(len(values))]

    def blocks(self):
        xticks = self.xticks()
        cells = [str(x) for x in self.cells]+[""]
        return " ".join("({}) {}".format(a,b) for a,b in zip(xticks, cells))

    def show_blocks(self):
        print(self.blocks())

    def show(self, ymin=None, ymax=None):
        values = self.cached_values()

        fig, ax = plt.subplots()
        x = range(len(values))
        ax.semilogy(x, self.values, marker="x")
        ax.grid()

        xticks = self.xticks()
        idx = -1
        for cell in self.cells:
            idx += 1
            if cell.max is not None:
                ax.plot([idx, idx+1], [cell.max, cell.max], zorder=100, linewidth=2.5, linestyle="--", label=cell.label, color=None if cell.label else "lightgrey")
        plt.xticks(x, xticks)
        plt.ylabel("R{}".format(" [{}]".format(self.units) if self.units else ""))
        plt.xlabel("Correlator stage")
        if ymin:
            plt.ylim(bottom=ymin)
        if ymax:
            plt.ylim(top=ymax)
        plt.legend(loc="lower left")

