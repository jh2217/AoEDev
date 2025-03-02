## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import random

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaSpawnGroup:
	"Civilopedia Screen for SpawnGroups"

	def __init__(self, main):
		self.iSpawnGroup = -1
		self.top = main

		self.X_STRATEGY = 30
		self.Y_STRATEGY = 65
		self.W_STRATEGY = 365
		self.H_STRATEGY = 390

		self.X_HISTORY = self.X_STRATEGY + self.W_STRATEGY + 20
		self.Y_HISTORY = self.Y_STRATEGY
		self.W_HISTORY = self.W_STRATEGY
		self.H_HISTORY = self.H_STRATEGY

		self.X_DETAILS = self.X_STRATEGY + 10
		self.Y_DETAILS = self.Y_STRATEGY + self.H_STRATEGY + 20
		self.W_DETAILS = self.W_STRATEGY * 2
		self.H_DETAILS = self.H_STRATEGY / 2

		self.X_BANNER_UNIQUE = 40
		self.Y_BANNER_UNIQUE = 75
		self.W_BANNER_UNIQUE = 730
		self.H_BANNER_UNIQUE = 175

		self.X_STRATEGY_UNIQUE = self.X_BANNER_UNIQUE - 10
		self.Y_STRATEGY_UNIQUE = self.Y_BANNER_UNIQUE + self.H_BANNER_UNIQUE + 20
		self.W_STRATEGY_UNIQUE = (self.W_BANNER_UNIQUE / 2)
		self.H_STRATEGY_UNIQUE = self.H_BANNER_UNIQUE + 10

		self.X_HISTORY_UNIQUE = self.X_STRATEGY_UNIQUE + self.W_STRATEGY_UNIQUE + 20
		self.Y_HISTORY_UNIQUE = self.Y_BANNER_UNIQUE + self.H_BANNER_UNIQUE + 20
		self.W_HISTORY_UNIQUE = (self.W_BANNER_UNIQUE / 2)
		self.H_HISTORY_UNIQUE = self.H_STRATEGY_UNIQUE

		self.X_DETAILS_UNIQUE = self.X_BANNER_UNIQUE
		self.Y_DETAILS_UNIQUE = self.Y_BANNER_UNIQUE + (self.H_STRATEGY_UNIQUE * 2) + 30
		self.W_DETAILS_UNIQUE = self.W_BANNER_UNIQUE
		self.H_DETAILS_UNIQUE = self.H_BANNER_UNIQUE + 20

		self.FILTERS =	[
			{
				"name" : "UnFiltered",		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eSpawnGroup is the SpawnGroupInfo object being tested
				"Desired Result" : 'None',
			},
			]

		# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
		self.ALLOWED_FILTERS = self.FILTERS
		self.CURRENT_FILTER = self.FILTERS[0]

		self.SORTS =	[
			{
				"name" : "Sort by Alphabet",
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'eSpawnGroup.getDescription()',
			},
			{
				"name" : "Sort by XML Order",
				"Purpose" : "Default, unsorted method",
				"Value to Sort" : None,
			},
			]

		# List the sorts which you want to be available initially, or self.SORTS to have all of them available from the start
		self.ALLOWED_SORTS = self.SORTS
		self.CURRENT_SORT = self.SORTS[0]
		self.SUB_SORT = self.SORTS[0]

	# Screen construction function
	def interfaceScreen(self, iSpawnGroup):
		self.iSpawnGroup = iSpawnGroup

		self.top.deleteAllWidgets()

		screen = self.top.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		#Filter/Sort dropdowns
		self.top.FILTER_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.FILTER_DROPDOWN_ID,self.top.X_FILTER_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, filter in enumerate(self.ALLOWED_FILTERS):
			screen.addPullDownString(self.top.FILTER_DROPDOWN_ID, filter["name"], i, i, filter == self.CURRENT_FILTER )

		self.top.SORT_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.SORT_DROPDOWN_ID, self.top.X_SORT_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, sort in enumerate(self.ALLOWED_SORTS):
			screen.addPullDownString(self.top.SORT_DROPDOWN_ID, sort["name"], 1, 1, sort == self.CURRENT_SORT )

		# Header...
		szHeader = u"<font=4b>" + gc.getSpawnGroupInfo(self.iSpawnGroup).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_SPAWNGROUP or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_SPAWNGROUP
		else:
			self.placeLinks(false)


		if 	gc.getSpawnGroupInfo(self.iSpawnGroup).isUnique():
			self.placeBannerUnique()
			self.placeStrategyUnique()
			self.placeHistoryUnique()
			self.placeDetailsUnique()
		else:
			self.placeStrategy()
			self.placeHistory()
			self.placeDetails()

