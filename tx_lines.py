import tkinter as tk
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
# App setup
app = Tk()
app.state("zoomed")

app.title("Tx_lines")

# Side frame
side = Frame(app, bg="white")
side.place(relx=0.8, rely=0, relheight=1, relwidth=0.21)
side.columnconfigure(0, weight=1)
side.columnconfigure(1, weight=7)

# Simulation speed slider and label
def speed(value):
    speed_field.configure(text=round(float(value), 2), anchor="nw")

speed_label = Label(side, bg="white", text="Simulation Speed", font=("helvetica", 14))
speed_label.grid(row=1, column=0,pady=10)
speed_field = Label(side, bg="white", text="1", font=("helvetica", 14))
speed_field.grid(row=1, column=1,pady=10)

speed_slider = Scale(
    side, from_=0, to=2, orient=HORIZONTAL, resolution=0.01, command=speed,length=200,troughcolor="#c6e7ff",bg="white"
)
speed_slider.set(1)
speed_slider.grid(row=2, columnspan=2,pady=10)

#channel length
def length(value):
    length_field.configure(text=round(float(value), 2), anchor="nw")

length_label = Label(side, bg="white", text="Channel Length", font=("helvetica", 15))
length_label.grid(row=3, column=0,pady=10)
length_field = Label(side, bg="white", text="1", font=("helvetica", 15))
length_field.grid(row=3, column=1,pady=10)

length_slider = Scale(
    side, from_=3, to=7, orient=HORIZONTAL, resolution=0.01, command=length,length=200,troughcolor="#c6e7ff",bg="white"
)
length_slider.set(5)
length_slider.grid(row=4, columnspan=2,pady=10)

#check points
var1 = tk.BooleanVar()
var2 = tk.BooleanVar()
var3 = tk.BooleanVar()
check1 = tk.Checkbutton(side, text="Forward wave", variable=var1,font=("helvetica", 15),bg="white",anchor="w",fg="green")
check1.grid(row=6,columnspan=2,pady=10)
check2 = tk.Checkbutton(side, text="Backward wave", variable=var2,font=("helvetica", 15),bg="white",anchor="w",fg="#00008b")
check2.grid(row=7,columnspan=2,pady=10)
check3 = tk.Checkbutton(side, text="Resultant wave", variable=var3,font=("helvetica", 15),bg="white",anchor="w",fg="#FF00FF")
check3.grid(row=8,columnspan=2,pady=10)

#reflection coefficient
impedance_label = Label(side, bg="white",text="Line Impedance(ohm)", font=("helvetica", 15))
impedance_label.grid(row=9, column=0,pady=30)
impedance=Entry(side,name="zo", font=("helvetica", 15))
impedance.grid(row=9,column=1,padx=30,pady=30)

L_impedance_label = Label(side, bg="white",text="Load Impedance(ohm)", font=("helvetica", 15))
L_impedance_label.grid(row=10, column=0,pady=30)
L_impedance=Entry(side,name="zl", font=("helvetica", 15))
L_impedance.grid(row=10,column=1,padx=30,pady=30)
R=0
G=0
C=0
H=0
def RLHC():
    global R,G,H,C
    try:
        # Try to convert the string to a complex number
        z0 = complex(impedance.get())
        p=complex(propagation.get())
        w=frequency_field.get()
        if(p==0):
            R=0
            G=0
            H=0
            C=0
        else:
            R=np.real(z0*p)
            H=np.real(z0*p)/w
            G=np.real(p/z0)
            C=np.real(p/z0)/w
    except ValueError:
        # If a ValueError occurs, it means the string is not a valid complex number
        R<0
        G<0
        H<0
        C<0
def get_gamma():
    try:
        # Try to convert the string to a complex number
        z0 = complex(impedance.get())
        Zl=complex(L_impedance.get())
        if(Zl==0 and z0==0):
            gamma="NAN"
        else:
            gamma=(Zl-z0)/(z0+Zl)
        return gamma  # Return the complex number if conversion is successful
    except ValueError:
        # If a ValueError occurs, it means the string is not a valid complex number
        return 0

