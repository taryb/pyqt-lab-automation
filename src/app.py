import sys, time, numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QSpinBox, QProgressBar
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

pg.setConfigOptions(antialias=True, background='w', foreground='k')

class CameraSim:
    def __init__(self, w=320, h=240, noise=8.0, seed=None):
        self.w, self.h = w, h
        self.rng = np.random.default_rng(seed)
        self.noise = noise
        self.t = 0
    def frame(self):
        self.t += 1
        yy, xx = np.mgrid[0:self.h, 0:self.w]
        cx = self.w/2 + 8*np.sin(self.t/12)
        cy = self.h/2 + 8*np.cos(self.t/15)
        r2 = ((xx-cx)/60)**2 + ((yy-cy)/60)**2
        img = 40 + 80*np.exp(-r2) + 10*(xx-self.w/2)/self.w
        img += self.rng.normal(0, self.noise, size=img.shape)
        return np.clip(img, 0, 255).astype(np.float32)

class CamView(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel(title))
        self.glw = pg.GraphicsLayoutWidget(); self.layout().addWidget(self.glw)
        self.vb = self.glw.addViewBox(lockAspect=True)
        self.img = pg.ImageItem(); self.vb.addItem(self.img); self.vb.invertY(True)
        self.img.setLookupTable(pg.colormap.get('inferno').getLookupTable(0.0,1.0,256))
    def set(self, frame): self.img.setImage(frame, levels=(0,255), autoLevels=False)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4-Camera Simulator")
        self.resize(1100, 700)
        self.cams = [CameraSim(seed=1), CameraSim(noise=5, seed=2), CameraSim(noise=10, seed=3), CameraSim(noise=7, seed=4)]
        self.views = [CamView("Camera A"), CamView("Camera B"), CamView("Camera C"), CamView("Camera D")]
        grid = QGridLayout(); self.setLayout(QVBoxLayout()); self.layout().addLayout(grid)
        grid.addWidget(self.views[0],0,0); grid.addWidget(self.views[1],0,1)
        grid.addWidget(self.views[2],1,0); grid.addWidget(self.views[3],1,1)
        ctr = QHBoxLayout()
        self.btnStart = QPushButton("Start Live"); self.btnStop = QPushButton("Stop Live"); self.btnStop.setEnabled(False)
        self.btnStart.clicked.connect(self.start); self.btnStop.clicked.connect(self.stop)
        self.avgSpin = QSpinBox(); self.avgSpin.setRange(5,1000); self.avgSpin.setValue(100)
        self.btnMeas = QPushButton("Run Measurement"); self.btnMeas.clicked.connect(self.measure)
        self.progress = QProgressBar(); self.progress.setRange(0,100); self.progress.setValue(0)
        for w in (self.btnStart,self.btnStop, QLabel("Frames to avg:"), self.avgSpin, self.btnMeas, self.progress): ctr.addWidget(w)
        self.layout().addLayout(ctr)
        self.log = QTextEdit(readOnly=True); self.layout().addWidget(self.log)
        self.timer = QTimer(self); self.timer.timeout.connect(self.tick)
        self._measuring=False; self._sum=None; self._sum2=None; self._n=0; self._N=0
        self._say("Ready. Click Start Live.")
    def _say(self,msg): self.log.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    def tick(self):
        frames=[c.frame() for c in self.cams]
        for v,f in zip(self.views,frames): v.set(f)
        if self._measuring:
            if self._sum is None:
                self._sum=[np.zeros_like(frames[0]) for _ in range(4)]
                self._sum2=[np.zeros_like(frames[0]) for _ in range(4)]
            for i in range(4):
                self._sum[i]+=frames[i]; self._sum2[i]+=frames[i]**2
            self._n+=1; self.progress.setValue(int(100*self._n/self._N))
            if self._n>=self._N: self.finish()
    def start(self):
        if not self.timer.isActive():
            self.timer.start(33); self.btnStart.setEnabled(False); self.btnStop.setEnabled(True); self._say("Live started (~30 FPS).")
    def stop(self):
        if self.timer.isActive():
            self.timer.stop(); self.btnStart.setEnabled(True); self.btnStop.setEnabled(False); self._say("Live stopped.")
    def measure(self):
        if not self.timer.isActive(): self.start()
        if self._measuring: self._say("Measurement already running."); return
        self._N=int(self.avgSpin.value()); self._n=0; self._sum=None; self._sum2=None; self._measuring=True; self.progress.setValue(0)
        self._say(f"Measuring: averaging {self._N} frames per camera…")
    def finish(self):
        self._measuring=False; self.progress.setValue(100)
        for i in range(4):
            mean=self._sum[i]/self._N
            var=self._sum2[i]/self._N - mean**2
            std=np.sqrt(np.clip(var,1e-6,None))
            mean_signal=float(np.mean(mean)); noise=float(np.median(std)); snr=mean_signal/max(noise,1e-6)
            self._say(f"Camera {chr(65+i)}: mean={mean_signal:.2f}, noise≈{noise:.2f}, SNR≈{snr:.2f}")
        self._sum=self._sum2=None; self._n=self._N=0

if __name__=="__main__":
    app=QApplication(sys.argv); w=App(); w.show(); sys.exit(app.exec_())