#Start Standard Functions
	def placeHistory(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )

		historyTextName = self.top.getNextWidgetName()
		CivilopediaText = gc.getSpawnGroupInfo(self.iSpawnGroup).getCivilopedia()
		CivilopediaText = u"<font=2>" + CivilopediaText + u"</font>"
		screen.attachMultilineText( panelName, historyTextName, CivilopediaText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeDetails(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_DETAILS, self.Y_DETAILS, self.W_DETAILS, self.H_DETAILS, PanelStyles.PANEL_STYLE_BLUE50 )

		detailsTextName = self.top.getNextWidgetName()
		DetailsText = CyGameTextMgr().parseSpawnGroups(self.iSpawnGroup)
		DetailsText = u"<font=2>" + DetailsText + u"</font>"
		screen.attachMultilineText( panelName, detailsTextName, DetailsText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeStrategy(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_STRATEGY, self.Y_STRATEGY, self.W_STRATEGY, self.H_STRATEGY, PanelStyles.PANEL_STYLE_BLUE50 )

		strategyTextName = self.top.getNextWidgetName()
		StrategyText = gc.getSpawnGroupInfo(self.iSpawnGroup).getStrategy()
		StrategyText = u"<font=2>" + StrategyText + u"</font>"
		screen.attachMultilineText( panelName, strategyTextName, StrategyText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

#Start Unique Functions
	def placeHistoryUnique(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_HISTORY_UNIQUE, self.Y_HISTORY_UNIQUE, self.W_HISTORY_UNIQUE, self.H_HISTORY_UNIQUE, PanelStyles.PANEL_STYLE_BLUE50 )

		historyTextName = self.top.getNextWidgetName()
		CivilopediaText = gc.getSpawnGroupInfo(self.iSpawnGroup).getCivilopedia()
		CivilopediaText = u"<font=2>" + CivilopediaText + u"</font>"
		screen.attachMultilineText( panelName, historyTextName, CivilopediaText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeDetailsUnique(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_DETAILS_UNIQUE, self.Y_DETAILS_UNIQUE, self.W_DETAILS_UNIQUE, self.H_DETAILS_UNIQUE, PanelStyles.PANEL_STYLE_BLUE50 )

		detailsTextName = self.top.getNextWidgetName()
		DetailsText = CyGameTextMgr().parseSpawnGroups(self.iSpawnGroup)
		DetailsText = u"<font=2>" + DetailsText + u"</font>"
		screen.attachMultilineText( panelName, detailsTextName, DetailsText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeStrategyUnique(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,
			self.X_STRATEGY_UNIQUE, self.Y_STRATEGY_UNIQUE, self.W_STRATEGY_UNIQUE, self.H_STRATEGY_UNIQUE, PanelStyles.PANEL_STYLE_BLUE50 )

		strategyTextName = self.top.getNextWidgetName()
		StrategyText = gc.getSpawnGroupInfo(self.iSpawnGroup).getStrategy()
		StrategyText = u"<font=2>" + StrategyText + u"</font>"
		screen.attachMultilineText( panelName, strategyTextName, StrategyText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeBannerUnique(self):
		screen = self.top.getScreen()

		szBanner = str(gc.getSpawnGroupInfo(self.iSpawnGroup).getBanner())
		screen.addDDSGFC(self.top.getNextWidgetName(), szBanner,
			self.X_BANNER_UNIQUE, self.Y_BANNER_UNIQUE, self.W_BANNER_UNIQUE, self.H_BANNER_UNIQUE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iSpawnGroup = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPAWNGROUP, iSpawnGroup, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iSpawnGroup == self.iSpawnGroup:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listSpawnGroups = []
		iCount = 0
		for iSpawnGroup in range(gc.getNumSpawnGroupInfos()):
			eSpawnGroup = gc.getSpawnGroupInfo(iSpawnGroup)
			if not eSpawnGroup.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for spawnGroup in self.CURRENT_FILTER["HardcodeList"]:
						if iSpawnGroup == gc.getInfoTypeForString(spawnGroup):
							listSpawnGroups.append(iSpawnGroup)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listSpawnGroups.append(iSpawnGroup)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iSpawnGroup in listSpawnGroups:
			eSpawnGroup = gc.getSpawnGroupInfo(iSpawnGroup)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			listSorted[iI] = (sort1, sort2, iSpawnGroup, eSpawnGroup.getDescription(), eSpawnGroup.getButton(), 1)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP, True)

		if not self.CURRENT_FILTER == filter:
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0