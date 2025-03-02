# FoxDebug.py
# 2009 Fredrik 'Grey Fox' Henriksson

from CvPythonExtensions import *
import CvScreensInterface
from colors import *
from TabElements import *
from collections import deque
import CvUtil
import string
import random
import time
import pickle

localText = CyTranslator()

# Grey Fox Debug
class FoxDebug:
	def __init__(self, title="Grey Fox Debug Window", width = 600, height = 440):
		self.title 					= title
		self.width 					= width
		self.height 				= height
		self.iScreenHeight			= 50
		self.DebugHistory 			= []
		self.szDebugThisTurn		= ""
		self.iRow 					= 0
		self.ffTimes				= {
			"totalTime"				: [0.0],
			"rebuildGraphics"		: [0.0],
			"doFFTurn"				: [0.0],
			"doTurnKhazad"			: [0.0],
			"doTurnLuchuirp"		: [0.0],
			"doTurnArchos"			: [0.0],
			"doTurnScions"			: [0.0],
			"doTurnGrigori"			: [0.0],
			"doTurnCualli"			: [0.0],

		}
		self.gfTimes				= {
			"totalTime"				: [0.0],
			"rebuildGraphics"		: [0.0],
			"doFFTurn"				: [0.0],
			"doTurnKhazad"			: [0.0],
			"doTurnLuchuirp"		: [0.0],
			"doTurnArchos"			: [0.0],
			"doTurnGrigori"			: [0.0],
			"doTurnScions"			: [0.0],
			"doTurnCualli"			: [0.0],

		}
		self.callbackIFace 		= "CvOptionsScreenCallbackInterface"

