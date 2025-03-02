from CvPythonExtensions import *
import CvScreenEnums
import CvUtil
import ScreenInput

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvCivSelectScreen:
	"Civilization Selection Screen for Custom Game Menu"

	def __init__(self):
		self.sWidgetPrefix = "CivSelectScreen"
		self.MANAGER_SCREEN_ID = self.sWidgetPrefix + "MainWindow"
		self.BACKGROUND_ID = self.sWidgetPrefix + "BackgroundImage"

	def getScreen(self):
		return CyGInterfaceScreen(self.MANAGER_SCREEN_ID, CvScreenEnums.CIVSELECT_SCREEN)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
		return None

	def update(self, fDelta):
		screen = self.getScreen()

		list=[(0,0)]*gc.getNumCivilizationInfos()
		for j in range(gc.getNumCivilizationInfos()):
			list[j] = (gc.getCivilizationInfo(j).getDescription(), j)
		list.sort()

		listCopy = list[:]
		for item in listCopy:
			if gc.getCivilizationInfo(item[1]).isGraphicalOnly():
				list.remove(item)

		nColumns = 2
		nEntries = len(list)
		nRows = nEntries // nColumns
		if (nEntries % nColumns):
			nRows += 1
		tableName = "CivSelectTable"
		xResolution = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE ).getXResolution()
		yResolution = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE ).getYResolution()
		screen.addTableControlGFC(tableName, nColumns, 5, 5, xResolution/2-5, yResolution/2+15, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", (xResolution/2-5)/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			bHuman = gc.getCivilizationInfo(item[1]).isPlayable()
			bAI = gc.getCivilizationInfo(item[1]).isAIPlayable()
			szText = ""
			if not bAI and bHuman:
				szText = localText.getText("TXT_KEY_HUMAN_ONLY", ())
			elif bAI and not bHuman:
				szText = localText.getText("TXT_KEY_AI_ONLY", ())
			elif not bAI and not bHuman:
				szText = localText.getText("TXT_KEY_LOCKED_OUT", ())
			screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + szText + u"</font>", gc.getCivilizationInfo(item[1]).getButton(), WidgetTypes.WIDGET_RESTRICT_CIV, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1
		return None

	def handleInput(self, inputClass):
		iNotifyCode = inputClass.getNotifyCode()
		iNotifyClicked = NotifyCode.NOTIFY_CLICKED
		iNotifyChar = NotifyCode.NOTIFY_CHARACTER

		if(iNotifyCode == iNotifyClicked):
			 sInputName = inputClass.getFunctionName()

		return 0

	def interfaceScreen(self):
		screen = self.getScreen()
		if (screen.isActive()):
			return None

		xResolution = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE ).getXResolution()
		yResolution = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE ).getYResolution()
		screen.setDimensions(xResolution/4, yResolution/4-30, xResolution/2, yResolution/2+60)
		screen.addDDSGFC(self.BACKGROUND_ID, "Art\Interface\Screens\civilopedia\civilopediabg2-opaque.dds", -2, -32, xResolution/2+2, yResolution/2+122, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.showWindowBackground(True)

		screen.setButtonGFC("CivSelectExit", localText.getText("TXT_KEY_SCREEN_CONTINUE", ()), "", xResolution/4-40, yResolution/2+20, 80, 30, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

	def sendMessage(self, argsList):
		iCiv, bAIPlayable, bPlayable = argsList
		CyMessageControl().sendModNetMessage(CvUtil.CivSelector, iCiv, bAIPlayable, bPlayable, 0)
