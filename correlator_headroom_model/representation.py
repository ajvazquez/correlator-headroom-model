import matplotlib.pyplot as plt
import ipywidgets as widgets

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

    def show(self, ymin=None, ymax=None, legend_loc=None, show_text=False):
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
        if show_text:
            plt.text(0, 0.9*self.R, "{} {}".format(eval("%.0e" % self.R), self.units), verticalalignment="top", color="blue")
            plt.text(len(self.values)-3, 0.9*self.values[-1], "{} {}".format(eval("%.0e" % self.values[-1]), self.units), verticalalignment="top", color="lightgrey")
        if ymin is None:
            ymin = min(self.values)/10
        if ymin:
            plt.ylim(bottom=ymin)
        if ymax:
            plt.ylim(top=ymax)
        if legend_loc is None:
            legend_loc = "best"
        plt.legend(loc=legend_loc)


def dashboard(model, parameters):
    """
    Simple dashboard for a model with parameters (param, default, step, min, max, type).
    """

    dict_widgets = {
        int: widgets.IntSlider,
        float: widgets.FloatSlider
    }

    def show(*args, **kwargs):
        m = model(*args, **kwargs)
        m.show(show_text=True)

    ws = {x[0]: dict_widgets[x[-1]](
        value=x[1],
        step=x[2],
        min=x[3],
        max=x[4],
        description=x[0],
        orientation="vertical",
        layout=widgets.Layout(width="40px")) for x in parameters}
    wi = widgets.interactive(show, **ws)
    disp = widgets.HBox(wi.children)
    wi.update()
    display(disp)
