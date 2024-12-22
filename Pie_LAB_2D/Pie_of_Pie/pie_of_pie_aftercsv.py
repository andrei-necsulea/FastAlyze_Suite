import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np
import tkinter as tk
from PyQt5 import QtGui
from File_Reader.import_csv import return_df_stacked_plot_csv



def pie_of_pie_csv():

 def create_bar_of_pie(explode_param , pie_labels_param , bar_labels_param , bar_ratios_param , master_wedge_pos):
  if len(return_df_stacked_plot_csv()) >= 1 :
      # make figure and assign axis objects
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
      fig.subplots_adjust(wspace=0)


      # pie chart parameters

      pie_ratios = list(return_df_stacked_plot_csv())
      pie_ratios = pie_ratios[len(pie_ratios)-1]

      '''
      #find position of max
      maximum_pie_ratios = max(pie_ratios)
      for i in range(0 , len(pie_ratios)):
        if maximum_pie_ratios == pie_ratios[i] :
          position_of_maximum = i
          break
      '''

      pie_labels = pie_labels_param
      explode = explode_param


      #Here we will determine and put in a list of all percents of wedeges
      percents = []
      sum_ratios = sum(pie_ratios)
      for i in pie_ratios :
       percents.append(i/sum_ratios*100)



      #here we determine the general formula of startangle
      angle = -180*max(percents)/100


      #determine the list of wedges and construct pie chart
      wedges, *_ = ax1.pie(pie_ratios, autopct='%1.1f%%', startangle = angle ,
                     labels=pie_labels, explode=explode)


      # bar chart parameters
      bar_ratios = bar_ratios_param
      bar_labels = bar_labels_param
      bottom = 1
      width = .2

      # Adding from the top matches the legend.
      ax2.pie(bar_ratios)


      # use ConnectionPatch to draw lines between the two plots
      theta1, theta2 = wedges[master_wedge_pos].theta1, wedges[master_wedge_pos].theta2
      center, r = wedges[master_wedge_pos].center, wedges[master_wedge_pos].r
      bar_height = sum(bar_ratios)


      # draw top connecting line
      x = r * np.cos(np.pi / 180 * theta1) + center[0]
      y = r * np.sin(np.pi / 180* theta1) + center[1]
      con = ConnectionPatch(xyA=(-width / 2, -bar_height+1), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
      con.set_color([0, 0, 0])
      con.set_linewidth(4)
      ax2.add_artist(con)


      # draw bottom connecting line
      x = r * np.cos(np.pi / 180 * theta2) + center[0]
      y = r * np.sin(np.pi / 180 * theta2) + center[1]
      con = ConnectionPatch(xyA=(-width / 2, 1), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
      con.set_color([0, 0, 0])
      ax2.add_artist(con)
      con.set_linewidth(4)


      #set icon to matplotlib window
      thismanager = plt.get_current_fig_manager()
      thismanager.window.setWindowIcon(QtGui.QIcon('chart.ico')) 
 
      # printing the plot
      plt.show()

  else:
      tk.messagebox.showerror("showerror", "Something went wrong !")
 

 window = tk.Tk()
 window.iconbitmap("chart.ico")
 window.geometry('350x300')
 window.title("PIE of PIE properties")
 window.resizable(0,0)
 window.config(bg = "#9fb49f")

 lbl = tk.Label(window , text = "Explode : ")
 lbl.place(relx = 0.2 , rely = 0.2)
 lbl.config(background="#9fb49f")

 lbl_2 = tk.Label(window , text = "Pie labels : ")
 lbl_2.place(relx = 0.15 , rely = 0.3)
 lbl_2.config(background="#9fb49f")

 lbl_3 = tk.Label(window , text = "Pie nr.2 labels : ")
 lbl_3.place(relx = 0.15 , rely = 0.4)
 lbl_3.config(background="#9fb49f")

 lbl_4 = tk.Label(window , text = "Pie nr.2 data : ")
 lbl_4.place(relx = 0.15 , rely = 0.5)
 lbl_4.config(background="#9fb49f")

 lbl_5 = tk.Label(window , text = "Master wedge pos : ")
 lbl_5.place(relx = 0.2 , rely = 0.6)
 lbl_5.config(background="#9fb49f")

 e = tk.Entry(window , width = 25)
 e.place(rely = 0.2 , relx = 0.4)

 e1 = tk.Entry(window , width = 25)
 e1.place(rely = 0.3 , relx = 0.4)

 e2 = tk.Entry(window , width = 25)
 e2.place(rely = 0.4 , relx = 0.4)

 e3 = tk.Entry(window , width = 25)
 e3.place(rely = 0.5 , relx = 0.4)

 e4 = tk.Entry(window , width = 7)
 e4.place(rely = 0.6 , relx = 0.52)

 '''
 e_list = list(map(float, str(e.get()).split(',')))
 e1_list = list(map(str , str(e1.get()).split(',')))
 e2_list = list(map(str , str(e2.get()).split(',')))
 e3_list = list(map(float , str(e3.get()).split(',')))
 '''

 btn = tk.Button(window , text = "Generate PIE Chart" , width = 25 , command=lambda : create_bar_of_pie(list(map(float, str(e.get()).split(','))) , list(map(str , str(e1.get()).split(','))) , list(map(str , str(e2.get()).split(','))) , list(map(float , str(e3.get()).split(','))) , int(e4.get())-1 ))
 btn.place(relx=0.25 , rely = 0.75)

 window.mainloop()
 