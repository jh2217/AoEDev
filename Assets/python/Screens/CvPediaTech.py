## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import CvPediaScreen
import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaTech(CvPediaScreen.CvPediaScreen):
	"Civilopedia Screen for Techs"

	def __init__(self, main):
		self.iTech = -1
		self.top = main

		self.X_ICON = 48
		self.Y_ICON = 105
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 64

		self.X_COST = 200
		self.Y_COST = 165

		self.BUTTON_SIZE = 64



		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eTech is the TechInfo object being tested
				"Desired Result" : 'None',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_GREAT_BARD", ())',
				"Purpose" : "Lightbulbing Sorts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : '(3*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_CULTURE")) + 2*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_GROWTH")) + 1*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_SCIENCE"))) > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_GREAT_ENGINEER", ())',
				"Purpose" : "Lightbulbing Sorts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : '(3*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_PRODUCTION")) + 2*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_MILITARY")) + 1*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_GROWTH"))) > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_GREAT_HEALER", ())',
				"Purpose" : "Lightbulbing Sorts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : '(3*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_HEALTH")) + 2*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_GROWTH")) + 1*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_CULTURE"))) > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_GREAT_MERCHANT", ())',
				"Purpose" : "Lightbulbing Sorts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : '(3*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_GOLD")) + 2*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_GROWTH")) + 1*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_PRODUCTION"))) > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_GREAT_PROPHET", ())',
				"Purpose" : "Lightbulbing Sorts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : '(3*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_RELIGION")) + 2*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_CULTURE")) + 1*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_SCIENCE"))) > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_GREAT_SAGE", ())',
				"Purpose" : "Lightbulbing Sorts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : '(3*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_SCIENCE")) + 2*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_GROWTH")) + 1*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_GOLD"))) > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_SAVANT", ())',
				"Purpose" : "Lightbulbing Sorts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : '(4*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_SCIENCE")) + 4*eTech.getFlavorValue(gc.getInfoTypeForString("FLAVOR_RELIGION"))) > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_GOODY_HUTS", ())',
				"Purpose" : "Clears all currently active filters",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTech.isGoodyTech()',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_TECH_CIV_SPECIFIC", ())',
				"Purpose" : "Unique Technologies",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTech.getResearchCost() == -1',
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
				"Value to Sort" : 'eTech.getDescription()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_COST_RESEARCH", ())',
				"Purpose" : "Sort by Beaker Cost",
				"Value to Sort" : '-eTech.getResearchCost()',
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

	def interfaceScreen(self, iTech):
		self.iTech = iTech

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
		szHeader = u"<font=4b>" + gc.getTechInfo(self.iTech).getDescription().upper() + u"</font>"
		screen.setLabel(self.top.getNextWidgetName(), "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, iTech)

		# Title (upper-right corner, above the list)
		szHeader = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.W_SCREEN -self.top.W_LINKS/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_TECH or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_TECH
		else:
			self.placeLinks(false)

		self.X_TECH_PANE = self.top.EXT_SPACING
		self.Y_TECH_PANE = self.top.H_TOP_BAR + self.top.INT_SPACING
		self.W_TECH_PANE = 368
		self.H_TECH_PANE = 210
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_TECH_PANE, self.Y_TECH_PANE, self.W_TECH_PANE, self.H_TECH_PANE, PanelStyles.PANEL_STYLE_BLUE50)

		# Icon
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getTechInfo(self.iTech).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		szCostId = self.top.getNextWidgetName()
		if self.top.iActivePlayer == -1:
			szCostText = localText.getText("TXT_KEY_PEDIA_COST", ( gc.getTechInfo(iTech).getResearchCost(), ) ) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		else:
			szCostText = localText.getText("TXT_KEY_PEDIA_COST", ( gc.getTeam(gc.getGame().getActiveTeam()).getResearchCost(iTech), ) ) + u"%c" % (gc.getCommerceInfo(CommerceTypes.COMMERCE_RESEARCH).getChar())
		screen.setLabel(szCostId, "Background", u"<font=4>" + szCostText.upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_COST + 25, self.Y_COST, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.placePrereqs()# Place Required techs
		self.placeLeadsTo()# Place Allowing techs
		self.placeSpecial()# Place the Special abilities block
		self.placeQuote()# Place the quote for this technology
		self.placeUnits()# Place Units
		self.placeBuildings()# Place buildings
		self.placeStrategy()# Place the strategy for this technology

	# Place prereqs...
	def placeLeadsTo(self):
		screen = self.top.getScreen()
		self.X_LEADS_TO_PANE = self.top.EXT_SPACING
		self.Y_LEADS_TO_PANE = self.Y_PREREQ_PANE + self.H_PREREQ_PANE
		self.W_LEADS_TO_PANE = self.W_TECH_PANE
		self.H_LEADS_TO_PANE = self.top.H_BLUE50_PANEL
		# add pane and text
		szLeadsTo = localText.getText("TXT_KEY_PEDIA_LEADS_TO", ())

		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, szLeadsTo, "", false, true, self.X_LEADS_TO_PANE, self.Y_LEADS_TO_PANE, self.W_LEADS_TO_PANE, self.H_LEADS_TO_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		for j in range(gc.getNumTechInfos()):
			for k in range(gc.getNUM_OR_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqOrTechs(k)
				if (iPrereq == self.iTech):
						screen.attachImageButton( panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )
			for k in range(gc.getNUM_AND_TECH_PREREQS()):
				iPrereq = gc.getTechInfo(j).getPrereqAndTechs(k)
				if (iPrereq == self.iTech):
						screen.attachImageButton( panelName, "", gc.getTechInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_DERIVED_TECH, j, self.iTech, False )

	# Place prereqs...
	def placePrereqs(self):
		screen = self.top.getScreen()
		self.X_PREREQ_PANE = self.top.EXT_SPACING
		self.Y_PREREQ_PANE = self.Y_TECH_PANE + self.H_TECH_PANE
		self.W_PREREQ_PANE = self.W_TECH_PANE
		self.H_PREREQ_PANE = self.top.H_BLUE50_PANEL
		
		szRequires = localText.getText("TXT_KEY_PEDIA_REQUIRES", ())

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, szRequires, "", false, true, self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		bFirst = True
		for j in range(gc.getNUM_AND_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqAndTechs(j)
			if (eTech > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_AND", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False )

		# count the number of OR techs
		nOrTechs = 0
		for j in range(gc.getNUM_OR_TECH_PREREQS()):
			if (gc.getTechInfo(self.iTech).getPrereqOrTechs(j) > -1):
				nOrTechs += 1

		szLeftDelimeter = ""
		szRightDelimeter = ""
		#  Display a bracket if we have more than one OR tech and at least one AND tech
		if (not bFirst):
			if (nOrTechs > 1):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ()) + "( "
				szRightDelimeter = " ) "
			elif (nOrTechs > 0):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ())
			else:
				return

		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panelName, "", szLeftDelimeter)

		bFirst = True
		for j in range(gc.getNUM_OR_TECH_PREREQS()):
			eTech = gc.getTechInfo(self.iTech).getPrereqOrTechs(j)
			if (eTech > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton( panelName, "", gc.getTechInfo(eTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH, eTech, j, False )

		if len(szRightDelimeter) > 0:
			screen.attachLabel(panelName, "", szRightDelimeter)

	def placeQuote(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		self.X_QUOTE_PANE = self.X_TECH_PANE + self.W_TECH_PANE + self.top.INT_SPACING
		self.Y_QUOTE_PANE = self.Y_TECH_PANE
		self.W_QUOTE_PANE = self.top.X_LINKS - self.X_QUOTE_PANE - self.top.EXT_SPACING
		self.H_QUOTE_PANE = self.H_TECH_PANE
		screen.addPanel(panelName, "", "", true, true,
			self.X_QUOTE_PANE, self.Y_QUOTE_PANE, self.W_QUOTE_PANE, self.H_QUOTE_PANE, PanelStyles.PANEL_STYLE_BLUE50)

		szQuote = gc.getTechInfo(self.iTech).getQuote()

		szQuoteTextWidget = self.top.getNextWidgetName()
		screen.addMultilineText( szQuoteTextWidget, szQuote, self.X_QUOTE_PANE + 15, self.Y_QUOTE_PANE + 15,
			self.W_QUOTE_PANE - (15 * 2), self.H_QUOTE_PANE - (15 * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	# Place units...
	def placeUnits(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		self.X_UNIT_PANE = self.X_QUOTE_PANE
		self.Y_UNIT_PANE = self.Y_QUOTE_PANE + self.H_QUOTE_PANE
		self.W_UNIT_PANE = self.W_QUOTE_PANE
		self.H_UNIT_PANE = self.top.H_BLUE50_PANEL
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_UNITS_ENABLED", ()), "", false, true, self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		for eLoopUnit in range(gc.getNumUnitInfos()):
			if (eLoopUnit != -1):
				if (isTechRequiredForUnit(self.iTech, eLoopUnit)):
					szButton = gc.getUnitInfo(eLoopUnit).getButton()
					if self.top.iActivePlayer != -1:
						szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(eLoopUnit)
					screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

	# Place buildings...
	def placeBuildings(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		
		self.X_BUILDING_PANE = self.X_QUOTE_PANE
		self.Y_BUILDING_PANE = self.Y_UNIT_PANE + self.H_UNIT_PANE
		self.W_BUILDING_PANE = self.W_QUOTE_PANE
		self.H_BUILDING_PANE = self.top.H_BLUE50_PANEL
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_BUILDINGS_ENABLED", ()), "", false, true, self.X_BUILDING_PANE, self.Y_BUILDING_PANE, self.W_BUILDING_PANE, self.H_BUILDING_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		for eLoopBuilding in range(gc.getNumBuildingInfos()):
			if (eLoopBuilding != -1):
				if (isTechRequiredForBuilding(self.iTech, eLoopBuilding)):
						screen.attachImageButton( panelName, "", gc.getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )

		for eLoopProject in range(gc.getNumProjectInfos()):
			if (isTechRequiredForProject(self.iTech, eLoopProject)):
					screen.attachImageButton( panelName, "", gc.getProjectInfo(eLoopProject).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, eLoopProject, 1, False )

	def placeSpecial(self):
		screen = self.top.getScreen()
		self.X_SPECIAL_PANE = self.top.EXT_SPACING
		self.Y_SPECIAL_PANE = self.Y_LEADS_TO_PANE + self.H_LEADS_TO_PANE
		self.W_SPECIAL_PANE = self.W_TECH_PANE
		self.H_SPECIAL_PANE = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_SPECIAL_PANE
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", true, false, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		listName = self.top.getNextWidgetName()

		szSpecialText = CyGameTextMgr().getTechHelp(self.iTech, True, False, False, False, -1)[0:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-35, self.H_SPECIAL_PANE-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStrategy(self):
		screen = self.top.getScreen()
		self.X_STRATEGY = self.X_BUILDING_PANE
		self.Y_STRATEGY = self.Y_BUILDING_PANE + self.H_BUILDING_PANE
		self.W_STRATEGY = self.top.X_LINKS - self.X_STRATEGY - self.top.EXT_SPACING
		self.H_STRATEGY = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_STRATEGY
		StrategyPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyPanel, localText.getText("TXT_KEY_STRATEGY", ()), "", True, True,
						self.X_STRATEGY, self.Y_STRATEGY,self.W_STRATEGY, self.H_STRATEGY,
						PanelStyles.PANEL_STYLE_BLUE50 )
		StrategyTextPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyTextPanel, "", "", true, true,self.X_STRATEGY+self.top.HM_TEXT, self.Y_STRATEGY+self.top.VM_TEXT, self.W_STRATEGY - 2 * self.top.HM_TEXT, self.H_STRATEGY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		StrategyText = gc.getTechInfo(self.iTech).getStrategy()
		screen.attachMultilineText( StrategyTextPanel, "", StrategyText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iTech = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iTech == self.iTech:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listTechs = []
		iCount = 0
		for iTech in range(gc.getNumTechInfos()):
			eTech = gc.getTechInfo(iTech)
			if not eTech.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for tech in self.CURRENT_FILTER["HardcodeList"]:
						if iTech == gc.getInfoTypeForString(tech):
							listTechs.append(iTech)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listTechs.append(iTech)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iTech in listTechs:
			eTech = gc.getTechInfo(iTech)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if self.CURRENT_SORT["Value to Sort"] == 'eTech.getDescription()':  
					sort1 = CvUtil.removeAccent(self,sort1) # alphabetical sorting in the Pedia for languages using accents/diacritics
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			listSorted[iI] = (sort1, sort2, iTech, eTech.getDescription(), eTech.getButton(), 1)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			bForceFilter = False
			if sort["name"] == "Great Bard Bulb List" or sort["name"] == "Great Engineer Bulb List" or sort["name"] == "Great Merchant Bulb List" or sort["name"] == "Great Prophet Bulb List" or sort["name"] == "Great Sage Bulb List" or sort["name"] == "Savant Bulb List":
				bForceFilter = True

			if bForceFilter:
				for i, filterlist in enumerate(self.FILTERS):
					if filterlist["name"] == sort["name"]:
						self.CURRENT_FILTER = filterlist
				for i, sortlist in enumerate(self.SORTS):
					if sortlist["name"] == "Sort by XML Order":
						self.SUB_SORT = sortlist
				screen = self.top.getScreen()
				screen.deleteWidget(self.top.FILTER_DROPDOWN_ID)
				self.top.FILTER_DROPDOWN_ID = self.top.getNextWidgetName()
				screen.addDropDownBoxGFC(self.top.FILTER_DROPDOWN_ID, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i, newfilter in enumerate(self.ALLOWED_FILTERS):
					screen.addPullDownString(self.top.FILTER_DROPDOWN_ID, newfilter["name"], i, i, newfilter == self.CURRENT_FILTER )
			else:
				self.SUB_SORT = self.CURRENT_SORT

			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, True)

		elif not self.CURRENT_FILTER == filter:
			bForceSort = False
			if filter["name"] == "Great Bard Bulb List" or filter["name"] == "Great Engineer Bulb List" or filter["name"] == "Great Merchant Bulb List" or filter["name"] == "Great Prophet Bulb List" or filter["name"] == "Great Sage Bulb List" or filter["name"] == "Savant Bulb List":
				bForceSort = True

			if bForceSort:
				for i, sortlist in enumerate(self.SORTS):
					if sortlist["name"] == filter["name"]:
						self.CURRENT_SORT = sortlist
					elif sortlist["name"] == "Sort by XML Order":
						self.SUB_SORT = sortlist
				screen = self.top.getScreen()
				screen.deleteWidget(self.top.SORT_DROPDOWN_ID)
				self.top.SORT_DROPDOWN_ID = self.top.getNextWidgetName()
				screen.addDropDownBoxGFC(self.top.SORT_DROPDOWN_ID, 700, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i, newsort in enumerate(self.ALLOWED_SORTS):
					screen.addPullDownString(self.top.SORT_DROPDOWN_ID, newsort["name"], 1, 1, newsort == self.CURRENT_SORT )

			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0