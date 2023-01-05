from tkinter import*
from tkinter import font
from tkinter.font import BOLD
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import insert
import pandas as pd
from matplotlib.pyplot import figure

# Main Window
root = Tk()
root.title("Lagrange Interpolation and Extrapolation Calculator")
w = 1000
h = 700
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(width=False,height=False)
root.iconphoto(False,PhotoImage(file='C:/Users/Kaloy/Desktop/Python/icon.png'))

# Frame and Label Widgets
inputFrame = LabelFrame(root,font="Tahoma",padx=10,pady=10)
inputFrame.place(relx=.98,rely=.63, anchor=E)
inst1 = Label(root,text="How to Use:",font=("Roboto",11,BOLD)).place(x=540,y=15)
inst2 = Label(root,text="1. Enter Data Points by completing X and Y fields and click Add",font=("Roboto",11)).place(x=540,y=40)
inst3 = Label(root,text="or simply import your data set via Import CSV",font=("Roboto",11)).place(x=540,y=65)
inst4 = Label(root,text="2. Indicate the x value of interest, Choose Degree to use.",font=("Tahoma",11)).place(x=540,y=90)
inst5 = Label(root,text="3. Select data points according to chosen degree by Ctrl (or Shift)",font=("Tahoma",11)).place(x=540,y=115)
inst6 = Label(root,text=" + Left Click.",font=("Tahoma",11)).place(x=550,y=140)
inst7 = Label(root,text="For better accuracy, choose data points closest to X",font=("Tahoma",11)).place(x=580,y=165)

xLabel = Label(inputFrame,text="Enter x value:").grid(row=1,column=0,pady=10,sticky=E)
xField = Entry(inputFrame, width=20)
xField.grid(row=1,column=1,columnspan=2)

yLabel = Label(inputFrame,text="Enter y value:").grid(row=2,column=0,pady=10,sticky=E)
yField = Entry(inputFrame, width=20)
yField.grid(row=2,column=1,padx=10,columnspan=2)

findLabel = Label(inputFrame,text="Enter data point to find (x):").grid(row=3,column=0,pady=10)
findField = Entry(inputFrame, width=20)
findField.grid(row=3,column=1,padx=10,columnspan=2)

orderLabel = Label(inputFrame,text="Choose Degree:").grid(row=4,column=0,pady=10,sticky=E)
options = [
    "1st\n(2 Points, N=1)",
    "2nd\n(3 Points, N=2)",
    "3rd\n(4 Points, N=3)",
    "4th\n(5 Points, N=4)",
    "5th\n(6 Points, N=5)",
]
global clicked
clicked = StringVar()
clicked.set(options[0])
cbox = OptionMenu(inputFrame,clicked,*options)
cbox.grid(row=4,column=1,padx=10, pady=10,columnspan=2)

tableFrame = LabelFrame(root,font="Tahoma",padx=15,pady=10)
tableFrame.place(relx=.5,rely=.5, anchor=E)
global columns 
global table
global lagrangetable
global content
global nCount
global result

nCount = 0
content = StringVar()
content.set("Total Data Point Entries (n): " + str(nCount))
nLabel = Label(tableFrame, textvariable=content).place(x= 100,y=-10)
result = Label(tableFrame,text="Step by Step Results").place(x=135,y=390)
#define columns
columns = ("x","y")
#instantiate table
table = ttk.Treeview(tableFrame,columns=columns,show="headings",height=17)
table.pack(padx=10,pady=20)
tableStyle = ttk.Style()
tableStyle.configure("Treeview.Heading",font=('Arial Bold',15))
scroll = ttk.Scrollbar(tableFrame, orient="vertical", command=table.yview)
scroll.place(x=415, y=15,height=370)
table.configure(yscrollcommand=scroll.set)
#format columns
table.column("x", anchor=CENTER, width=200)
table.column("y", anchor=CENTER, width=200)
#create column headings
table.heading("x",text="x",anchor=CENTER)
table.heading("y",text="y",anchor=CENTER)
for col in columns:
    table.heading(col, text=col,command=lambda c=col: sortTable(table, c, False))

