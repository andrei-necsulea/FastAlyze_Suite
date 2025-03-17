from autoviz import AutoViz_Class
import pandas as pd

AV = AutoViz_Class()
dfte = pd.read_csv("H:\\FastAlyze_Suite\\TESTING\\ex_2.csv")  # Load manually

import matplotlib.pyplot as plt

dft = AV.AutoViz(
    filename="",  # Leave empty when passing a dataframe
    dfte=dfte,
    sep=",",
    chart_format="png",
    save_plot_dir="H:\\FastAlyze_Suite\\TESTING\\plots"
)

plt.savefig("plots\\output_chart.png")
plt.show()