#propagation constant

def get_prop():
    try:
        # Try to convert the string to a complex number
        prop = complex(propagation.get())
        return prop  # Return the complex number if conversion is successful
    except ValueError:
        # If a ValueError occurs, it means the string is not a valid complex number
        return 0

prop_label = Label(side, bg="white",text="Propagation Const(m^-1)", font=("helvetica", 14))
prop_label.grid(row=11, column=0,pady=30)
propagation=Entry(side,name="a+b", font=("helvetica", 15))
propagation.grid(row=11,column=1,padx=23,pady=30)



# Source frame
source = Frame(app)
source.place(relx=0, rely=0, relheight=0.45, relwidth=0.17)


# Voltage slider and label
def voltage(value):
    voltage_value.configure(text=f"Voltage(V)={round(float(value), 2)}", anchor="center")


voltage_value = Label(source, text="Voltage(V)=2.5", font=("helvetica", 15),fg="red")
voltage_value.place(relx=0.2,rely=0.32,relheight=0.1,relwidth=0.6)

voltage_field = Scale(
    source, from_=0, to=5, orient=HORIZONTAL, resolution=0.1, command=voltage,length=200,troughcolor="#c6e7ff"
)
voltage_field.set(2.5)
voltage_field.place(relx=0.2,rely=0.43,relheight=0.1,relwidth=0.6)

# Frequency slider and label
def frequency(value):
    frequency_value.configure(text=f"Frequency(KHz)={round(float(value), 2)}", anchor="center")


frequency_value = Label(source, text="Frequency(KHz)=3", font=("helvetica", 15),fg="green")
frequency_value.place(relx=0.2,rely=0.60,relheight=0.1,relwidth=0.6)

frequency_field = Scale(
    source, from_=1, to=5, orient=HORIZONTAL, resolution=0.01, command=frequency,length=200,troughcolor="#c6e7ff"
)
frequency_field.set(3)
frequency_field.place(relx=0.2,rely=0.71,relheight=0.1,relwidth=0.6)


#output frame
output=Frame(app)
output.place(relx=0.6,rely=0,relwidth=0.2,relheight=0.45)
output.columnconfigure(0, weight=1)
output.columnconfigure(1, weight=6)

def update_output():
    gamma=get_gamma()
    Reflection_coefficient.delete(0,END)
    Reflection_coefficient.insert(0,gamma)
    if(abs(gamma)==1):
        VSWR="inf"
    elif(gamma=="NAN"):
        VSWR=1
    else:
        VSWR=(np.abs(gamma)+1)/(1-np.abs(gamma))
        VSWR=round(VSWR)
    VSWR_coefficient.delete(0,END)
    VSWR_coefficient.insert(0,VSWR)


Reflection_label = Label(output,text="Reflection coeff :", font=("helvetica", 15),anchor="s")
Reflection_label.grid(row=1, column=0,pady=100)
Reflection_coefficient=Entry(output,name="gamma", font=("helvetica", 12))
Reflection_coefficient.grid(row=1,column=1)

VSWR_label = Label(output,text="VSWR :", font=("helvetica", 15),anchor="n")
VSWR_label.grid(row=2, column=0,pady=50)
VSWR_coefficient=Entry(output,name="vswr", font=("helvetica", 12))
VSWR_coefficient.grid(row=2,column=1)

#line plot

line=Frame(app)
line.place(relx=0.18,rely=0,relheight=0.45,relwidth=0.41)

point_length_field=Scale(
    line, from_=0, to=length_slider.get(), orient=HORIZONTAL, resolution=0.01, command=speed,length=200,troughcolor="#c6e7ff",bg="white"
)
point_length_field.set(length_slider.get()/2)
point_length_label=Label(line,text=f"length={point_length_field.get()}",font=("helvetica",15))
point_length_label.pack()
point_length_field.pack()