columns2 = ("L(xn)","f(xn)")
lagrangetable = ttk.Treeview(tableFrame,columns=columns2,show="headings",height=5)
lagrangetable.pack(padx=10,pady=15)
lagrangeStyle = ttk.Style()
lagrangeStyle.configure("Treeview.Heading",font=('Arial Bold',15))
lagrangescroll = ttk.Scrollbar(tableFrame, orient="vertical", command=lagrangetable.yview)
lagrangescroll.place(x=415, y=420,height=130)
lagrangetable.configure(yscrollcommand=lagrangescroll.set)
# format columns
lagrangetable.column("L(xn)", anchor=W, width=250)
lagrangetable.column("f(xn)", anchor=CENTER, width=150)
# create column headings
lagrangetable.heading("L(xn)",text="L(xn)",anchor=CENTER)
lagrangetable.heading("f(xn)",text="f(xn)",anchor=CENTER)

result = StringVar()
result.set("Inter/Extrapolated Point:\nX = 0\nY = 0")
outputLabel = Label(tableFrame,textvariable=result,font=("Robot",14,BOLD)).pack()
# Function list
# add data
def add():
    global nCount
    global table
    global content
    if len(xField.get()) == 0 or len(yField.get()) == 0:
        messagebox.showerror("Empty Input", "X and Y fields must not be empty!")
    else:
        try:
            attemptX=float(xField.get())
            attemptY=float(yField.get())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid X and Y values!")
        else:
            nCount += 1
            content.set("Total Data Point Entries (n): " + str(nCount))
            table.insert(parent=(''),index='end',text="",values=(float(xField.get()), float(yField.get())))
            # sort table based on "x" column
            sortTable(table,"x", False)     
            # Clear fields
            xField.delete(0,END)
            yField.delete(0,END)
# delete selected data
def delete():
    global table
    global nCount
    global content
    x = table.selection()
    if len(x) != 0:
        for data in x:
            nCount -= 1
            table.delete(data)
            content.set("Total Data Point Entries (n): " + str(nCount))
    else:
        messagebox.showinfo("Delete Failed", "No selected data to be deleted")
# empty table
def reset():
    global table
    global lagrangetable
    global nCount
    global content
    global result
    if len(table.get_children()) != 0:
        response = messagebox.askquestion("Delete Data", "All entries and results will be deleted. Proceed?")
        if response == "yes":
            for data in table.get_children():
                table.delete(data)
            for data in lagrangetable.get_children():
                lagrangetable.delete(data)
            nCount = 0
            content.set("Total Data Point Entries (n): " + str(nCount))
            result.set("Inter/Extrapolated Point:\nX = 0\nY = 0")
    else:
        messagebox.showinfo("Empty Entry", "No data in the table")
