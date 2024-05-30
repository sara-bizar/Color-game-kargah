import tkinter as tk
import random

class game:
    def __init__(self,window):
        self.window=window

        # self.colors=[("Orange","#ee541a"),("Blue","#1a6dec"),("Yellow","#f3d332"),("Purple","#b244d3"),("Pink","#e65f7c"),("Green","#52d734"),("red","#ea2e35")]
        self.colors={"Orange":"#ee541a","Blue":"#1a6dec","Yellow":"#f3d332","Purple":"#b244d3","Pink":"#e6869a","Green":"#52d734","red":"#ea2e35"}

        self.colorWords=["Orange","Blue","Yellow","Purple","Pink","Green","red",]
        self.realText=random.choice(self.colorWords)
        
        self.textColor=random.choice([i for i in self.colorWords  ])
        self.bgColor=random.choice([i for i in self.colorWords if i != self.textColor ])
        self.backScreen=tk.Frame(window,background=self.colors.get(self.bgColor))
        self.text=tk.Label(self.backScreen,text=self.realText,font =("Calibri",90,"bold"),fg=self.colors.get(self.textColor),bg=self.colors.get(self.bgColor) )
        self.backScreen.pack(fill ="both", expand = True)
        self.text.place(x=300,y=200)
        
    