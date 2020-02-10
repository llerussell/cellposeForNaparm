# cellpose for naparm
# Lloyd Russell 10th January 2020

from GUI import GUI
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QTimer, QRectF, QUrl
from PyQt5.QtWidgets import (QComboBox, QCheckBox, QLineEdit, QSpinBox,
							 QDoubleSpinBox, QFileDialog, QApplication,
							 QDesktopWidget, QMainWindow, QMessageBox)
from PyQt5.QtGui import QColor, QIcon, QPalette, QDesktopServices
import sys
import os
import ctypes
import json
import numpy as np
import glob
from skimage.external import tifffile
from scipy import io as sio
import mxnet as mx
from cellpose import models



class Worker(QObject):

	status_signal = pyqtSignal(str, name='statusSignal')
	finished_signal = pyqtSignal()

	def __init__(self, gui_values, filepaths):
		super().__init__()
		self.p = gui_values
		self.filepaths = filepaths


	def work(self):
		# get the parameters from gui
		p = self.p

		# check if GPU
		if p['useGPU']:
			device = mx.gpu()
		else:
			device = mx.cpu()

		# load files
		self.status_signal.emit('Loading images...')
		files = self.filepaths
		nimgs = len(files)
		imgs = [tifffile.TiffFile(f, multifile=True).asarray() for f in files]
		# imgs = [plt.imread(f) for f in files]

		# adjust the dimensions of the images if needed
		# if z-stack, reorder the stack to be x,y,z:
		if nimgs==1:
			if len(imgs[0].shape) > 2 and imgs[0].shape[0] < imgs[0].shape[1] and imgs[0].shape[0] < imgs[0].shape[2]:
				imgs_new = []
				for z in range(imgs[0].shape[0]):
					imgs_new.append(imgs[0][z,:,:].squeeze())
				imgs = imgs_new
				nimgs = len(imgs)

		# assuming single channel grayscale image, reshape into 3d array:
		for f in range(nimgs):
			if len(imgs[f].shape) < 3:
				imgs[f] = imgs[f].reshape(512,512,1)  # assuming 512x512!

		# run cellpose
		self.status_signal.emit('Running segmentation...')
		cell_diam_px = p['cellSize']
		rescale = 30 / cell_diam_px
		model = models.Cellpose(device, model_type=p['modelType'])
		masks, flows, styles, diams = model.eval(imgs, rescale=rescale, channels=[0,0], threshold=p['threshold'])

		# save the results to MAT file
		self.status_signal.emit('Saving to MAT file...')
		base = os.path.splitext(files[0])[0]
		sio.savemat(base + '_CELLPOSE.mat',
		                    {'software': 'cellpose',
		                    'files': files,
		                    'model': p['modelType'],
		                    'cellsize': p['cellSize'],
		                    'threshold': p['threshold'],
		                     'styles': styles,
		                     'masks': masks,
		                     'img': imgs,
		                     'filename': base,
		                     'flows': flows,
		                     'diams': diams})

		self.status_signal.emit('Done')
		self.finished_signal.emit()