# calculate data
def calculate():
    global nCount
    global table
    if len(findField.get()) == 0:
        messagebox.showerror("Empty Input", "Indicate data point to find")
    elif len(table.get_children()) < 2:
        messagebox.showerror("Insufficient Input", "Data set must contain at least 2")
    else:
        try:
            attemptN=float(findField.get())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid data point value!")
        else:
            global clicked 
            datapoints = 0
            order = ""
            if clicked.get() == "1st\n(2 Points, N=1)":
                datapoints = 2
                order = "1st"
            elif clicked.get() == "2nd\n(3 Points, N=2)":
                datapoints = 3
                order = "2nd"
            elif clicked.get() == "3rd\n(4 Points, N=3)":
                datapoints = 4
                order = "3rd"
            elif clicked.get() == "4th\n(5 Points, N=4)":
                datapoints = 5
                order = "4th"
            elif clicked.get() == "5th\n(6 Points, N=5)":
                datapoints = 6
                order = "5th"
     
            if(datapoints != len(table.selection())):
                messagebox.showerror("Selection Error", "Chosen " + order + " Degree requires exactly " + 
                                     str(datapoints) + " data points")
            else:
                global nCount
                # initializing to zero for storing x and y values and L(x)
                x = np.zeros((datapoints))
                y = np.zeros((datapoints))
                L = np.zeros((datapoints))
                all_x = np.zeros((nCount))
                all_y = np.zeros((nCount))
                counter = 0
                # Get all data points in the table
                for data in table.get_children():
                    if(counter < nCount):
                        all_x[counter] = float(table.item(data)["values"][0])
                        all_y[counter] = float(table.item(data)["values"][1])
                    counter += 1
                # Get selected data points
                selectedData = table.selection()
                counter = 0
                for data in selectedData:
                    if(counter < datapoints):
                        x[counter] = float(table.item(data)["values"][0])
                        y[counter] = float(table.item(data)["values"][1])
                    counter += 1
                # convert data x to find to float data type
                xp = float(findField.get())
                # set initial data y to 0
                yp = 0
                for i in range(datapoints):
                    Lfactor = 1
                    for j in range(datapoints):
                        if i != j:
                            Lfactor = Lfactor * (xp - x[j])/(x[i] - x[j])
                    L[i] = Lfactor
                    yp = yp + Lfactor * y[i] 
                    
                global lagrangetable
                global result
                # empty previous lagrange entries
                for data in lagrangetable.get_children():
                    lagrangetable.delete(data)
                LCount = 0
                for i in range(datapoints):
                    lagrangetable.insert(parent=(''),index='end',iid=i,text="",
                                         values=("L(x"+str(i)+") = " + str(L[i]), "f(x"+str(i)+") = " + str(y[i])) )
                result.set("Inter/Extrapolated Point:\nX = " + str(xp) + "\nY = " + str(yp))
                x_axis = x
                y_axis = y
                int_point = xp
                plt.close()
                # plotting the points
                figure(figsize=(8, 6), dpi=120)
                # set x range minimum
                plt.xlim(all_x[0]-10,all_x[nCount-1]+10)
                #plt.ylim(all_y[0]-10,all_x[nCount-1]+10)
                # plot all data points
                plt.plot(all_x, all_y, color='magenta', marker='H', markerfacecolor='cyan')
                # plot data points used in calculation
                plt.plot(x_axis, y_axis, color='blue', marker='o', markerfacecolor='cyan')
                # plot lines tangent to point of interest
                plt.plot([int_point, int_point], [0, yp+10], color='green', linestyle='dashed')
                plt.plot([int_point+10,0],[yp,yp], color='green', linestyle='dashed')
                #plot point of interest
                plt.plot(xp,yp,'ro')
                #plot annotation
                plt.annotate('Point of Interest', xy=(int_point+.5, yp), xytext=(int_point+2, yp+3),
                            arrowprops=dict(facecolor='black', shrink=0.04))
                # x axis label
                plt.xlabel('X - Axis')
                # y axis label
                plt.ylabel('Y - Axis')
                # Graph title
                plt.title('Data Set Line Graph') 
                # show plot
                plt.show()
                # Clear fields
                findField.delete(0,END)
                xField.delete(0,END)
                yField.delete(0,END)
# sorts Table
def sortTable(tv, col, reverse):
    l = [(table.set(k, col), k) for k in table.get_children('')]
    l.sort(key=lambda t: float(t[0]), reverse=FALSE)
    for index, (val, k) in enumerate(l):
        table.move(k, '', index) 
# file open dialogue
def fileOpen():
    global table
    global nCount
    global table
    global content
    filename = filedialog.askopenfilename(
        title="Open a File",
        filetype=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_csv(filename)
        except ValueError:
            messagebox.showerror("File Error", "File couldn't be opened! Try again.")
            return None
        except FileNotFoundError:
            messagebox.showerror("File Error", f"No such file as {filename}")
            return None
        else:
            df_rows = df.to_numpy().tolist()
            try:
                for row in df_rows:
                    test_x = float(row[0])
                    test_y = float(row[1])
            except ValueError:
                messagebox.showerror("Import Failed", "Some values in the file are invalid. All data must be float data type")
                return None
            else:
                for row in df_rows:
                    nCount += 1
                    content.set("Total Data Point Entries (n): " + str(nCount))
                    #table.insert("", "end", values=row)
                    table.insert(parent=(''),index='end',text="",values=(float(row[0]), float(row[1])))
                    
                # sort table based on "x" column
                sortTable(table,"x", False) 
# Buttons
addButton = Button(inputFrame, text ="Add Data", padx=50,pady=10,bg="light grey",command=add)
addButton.grid(row=6,column=0,pady=5)

delButton = Button(inputFrame, text ="Delete Data", padx=45,pady=10,bg="light grey",command=delete)
delButton.grid(row=6,column=1,pady=5)

importButton = Button(inputFrame, text ="Import CSV", padx=45,pady=10,bg="light grey",command=fileOpen)
importButton.grid(row=7,column=0,pady=5)

resetButton = Button(inputFrame, text ="Empty Table", padx=45,pady=10,bg="light grey",command=reset)
resetButton.grid(row=7,column=1,pady=5)

calcuButton = Button(inputFrame, text ="Calculate", padx=100,pady=20,bg="light grey",command=calculate)
calcuButton.grid(row=8,column=0,pady=10,columnspan=2)

root.mainloop()