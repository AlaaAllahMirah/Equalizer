from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog , QPushButton
from PyQt5 import QtWidgets, QtCore,QtGui,uic,QtMultimedia
from mainwindow import Ui_MainWindow
import matplotlib.pyplot as plot
from scipy.fftpack import fft,rfft
from scipy.io import wavfile
from random import randint
import pandas as pd
import pyqtgraph as pg
import numpy as np 
import sys  # We need sys so that we can pass argv to QApplication
import os
import cmath 
import itertools
import operator
import wavio



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    #Actions of open menulist
        self.ui.actionChannel1.triggered.connect(self.load)
        self.ui.Channel1_2.setBackground('w')
        self.ui.Channel1_3.setBackground('w')
    #Colors of every channels
        self.pen1 = pg.mkPen(color=(255, 0, 0))
        self.pen2 = pg.mkPen(color=(100, 100, 100))
     #Timers
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
    #pause&resume buttons
        #ch_1
        self.ui.pushButton_9.clicked.connect(self.resume_1)
        self.ui.pushButton_10.clicked.connect(self.pause_1)
    #Actions for zooming in:
        self.ui.pushButton_7.clicked.connect(lambda: self.zoomin1())
     #Actions for zooming out:
        self.ui.pushButton_8.clicked.connect(lambda: self.zoomout1())
     #Action for Scrolling:
        self.ui.pushButton_5.clicked.connect(lambda: self.scroll_right1())
        self.ui.pushButton_6.clicked.connect(lambda: self.scroll_left1())
        self.ui.spinBox.setSingleStep(10)
        self.ui.spinBox.setValue(10)
        self.ui.spinBox.setMinimum(10)
        self.ui.spinBox.setMaximum(90)
    #Set_speed 
        self.ui.spinBox.valueChanged.connect(lambda: self.set_speed())
    #Show / Hide
        self.ui.checkBox.clicked.connect(self.ui.scrollArea_4.hide)
        self.ui.checkBox_2.clicked.connect(self.ui.scrollArea_5.hide)
    ##Sliders
        self.sliders = [self.ui.verticalSlider,self.ui.verticalSlider_2,self.ui.verticalSlider_3,self.ui.verticalSlider_4,self.ui.verticalSlider_5,self.ui.verticalSlider_6,self.ui.verticalSlider_7,self.ui.verticalSlider_8,self.ui.verticalSlider_9,self.ui.verticalSlider_10]
  # #Configure each sliderflat_list
        for slid in self.sliders:
            slid.setMinimum(0)
            slid.setMaximum(5)
            slid.setPageStep(1)
            slid.setValue(1)
            slid.setSingleStep(1)
      # sliders 
        self.sliders[0].valueChanged.connect(lambda: self.sliderChanged(0))
        self.sliders[1].valueChanged.connect(lambda: self.sliderChanged(1))
        self.sliders[2].valueChanged.connect(lambda: self.sliderChanged(2))
        self.sliders[3].valueChanged.connect(lambda: self.sliderChanged(3))
        self.sliders[4].valueChanged.connect(lambda: self.sliderChanged(4))
        self.sliders[5].valueChanged.connect(lambda: self.sliderChanged(5))
        self.sliders[6].valueChanged.connect(lambda: self.sliderChanged(6))
        self.sliders[7].valueChanged.connect(lambda: self.sliderChanged(7))
        self.sliders[8].valueChanged.connect(lambda: self.sliderChanged(8))
        self.sliders[9].valueChanged.connect(lambda: self.sliderChanged(9))

    def sliderChanged(self, slider):
        sliderValue = self.sliders[slider].value()
        self.gain(slider,sliderValue)
        
    def load(self):
        options =  QtWidgets.QFileDialog.Options()
        fname = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",
                        "(*.wav) ", options=options) 
        if(fname[0]!=''):
            self.read_data(fname)
             
        else:
            pass
        
    #Reading data from files
    def read_data(self,fname):
        path = fname[0]
        self.samplerate,self.data = wavfile.read(path)
        self.sample_length = self.data.shape[0] 
        self.time = np.arange(self.sample_length) / self.samplerate
        self.Channel1(self.data,self.time)
        #self.ui.Channel1_2.plot(self.time,self.data,pen=self.pen1)
        #self.ui.Channel1_2.setXRange(0,len(self.data))
        self.spectrogram(self.data)
        self.min_sliderChanged(self.data)
        self.max_sliderChanged(self.data)
        self.FFT(self.data,self.samplerate,self.sample_length)
      
            
    #==================================================================================================================================
    #pallettes
        self.ui.comboBox.activated.connect(self.min_sliderChanged)
     #Hoizontal sliders
        self.ui.horizontalSlider.valueChanged.connect(self.min_sliderChanged)
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider_2.valueChanged.connect(self.max_sliderChanged)
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.setMinimum(0)
    #min_slider
    def min_sliderChanged(self,data):
        if (self.ui.horizontalSlider.value()>0 and self.ui.horizontalSlider.value()<20):
                #self.data_=self.data[100:2000]
                self.choose_pallete(self.data,-80,-50)
        elif(self.ui.horizontalSlider.value()>20 and self.ui.horizontalSlider.value()<60):
                self.choose_pallete(self.data,-50,-20)   
        else:
            self.choose_pallete(self.data,-100,40)
    def max_sliderChanged(self,data):
        if (self.ui.horizontalSlider_2.value()>0 and self.ui.horizontalSlider_2.value()<20):
                #self.data_=self.data[100:2000]
                self.choose_pallete(self.data,-80,-50)
        elif(self.ui.horizontalSlider_2.value()>20 and self.ui.horizontalSlider_2.value()<60):
                self.choose_pallete(self.data,-50,-20)   
        else:
            self.choose_pallete(self.data,-100,40)

    def choose_pallete(self, data,min_value,max_value):
        if(self.ui.comboBox.currentText()=="Pallette 1"):
             self.spectrogram_updated(self.data,"RdGy",min_value,max_value)
        elif(self.ui.comboBox.currentText()=="Pallette 2"):
             self.spectrogram_updated(self.data,"inferno",min_value,max_value)
        elif(self.ui.comboBox.currentText()=="Pallette 3"):
             self.spectrogram_updated(self.data,"magma",min_value,max_value)
        elif(self.ui.comboBox.currentText()=="Pallette 4"):
            self.spectrogram_updated(self.data,"Greys",min_value,max_value)
        else:
             self.spectrogram_updated(self.data,"plasma",min_value,max_value)
       

    def spectrogram_updated(self,data,color=None,min_value=None,max_value=None):
               sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000,Fc=1000,vmin=min_value,vmax=max_value,cmap=color)
               #plot.colorbar(label='1')
               plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
               self.ui.scrollArea_5.setPixmap(QtGui.QPixmap('Input1.png'))
               os.remove("Input1.png")


    def spectrogram(self,data):
               sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000,Fc=1000,cmap="plasma")
               #plot.colorbar(label='1')
               plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
               self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
               os.remove("Input1.png")

    #=========================================================================================================
    
             
 ##Plotting input signal 
    def Channel1 (self,data,time):
        self.data_line1 =self.ui.Channel1_2.plot(time,data,pen=self.pen1)
        self.ui.Channel1_2.plotItem.setLimits(xMin=0 )
        self.idx1=0
        self.ui.Channel1_2.plotItem.getViewBox().setAutoPan(x=True,y=True)
        self.timer1.setInterval(10)
        self.timer1.timeout.connect(lambda:self.update_plot_data1(self.data_line1,time,data))
        self.timer1.start()
        self.ui.Channel1_2.show()
       #self.ui.Channel1_2.setXRange(0)
