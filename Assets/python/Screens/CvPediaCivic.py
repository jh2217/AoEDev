## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaCivic:
	"Civilopedia Screen for Civics"

	def __init__(self, main):
		self.iCivic = -1
		self.top = main

		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eCivic is the CivicInfo object being tested
				"Desired Result" : 'None',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_CIVIC_GOVERNMENT", ())',
				"Purpose" : "Filter by Option Type",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eCivic.getCivicOptionType()',
				"Desired Result" : 'gc.getInfoTypeForString("CIVICOPTION_GOVERNMENT")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_CIVIC_CULTURE", ())',
				"Purpose" : "Filter by Option Type",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eCivic.getCivicOptionType()',
				"Desired Result" : 'gc.getInfoTypeForString("CIVICOPTION_CULTURAL_VALUES")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_CIVIC_LABOR", ())',
				"Purpose" : "Filter by Option Type",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eCivic.getCivicOptionType()',
				"Desired Result" : 'gc.getInfoTypeForString("CIVICOPTION_LABOR")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_CIVIC_ECONOMY", ())',
				"Purpose" : "Filter by Option Type",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eCivic.getCivicOptionType()',
				"Desired Result" : 'gc.getInfoTypeForString("CIVICOPTION_ECONOMY")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_CIVIC_MEMBERSHIP", ())',
				"Purpose" : "Filter by Option Type",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eCivic.getCivicOptionType()',
				"Desired Result" : 'gc.getInfoTypeForString("CIVICOPTION_MEMBERSHIP")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_CIVIC_SPECIFIC", ())',
				"Purpose" : "Filter by Option Type",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eCivic.getPrereqCivilization() > -1',
				"Desired Result" : 'True',
			},
			]

		# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
		self.ALLOWED_FILTERS = self.FILTERS
		self.CURRENT_FILTER = self.FILTERS[0]

		self.SORTS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_ALPHABETICAL", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'eCivic.getDescription()',
			},
			#{ test Ronkhar
			#	"name" : "Sort by Civic Option",
			#	"Purpose" : "Sort by Civic Option Category",
			#	"Value to Sort" : 'eCivic.getCivicOptionType()',
			#},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_CIVIC_UPKEEP", ())',
				"Purpose" : "Default, unsorted method",
				"Value to Sort" : 'eCivic.getUpkeep()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_XML_ORDER", ())',
				"Purpose" : "Default, unsorted method",
				"Value to Sort" : None,
			},
			]

		# List the sorts which you want to be available initially, or self.SORTS to have all of them available from the start
		self.ALLOWED_SORTS = self.SORTS
		self.CURRENT_SORT = self.SORTS[0]
		self.SUB_SORT = self.SORTS[0]

	# Screen construction function
	def interfaceScreen(self, iCivic):

		self.iCivic = iCivic

		self.top.deleteAllWidgets()

		screen = self.top.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		#Filter/Sort dropdowns
		self.top.FILTER_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.FILTER_DROPDOWN_ID,self.top.X_FILTER_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, filter in enumerate(self.ALLOWED_FILTERS):
			screen.addPullDownString(self.top.FILTER_DROPDOWN_ID, eval(filter["name"]), i, i, filter == self.CURRENT_FILTER )

		self.top.SORT_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.SORT_DROPDOWN_ID, self.top.X_SORT_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, sort in enumerate(self.ALLOWED_SORTS):
			screen.addPullDownString(self.top.SORT_DROPDOWN_ID, eval(sort["name"]), 1, 1, sort == self.CURRENT_SORT )

		# Header...
		szHeader = u"<font=4b>" + gc.getCivicInfo(self.iCivic).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Title (upper-right corner, above the list)
		szHeader = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC", ()).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.W_SCREEN -self.top.W_LINKS/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_CIVIC or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_CIVIC
		else:
			self.placeLinks(false)

		# Icon
		self.X_MAIN_PANE = self.top.EXT_SPACING
		self.Y_MAIN_PANE = 70
		self.W_MAIN_PANE = 433
		self.H_MAIN_PANE = 210

		self.X_ICON = 48
		self.Y_ICON = 105
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 64
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
			self.X_MAIN_PANE, self.Y_MAIN_PANE, self.W_MAIN_PANE, self.H_MAIN_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getCivicInfo(self.iCivic).getButton(),
			self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeStats()
		self.placeRequires()
		self.placeSpecial()
		self.placeText()

	def placeStats(self):
		screen = self.top.getScreen()
		self.X_STATS_PANE = self.X_ICON + self.W_ICON + 20
		self.Y_STATS_PANE = 165
		self.W_STATS_PANE = 250
		self.H_STATS_PANE = 200
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "",
			self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)

		# Civic Category
		iCivicOptionType = gc.getCivicInfo(self.iCivic).getCivicOptionType()
		if (iCivicOptionType != -1):
			screen.appendListBoxString(panelName, u"<font=4>" + gc.getCivicOptionInfo(iCivicOptionType).getDescription().upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		# Upkeep
		pUpkeepInfo = gc.getUpkeepInfo(gc.getCivicInfo(self.iCivic).getUpkeep())
		if (pUpkeepInfo):
			screen.appendListBoxString(panelName, u"<font=4>" + pUpkeepInfo.getDescription().upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)


	def placeRequires(self):
		screen = self.top.getScreen()
		self.X_REQUIRES = self.X_MAIN_PANE
		self.Y_REQUIRES = self.Y_MAIN_PANE + self.H_MAIN_PANE
		self.W_REQUIRES = self.W_MAIN_PANE
		self.H_REQUIRES = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
				 self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.enableSelect(panelName, False)
		screen.attachLabel(panelName, "", "  ")

		iTech = gc.getCivicInfo(self.iCivic).getTechPrereq()
		if (iTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

	def placeSpecial(self):
		screen = self.top.getScreen()
		self.X_SPECIAL = self.X_MAIN_PANE
		self.Y_SPECIAL = self.Y_REQUIRES + self.H_REQUIRES
		self.W_SPECIAL = self.W_MAIN_PANE
		self.H_SPECIAL = 262

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false,
				 self.X_SPECIAL, self.Y_SPECIAL, self.W_SPECIAL, self.H_SPECIAL, PanelStyles.PANEL_STYLE_BLUE50 )

		listName = self.top.getNextWidgetName()
		screen.attachListBoxGFC( panelName, listName, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(listName, False)

		szSpecialText = CyGameTextMgr().parseCivicInfo(self.iCivic, True, False, True)
		screen.addMultilineText(listName, szSpecialText[1:], self.X_SPECIAL+5, self.Y_SPECIAL+25, self.W_SPECIAL-10, self.H_SPECIAL-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeText(self):
		screen = self.top.getScreen()
		self.X_TEXT = self.X_MAIN_PANE + self.W_MAIN_PANE + self.top.INT_SPACING
		self.Y_TEXT = self.Y_REQUIRES
		self.W_TEXT = self.top.X_LINKS - self.top.EXT_SPACING - self.X_TEXT
		self.H_TEXT = self.H_SPECIAL + self.H_REQUIRES + self.top.INT_SPACING
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
				 self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_BLUE50 )

		szText = gc.getCivicInfo(self.iCivic).getCivilopedia() + localText.getText("[NEWLINE]", ()) + gc.getCivicInfo(self.iCivic).getStrategy()
		screen.attachMultilineText( panelName, "Text", szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iCivic = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iCivic == self.iCivic:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listCivics = []
		iCount = 0
		for iCivic in range(gc.getNumCivicInfos()):
			eCivic = gc.getCivicInfo(iCivic)
			if not eCivic.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for civic in self.CURRENT_FILTER["HardcodeList"]:
						if iCivic == gc.getInfoTypeForString(civic):
							listCivics.append(iCivic)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listCivics.append(iCivic)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iCivic in listCivics:
			eCivic = gc.getCivicInfo(iCivic)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if self.CURRENT_SORT["Value to Sort"] == 'eCivic.getDescription()':
					sort1 = CvUtil.removeAccent(self,sort1) # alphabetical sorting in the Pedia for languages using accents/diacritics
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			listSorted[iI] = (sort1, sort2, iCivic, eCivic.getDescription(), eCivic.getButton(), 1)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC, True)

		if not self.CURRENT_FILTER == filter:
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0