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
    #pallettes
      #  self.ui.comboBox.activated.connect(self.default_palette)
    ##Sliders
        self.sliders = [self.ui.verticalSlider,self.ui.verticalSlider_2,self.ui.verticalSlider_3,self.ui.verticalSlider_4,self.ui.verticalSlider_5,self.ui.verticalSlider_6,self.ui.verticalSlider_7,self.ui.verticalSlider_8,self.ui.verticalSlider_9,self.ui.verticalSlider_10]
  # #Configure each slider
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
    #    self.default_palette(self.data)
        self.FFT(self.data,self.samplerate,self.sample_length)
   
   ## def default_palette(self, data):
   ##     if(self.ui.comboBox.currentText()=="Pallette 1"):
   ##          sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="viridis")
   ##          plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
   ##          self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
   ##          os.remove("Input1.png")
   ##          print("1")
    #         
    #    elif(self.ui.comboBox.currentText()=="Pallette 2"):
    #         self.palette_2(self.data)
    #
    #    elif(self.ui.comboBox.currentText()=="Pallette 3"):
    #
    #        self.palette_3(self.data)
    #
    #    elif(self.ui.comboBox.currentText()=="Pallette 4"):
    #
    #        self.palette_4(self.data)
    #    else:
    #        self.palette_5(self.data)
#
#
    #def palette_2(self,data):
    #         self.ui.scrollArea_4.clear
    #         sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="inferno")
    #         plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
    #         self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
    #         os.remove("Input1.png")
    #         print("2")
    #def palette_3(self,data):
    #         self.ui.scrollArea_4.clear
    #         sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="magma")
    #         plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
    #         self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
    #         os.remove("Input1.png")
    #         print("3")
    #def palette_4(self,data):
    #         self.ui.scrollArea_4.clear
    #         sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="plasma")
    #         plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
    #         self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
    #         os.remove("Input1.png")
    #         print("4")
    #def palette_5(self,data):
    #         self.ui.scrollArea_4.clear
    #         sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None,cmap="Greys")
    #         plot.savefig('Input1.png', dpi=300, bbox_inches='tight')
    #         self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input1.png'))
    #         os.remove("Input1.png")
    #         print("5")
             
    #Plotting input signal 
    def Channel1 (self,data,time):
        self.data_line1 =self.ui.Channel1_2.plot(time,data,pen=self.pen1)
        self.ui.Channel1_2.plotItem.setLimits(xMin =0, xMax=12)
        self.idx1=0
        self.ui.Channel1_2.plotItem.getViewBox().setAutoPan(x=True,y=True)
        self.timer1.setInterval(10)
        self.timer1.timeout.connect(lambda:self.update_plot_data1(self.data_line1,time,data))
        self.timer1.start()
        self.ui.Channel1_2.show()
        #self.ui.Channel1_2.setXRange(0)

  #Updating plots and repeating signals 
    def update_plot_data1(self,data_line,time,data):
        x = time[:self.idx1]
        y = data[:self.idx1]  
        self.idx1 +=10
        if self.idx1 > len(self.time) :
            self.idx1 = 0 
        if  self.time[self.idx1] >0.5:
            self.ui.Channel1_2.setLimits(xMin =min(x , default=0), xMax=max(x, default=0))
        self.ui.Channel1_2.plotItem.setXRange(max(x,default=0)-0.5 , max(x,default=0))
        self.data_line1.setData(x, y)

    def FFT(self,data,samplerate,sample_length):
        self.FFT = np.fft.rfft(data)
        # Normalize
        self.fftmagnitude = abs(self.FFT)
        self.phase=np.angle(self.FFT)
        self.freqs = np.fft.rfftfreq(len(data),1/samplerate) 
        self.bands = []  # creating Bands
        for i in range(10):
            self.bands.append(self.fftmagnitude[int(i / 10 * len(self.fftmagnitude)): int(
                min(len(self.fftmagnitude) + 1, (i + 1) / 10 * len(self.fftmagnitude)))])
    
    def gain(self,slider,sliderValue):
        self.bands[slider] = np.multiply(self.bands[slider], sliderValue)
        flat_list = [item for sublist in self.bands for item in sublist]
        new_signal = []
        for sublist in self.bands:
           for item in sublist:
               new_signal.append(item)
        final= np.multiply(self.phase,new_signal)
        self.inverse = np.fft.irfft(final)
        self.time = np.arange(self.sample_length) / self.samplerate
        wavio.write("sine.wav", self.inverse , self.samplerate, sampwidth=1)
        self.Channel2(self.inverse,self.time)

    def Channel2 (self,data,time):
       self.data_line2 =self.ui.Channel1_3.plot(time,data,pen=self.pen2)
       self.ui.Channel1_3.plotItem.setLimits(xMin =0, xMax=12)
       self.idx2=0
       self.ui.Channel1_3.plotItem.getViewBox().setAutoPan(x=True,y=True)
       self.timer2.setInterval(10)
       self.timer2.timeout.connect(lambda:self.update_plot_data2(self.data_line2,time,data))
       self.timer2.start()
       self.ui.Channel1_3.show()
     

  #dating plots and repeating signals 
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

#Input spectro 
    def spectro(self,data):
     sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None)
     plot.savefig('Input.png', dpi=300, bbox_inches='tight')
     self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Input.png'))
     os.remove("Input.png")
 #Ouput spectro 
  #  def spectro1(self,data):
       #sepowerSpectrum, freqenciesFound, time, imageAxis = plot.specgram(data,Fs=2000, Fc=None)
       #plot.savefig('Output.png', dpi=300, bbox_inches='tight')
       #self.ui.scrollArea_4.setPixmap(QtGui.QPixmap('Output.png'))
       #os.remove("Output.png")

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
