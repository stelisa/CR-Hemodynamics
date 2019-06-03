import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import pandas as pd
import numpy as np

import dash_analysis_toolbox as dat
# select unusual sleep id with self written function
# control group 
H_control_unusual = dat.select_id("H_control.csv",1,12)
M_control_unusual = dat.select_id("M_control.csv",1,10)
L_control_unusual = dat.select_id("L_control.csv",1,10)

# dash group
H_dash_unusual = dat.select_id("H_dash.csv",1,9)
M_dash_unusual = dat.select_id("M_dash.csv",1,12)
L_dash_unusual = dat.select_id("L_dash.csv",1,10)

#=================
# draw lineplot and save figure
# control group
control_H = dat.unusual_sleep_lineplot("H_control.csv",H_control_unusual,"H_control_unusualsleep_lineplot",1,12)
control_M = dat.unusual_sleep_lineplot("M_control.csv",M_control_unusual,"M_control_unusualsleep_lineplot",1,10)
control_L = dat.unusual_sleep_lineplot("L_control.csv",L_control_unusual,"L_control_unusualsleep_lineplot",1,10)

# dash group
dash_H = dat.unusual_sleep_lineplot("H_dash.csv",H_dash_unusual,"H_dash_unusualsleep_lineplot", 1,9)
dash_M = dat.unusual_sleep_lineplot("M_dash.csv",M_dash_unusual,"M_dash_unusualsleep_lineplot", 1,12)
dash_L = dat.unusual_sleep_lineplot("L_dash.csv",L_dash_unusual,"L_dash_unusualsleep_lineplot", 1,10)