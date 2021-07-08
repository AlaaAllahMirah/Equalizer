def loadsignal(self) :
        fname = QtGui.QFileDialog.getOpenFileName()
        self.path = fname[0]
        self.fs, self.data = wavfile.read(self.path)
        self.pen = pg.mkPen(color=(0,160, 0))
        self.graphicsView1.plot(self.data, pen=self.pen)
        self.graphicsView1.setYRange(min(self.data), max(self.data))
        self.data = fftpack.rfft(self.data)
        new_data =np.abs(self.data)
        self.phase = np.angle(self.data)
        freqs = fftpack.fftfreq(len(self.data)) * self.fs
        self.graphicsView3.plot(freqs, new_data)
        while len(freqs) % 10 != 0:
            freqs = freqs[:-1]
        self.bands = list()  # creating Bands
        for i in range(10):
            self.bands.append(new_data[int(i / 10 * len(new_data)): int(
                min(len(new_data) + 1, (i + 1) / 10 * len(new_data)))])

    def gain(self):
        for i in range(10):
            self.bands[i] = np.multiply(self.bands[i], self.slider[i].value())
        flat_list = [item for sublist in self.bands for item in sublist]
        new_signal = []
        for sublist in self.bands:
           for item in sublist:
               new_signal.append(item)
        final= np.multiply(self.phase,new_signal)
        self.inverse = np.fft.irfft(final)
        self.graphicsView2.setYRange(min(self.inverse), max(self.inverse))
        self.graphicsView2.plot(self.inverse, pen=self.pen)