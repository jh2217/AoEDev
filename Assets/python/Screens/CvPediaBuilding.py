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

class CvPediaBuilding:
	"Civilopedia Screen for Buildings"

	def __init__(self, main):
		self.iBuilding = -1
		self.top = main

		self.BUTTON_SIZE = 46

		self.X_BUILDING_PANE = 20
		self.Y_BUILDING_PANE = 70
		self.W_BUILDING_PANE = 433
		self.H_BUILDING_PANE = 210

		self.X_BUILDING_ANIMATION = 475
		self.Y_BUILDING_ANIMATION = 78
		self.W_BUILDING_ANIMATION = 303
		self.H_BUILDING_ANIMATION = 200
		self.X_ROTATION_BUILDING_ANIMATION = -20
		self.Z_ROTATION_BUILDING_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0

		self.X_STATS_PANE = 210
		self.Y_STATS_PANE = 90
		self.W_STATS_PANE = 250
		self.H_STATS_PANE = 200

		self.X_ICON = 48
		self.Y_ICON = 105
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 64

		self.X_PREREQ_PANE = 20
		self.Y_PREREQ_PANE = 292
		self.W_PREREQ_PANE = 433
		self.H_PREREQ_PANE = 124

		self.X_SPECIAL_PANE = 20
		self.Y_SPECIAL_PANE = 420
		self.W_SPECIAL_PANE = 433
		self.H_SPECIAL_PANE = 278

		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eBuilding is the BuildingInfo object being tested
				"Desired Result" : 'None',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_BUILDING_STANDARD", ())',
				"Purpose" : "Standard buildings",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eBuilding.getProductionCost() > 0 and isNationalWonderClass(eBuilding.getBuildingClassType()) == False and isWorldWonderClass(eBuilding.getBuildingClassType()) == False and gc.getBuildingClassInfo(eBuilding.getBuildingClassType()).getDefaultBuildingIndex() == iBuilding and not gc.getBuildingClassInfo(eBuilding.getBuildingClassType()).isUnique()',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_BUILDING_W_WONDERS", ())',
				"Purpose" : "World Wonders",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'isWorldWonderClass(eBuilding.getBuildingClassType())',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_BUILDING_N_WONDERS", ())',
				"Purpose" : "National Wonders",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'isNationalWonderClass(eBuilding.getBuildingClassType())',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_BUILDING_NON_WONDERS", ())',
				"Purpose" : "Standard Buildings",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'isNationalWonderClass(eBuilding.getBuildingClassType()) == False and isWorldWonderClass(eBuilding.getBuildingClassType()) == False',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_BUILDING_UNBUILDABLE", ())',
				"Purpose" : "Buildings",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eBuilding.getProductionCost() < 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_BUILDING_BUILDABLE", ())',
				"Purpose" : "Buildings",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eBuilding.getProductionCost() < 0',
				"Desired Result" : 'False',
			},
			#{ test Ronkhar
			#	"name" : "Default Buildings",
			#	"Purpose" : "Buildings not requiring a certain Civ to build them",
			#	"Hardcoded" : False,
			#	"HardcodeList" : [],
			#	"Value to Check" : 'gc.getBuildingClassInfo(eBuilding.getBuildingClassType()).getDefaultBuildingIndex() != iBuilding or gc.getBuildingClassInfo(eBuilding.getBuildingClassType()).isUnique()',
			#	"Desired Result" : 'False',
			#},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_BUILDING_CIV_SPECIFIC", ())',
				"Purpose" : "Buildings requiring a certain Civ to build them",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'gc.getBuildingClassInfo(eBuilding.getBuildingClassType()).getDefaultBuildingIndex() != iBuilding or gc.getBuildingClassInfo(eBuilding.getBuildingClassType()).isUnique()',
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
				"Value to Sort" : 'eBuilding.getDescription()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_COST_PRODUCTION", ())',
				"Purpose" : "Production Sort, the easiest choice",
				"Value to Sort" : 'eBuilding.getProductionCost()',
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
	def interfaceScreen(self, iBuilding):
		self.iBuilding = iBuilding

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
		szHeader = u"<font=4b>" + gc.getBuildingInfo(self.iBuilding).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, iBuilding)

		# Title (upper-right corner, above the list)
		szHeader = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.W_SCREEN -self.top.W_LINKS/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_BUILDING or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_BUILDING
		else:
			self.placeLinks(false)

		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50)

		# Icon
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBuildingInfo(self.iBuilding).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Unit animation
		screen.addBuildingGraphicGFC(self.top.getNextWidgetName(), self.iBuilding, self.X_BUILDING_ANIMATION, self.Y_BUILDING_ANIMATION, self.W_BUILDING_ANIMATION, self.H_BUILDING_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BUILDING_ANIMATION, self.Z_ROTATION_BUILDING_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStats()
		self.placeRequires()
		self.placeSpecial()
		self.placeHistory()
		self.placeStrategy()

	# Place happiness/health/commerce/great people modifiers
	def placeStats(self):
		screen = self.top.getScreen()

		buildingInfo = gc.getBuildingInfo(self.iBuilding)

		panelName = self.top.getNextWidgetName()

		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)

		if (isWorldWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxGlobalInstances()
			szBuildingType = localText.getText("TXT_KEY_PEDIA_WORLD_WONDER", ())
			if (iMaxInstances > 1):
				szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (isTeamWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxTeamInstances()
			szBuildingType = localText.getText("TXT_KEY_PEDIA_TEAM_WONDER", ())
			if (iMaxInstances > 1):
				szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (isNationalWonderClass(gc.getBuildingInfo(self.iBuilding).getBuildingClassType())):
			iMaxInstances = gc.getBuildingClassInfo(gc.getBuildingInfo(self.iBuilding).getBuildingClassType()).getMaxPlayerInstances()
			szBuildingType = localText.getText("TXT_KEY_PEDIA_NATIONAL_WONDER", ())
			if (iMaxInstances > 1):
				szBuildingType += " " + localText.getText("TXT_KEY_PEDIA_WONDER_INSTANCES", (iMaxInstances,))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szBuildingType.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (buildingInfo.getProductionCost() > 0):
			if self.top.iActivePlayer == -1:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", ((buildingInfo.getProductionCost() * gc.getDefineINT("BUILDING_PRODUCTION_PERCENT"))/100,))
			else:
				szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getPlayer(self.top.iActivePlayer).getBuildingProductionNeeded(self.iBuilding),))
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		for k in range(YieldTypes.NUM_YIELD_TYPES):
			if (buildingInfo.getYieldChange(k) != 0):
				if (buildingInfo.getYieldChange(k) > 0):
					szSign = "+"
				else:
					szSign = ""

				szYield = gc.getYieldInfo(k).getDescription() + ": "

				szText1 = szYield.upper() + szSign + str(buildingInfo.getYieldChange(k))
				szText2 = szText1 + (u"%c" % (gc.getYieldInfo(k).getChar()))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText2 + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		for k in range(CommerceTypes.NUM_COMMERCE_TYPES):
			iTotalCommerce = buildingInfo.getObsoleteSafeCommerceChange(k) + buildingInfo.getCommerceChange(k)
			if (iTotalCommerce != 0):
				if (iTotalCommerce > 0):
					szSign = "+"
				else:
					szSign = ""

				szCommerce = gc.getCommerceInfo(k).getDescription() + ": "

				szText1 = szCommerce.upper() + szSign + str(iTotalCommerce)
				szText2 = szText1 + (u"%c" % (gc.getCommerceInfo(k).getChar()))
				screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText2 + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iHappiness = buildingInfo.getHappiness()
		if self.top.iActivePlayer != -1:
			if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
				iHappiness += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHappiness(self.iBuilding)

		if (iHappiness > 0):
			szText = localText.getText("TXT_KEY_PEDIA_HAPPY", (iHappiness,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		elif (iHappiness < 0):
			szText = localText.getText("TXT_KEY_PEDIA_UNHAPPY", (-iHappiness,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iHealth = buildingInfo.getHealth()
		if self.top.iActivePlayer != -1:
			if (self.iBuilding == gc.getCivilizationInfo(gc.getPlayer(self.top.iActivePlayer).getCivilizationType()).getCivilizationBuildings(buildingInfo.getBuildingClassType())):
				iHealth += gc.getPlayer(self.top.iActivePlayer).getExtraBuildingHealth(self.iBuilding)

		if (iHealth > 0):
			szText = localText.getText("TXT_KEY_PEDIA_HEALTHY", (iHealth,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		elif (iHealth < 0):
			szText = localText.getText("TXT_KEY_PEDIA_UNHEALTHY", (-iHealth,)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if (buildingInfo.getGreatPeopleRateChange() != 0):
			szText = localText.getText("TXT_KEY_PEDIA_GREAT_PEOPLE", (buildingInfo.getGreatPeopleRateChange(),)).upper()
			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szText + u"%c" % CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		screen.updateListBox(panelName)

	# Place prereqs (techs, resources)
	def placeRequires(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
								 self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		# add tech buttons
		for iPrereq in range(gc.getNumTechInfos()):
			if isTechRequiredForBuilding(iPrereq, self.iBuilding):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iPrereq, 1, False )

		# add resource buttons
		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqAndBonus()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		for k in range(gc.getNUM_BUILDING_PREREQ_OR_BONUSES()):
			iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqOrBonuses(k)
			if (iPrereq >= 0):
				screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		iCorporation = gc.getBuildingInfo(self.iBuilding).getFoundsCorporation()
		bFirst = true
		if (iCorporation >= 0):
			for k in range(gc.getNUM_CORPORATION_PREREQ_BONUSES()):
				iPrereq = gc.getCorporationInfo(iCorporation).getPrereqBonus(k)
				if (iPrereq >= 0):
					if not bFirst:
						screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
					else:
						bFirst = false
					screen.attachImageButton( panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False )

		# add religion button
		iPrereq = gc.getBuildingInfo(self.iBuilding).getPrereqReligion()
		if (iPrereq >= 0):
			screen.attachImageButton( panelName, "", gc.getReligionInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iPrereq, -1, False )

	# Place Special abilities
	def placeSpecial(self):
		screen = self.top.getScreen()
		self.H_SPECIAL_PANE = self.top.H_SCREEN-self.top.H_BOT_BAR-self.top.EXT_SPACING-self.Y_SPECIAL_PANE
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		listName = self.top.getNextWidgetName()

		szSpecialText = CyGameTextMgr().getBuildingHelp(self.iBuilding, True, False, False, None,False)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeHistory(self):
		screen = self.top.getScreen()
		self.X_HISTORY = self.X_BUILDING_ANIMATION
		self.Y_HISTORY = self.Y_BUILDING_ANIMATION + self.H_BUILDING_ANIMATION
		self.W_HISTORY = self.top.X_LINKS - self.X_HISTORY - self.top.EXT_SPACING
		# the remaining vertical space under the logo is split in 2. upper-half --> History ; bottom-half --> Strategy
		self.H_HISTORY = int(0.5 * (self.top.H_SCREEN-self.top.H_BOT_BAR-self.top.EXT_SPACING-self.Y_HISTORY))
		HistoryPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryPanel, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True,self.X_HISTORY, self.Y_HISTORY,self.W_HISTORY, self.H_HISTORY,PanelStyles.PANEL_STYLE_BLUE50 )
		HistoryTextPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryTextPanel, "", "", true, true,self.X_HISTORY+self.top.HM_TEXT, self.Y_HISTORY+self.top.VM_TEXT, self.W_HISTORY - 2 * self.top.HM_TEXT, self.H_HISTORY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		HistoryText = gc.getBuildingInfo(self.iBuilding).getCivilopedia()
		screen.attachMultilineText( HistoryTextPanel, "", HistoryText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStrategy(self):
		screen = self.top.getScreen()
		self.X_STRATEGY = self.X_HISTORY
		self.Y_STRATEGY = self.Y_HISTORY + self.H_HISTORY
		self.W_STRATEGY = self.W_HISTORY
		self.H_STRATEGY = self.H_HISTORY
		StrategyPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyPanel, localText.getText("TXT_KEY_STRATEGY", ()), "", true, true,self.X_STRATEGY, self.Y_STRATEGY, self.W_STRATEGY, self.H_STRATEGY, PanelStyles.PANEL_STYLE_BLUE50 )
		StrategyTextPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyTextPanel, "", "", true, true,self.X_STRATEGY+self.top.HM_TEXT, self.Y_STRATEGY+self.top.VM_TEXT, self.W_STRATEGY - 2 * self.top.HM_TEXT, self.H_STRATEGY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		StrategyText = gc.getBuildingInfo(self.iBuilding).getStrategy()
		screen.attachMultilineText( StrategyTextPanel, "", StrategyText,WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )


	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iBuilding = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iBuilding == self.iBuilding:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listBuildings = []
		iCount = 0
		for iBuilding in range(gc.getNumBuildingInfos()):
			eBuilding = gc.getBuildingInfo(iBuilding)
			if not eBuilding.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for building in self.CURRENT_FILTER["HardcodeList"]:
						if iBuilding == gc.getInfoTypeForString(building):
							listBuildings.append(iBuilding)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listBuildings.append(iBuilding)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iBuilding in listBuildings:
			eBuilding = gc.getBuildingInfo(iBuilding)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if self.CURRENT_SORT["Value to Sort"] == 'eBuilding.getDescription()':
					sort1 = CvUtil.removeAccent(self,sort1) # alphabetical sorting in the Pedia for languages using accents/diacritics
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			listSorted[iI] = (sort1, sort2, iBuilding, eBuilding.getDescription(), eBuilding.getButton(), 1)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, True)

		if not self.CURRENT_FILTER == filter:
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0