#
  #Updating plots and repeating signals 
    def update_plot_data1(self,data_line,time,data):
        x = time[:self.idx1]
        y = data[:self.idx1]  
        self.idx1 +=10
        if self.idx1 > len(self.time) :
            self.idx1 = 0 
        if  self.time[self.idx1] >0.5:
            self.ui.Channel1_2.setLimits(xMin =min(x , default=0), xMax=max(x, default=0))
        self.ui.Channel1_2.plotItem.setXRange(max(x,default=0)-0.5, max(x,default=0))
        self.data_line1.setData(x, y)

    def FFT(self,data,samplerate,sample_length):
        self.FFT = np.fft.rfft(data)
        # Normalize
        self.fftmagnitude = abs(self.FFT)
        self.phase=np.angle(self.FFT)
        #print(len(self.phase))
        self.freqs = np.fft.rfftfreq(len(data),1/samplerate) 
        self.bands = []  # creating Bands
        for i in range(10):
            self.bands.append(self.fftmagnitude[int(i / 10 * len(self.fftmagnitude)): int(
                min(len(self.fftmagnitude) + 1, (i + 1) / 10 * len(self.fftmagnitude)))])
        self.bandsdata=[]
        for i in range (10):
           self.bandsdata.append([])
        self.bandsdata=list.copy(self.bands)
        #print(self.bands[0][0])
        if (self.sliders[0].value()==1 &self.sliders[1].value()==1&self.sliders[2].value()==1&self.sliders[3].value()==1&self.sliders[4].value()==1&self.sliders[5].value()==1&self.sliders[6].value()==1&self.sliders[7].value()==1&self.sliders[8].value()==1&self.sliders[9].value()==1):
                self.ifft = np.fft.irfft(self.FFT)
                self.sample_length = self.ifft.shape[0] 
                time = np.arange(self.sample_length) / self.samplerate
                #self.data_line1=self.ui.Channel1_3.plot(time,self.ifft,pen=self.pen2)
                self.Channel2(self.ifft,self.time)
                
          
    def gain(self,slider,sliderValue):
        self.bandsdata[slider] = np.multiply(self.bands[slider], sliderValue)
        self.ui.Channel1_3.removeItem(self.data_line2)
        #print(self.bandsdata[slider][0])
        flat_list = [item for sublist in self.bandsdata for item in sublist]
        self.gaineddata = []
        for sublist in self.bandsdata:
           for item in sublist:
               self.gaineddata.append(item)
        #print(len(self.gaineddata))
        self.gained=np.multiply(np.array(self.gaineddata),np.exp(1j*self.phase))
        self.IFFT= np.fft.irfft(self.gained)
        time = np.arange(self.sample_length) / self.samplerate
        wavio.write("Output.wav", self.IFFT, self.samplerate, sampwidth=1)
        #self.data_line1= self.ui.Channel1_3.plot(time,self.IFFT,pen=self.pen2)
        self.min_sliderChanged(self.IFFT)
        self.max_sliderChanged(self.IFFT)
        self.spectrogram_updated(self.IFFT)
        self.Channel2(self.IFFT,self.time)

    def Channel2 (self,ifft,time):
       self.data_line2 =self.ui.Channel1_3.plot(time,ifft,pen=self.pen2)
       self.ui.Channel1_3.plotItem.setLimits(xMin =0,yMin=0.6)
       self.idx2=0
       self.ui.Channel1_3.plotItem.getViewBox().setAutoPan(x=True,y=True)
       self.timer2.setInterval(10)
       self.timer2.timeout.connect(lambda:self.update_plot_data2(self.data_line2,time,ifft))
       self.timer2.start()
       self.ui.Channel1_3.show()
     

    #udating plots and repeating signals 
    def update_plot_data2(self,data_line,time,data):
       x = time[:self.idx2]
       y = data[:self.idx2]  
       self.idx2 +=10
       if self.idx2 > len(self.time) :
           self.idx2 = 0 
       if  self.time[self.idx2] >0.5:
           self.ui.Channel1_3.setLimits(xMin =min(x , default=0), xMax=max(x, default=0))
       self.ui.Channel1_3.plotItem.setXRange(max(x,default=0)-0.5 , max(x,default=0))
       self.data_line2.setData(x,y)



 

   

 #rume&pause
    def resume_1(self):
        self.timer1.start()
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(True)
    def pause_1(self):
        self.timer1.stop()
        self.ui.pushButton_10.setEnabled(False)
        self.ui.pushButton_9.setEnabled(True)
    #Zooming in and out 
    def zoomin1 (self):
        self.ui.Channel1_2.plotItem.getViewBox().scaleBy(y=0.9 ,x=0.9)
    def zoomout1 (self):
       self.ui.Channel1_2.plotItem.getViewBox().scaleBy(y=1/0.9 ,x=1/0.9)
    #Scrolling Left,right
    def scroll_right1(self):
        self.ui.Channel1_2.plotItem.getViewBox().translateBy(x=-0.1,y=0)
    def scroll_left1(self):
        self.ui.Channel1_2.plotItem.getViewBox().translateBy(x=0.1,y=0)
    def set_speed(self):
        self.timer1.setInterval(self.ui.spinBox.value())
        self.timer1.timeout.connect(self.update_plot_data1(self.data_line1,time,data))
        self.timer1.start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
 main()
