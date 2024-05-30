import tkinter as tk
import random

class game:
    def __init__(self,window):
        self.window=window

        # self.colors=[("Orange","#ee541a"),("Blue","#1a6dec"),("Yellow","#f3d332"),("Purple","#b244d3"),("Pink","#e65f7c"),("Green","#52d734"),("red","#ea2e35")]
        self.colors={"Orange":"#ee541a","Blue":"#1a6dec","Yellow":"#f3d332","Purple":"#b244d3","Pink":"#e6869a","Green":"#52d734","red":"#ea2e35"}

        self.colorWords=["Orange","Blue","Yellow","Purple","Pink","Green","red",]
        
        self.textColor=random.choice(self.colorWords)    
        self.text=random.choice( self.colorWords )
        self.bgColor=random.choice([i for i in self.colorWords if i != self.textColor ])
        self.backScreen=tk.Frame(window,background=self.colors.get(self.bgColor))
        self.textLable=tk.Label(self.backScreen,text=self.text,font =("Calibri",90,"bold"),fg=self.colors.get(self.textColor),bg=self.colors.get(self.bgColor) )
        self.backScreen.pack(fill ="both", expand = True)
        self.textLable.place(x=300,y=200)

        
    