#create a figure and canvas
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=line)
s_plot = canvas.get_tk_widget()
s_plot.place(relx=0.1,rely=0.15,relheight=0.85)
ax.set_title("Voltage across channel").set_color("white") 
fig.patch.set_facecolor('black') 
ax.set_facecolor('black')
ax.tick_params(colors='white') 
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')





# Plots frame
plots = Frame(app)
plots.place(relx=0, rely=0.44, relheight=0.59, relwidth=0.8)

# Create a figure and canvas for the plot
fig1, ax1 = plt.subplots()
canvas1 = FigureCanvasTkAgg(fig1, master=plots)
s_plot = canvas1.get_tk_widget()
s_plot.place(relx=0.01,rely=0.15,relwidth=0.28,relheight=0.7)
ax1.set_title("Source").set_color("white") 
fig1.patch.set_facecolor('black') 
ax1.set_facecolor('black')
ax1.tick_params(colors='white') 
ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.xaxis.label.set_color('white')
ax1.yaxis.label.set_color('white')



fig2, ax2 = plt.subplots()
canvas2 = FigureCanvasTkAgg(fig2, master=plots)
c_plot = canvas2.get_tk_widget()
c_plot.place(relx=0.3,rely=0.15,relwidth=0.4,relheight=0.7)
ax2.set_title("Channel").set_color("white") 
fig2.patch.set_facecolor('black') 
ax2.set_facecolor('black')
ax2.tick_params(colors='white') 
ax2.spines['bottom'].set_color('white')
ax2.spines['left'].set_color('white')
ax2.xaxis.label.set_color('white')
ax2.yaxis.label.set_color('white')

fig3, ax3 = plt.subplots()
canvas3 = FigureCanvasTkAgg(fig3, master=plots)
l_plot = canvas3.get_tk_widget()
l_plot.place(relx=0.71,rely=0.15,relwidth=0.28,relheight=0.7)
ax3.set_title("LOAD").set_color("white") 
fig3.patch.set_facecolor('black') 
ax3.set_facecolor('black')
ax3.tick_params(colors='white') 
ax3.spines['bottom'].set_color('white')
ax3.spines['left'].set_color('white')
ax3.xaxis.label.set_color('white')
ax3.yaxis.label.set_color('white')

