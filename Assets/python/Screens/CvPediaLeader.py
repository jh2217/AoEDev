## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Alex Mantzaris / Jesse Smith 09-2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import random

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaLeader:
	"Civilopedia Screen for Leaders"

	def __init__(self, main):
		self.iLeader = -1
		self.top = main

		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eLeader is the LeaderHeadInfo object being tested
				"Desired Result" : 'None',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_GOOD", ())',
				"Purpose" : "Filter by basic Alignment",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eLeader.getAlignment()',
				"Desired Result" : 'gc.getInfoTypeForString("ALIGNMENT_GOOD")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_NEUTRAL", ())',
				"Purpose" : "Filter by basic Alignment",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eLeader.getAlignment()',
				"Desired Result" : 'gc.getInfoTypeForString("ALIGNMENT_NEUTRAL")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_EVIL", ())',
				"Purpose" : "Filter by basic Alignment",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eLeader.getAlignment()',
				"Desired Result" : 'gc.getInfoTypeForString("ALIGNMENT_EVIL")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_MALE", ())',
				"Purpose" : "Filter by Gender",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eLeader.isFemale()',
				"Desired Result" : 'False',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_FEMALE", ())',
				"Purpose" : "Filter by Gender",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eLeader.isFemale()',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_HISTORICAL", ())',
				"Purpose" : "Filter by Historical status",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'gc.getLeaderClassInfo(eLeader.getLeaderClass()).getLeaderStatus()',
				"Desired Result" : 'gc.getInfoTypeForString("HISTORICAL_STATUS")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_IMPORTANT", ())',
				"Purpose" : "Filter by Important status",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'gc.getLeaderClassInfo(eLeader.getLeaderClass()).getLeaderStatus()',
				"Desired Result" : 'gc.getInfoTypeForString("IMPORTANT_STATUS")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_EMERGENT", ())',
				"Purpose" : "Filter by Emergent status",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'gc.getLeaderClassInfo(eLeader.getLeaderClass()).getLeaderStatus()',
				"Desired Result" : 'gc.getInfoTypeForString("EMERGENT_STATUS")',
			},
			]

		# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
		self.ALLOWED_FILTERS = self.FILTERS
		self.CURRENT_FILTER = self.FILTERS[0]

		self.SORTS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_ALPHABETICAL", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'eLeader.getDescription()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_ALIGNMENT", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : '-eLeader.getAlignmentModifier()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_LEADER_STATUS", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'gc.getLeaderClassInfo(eLeader.getLeaderClass()).getLeaderStatus()',
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
	def interfaceScreen(self, iLeader):
		self.iLeader = iLeader

		self.top.deleteAllWidgets()

		screen = self.top.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		#Filter/Sort dropdowns
		self.top.FILTER_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.FILTER_DROPDOWN_ID, self.top.X_FILTER_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, filter in enumerate(self.ALLOWED_FILTERS):
			screen.addPullDownString(self.top.FILTER_DROPDOWN_ID, eval(filter["name"]), i, i, filter == self.CURRENT_FILTER )

		self.top.SORT_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.SORT_DROPDOWN_ID, self.top.X_SORT_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, sort in enumerate(self.ALLOWED_SORTS):
			screen.addPullDownString(self.top.SORT_DROPDOWN_ID, eval(sort["name"]), 1, 1, sort == self.CURRENT_SORT )

		# Header...
		szHeader = u"<font=4b>" + gc.getLeaderHeadInfo(self.iLeader).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Title (upper-right corner, above the list)
		szHeader = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.W_SCREEN -self.top.W_LINKS/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_LEADER or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_LEADER
		else:
			self.placeLinks(false)

		self.placePortrait()
		self.placeCivIcon()
		self.placeHistory()
		self.placeFavorites()
		self.placeTraits()

	def placePortrait(self):
		screen = self.top.getScreen()
		self.leaderWidget = self.top.getNextWidgetName()
		self.W_LEADERHEAD = 320
		self.H_LEADERHEAD = 384
		self.X_LEADERHEAD = self.top.EXT_SPACING
		self.Y_LEADERHEAD = 55 # same as civilization banner. use self.top variable?
		screen.addLeaderheadGFC(self.leaderWidget, self.iLeader, AttitudeTypes.ATTITUDE_PLEASED,
			self.X_LEADERHEAD, self.Y_LEADERHEAD, self.W_LEADERHEAD, self.H_LEADERHEAD, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def placeCivIcon(self):
		civ_number = 0
		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isPediaLeaders(self.iLeader):
				civ_number += 1
		if civ_number ==0: # favorites can be placed directly under the portrait
			self.X_ICON_FRAME = self.X_LEADERHEAD + self.W_LEADERHEAD
			self.W_ICON_FRAME = 0
		else:
			screen = self.top.getScreen()
			self.S_CIV = 64 # icon size
			self.H_ICON_FRAME = 77 + 6 # (77 pixels visually + 6 pixels offset)
			self.W_ICON_FRAME = 82 # I guess
			self.X_ICON_FRAME = self.X_LEADERHEAD + self.W_LEADERHEAD + self.top.INT_SPACING
			self.X_CIV = self.X_ICON_FRAME + 10
			#self.Y_ICON_FRAME = self.top.EXT_SPACING + (self.H_LEADERHEAD - civ_number * self.H_ICON_FRAME - (civ_number -1)*self.top.INT_SPACING)/2 # perhaps y_leaderhead instead of ext_spacing
			self.Y_ICON_FRAME = self.Y_LEADERHEAD # perhaps y_leaderhead instead of ext_spacing
			self.Y_CIV = self.Y_ICON_FRAME + 12
			civ_ii = 0
			for iCiv in range(gc.getNumCivilizationInfos()):
				civ = gc.getCivilizationInfo(iCiv)
				if civ.isPediaLeaders(self.iLeader):
					screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
					self.X_ICON_FRAME, self.Y_ICON_FRAME + civ_ii * (self.H_ICON_FRAME+self.top.INT_SPACING),self.W_ICON_FRAME, self.H_ICON_FRAME, PanelStyles.PANEL_STYLE_BLUE50)
					screen.setImageButton(self.top.getNextWidgetName(), civ.getButton(), self.X_CIV, self.Y_CIV + civ_ii * (self.H_ICON_FRAME+self.top.INT_SPACING), self.S_CIV, self.S_CIV, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1)
					civ_ii +=1

	def placeHistory(self):
		screen = self.top.getScreen()
		self.X_HISTORY = self.X_ICON_FRAME + self.W_ICON_FRAME + self.top.INT_SPACING
		self.W_HISTORY = self.top.X_LINKS - self.X_HISTORY - self.top.EXT_SPACING
		self.Y_HISTORY = self.Y_LEADERHEAD
		self.H_HISTORY = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_HISTORY
		HistoryPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryPanel, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, true,
			self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )
		HistoryTextPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryTextPanel, "", "", true, true,self.X_HISTORY+self.top.HM_TEXT, self.Y_HISTORY+self.top.VM_TEXT, self.W_HISTORY - 2 * self.top.HM_TEXT, self.H_HISTORY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		historyTextName = self.top.getNextWidgetName()
		HistoryText = gc.getLeaderHeadInfo(self.iLeader).getCivilopedia()
		screen.attachMultilineText( HistoryTextPanel, historyTextName, HistoryText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeFavorites(self):
		screen = self.top.getScreen()
		self.X_FAVORITE = self.top.EXT_SPACING
		self.Y_FAVORITE = self.Y_LEADERHEAD + self.H_LEADERHEAD
		self.W_FAVORITE = self.X_HISTORY - self.top.INT_SPACING - self.X_FAVORITE
		self.H_FAVORITE = 95

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_FAV_CIVIC", ()), "", true, true,
								 self.X_FAVORITE, self.Y_FAVORITE, self.W_FAVORITE, self.H_FAVORITE, PanelStyles.PANEL_STYLE_BLUE50 )

		iCivic = gc.getLeaderHeadInfo(self.iLeader).getFavoriteCivic()
		if (-1 != iCivic):

			szCivicText = u"" + localText.getText("TXT_KEY_MISC_FAVORITE_CIVIC", ())  + " <link=literal>" + gc.getCivicInfo(iCivic).getDescription() + u"</link>"

			listName = self.top.getNextWidgetName()
			screen.addMultilineText(listName, szCivicText, self.X_FAVORITE+5, self.Y_FAVORITE+30, self.W_FAVORITE-10, self.H_FAVORITE-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

#Opera: Hated Civic
		iHatedCivic = gc.getLeaderHeadInfo(self.iLeader).getHatedCivic()
		if (-1 != iHatedCivic):
			szHatedCivicText = u"" + localText.getText("TXT_KEY_MISC_HATED_CIVIC", ()) + " <link=literal>" + gc.getCivicInfo(iHatedCivic).getDescription() + u"</link>"
			listName = self.top.getNextWidgetName()
			screen.addMultilineText(listName, szHatedCivicText, self.X_FAVORITE+5, self.Y_FAVORITE+50, self.W_FAVORITE-10, self.H_FAVORITE-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
#End: Hated Civic

		iWonder = gc.getLeaderHeadInfo(self.iLeader).getFavoriteWonder()
		if (-1 != iWonder):
			szWonderText = u"" + localText.getText("TXT_KEY_MISC_FAVORITE_WONDER", ())  + " <link=literal>" + gc.getBuildingInfo(iWonder).getDescription() + u"</link>"
			listName = self.top.getNextWidgetName()
			screen.addMultilineText(listName, szWonderText, self.X_FAVORITE+5, self.Y_FAVORITE+70, self.W_FAVORITE-10, self.H_FAVORITE-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeTraits(self):
		screen = self.top.getScreen()
		self.X_TRAITS = self.top.EXT_SPACING
		self.Y_TRAITS = self.Y_FAVORITE + self.H_FAVORITE
		self.H_TRAITS = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_TRAITS
		self.W_TRAITS = self.W_FAVORITE
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_TRAITS", ()), "", true, false,
								 self.X_TRAITS, self.Y_TRAITS, self.W_TRAITS, self.H_TRAITS, PanelStyles.PANEL_STYLE_BLUE50 )
		listName = self.top.getNextWidgetName()
		iNumCivs = 0
		iLeaderCiv = -1
		for iCiv in range(gc.getNumCivilizationInfos()):
			civ = gc.getCivilizationInfo(iCiv)
			if civ.isPediaLeaders(self.iLeader):
				iNumCivs += 1
				iLeaderCiv = iCiv

		if iNumCivs == 1:
			szSpecialText = CyGameTextMgr().parseLeaderTraits(self.iLeader, iLeaderCiv, False, True)
		else:
			szSpecialText = CyGameTextMgr().parseLeaderTraits(self.iLeader, -1, False, True)
		szSpecialText = szSpecialText[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_TRAITS+5, self.Y_TRAITS+30, self.W_TRAITS-10, self.H_TRAITS-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)
		listSorted = self.getSortedList()
		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iLeader = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iLeader == self.iLeader:
				iSelected = i
			i += 1
		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listLeaders = []
		iCount = 0
		for iLeader in range(gc.getNumLeaderHeadInfos()):
			eLeader = gc.getLeaderHeadInfo(iLeader)
			if not eLeader.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for leader in self.CURRENT_FILTER["HardcodeList"]:
						if iLeader == gc.getInfoTypeForString(leader):
							listLeaders.append(iLeader)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listLeaders.append(iLeader)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iLeader in listLeaders:
			eLeader = gc.getLeaderHeadInfo(iLeader)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			for iCiv in range(gc.getNumCivilizationInfos()):
					eCiv = gc.getCivilizationInfo(iCiv)
					if eCiv.isPediaLeaders(iLeader):
						iBestCiv = iCiv
						break
			listSorted[iI] = (sort1, sort2, iLeader, eLeader.getDescription(), eLeader.getButton(), iBestCiv)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER, True)

		if not self.CURRENT_FILTER == filter:
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0