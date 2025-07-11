'''
Line2D(xdata, ydata, linewidth=None, linestyle=None, color=None, marker=None, markersize=None, markeredgewidth=None, markeredgecolor=None, markerfacecolor=None, markerfacecoloralt ='none', fillstyle=None, antialiased=None, dash_capstyle=None, solid_capstyle=None, dash_joinstyle=None, solid_joinstyle=None, pickradius=5, drawstyle=None, markevery=None, **kwargs)
'''

import tkinter as tk
from File_Reader.import_excel import return_df
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")
import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '...')))

#import plot_properties_class as ppc


def line() :
                   
      if len(return_df()) > 0 :  
              #param_dict = ppc.dictionary_rcparam
              plt.plot(return_df())
                      
              #)
              

              plt.grid()#visible=param_dict['visible'])
              #ydata=param_dict['y-data']
              #xdata=param_dict['x-data'],


              #De bagat : legend , x-label , y-label , title  
              #De editat figura cu mouse-ul (dynamic editing)

              plt.show()
      else:
              tk.messagebox.showerror("showerror", "Something went wrong !")

'''
alpha=param_dict['alpha'] , animated=param_dict['animated'] , antialiased=param_dict['antialiased'] , 
color=param_dict['color'] , dash_capstyle=param_dict['dash_capstyle'] , dash_joinstyle=param_dict['dash_joinstyle'],
drawstyle=param_dict['drawstyle'] , fillstyle=param_dict['fillstyle'] , gid=param_dict['grid'],
in_layout=param_dict['in_layout'] , label=param_dict['label'] , linewidth=param_dict['linewidth'],
linestyle=param_dict['linestyle'] , 
marker=param_dict['marker'] , mec=param_dict['mec'], mew=param_dict['mew'] ,
mfc=param_dict['mfc'], mfcalt=param_dict['mfalt'] , rasterized=param_dict['rasterized'],
ms=param_dict['ms'] , markevery=param_dict['mev'] , path_effects=param_dict['path_effects'],
solid_capstyle=param_dict['solid_capstyle'] , solid_joinstyle=param_dict['solid_joinstyle'] ,
snap=param_dict['snap'] , url=param_dict['url'] , zorder=param_dict['zorder']
'''