# Function to animate the graph
t = np.linspace(-1, 0, 1000)
y = np.zeros_like(t)  # Initialize y-values
animation_id = None  # To store the after() id
running = True  # Flag to indicate if the simulation is running
def update_plot():
    global t, y, animation_id, running,R,H,G,C
    g=RLHC()
    if(R<0 or G<0 or H<0 or C<0):
        running=False
        message_.configure(text="R0,gamma are practically impossible")
    else:
        running=True
        message_.configure(text=" ")


    j=complex(0,1)
    if not running:
        return  # Exit the function if the simulation is stopped
    v = voltage_field.get()
    f = frequency_field.get()
    if(stop):
        speed = speed_slider.get()
    else:
        speed=0
        return

    # Shift the time values to the left
    t = t + speed * 0.02  # Adjust speed scaling as needed
    y = v * np.exp(j*2 * np.pi * f * t)
    # Clear the axis and plot the new data
    ax1.clear()
    ax1.plot(t, np.real(y),color="coral")
    ax1.set_title("Source").set_color("white")
    ax1.set_xlabel("Time (ms)").set_color("white")
    ax1.set_ylabel("Voltage (V)").set_color("white")
    ax1.set_xlim(t.min(), t.max())
    ax1.set_ylim(-2*v - 1, 2*v + 1)  # Set y-limits dynamically

    canvas1.draw()

    #channel plots
    l=length_slider.get()
    del_l=l/10000
    p_constant=get_prop()
    x=np.linspace(0,l,10000)
    f_wave=v*np.exp(j*2*np.pi*f*t[-1]-2*np.pi*p_constant*x)
    
    update_output()
    gamma=complex(Reflection_coefficient.get())
    b_wave=v*np.exp(j*2*np.pi*f*t[-1]-2*np.pi*p_constant*(2*l-x))*gamma
    t_wave=f_wave+b_wave

    ax2.clear()
    forward_wave, = ax2.plot(x, np.real(f_wave), label="forward wave", color="#39FF14", visible=var1.get())  # Bright green (radium)
    backward_wave, = ax2.plot(x, np.real(b_wave), label="backward wave", color="#00FFFF", visible=var2.get())   # Cyan (radium)
    sum_line, = ax2.plot(x, np.real(t_wave), label="Combined wave (Sum)", color="#FF00FF", linestyle="--", visible=var3.get())
    ax2.set_title("Channel").set_color("white")
    ax2.set_xlabel("channel length(2*pi)").set_color("white")
    ax2.set_ylabel("Voltage (V)").set_color("white")
    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim(-2*v - 1, 2*v + 1)  # Set y-limits dynamically
    # Function to toggle visibility of each wave
    def toggle_visibility():
        forward_wave.set_visible(var1.get())
        backward_wave.set_visible(var2.get())
        sum_line.set_visible(var3.get())
    canvas2.draw()

    #load voltage
    r=v*np.exp(j*2*np.pi*f*t-2*np.pi*p_constant*l)*(1+gamma)



    # Clear the axis and plot the new data
    ax3.clear()
    ax3.plot(t, np.real(r),label="backward wave",color="yellow")
    ax3.set_title("LOAD").set_color("white")
    ax3.set_xlabel("Time (ms)").set_color("white")
    ax3.set_ylabel("Voltage (V)").set_color("white")
    ax3.set_xlim(t.min(), t.max())
    ax3.set_ylim(-2*v - 1, 2*v + 1)  # Set y-limits dynamically

    canvas3.draw()

    
    point_length_field.configure(to=l)
    L=point_length_field.get()
    point_length_label.configure(text=f"length={L}")
    p=v*np.exp(j*2*np.pi*f*t-2*np.pi*p_constant*L)+gamma*v*np.exp(j*2*np.pi*f*t-2*np.pi*p_constant*(l+2*L))
    ax.clear()
    ax.plot(t, np.real(p),label="backward wave",color="yellow")
    ax.set_title("Voltage across channel").set_color("white")
    ax.set_xlabel("Time (ms){gamma})").set_color("white")
    ax.set_xlim(t.min(), t.max())
    ax.set_ylim(-2*v - 1, 2*v + 1)  # Set y-limits dynamically
    canvas.draw()

    # Schedule the function to be called again
    animation_id = app.after(50, update_plot)

# Simulate and Close buttons
stop=False
def stop_simulation():
    global stop
    stop=stop^True
    if stop:
        simulate.configure(bg="lightgreen")
    else:
        simulate.configure(bg="red")
    update_plot()

simulate = Button(side, text="Simulate/Stop", command=stop_simulation,font=("helvetica", 15),cursor="hand2")
simulate.grid(row=13, columnspan=2,pady=30)

def close():
    global running
    running = False  # Stop the animation
    if animation_id is not None:
        app.after_cancel(animation_id)  # Cancel the scheduled callback
    app,quit()
    app.destroy()

close_button = Button(side, text="Close", command=close,bg="red",fg="white",font=("helvetica", 15),cursor="hand2")
close_button.grid(row=14, columnspan=2,pady=30)

message_=Label(side,text=" ", font=("helvetica", 17),anchor="s",bg="white",fg="red")
message_.grid(row=15,columnspan=2)


img = PhotoImage(file='logo.png')
app.iconphoto(False, img)
app.mainloop()
