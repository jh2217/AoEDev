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

class CvPediaSpell:
	"Civilopedia Screen for Spells"

	def __init__(self, main):
		self.iSpell = -1
		self.top = main

		self.BUTTON_SIZE = 46

		self.X_ICON = 98
		self.Y_ICON = 110
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 64

		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eSpell is the SpellInfo object being tested
				"Desired Result" : 'None',
				"Mana Based" : False,
			},
			{
				"name" : 'localText.getText("TXT_KEY_CONCEPT_WORLD_SPELLS", ())',
				"Purpose" : "Global Spells",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eSpell.isGlobal()',
				"Desired Result" : 'True',
				"Mana Based" : False,
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_SPELL_ABILITIES", ())',
				"Purpose" : "Spells unaffected by Arcane Lacuna",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eSpell.isAbility()',
				"Desired Result" : 'True',
				"Mana Based" : False,
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_SPELL_SUMMMON", ())',
				"Purpose" : "Spells that create units (by non-python methods",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eSpell.getCreateUnitType() != -1',
				"Desired Result" : 'True',
				"Mana Based" : False,
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_SPELL_DIVINE", ())',
				"Purpose" : "Spells granted by the Divine promotion",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eSpell.getPromotionPrereq1()',
				"Desired Result" : 'gc.getInfoTypeForString("PROMOTION_DIVINE")',
				"Mana Based" : False,
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_SPELL_MANA", ())',
				"Purpose" : "Mana related Spells",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_FAIR_WINDS',
					'SPELL_MAELSTROM',
					'SPELL_SUMMON_AIR_ELEMENTAL',
					'SPELL_HASTE',
					'SPELL_REGENERATION',
					'SPELL_GRAFT_FLESH',
					'SPELL_DANCE_OF_BLADES',
					'SPELL_MUTATION',
					'SPELL_WONDER',
					'SPELL_GROWTH',
					'SPELL_FERTILITY',
					'SPELL_BIRTH',
					'SPELL_RAISE_SKELETON',
					'SPELL_SUMMON_SPECTRE',
					'SPELL_SUMMON_WRAITH',
					'SPELL_LICHDOM',
					'SPELL_ESCAPE',
					'SPELL_GATE',
					'SPELL_WALL_OF_STONE',
					'SPELL_STONESKIN',
					'SPELL_SUMMON_EARTH_ELEMENTAL',
					'SPELL_ENCHANTED_BLADE',
					'SPELL_FLAMING_ARROWS',
					'SPELL_ENCHANT_SPELLSTAFF',
					'SPELL_RUST',
					'SPELL_SUMMON_PIT_BEAST',
					'SPELL_WITHER',
					'SPELL_BLAZE',
					'SPELL_FIREBALL',
					'SPELL_SUMMON_FIRE_ELEMENTAL',
					'SPELL_ACCELERATE',
					'SPELL_WALL_OF_FORCE',
					'SPELL_SLOW',
					'SPELL_SUMMON_ICE_ELEMENTAL',
					'SPELL_FROZEN_LANDS',
					'SPELL_LOYALTY',
					'SPELL_SUMMON_EINHERJAR',
					'SPELL_VALOR',
					'SPELL_SANCTIFY',
					'SPELL_DESTROY_UNDEAD',
					'SPELL_RESURRECTION',
					'SPELL_FLOATING_EYE',
					'SPELL_DISPEL_MAGIC',
					'SPELL_SUMMON_DJINN',
					'SPELL_INSPIRATION',
					'SPELL_CHARM_PERSON',
					'SPELL_DOMINATION',
					'SPELL_TREETOP_DEFENCE',
					'SPELL_POISONED_BLADE',
					'SPELL_VITALIZE',
					'SPELL_BLUR',
					'SPELL_SHADOWWALK',
					'SPELL_SUMMON_MISTFORM',
					'SPELL_COURAGE',
					'SPELL_HOPE',
					'SPELL_TRUST',
					'SPELL_SCORCH',
					'SPELL_BLINDING_LIGHT',
					'SPELL_SUMMON_AUREALIS',
					'SPELL_SPRING',
					'SPELL_WATER_WALKING',
					'SPELL_SUMMON_WATER_ELEMENTAL'
				],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : False,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_AIR", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_FAIR_WINDS',
					'SPELL_MAELSTROM',
					'SPELL_SUMMON_AIR_ELEMENTAL'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_BODY", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_HASTE',
					'SPELL_REGENERATION',
					'SPELL_GRAFT_FLESH'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_PROMOTION_CORPUS", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_DRAW_STRENGTH',
					'SPELL_DEATH_GEAS',
					'SPELL_GRAND_WARD'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_CHAOS", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_DANCE_OF_BLADES',
					'SPELL_MUTATION',
					'SPELL_WONDER'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_CREATION", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_GROWTH',
					'SPELL_FERTILITY',
					'SPELL_BIRTH'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_DEATH", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_RAISE_SKELETON',
					'SPELL_SUMMON_SPECTRE',
					'SPELL_SUMMON_WRAITH',
					'SPELL_LICHDOM'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_DIMENSIONAL", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_ESCAPE',
					'SPELL_GATE'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_EARTH", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_WALL_OF_STONE',
					'SPELL_STONESKIN',
					'SPELL_SUMMON_EARTH_ELEMENTAL'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_ENCHANTMENT", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_ENCHANTED_BLADE',
					'SPELL_FLAMING_ARROWS',
					'SPELL_ENCHANT_SPELLSTAFF'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_ENTROPY", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_RUST',
					'SPELL_SUMMON_PIT_BEAST',
					'SPELL_WITHER'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_FIRE", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_BLAZE',
					'SPELL_FIREBALL',
					'SPELL_SUMMON_FIRE_ELEMENTAL'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_FORCE", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_ACCELERATE',
					'SPELL_WALL_OF_FORCE'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_ICE", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_SLOW',
					'SPELL_SUMMON_ICE_ELEMENTAL',
					'SPELL_FROZEN_LANDS'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_LAW", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_LOYALTY',
					'SPELL_SUMMON_EINHERJAR',
					'SPELL_VALOR'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_LIFE", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_SANCTIFY',
					'SPELL_DESTROY_UNDEAD',
					'SPELL_RESURRECTION'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_METAMAGIC", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_FLOATING_EYE',
					'SPELL_DISPEL_MAGIC',
					'SPELL_SUMMON_DJINN'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_MIND", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_INSPIRATION',
					'SPELL_CHARM_PERSON',
					'SPELL_DOMINATION'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_NATURE", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_TREETOP_DEFENCE',
					'SPELL_POISONED_BLADE',
					'SPELL_VITALIZE'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_SHADOW", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_BLUR',
					'SPELL_SHADOWWALK',
					'SPELL_SUMMON_MISTFORM'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_SPIRIT", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_COURAGE',
					'SPELL_HOPE',
					'SPELL_TRUST'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_SUN", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_SCORCH',
					'SPELL_BLINDING_LIGHT',
					'SPELL_SUMMON_AUREALIS'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			{
				"name" : 'localText.getText("TXT_KEY_BONUS_MANA_WATER", ())',
				"Purpose" : "Ok, this is more annoying that sorting units by Civilization...",
				"Hardcoded" : True,
				"HardcodeList" : [
					'SPELL_SPRING',
					'SPELL_WATER_WALKING',
					'SPELL_SUMMON_WATER_ELEMENTAL'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
				"Mana Based" : True,
			},
			]

		# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
		self.ALLOWED_FILTERS = []
		for i, filter in enumerate(self.FILTERS):
			if not self.FILTERS[i]["Mana Based"]:
				self.ALLOWED_FILTERS.append(self.FILTERS[i])
		self.CURRENT_FILTER = self.FILTERS[0]

		self.SORTS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_ALPHABETICAL", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'eSpell.getDescription()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_XML_ORDER", ())',
				"Purpose" : "Default, unsorted method",
				"Value to Sort" : None,		# Still provides eSpell as the value being tested
			},
			]

		# List the sorts which you want to be available initially, or self.SORTS to have all of them available from the start
		self.ALLOWED_SORTS = self.SORTS
		self.CURRENT_SORT = self.SORTS[0]
		self.SUB_SORT = self.SORTS[0]

	# Screen construction function
	def interfaceScreen(self, iSpell):
		self.iSpell = iSpell

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
		szHeader = u"<font=4b>" + gc.getSpellInfo(self.iSpell).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Title (upper-right corner, above the list)
		szHeader = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_SPELL", ()).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.W_SCREEN -self.top.W_LINKS/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_SPELL or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_SPELL
		else:
			self.placeLinks(false)

		self.placeIcon()
		self.placePrereqs() # Place Required promotions
		self.placeHelp()    # Place Allowing promotions
		self.placeHistory()
		self.placeStrategy()

		#self.placeUnitGroups()

	def placeIcon(self):
		screen = self.top.getScreen()
		self.X_ICON = self.top.EXT_SPACING
		self.Y_ICON = self.top.H_TOP_BAR + self.top.INT_SPACING
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 64
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
			self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getSpellInfo(self.iSpell).getButton(),
			self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placePrereqs(self):
		screen = self.top.getScreen()
		self.X_PREREQ_PANE = self.X_ICON + self.W_ICON + self.top.INT_SPACING
		self.Y_PREREQ_PANE = self.top.H_TOP_BAR + self.top.INT_SPACING
		self.W_PREREQ_PANE = 420
		self.H_PREREQ_PANE = self.top.H_BLUE50_PANEL
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
				 self.X_PREREQ_PANE, self.Y_PREREQ_PANE, self.W_PREREQ_PANE, self.H_PREREQ_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		ePromo = gc.getSpellInfo(self.iSpell).getPromotionPrereq1()
		if (ePromo > -1):
			screen.attachImageButton( panelName, "", gc.getPromotionInfo(ePromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromo, 1, False )

			ePromo = gc.getSpellInfo(self.iSpell).getPromotionPrereq2()
			if (ePromo > -1):
				screen.attachTextGFC(panelName, "", localText.getText("TXT_KEY_AND", ()), FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.attachImageButton( panelName, "", gc.getPromotionInfo(ePromo).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, ePromo, 1, False )

	def placeHelp(self):
		screen = self.top.getScreen()
		self.X_HELP_PANE = self.X_PREREQ_PANE + self.W_PREREQ_PANE + self.top.INT_SPACING
		self.Y_HELP_PANE = self.Y_PREREQ_PANE
		self.W_HELP_PANE = self.top.X_LINKS - self.X_HELP_PANE - self.top.EXT_SPACING
		self.H_HELP_PANE = self.top.H_BLUE50_PANEL * 2
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_HELP", ()), "", false, true,
				 self.X_HELP_PANE, self.Y_HELP_PANE, self.W_HELP_PANE, self.H_HELP_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")
		listName = self.top.getNextWidgetName()

		szSpecialText = CyGameTextMgr().getSpellHelp(self.iSpell, True)[1:]

		screen.addMultilineText(listName, szSpecialText, self.X_HELP_PANE+5, self.Y_HELP_PANE+30, self.W_HELP_PANE-10, self.H_HELP_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeHistory(self):
		screen = self.top.getScreen()
		self.X_HISTORY = self.top.EXT_SPACING
		self.Y_HISTORY = self.Y_HELP_PANE + self.H_HELP_PANE
		# the remaining horizontal space is split in 2. left --> History ; right --> Strategy
		self.W_HISTORY = int(0.5*(self.top.X_LINKS - self.top.EXT_SPACING*2 - self.top.INT_SPACING))
		self.H_HISTORY = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_HISTORY
		HistoryPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryPanel, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True,
						self.X_HISTORY, self.Y_HISTORY,self.W_HISTORY, self.H_HISTORY,
						PanelStyles.PANEL_STYLE_BLUE50 )
		HistoryTextPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryTextPanel, "", "", true, true,self.X_HISTORY+self.top.HM_TEXT, self.Y_HISTORY+self.top.VM_TEXT, self.W_HISTORY - 2 * self.top.HM_TEXT, self.H_HISTORY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		HistoryText = gc.getSpellInfo(self.iSpell).getCivilopedia()
		screen.attachMultilineText( HistoryTextPanel, "", HistoryText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStrategy(self):
		screen = self.top.getScreen()
		self.X_STRATEGY = self.X_HISTORY + self.W_HISTORY + self.top.INT_SPACING
		self.Y_STRATEGY = self.Y_HISTORY
		# the remaining horizontal space is split in 2. left --> History ; right --> Strategy
		self.W_STRATEGY = self.W_HISTORY
		self.H_STRATEGY = self.H_HISTORY
		StrategyPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyPanel, localText.getText("TXT_KEY_STRATEGY", ()), "", True, True,
						self.X_STRATEGY, self.Y_STRATEGY,self.W_STRATEGY, self.H_STRATEGY,
						PanelStyles.PANEL_STYLE_BLUE50 )
		StrategyTextPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyTextPanel, "", "", true, true,self.X_STRATEGY+self.top.HM_TEXT, self.Y_STRATEGY+self.top.VM_TEXT, self.W_STRATEGY - 2 * self.top.HM_TEXT, self.H_STRATEGY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		StrategyText = gc.getSpellInfo(self.iSpell).getStrategy()
		screen.attachMultilineText( StrategyTextPanel, "", StrategyText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iSpell = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, iSpell, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iSpell == self.iSpell:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listSpells = []
		iCount = 0
		for iSpell in range(gc.getNumSpellInfos()):
			eSpell = gc.getSpellInfo(iSpell)
			if not eSpell.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for spell in self.CURRENT_FILTER["HardcodeList"]:
						if iSpell == gc.getInfoTypeForString(spell):
							listSpells.append(iSpell)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listSpells.append(iSpell)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iSpell in listSpells:
			eSpell = gc.getSpellInfo(iSpell)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if self.CURRENT_SORT["Value to Sort"] == 'eSpell.getDescription()':
					sort1 = CvUtil.removeAccent(self,sort1) # alphabetical sorting in the Pedia for languages using accents/diacritics
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			listSorted[iI] = (sort1, sort2, iSpell, eSpell.getDescription(), eSpell.getButton(), 1)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL, True)

		if not self.CURRENT_FILTER == filter:
			if eval(filter["name"]) == eval('localText.getText("TXT_KEY_PEDIA_FILTER_SPELL_MANA", ())') or filter["Mana Based"]:
				self.ALLOWED_FILTERS = []
				for i, filterlist in enumerate(self.FILTERS):
					if filterlist["Mana Based"] or eval(filterlist["name"]) == eval('localText.getText("TXT_KEY_PEDIA_FILTER_SPELL_MANA", ())') or eval(filterlist["name"]) == eval('localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())'):	#Things break if the item you use to get into a sublist is not also a part of that sublist
						self.ALLOWED_FILTERS.append(filterlist)
			elif (self.CURRENT_FILTER["Mana Based"] and (not filter["Mana Based"])) or eval(self.CURRENT_FILTER["name"]) == eval('localText.getText("TXT_KEY_PEDIA_FILTER_SPELL_MANA", ())'):
				self.ALLOWED_FILTERS = []
				for i, filterlist in enumerate(self.FILTERS):
					if not filterlist["Mana Based"]:
						self.ALLOWED_FILTERS.append(filterlist)
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0