class MainWindow(QMainWindow, GUI.Ui_MainWindow):
	'''
	The GUI window
	'''

	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)

		# set up install paths
		self.install_dir = os.getcwd()

		# make worker thread
		self.workerThread = QThread()

		# restore default values
		self.loadDefaults()

		# allow drag and drop
		self.setAcceptDrops(True)

		# signal/slot connections
		self.setConnects()

		# get gui elements
		self.getValues()


	def dragEnterEvent( self, event ):
		data = event.mimeData()
		urls = data.urls()
		if ( urls and urls[0].scheme() == 'file' ):
			event.acceptProposedAction()


	def dragMoveEvent( self, event ):
		data = event.mimeData()
		urls = data.urls()
		if ( urls and urls[0].scheme() == 'file' ):
			event.acceptProposedAction()


	def dropEvent( self, event ):
		data = event.mimeData()
		urls = data.urls()
		if ( urls and urls[0].scheme() == 'file' ):
			filepaths = [u.path() for u in urls]

			# for some reason, this doubles up the intro slash
			if os.name == 'nt':
				filepaths = [f[1:] for f in filepaths]

			filepaths = sorted(filepaths)
			self.ImagesLoaded_label.setText('\n'.join(filepaths))
			self.filepaths = filepaths


	def setConnects(self):
		self.setDefaults_pushButton.clicked.connect(self.setDefaults)
		self.run_pushButton.clicked.connect(self.clickRun)

		# auto add connects to update p and trial config plot whenever anything changes
		widgets = (QComboBox, QCheckBox, QLineEdit, QSpinBox, QDoubleSpinBox)
		for obj in self.findChildren(widgets):
			if isinstance(obj, QComboBox):
				obj.currentIndexChanged.connect(self.getValues)
			if isinstance(obj, QCheckBox):
				obj.stateChanged.connect(self.getValues)
			if isinstance(obj, QLineEdit):
				obj.textChanged.connect(self.getValues)
			if isinstance(obj, QSpinBox):
				obj.valueChanged.connect(self.getValues)
			if isinstance(obj, QDoubleSpinBox):
				obj.valueChanged.connect(self.getValues)


	def getValues(self):
		# extract gui values store in self.p
		widgets = (QComboBox, QCheckBox, QLineEdit, QSpinBox, QDoubleSpinBox)
		p = {}
		for obj in self.findChildren(widgets):
			fullname = str(obj.objectName())
			trimmed_name = fullname.split('_')[0]
			if isinstance(obj, QComboBox):
				p[trimmed_name] = str(obj.currentText())
			if isinstance(obj, QCheckBox):
				p[trimmed_name] = bool(obj.isChecked())
			if isinstance(obj, QLineEdit):
				if 'spinbox' not in fullname:
					p[trimmed_name] = str(obj.text())
			if isinstance(obj, QSpinBox):
				p[trimmed_name] = int(obj.value())
			if isinstance(obj, QDoubleSpinBox):
				p[trimmed_name] = float(obj.value())

		# save parameters
		self.p = p


	def setValues(self, p):
		# populate gui with new values
		widgets = (QComboBox, QCheckBox, QLineEdit, QSpinBox, QDoubleSpinBox)
		for obj in self.settings_groupBox.findChildren(widgets):
			fullname = str(obj.objectName())
			trimmed_name = fullname.split('_')[0]
			try:
				if isinstance(obj, QComboBox):
					value = p[trimmed_name]
					index = obj.findText(value)  # get the corresponding index for specified string in combobox
					obj.setCurrentIndex(index)  # preselect a combobox value by index
				if isinstance(obj, QLineEdit):
					value = p[trimmed_name]
					if 'spinbox' not in trimmed_name:
						obj.setText(value)  # restore lineEditFile
				if isinstance(obj, QCheckBox):
					value = p[trimmed_name]
					if value is not None:
						obj.setChecked(value)  # restore checkbox
				if isinstance(obj, QSpinBox):
					value = p[trimmed_name]
					obj.setValue(value)  # restore lineEditFile
				if isinstance(obj, QDoubleSpinBox):
					value = p[trimmed_name]
					obj.setValue(value)  # restore lineEditFile
			except:
				continue


	def setDefaults(self):
		defaults_file = os.path.join(self.install_dir, 'GUIdefaults.cfg')
		json.dump(self.p, open(defaults_file, 'w'), sort_keys=True, indent=4)


	def loadDefaults(self):
		defaults_file = os.path.join(self.install_dir, 'GUIdefaults.cfg')
		if os.path.isfile(defaults_file):
			p = json.load(open(defaults_file, 'r'))
			self.setValues(p)
			self.p = p


	def clickRun(self):
		self.getValues()

		# setup threading
		self.workerObject = Worker(self.p, self.filepaths)
		self.workerObject.moveToThread(self.workerThread)
		self.workerObject.status_signal.connect(self.updateStatusBar)
		self.workerThread.started.connect(self.workerObject.work)
		self.workerObject.finished_signal.connect(self.workerThread.exit)
		self.workerThread.start()


	def updateStatusBar(self, msg):
		self.statusbar.showMessage(msg)



# Main entry to program.  Sets up the main app and create a new window.
def main(argv):
	# create Qt application
	app = QApplication(argv)

	# create main window
	window = MainWindow()

	# fix for windows to show icon in taskbar
	if os.name == 'nt':
		myappid = 'cellposeForNaparm' # arbitrary string
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

	# show the window icon
	if os.path.isfile('GUI/cellpose.png'):
		window.setWindowIcon(QIcon('GUI/cellpose.png'))

	# show it and bring to front
	window.show()
	window.raise_()

	# start the app
	sys.exit(app.exec_())

if __name__ == '__main__':
	# launch program
	main(sys.argv)