#################### GREY FOX DEBUG TEXT ######################
	def addEntry(self, which, index, data):
		if which == "ff":
			list = self.ffTimes[index]
			list.append(data)
			self.ffTimes[index] = list
		else:
			list = self.gfTimes[index]
			list.append(data)
			self.gfTimes[index] = list

	def compareAndPrint(self, iGameTurn, szCompare):
		ffTimes	= self.ffTimes[szCompare]
		gfTimes	= self.gfTimes[szCompare]

		iFFEntries = len(ffTimes)
		iGFEntries = len(gfTimes)
		iNumTimes = 0
		iGFtime = 0 ; iFFtime = 0;
		if iFFEntries > iGFEntries:
			iNumTimes = iGFEntries
			ffTimes = ffTimes[:iNumTimes]
		elif  iFFEntries < iGFEntries:
			iNumTimes = iFFEntries
			gfTimes = gfTimes[:iNumTimes]
		else:
			iNumTimes = iFFEntries

		for iFF in ffTimes:
			iFFtime += iFF
		for iGF in gfTimes:
			iGFtime += iGF

		iDiff = iFFtime - iGFtime

		if iDiff != 0:
			#szText = "[NEWLINE]"; self.addLine( szText );
			szText = "Turn: %s -=-=-=- %s difference -=-=-=- [NEWLINE]" % (iGameTurn, szCompare); self.addLine( szText );
			if iDiff < 0:
				szText = "Grey Fox slower by: %.9f [NEWLINE]" % (iDiff)
				self.addLine( szText );
			elif iDiff > 0:
				szText = "Grey Fox faster by: %.9f [NEWLINE]" % (iDiff)
				self.addLine( szText );

	def saveData(self):

		aData = []

		aData.append(self.iRow)
		aData.append(self.DebugHistory)
		aData.append(self.szDebugThisTurn)
		aData.append(self.ffTimes)
		aData.append(self.gfTimes)

		return aData

	def loadData(self, aData):

		iIterator = 0

		self.iRow = aData[iIterator]
		iIterator += 1
		self.DebugHistory = aData[iIterator]
		iIterator += 1
		self.szDebugThisTurn = aData[iIterator]
		iIterator += 1
		self.ffTimes = aData[iIterator]
		iIterator += 1
		self.gfTimes = aData[iIterator]
		iIterator += 1

	def timing(self, f, n):
		print f.__name__,
		r = range(n)
		t1 = time.clock()
		for i in r:
			f(); f(); f(); f(); f(); f(); f(); f(); f(); f()
		t2 = time.clock()
		iTime = t2-t1
		return round(iTime, 4)

	def timingArg(self, f, n, a):
		print f.__name__,
		r = range(n)
		t1 = time.clock()
		for i in r:
			f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a)
		t2 = time.clock()
		iTime = t2-t1
		return round(iTime, 4)

	def clearDebugText(self):
		self.szDebugThisTurn = ""

	def getDebugText(self):
		return self.szDebugThisTurn

	def addDebugHistory(self, szText):
		self.DebugHistory.append(szText)

	def getDebugHistory(self):
		return self.DebugHistory

	def getTabControl(self):
		return self.pTabControl

	def addLine(self, text, color = None):
		self.szDebugThisTurn += text
		print text

	def updateDebugPanel(self):
		"""
		Called everytime the window is to be created/redrawn
		"""
		screen = CyGInterfaceScreen( "MainInterface", 99 )
		screen.hide( "DEBUGPanel" )
		screen.hide( "DEBUGTextPanel" )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		self.addDebugHistory(self.getDebugText())

		title = self.title

		self.pTabControl = CyGTabCtrl(title, True, True)
		tab = self.pTabControl

		tab.setModal(0)
		tab.setSize(self.width, self.height)
		tab.setControlsExpanding(False)
		tab.setColumnLength(self.iScreenHeight)
		tab.setNumColumns(200)

		self.createTabs()

	def createTabs(self):
		"""
		Creates the tabs in the window
		"""
		self.drawDebugMessagesTab()
		self.drawSetupTab()

	def drawDebugMessagesTab(self):
		"""
		Tab where Messages are shown
		"""
		tab = self.pTabControl
		title = "Debug"

		panel = title+"Form"
		tab.attachTabItem(panel, title)

		parent = panel
		panel = title+"VBoxParent"
		tab.attachVBox(parent, panel)

		parent = panel
		panel = title+"PanelCenter"
		tab.attachPanel(parent, panel)
		tab.setStyle(panel, "Panel_Empty")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_VEXPANDING")

		parent = panel
		panel = title+"Panel"
		tab.attachScrollPanel(parent, panel)
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_VEXPANDING")

		parent = panel
		panel = title+"TextBox"
		tab.attachVBox(parent, panel)
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HMIN")

		self.populateRows()

	def drawSetupTab(self):
		"""
		Tab for setting the debug up
		"""
		tab = self.pTabControl
		title = "Setup"

		panel = title+"Form"
		tab.attachTabItem(panel, title)

		parent = panel
		panel = title+"VBoxParent"
		tab.attachVBox(parent, panel)

		parent = panel
		panel = title+"PanelCenter"
		tab.attachPanel(parent, panel)
		tab.setStyle(panel, "Panel_Empty")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_VEXPANDING")

		parent = panel
		panel = title+"Panel"
		tab.attachScrollPanel(parent, panel)
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HEXPANDING")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_VEXPANDING")

		parent = panel
		panel = title+"TextBox"
		tab.attachVBox(parent, panel)
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HMIN")
		tab.setLayoutFlag(panel, "LAYOUT_SIZE_HMIN")


	def populateRows(self):
		"""
		Prints out the rows of text on the window tab
		"""
		aString = ""

		HistoryText = self.getDebugHistory()
		size = len(HistoryText)
		if size > 0:
			queue = deque(reversed(HistoryText))
			while size > 0:
				self.addRow(queue.popleft())
				size-=1
		self.clearDebugText()

	def addRow(self, szText):
		"""
		Add rows, which is basically or several labels, with a separator after
		"""
		tab = self.pTabControl
		prefix = "GF_DebugRow"
		iRow = self.iRow
		szBox = "DebugTextBox"
		szName = szBox

		bList = szText.split()
		cNewString = ""; i = 0
		Lines = deque([])
		for word in bList:
			find = word.find("[NEWLINE]")
			if find != -1:
				if word[:9] == '[NEWLINE]':
					szDebug = "word[:9] == [NEWLINE]\n"
					szDebug += "Lines.append(cNewString)\n"
					split = word.split('[NEWLINE]')
					Lines.append(cNewString)
					cNewString = split[1]+" "
					szDebug += "cNewString = split[1] : "+cNewString+"\n"
				else:
					split = word.split('[NEWLINE]')

					cNewString += split[0]+" "
					Lines.append(cNewString)
					cNewString = split[1]+" "

				continue

			if len(cNewString) >= 56:
				Lines.append(cNewString)
				cNewString = ""

			cNewString += word +" "

		sep = szName +str(iRow)+ "Sep"
		for line in Lines:
			szName = prefix+str(iRow)
			addLabel( tab, szBox, szName, localText.getText(line,()));
			tab.attachHSeparator(szBox, sep)
			iRow += 1

		self.iRow = iRow
		sep = szName +str(iRow)+ "Sep"
		tab.attachHSeparator(szBox, sep)




	