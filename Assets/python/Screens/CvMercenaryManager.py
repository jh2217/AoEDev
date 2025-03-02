#
# Mercenaries Mod
# By: The Lopez
# CvMercenaryManager
# 

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import time
import PyHelpers
import Popup as PyPopup
import CvConfigParser
import CvScreenEnums
import math
from CvMercenaryScreensEnums import *

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


class CvMercenaryManager:
	"Mercenary Manager"
	
	def __init__(self, iScreenId):
	
		self.mercenaryName = None
		self.screenFunction = None
		
		# The different UI wiget names
		self.MERCENARY_MANAGER_SCREEN_NAME = "MercenaryManager"

		self.WIDGET_ID = "MercenaryManagerWidget"
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.EventKeyDown=6
						
		self.iScreenId = iScreenId
		
		# When populated this dictionary will contain the information needed to build
		# the widgets for the current screen resolution.		
		self.screenWidgetData = {}
	
		self.nWidgetCount = 0
		self.iActivePlayer = -1
		
		self.currentScreen = MERCENARY_MANAGER
		
		
	# Returns the instance of the mercenary manager screen.						
	def getScreen(self):
		return CyGInterfaceScreen(self.MERCENARY_MANAGER_SCREEN_NAME, self.iScreenId)


	# Gets the instance of the mercenary manager screen and hides it.
	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()


	# Returns true if the screen is active, false otherwise.	
	def isActive(self):
		return self.getScreen().isActive()

					
	# Screen construction function
	def interfaceScreen(self):
							
		# Create a new screen
		screen = self.getScreen()
				
		if screen.isActive():
			return
			
 		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.nWidgetCount = 0
	
		self.iActivePlayer = gc.getGame().getActivePlayer()
		
		screen = self.getScreen()

		# Calculate all of the screen position data
		self.calculateScreenWidgetData(screen)
		
		if(self.currentScreen == MERCENARY_MANAGER):
			self.drawMercenaryScreenContent(screen)
		elif(self.currentScreen == MERCENARY_GROUPS_MANAGER):
			self.drawMercenaryGroupsScreenContent(screen)
		elif(self.currentScreen == MERCENARY_CONTRACT_MANAGER):
			self.drawMercenaryContractsScreenContent(screen)
		

	# Populates the panel that shows all of the available mercenaries in the
	# global mercenary pool.
	def populateAvailableMercenariesPanel(self, screen):

		# Get the available mercenaries
		mercenaryCount = gc.getGame().getNumMercenaries()
		
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the actual current player object
		player = gc.getPlayer(iPlayer)
		
		# Get the players current gold amount
		currentGold = player.getGold()

		effectiveMercenaryCount=0
		# Go through the mercenaries and populate the available mercenaries panel
		for mercenaryid in range(mercenaryCount):

			# Get the mercenary from the dictionary	
			mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
			if (mercenary.iCurrentOwner!=-1):
				continue
			if(self.iActivePlayer == mercenary.iOriginalOwner):
				continue
			print mercenary.iUnitType
			print gc.getUnitInfo(mercenary.iUnitType).getType()
			mercenaryButtonName = CvUtil.convertToStr(mercenary.name)+"_"+self.numberToAlpha(mercenaryid)

			screen.attachPanel(AVAILABLE_MERCENARIES_INNER_PANEL_ID, mercenaryButtonName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( mercenaryButtonName, mercenaryButtonName+"_InfoButton", 
										gc.getUnitInfo(mercenary.iUnitType).getArtInfo(0, EraTypes(-1),UnitArtStyleTypes(mercenary.iUnitArtStyle)).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(mercenaryButtonName, mercenaryButtonName+"Text",mercenary.name, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Build the mercenary hire cost string
			strHCost = u"%d%c" %(mercenary.getCost(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

			# Build the mercenary maintenance cost string
			strMCost = u"%d%c" %(mercenary.getUpkeep(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

			screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text3", "     Level: " + str(mercenary.iLevel))			
			screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text4", "     Hire Cost: " + strHCost + "  Maint. Cost: " + strMCost)

			bEnableHireMercenary = true

			# Check to see if the player has enough gold to hire the mercenary. If they don't then
			# don't let them hire the mercenary.
			if	(currentGold-mercenary.getCost(iPlayer) <= 0):
				bEnableHireMercenary = false
							
			# Add the hire button for the mercenary
			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryButtonName, CvUtil.convertToStr(mercenary.name)+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryButtonName, mercenaryButtonName+"_HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

			effectiveMercenaryCount=effectiveMercenaryCount+1

#		# Add the padding to the available mercenaries panel to improve the look of the screen
#		if((4-effectiveMercenaryCount)>0):
#
#			for i in range(4-effectiveMercenaryCount):
#				screen.attachPanel(AVAILABLE_MERCENARIES_INNER_PANEL_ID, "dummyPanelHire"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
#				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
#				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")
#				screen.attachLabel( "dummyPanelHire"+str(i), "", "     ")


	# Populates the panel that shows all of the players hired mercenaries
	def populateHiredMercenariesPanel(self, screen):

		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the actual current player object
		player = gc.getPlayer(iPlayer)
		# Get all of the players hired mercenaries
		mercenaryCount = gc.getGame().getNumMercenaries()
		effectiveMercenaryCount=0
		# Go through the mercenaries and populate the hired mercenaries panel
		for mercenaryid in range(mercenaryCount):

			# Get the mercenary from the dictionary	
			mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
			if (mercenary.iCurrentOwner!=iPlayer):
				continue
			mercenaryName = CvUtil.convertToStr(mercenary.name)
			mercenaryButtonName=mercenaryName+"_"+self.numberToAlpha(mercenaryid)
			
			# Continue if the builder of the mercenary is the same as the owner of the mercenary
			if(mercenary.iCurrentOwner == mercenary.iOriginalOwner):
				continue
			
			screen.attachPanel(HIRED_MERCENARIES_INNER_PANEL_ID, mercenaryButtonName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( mercenaryButtonName, mercenaryButtonName+"_InfoButton", 
										gc.getUnitInfo(mercenary.iUnitType).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(mercenaryButtonName, mercenaryButtonName+"Text",mercenary.name, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Build the mercenary hire cost string
			strCost = u"%d%c" %(mercenary.getUpkeep(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

			# Build the mercenary XP string
			strXP = u"%d/%d" %(mercenary.iExperience/100., mercenary.iNextLevelExperience/100.)
			 
			screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text3", "     Level: " + str(mercenary.iLevel) + "      XP: " + strXP)
			screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text4", "     Maint. Cost: " + strCost)

			screen.attachPanel(mercenaryButtonName, mercenaryButtonName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)


			# Only show the fire button if the mercenary is in the game
			if(mercenary.iUnitID != -1):
				
				screen.attachImageButton( mercenaryButtonName, mercenaryName+"_"+self.numberToAlpha(mercenary.iUnitID)+"_FindButton", 
											"Art/Interface/Buttons/Actions/Wake.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, False )

				screen.attachImageButton( mercenaryButtonName, mercenaryButtonName+"_FireButton", 
											"Art/Interface/Buttons/Actions/Cancel.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			effectiveMercenaryCount=effectiveMercenaryCount+1
			
		i = 0

		# Add the padding to the hired mercenaries panel to improve the look of the screen
#		if((4-effectiveMercenaryCount)>0):
#			for i in range(4-effectiveMercenaryCount):
#				screen.attachPanel(HIRED_MERCENARIES_INNER_PANEL_ID, "dummyPanelFire"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
#				screen.attachLabel( "dummyPanelFire"+str(i), "", "     ")
#				screen.attachLabel( "dummyPanelFire"+str(i), "", "     ")
#				screen.attachLabel( "dummyPanelFire"+str(i), "", "     ")


	# Populates the panel that shows all of the players units available to be
	# contracted out as mercenaries
	def clearAvailableUnitsPanel(self,screen):
		# Get all of the units available to be contracted out as mercenaries.
		iPlayer = gc.getGame().getActivePlayer()
		pyPlayer = PyPlayer(iPlayer)
		unitList = pyPlayer.getUnitList()
		effectiveUnitList=0
		# Go through all of the units
		for unit in unitList:
	
			if not unit.canContractOut():
				continue
			
			effectiveUnitList=effectiveUnitList+1
			unitName = str(unit.getNameNoDesc()) 
		
			unitID = unitName + "_" + self.numberToAlpha(unit.getID())
			screen.deleteWidget(unitID)
			
	
	def populateAvailableUnitsPanel(self, screen):

		# Get all of the units available to be contracted out as mercenaries.
		iPlayer = gc.getGame().getActivePlayer()
		pyPlayer = PyPlayer(iPlayer)
		unitList = pyPlayer.getUnitList()
		effectiveUnitList=0
		# Go through all of the units
		for unit in unitList:
	
			
			unitName = str(unit.getNameNoDesc()) 
		
			unitID = unitName + "_" + self.numberToAlpha(unit.getID())
			print "checking if the unit can contract out"
			print unitName
			print unitID
			print unit.canContractOut()
			print "done checking"
			if not unit.canContractOut():
				continue
			
			effectiveUnitList=effectiveUnitList+1
			unitName = ""
			

			screen.attachPanel(AVAILABLE_UNITS_INNER_PANEL_ID, unitID, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( unitID, unitID+"_UnitInfoButton", 
										gc.getUnitInfo(unit.getUnitType()).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(unitID, unitID+"Text",unitName, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Build the unit XP string
			strXP = u"%d/%d" %(unit.getExperience(), unit.experienceNeeded())
			 
			screen.attachLabel( unitID+"Text", unitID  + "text3", "     Level: " + str(unit.getLevel()) + "      XP: " + strXP)

			screen.attachPanel(unitID, unitID+"CreateContractButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
			screen.attachImageButton( unitID+"CreateContractButtonPanel", unitID+"_FindButton", 
										"Art/Interface/Buttons/Actions/Wake.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, False )
			screen.attachImageButton( unitID+"CreateContractButtonPanel", unitID+"_CreateContractButton", 
										"Art/Interface/Buttons/Actions/StealPlans.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

			bCreateContract = true
			
			# If the require city unit contract creation and the unit is not in a city then
			# don't show the create contract button for the unit
			if(not unit.plot().isCity()):
				bCreateContract = false
			
			# Show the create contract button if the player can contract out the unit
			print unitName
			print unitID
			print bCreateContract
			if(bCreateContract):
				print "trying to attach the label"
				screen.attachLabel( unitID+"Text", unitID  + "text4", "     In: " + unit.plot().getPlotCity().getName())
	#		print "trying to attach the button"		
	#		screen.attachImageButton( unitID, unitID+"_CreateContractButton", 
	#										"Art/Interface/Buttons/Actions/StealPlans.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
	#		print "done attaching the button"
		# Add the padding to the available units panel to improve the look of the screen										
#		if((4-effectiveUnitList)>0):
#			for i in range(4-effectiveUnitList):
#				screen.attachPanel(AVAILABLE_UNITS_INNER_PANEL_ID, "dummyPanelCreateContract"+str(i), "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
#				screen.attachLabel( "dummyPanelCreateContract"+str(i), "", "     ")
#				screen.attachLabel( "dummyPanelCreateContract"+str(i), "", "     ")
#				screen.attachLabel( "dummyPanelCreateContract"+str(i), "", "     ")
				
				
	# Populates the panel that shows all of the players units contracted out 
	# as mercenaries
	def populateContractedOutUnitsPanel(self, screen):
		
		# Get all of the units contracted out as mercenaries.
		print "populating contracted out units right now"

		mercenaryCount = gc.getGame().getNumMercenaries()
		effectiveMercenaryCount=0
		
		# Go through all of the units
		print "starting looking through the mercenaries"
		for mercenaryid in range(mercenaryCount):

			# Get the mercenary from the dictionary	
			mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
			if (mercenary.iOriginalOwner!=self.iActivePlayer):
				continue
			print mercenary
			print CvUtil.convertToStr(mercenary.name)
			print mercenary.iUnitType
			mercenaryName = CvUtil.convertToStr(mercenary.name)
			mercenaryButtonName=mercenaryName+"_"+self.numberToAlpha(mercenaryid)
			
			
			# If the unit is actually in the game then convert their ID number
			# to the alpha representation, otherwise just use a dummy value.
			
			bPlaced = false
			
			if(mercenary.iCurrentOwner!=-1):
				bPlaced = true
				
			screen.attachPanel(UNITS_CONTRACTED_OUT_INNER_PANEL_ID, mercenaryButtonName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
			screen.attachImageButton( mercenaryButtonName, mercenaryButtonName+"_InfoButton", 
										gc.getUnitInfo(mercenary.iUnitType).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.attachPanel(mercenaryButtonName, mercenaryButtonName+"Text",mercenary.name, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Build the unit XP string
			strXP = u"%d/%d" %(mercenary.iExperience/100., mercenary.iNextLevelExperience/100.)
			 
			screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text3", "     Level: " + str(mercenary.iLevel) + "      XP: " + strXP)

			# If the unit is hired then display their employeers information
			if(mercenary.iCurrentOwner!=-1):
				screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text4", "     Hired by: " + gc.getPlayer(mercenary.iCurrentOwner).getName())
				
			print "now trying to make the cancel contract button appear"			
			screen.attachPanel(mercenaryButtonName, mercenaryButtonName+"CancelContractButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
			screen.attachImageButton( mercenaryButtonName+"CancelContractButtonPanel", mercenaryButtonName+"_CancelContractButton", 
											"Art/Interface/Buttons/Actions/Cancel.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			effectiveMercenaryCount=effectiveMercenaryCount+1
			

				
	# Clears out the unit information panel contents
	def clearUnitInformation(self, screen):
		screen.deleteWidget(UNIT_INFORMATION_PROMOTION_PANEL_ID)
		screen.deleteWidget(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID)
		screen.deleteWidget(UNIT_INFORMATION_DETAILS_PANEL_ID)
		screen.deleteWidget(UNIT_GRAPHIC)
		

	# Populates the unit information panel with the unit information details		
	def populateUnitInformation(self, screen, unitid):
			# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		player = gc.getPlayer(iPlayer)
		mercenary = player.getUnit(unitid)
		
		screen.addPanel(UNIT_INFORMATION_PROMOTION_PANEL_ID, "", "", True, True, self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID, "Promotions", "", True, True, self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.addPanel(UNIT_INFORMATION_DETAILS_PANEL_ID, "", "", True, False, self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC( UNIT_INFORMATION_DETAILS_PANEL_ID, UNIT_INFORMATION_DETAILS_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(UNIT_INFORMATION_DETAILS_LIST_ID, False)

		# Build the unit XP string
		strXP = u"%d/%d" %(mercenary.getExperienceTimes100()/100., mercenary.experienceNeededTimes100()/100.)

		# Build the unit stats string
		strStats = u"%d%c    %d%c" %(gc.getUnitInfo(mercenary.getUnitType()).getCombat(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),gc.getUnitInfo(mercenary.getUnitType()).getMoves(),CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, mercenary.getName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Unit Type: " + gc.getUnitInfo(mercenary.getUnitType()).getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  Level: " + str(mercenary.getLevel()) + "     XP: " + strXP, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  " + strStats, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "  ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		

		screen.attachMultiListControlGFC(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID, UNIT_INFORMATION_PROMOTION_LIST_CONTROL_ID, "", 1, 64, 64, TableStyles.TABLE_STYLE_STANDARD)

		# Add all of the promotions the mercenary/unit has.
		for id in range(gc.getNumPromotionInfos()):
			if mercenary.isHasPromotion(id):
				screen.appendMultiListButton( UNIT_INFORMATION_PROMOTION_LIST_CONTROL_ID, gc.getPromotionInfo(id).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, id, -1, false )

		screen.addSpecificUnitGraphicGFC(UNIT_GRAPHIC, mercenary, self.screenWidgetData[UNIT_ANIMATION_X], self.screenWidgetData[UNIT_ANIMATION_Y], self.screenWidgetData[UNIT_ANIMATION_WIDTH], self.screenWidgetData[UNIT_ANIMATION_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1, self.screenWidgetData[UNIT_ANIMATION_ROTATION_X], self.screenWidgetData[UNIT_ANIMATION_ROTATION_Z], self.screenWidgetData[UNIT_ANIMATION_SCALE], True)
		
	# Clears out the mercenary information panel contents
	def clearMercenaryInformation(self, screen):
		screen.deleteWidget(MERCENARY_INFORMATION_PROMOTION_PANEL_ID)
		screen.deleteWidget(MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID)
		screen.deleteWidget(MERCENARY_INFORMATION_DETAILS_PANEL_ID)
		screen.deleteWidget(MERCENARIES_UNIT_GRAPHIC)		
		
			
	# Populates the mercenary information panel with the unit information details		
	def populateMercenaryInformation(self, screen, mercenary):
		
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the actual current player object
		player = gc.getPlayer(iPlayer)
		
		screen.addPanel(MERCENARY_INFORMATION_PROMOTION_PANEL_ID, "", "", True, True, self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID, "Promotions", "", True, True, self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.addPanel(MERCENARY_INFORMATION_DETAILS_PANEL_ID, "", "", True, False, self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC( MERCENARY_INFORMATION_DETAILS_PANEL_ID, MERCENARY_INFORMATION_DETAILS_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(MERCENARY_INFORMATION_DETAILS_LIST_ID, False)

		# Build the mercenary hire cost string
		strHCost = u"%d%c" %(mercenary.getCost(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

		# Build the mercenary maintenance cost string
		strMCost = u"%d%c" %(mercenary.getUpkeep(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

		# Build the mercenary XP string
		strXP = u"%d/%d" %(mercenary.iExperience/100., mercenary.iNextLevelExperience/100.)

		# Build the unit stats string
		strStats = u"%d%c    %d%c" %(gc.getUnitInfo(mercenary.iUnitType).getCombat(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),gc.getUnitInfo(mercenary.iUnitType).getMoves(),CyGame().getSymbolID(FontSymbols.MOVES_CHAR))

		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, mercenary.name, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Unit Type: " + gc.getUnitInfo(mercenary.iUnitType).getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Level: " + str(mercenary.iLevel) + "     XP: " + strXP, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  " + strStats, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Hire Cost: " + strHCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		# Show the mercenary costs if it is in the game			
		screen.appendListBoxString( MERCENARY_INFORMATION_DETAILS_LIST_ID, "  Maint. Cost: " + strMCost, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
	
		# Get the promotion list for the mercenary
		promotionsize = mercenary.getPromotionsLength()

		screen.attachMultiListControlGFC(MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_ID, MERCENARY_INFORMATION_PROMOTION_LIST_CONTROL_ID, "", 1, 64, 64, TableStyles.TABLE_STYLE_STANDARD)

		# Add all of the promotions the mercenary has.
		for id in range(promotionsize):
			promotion= mercenary.getPromotion(id)
			screen.appendMultiListButton( MERCENARY_INFORMATION_PROMOTION_LIST_CONTROL_ID, gc.getPromotionInfo(promotion).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, promotion, -1, false )
		pPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())	
		newUnit = pPlayer.initUnit(mercenary.iUnitType, 0, 0, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setUnitArtStyleType(mercenary.iUnitArtStyle)	
		screen.addSpecificUnitGraphicGFC(MERCENARIES_UNIT_GRAPHIC, newUnit, self.screenWidgetData[MERCENARY_ANIMATION_X], self.screenWidgetData[MERCENARY_ANIMATION_Y], self.screenWidgetData[MERCENARY_ANIMATION_WIDTH], self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1, self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_X], self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_Z], self.screenWidgetData[MERCENARY_ANIMATION_SCALE], True)
		newUnit.kill(False, -1)

	
	# Draws the gold information in the "Mercenary Manager" screens
	def drawGoldInformation(self, screen):
	
		iCost = 0
		strCost = ""		
		player = gc.getGame().getActivePlayer()
		pPlayer=gc.getPlayer(player)
		# If the current screen is the mercenary contract manager screen then 
		# get the mercenary contract income information
		if(self.currentScreen == MERCENARY_CONTRACT_MANAGER):
			iCost = -pPlayer.getMercenaryUpkeep()
			strCost = u"%s %c: %d" %("Mercenary Contract Income", gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),iCost)
		
		# Otherwise get the mercenary maintenance information
		else:
			iCost = pPlayer.getMercenaryUpkeep()
			strCost = u"%s %c: %d" %("Mercenary Maintenance", gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar(),iCost)

		# Get the players current gold text		
		szText = CyGameTextMgr().getGoldStr(gc.getGame().getActivePlayer())
		screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12, 6, -1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.show( "GoldText" )
		screen.moveToFront( "GoldText" )

		screen.setLabel( "MaintainText", "Background", strCost, CvUtil.FONT_LEFT_JUSTIFY, 12, 24, -1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.show( "MaintainText" )
		screen.moveToFront( "MaintainText" )
		

	# Draws the top bar of the "Mercenary Manager" screens
	def drawScreenTop(self, screen):
		screen.setDimensions(0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT])
		screen.addDrawControl(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )
 		screen.addDDSGFC(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		screen.addPanel(SCREEN_TITLE_PANEL_ID, u"", u"", True, False, self.screenWidgetData[SCREEN_TITLE_PANEL_X], self.screenWidgetData[SCREEN_TITLE_PANEL_Y], self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH], self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_TOPBAR )
		screen.setText(SCREEN_TITLE_TEXT_PANEL_ID, "Background", self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X], self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Draw the gold information for the screen
		self.drawGoldInformation(screen)


	# Draws the bottom bar of the "Mercenary Manager" screens
	def drawScreenBottom(self, screen):
		iPlayer = gc.getGame().getActivePlayer()
		player = gc.getPlayer(iPlayer)
		screen.addPanel(BOTTOM_PANEL_ID, "", "", True, True, self.screenWidgetData[BOTTOM_PANEL_X], self.screenWidgetData[BOTTOM_PANEL_Y], self.screenWidgetData[BOTTOM_PANEL_WIDTH], self.screenWidgetData[BOTTOM_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText(MERCENARIES_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARIES_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[MERCENARIES_TEXT_PANEL_X], self.screenWidgetData[MERCENARIES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		# Commented out due to mercenary groups not being implemented yet.
		# screen.setText(MERCENARY_GROUPS_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		if player.isContractOut():
			screen.setText(MERCENARY_CONTRACTS_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(EXIT_TEXT_PANEL_ID, "Background", self.screenWidgetData[EXIT_TEXT_PANEL], CvUtil.FONT_RIGHT_JUSTIFY, self.screenWidgetData[EXIT_TEXT_PANEL_X], self.screenWidgetData[EXIT_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )


	# Draws the mercenary groups screen content	
	def drawMercenaryGroupsScreenContent(self, screen):
	
		# Draw the top bar
		self.drawScreenTop(screen)

		# Draw the bottom bar
		self.drawScreenBottom(screen)

		screen.addPanel(AVAILABLE_MERCENARY_GROUPS_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(HIRED_MERCENARY_GROUPS_PANEL_ID, "", "", True, True, self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y], self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(HIRED_MERCENARY_GROUPS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_Y], self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(HIRED_MERCENARY_GROUPS_TEXT_PANEL_ID, "Background", self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_X], self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(MERCENARY_GROUP_INFORMATION_PANEL_ID, "", "", True, True, self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(MERCENARY_GROUP_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.showWindowBackground(False)

	
	# Draws the mercenary contract screen content
	def	drawMercenaryContractsScreenContent(self, screen):

		# Draw the top bar
		self.drawScreenTop(screen)

		# Draw the bottom bar
		self.drawScreenBottom(screen)

		screen.addPanel(UNITS_CONTRACTED_OUT_PANEL_ID, "", "", True, True, self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X], self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y], self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH], self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(UNITS_CONTRACTED_OUT_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_X], self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_Y], self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_WIDTH], self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(UNITS_CONTRACTED_OUT_TEXT_PANEL_ID, "Background", self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_X], self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(AVAILABLE_UNITS_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_UNITS_PANEL_X], self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y], self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_UNITS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_UNITS_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_UNITS_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(UNIT_INFORMATION_PANEL_ID, "", "", True, True, self.screenWidgetData[UNIT_INFORMATION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(UNIT_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.showWindowBackground(False)

		# Populate the contents of the contracted out units panel
		self.populateContractedOutUnitsPanel(screen)

		# Populate the available units panel
		self.populateAvailableUnitsPanel(screen)
	

	# Draws the mercenary screen content
	def drawMercenaryScreenContent(self, screen):

		# Draw the top bar
		self.drawScreenTop(screen)
 
		# Draw the bottom bar
		self.drawScreenBottom(screen)
				
		screen.addPanel(AVAILABLE_MERCENARIES_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(AVAILABLE_MERCENARIES_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(AVAILABLE_MERCENARIES_TEXT_PANEL_ID, "Background", self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_X], self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(HIRED_MERCENARIES_PANEL_ID, "", "", True, True, self.screenWidgetData[HIRED_MERCENARIES_PANEL_X], self.screenWidgetData[HIRED_MERCENARIES_PANEL_Y], self.screenWidgetData[HIRED_MERCENARIES_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARIES_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(HIRED_MERCENARIES_INNER_PANEL_ID, "", "", True, True, self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_X], self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_Y], self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(HIRED_MERCENARIES_TEXT_PANEL_ID, "Background", self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_X], self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addPanel(MERCENARY_INFORMATION_PANEL_ID, "", "", True, True, self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(MERCENARY_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
		screen.showWindowBackground(False)

		# Populate the available mercenaries panel
		self.populateAvailableMercenariesPanel(screen)
		print "here we are in the main call to populate, screen is :"
		print self.getScreen()
		# Populate the hired mercenaries panel
		self.populateHiredMercenariesPanel(screen)

	# Performs the operation needed to contract out a player's unit as a
	# mercenary
	def contractOutMercenary(self, screen, panelID, unitID):

		# Get the active player ID
		iPlayer = gc.getGame().getActivePlayer()
	
		# Get the reference of the actual player
		player = gc.getPlayer(iPlayer)
		
		# Delete the UI representation of the unit from the available units
		# panel
		screen.deleteWidget(panelID)

		# Get the available units for the player		
#		unitDict = objMercenaryUtils.getAvailableUnits(iPlayer)
				
#		i = 0
		
#		# Delete the padding from the available units panel
#		if((4-len(unitDict))>0):
#			for i in range(4-len(unitDict)):
#				screen.deleteWidget("dummyPanelCreateContract"+str(i))

		
		# Get the contracted out units for the player		
#		unitDict = objMercenaryUtils.getContractedOutUnits(iPlayer)
		
#		i = 0
		# Delete the padding from the units contracted out panel
#		if((4-len(unitDict))>0):
#			for i in range(4-len(unitDict)):
#				screen.deleteWidget("dummyPanelContractedOut"+str(i))
		
		# Get the actual unit in the game
		objUnit = player.getUnit(unitID)

		
		# Contract out the unit as a mercenary.
		gc.getGame().generateNewMercenaryFromUnit(objUnit)
		self.clearUnitInformation(screen)
		self.clearMercenaryInformation(screen)
		self.populateContractedOutUnitsPanel(screen)
		# Draw the gold information for the screen
		self.drawGoldInformation(screen)
		
		
	
	# Cancels the contract of a unit contracted out by a player
	def cancelContract(self, screen, unitID):
	
		# Get the active player ID
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the reference of the actual player
		player = gc.getPlayer(iPlayer)
		
		# Delete the UI representation of the unit from the units contracted out
		# panel
		
		# Cancel the units contract
		mercenary = gc.getGame().getMercenaryByIndex(unitID)
		mercenaryName = CvUtil.convertToStr(mercenary.name)
		mercenaryButtonName=mercenaryName+"_"+self.numberToAlpha(unitID)
		screen.deleteWidget(mercenaryButtonName)
		if(mercenary == None):
			return
		print "current owner is"
		print mercenary.iCurrentOwner
		if mercenary.iCurrentOwner!=-1:
			unit = gc.getPlayer(mercenary.iCurrentOwner).getUnit(mercenary.iUnitID)
			gc.getGame().updateMercenaryfromUnit(unit)
		else:
			gc.getGame().generateUnitFromMercenary(unitID,iPlayer)

			
		# Draw the gold information for the screen
		self.drawGoldInformation(screen)
		self.clearUnitInformation(screen)
		self.clearMercenaryInformation(screen)
		self.clearAvailableUnitsPanel(screen)
		self.populateAvailableUnitsPanel(screen)
		# Clear out the unit information panel

				
	
	# Hires a mercenary for a player
	def hireMercenary(self, screen, mercenaryid):

		# Get the active player ID
		iPlayer = gc.getGame().getActivePlayer()
		
		player = gc.getPlayer(iPlayer)
		# Delete the UI representation of the unit from the available mercenaries
		# panel
		mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
		mercenaryName = CvUtil.convertToStr(mercenary.name)
		mercenaryButtonName=mercenaryName+"_"+self.numberToAlpha(mercenaryid)
		screen.deleteWidget(mercenaryButtonName)
		gc.getGame().generateUnitFromMercenary(mercenaryid,iPlayer)
		mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
								

		# Return immediately if we couldn't get the mercenary
		if(mercenary == None):
			return
				

		screen.attachPanel(HIRED_MERCENARIES_INNER_PANEL_ID, mercenaryButtonName, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)
		screen.attachImageButton( mercenaryButtonName, mercenaryButtonName+"_InfoButton", 
									gc.getUnitInfo(mercenary.iUnitType).getArtInfo(0, EraTypes(-1),UnitArtStyleTypes(mercenary.iUnitArtStyle)).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
		screen.attachPanel(mercenaryButtonName, mercenaryButtonName+"Text",mercenary.name, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

		# Build the mercenary maintenance cost string
		strCost = u"%d%c" %(mercenary.getUpkeep(iPlayer), gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

		# Build the mercenary XP string
		strXP = u"%d/%d" %(mercenary.iExperience/100., mercenary.iNextLevelExperience/100.)
				 
		screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text3", "     Level: " + str(mercenary.iLevel) + "      XP: " + strXP)
		screen.attachLabel( mercenaryButtonName+"Text", mercenaryButtonName  + "text4", "     Maint. Cost: " + strCost)

		screen.attachPanel(mercenaryButtonName, mercenaryButtonName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)

		# Only show the fire button if the mercenary is in the game
		screen.attachImageButton( mercenaryButtonName, mercenaryName+"_"+self.numberToAlpha(mercenary.iUnitID)+"_FindButton", 
										"Art/Interface/Buttons/Actions/Wake.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, False )

		screen.attachImageButton( mercenaryButtonName, mercenaryName+"_"+self.numberToAlpha(mercenaryid)+"_FireButton", 
										"Art/Interface/Buttons/Actions/Cancel.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
									

		# Draw the gold information for the screen
		self.drawGoldInformation(screen)

		# Update the available mercenaries in the available mercenaries panel
		self.populateAvailableMercenariesPanel(screen)

		# Clear the information in the mercenary information panel
		self.clearMercenaryInformation(screen)
				
	# Updates the available mercenaries panel, displays the hire button to the 
	# player only for the mercenaries they can hire.
	def updateAvailableMercenaries(self, screen):

		# Get the available mercenaries
		mercenaryCount = gc.getGame().getNumMercenaries()
		
		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the actual current player object
		player = gc.getPlayer(iPlayer)
		
		# Get the players current gold amount
		currentGold = player.getGold()

		effectiveMercenaryCount=0
		# Go through the mercenaries and populate the available mercenaries panel
		for mercenaryid in range(mercenaryCount):

			# Get the mercenary from the dictionary	
			mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
			if (mercenary.iCurrentOwner!=-1):
				continue
			if(self.iActivePlayer == mercenary.iOriginalOwner):
				continue
			
			mercenaryName = CvUtil.convertToStr(mercenary.name)

			# Delete the hire button for the current mercenary we are processing.
			screen.deleteWidget(mercenaryName+"_HireButton")

			bEnableHireMercenary = true

			# Check to see if the player has enough gold to hire the mercenary. If they don't then
			# don't let them hire the mercenary.
			if	(currentGold-mercenary.getCost(iPlayer) <= 0):
				bEnableHireMercenary = false


			if(bEnableHireMercenary):
				screen.attachPanel(mercenaryName, mercenaryName+"hireButtonPanel", "", "", False, True, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachImageButton( mercenaryName, mercenaryid+"_HireButton", 
											"Art/Interface/Buttons/Actions/Join.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

	# Fire the mercenary from the player										
	def fireMercenary(self, screen, mercenaryid):

		# Get the ID for the current active player
		iPlayer = gc.getGame().getActivePlayer()
		
		# Get the actual current player object
		player = gc.getPlayer(iPlayer)
		
		# Get the players current gold amount
		currentGold = player.getGold()
		mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
		unit = gc.getPlayer(mercenary.iCurrentOwner).getUnit(mercenary.iUnitID)
		gc.getGame().updateMercenaryfromUnit(unit)
		# Delete the UI representation of the unit from the hired mercenaries
		# panel
		MercenaryButtonName = CvUtil.convertToStr(mercenary.name)+"_"+self.numberToAlpha(mercenaryid)
		screen.deleteWidget(MercenaryButtonName)
				
		# Draw the gold information for the screen
		self.drawGoldInformation(screen)		
		self.clearMercenaryInformation(screen)
		print "do we get to that part of the firing system"
		# Update the available mercenaries in the available mercenaries panel
		self.populateAvailableMercenariesPanel(screen)
		print "here we are in the fire call to populate, screen is :"
		print self.getScreen()
		# Clear the information in the mercenary information panel
				
	
	# Handles the input to the mercenary manager screens
	def handleInput (self, inputClass):

		print "mercenary input 101"
		# Get the instance of the screen
		screen = self.getScreen()
		
		# Get the data
		theKey = int(inputClass.getData())
		print "starting an input"
		print inputClass
		print inputClass.getFunctionName()
		# If the escape key was pressed then set the current screen to mercenary manager
		if (inputClass.getNotifyCode() == self.EventKeyDown and theKey == int(InputTypes.KB_ESCAPE)):
			self.currentScreen = MERCENARY_MANAGER

		# If the exit text was pressed then set the current screen to mercenary manager.
		if(inputClass.getFunctionName() == EXIT_TEXT_PANEL_ID):
			self.currentScreen = MERCENARY_MANAGER
		
		# If the mercenaries text was pressed and we aren't currently looking at 
		# the main mercenaries manager screen then set the current screen to 
		# mercenaries manager, hide the screen and redraw the screen.
		if(inputClass.getFunctionName() == MERCENARIES_TEXT_PANEL_ID and self.currentScreen != MERCENARY_MANAGER):
			self.currentScreen = MERCENARY_MANAGER
			self.hideScreen()
			self.interfaceScreen()
			return

		# If the mercenary groups text was pressed and we aren't currently looking 
		# at the mercenary groups screen then set the current screen to 
		# mercenary groups, hide the screen and redraw the screen.		
		if(inputClass.getFunctionName() == MERCENARY_GROUPS_TEXT_PANEL_ID and self.currentScreen != MERCENARY_GROUPS_MANAGER):
			self.currentScreen = MERCENARY_GROUPS_MANAGER
			self.hideScreen()
			self.interfaceScreen()
			return

		# If the mercenary contract text was pressed and we aren't currently looking 
		# at the mercenary contract screen then set the current screen to 
		# mercenary contract, hide the screen and redraw the screen.		
		if(inputClass.getFunctionName() == MERCENARY_CONTRACTS_TEXT_PANEL_ID and self.currentScreen != MERCENARY_CONTRACT_MANAGER):
			self.currentScreen = MERCENARY_CONTRACT_MANAGER
			self.hideScreen()
			self.interfaceScreen()
			return

		# If someone pressed one of the buttons in the screen then handle the
		# action
		if(inputClass.getFunctionName().endswith("Button")):
			# Split up the function name into the mercenary name and the actual
			# action that was performed
			mercenaryName,mercenaryalphaid, function = inputClass.getFunctionName().split("_")
			mercenaryid=self.alphaToNumber(mercenaryalphaid)
			self.screenFunction = function
			self.mercenaryName = None

			# If the function was find, then close the screen and find the unit
			if(function == "FindButton"):

				# Convert the unit ID string back into a number

				# Get the player ID
				iPlayer = gc.getGame().getActivePlayer()

				# Get the actual player reference
				player = gc.getPlayer(iPlayer)

				# Get the actual unit in the game
				objUnit = player.getUnit(mercenaryid)

				# If the unit is not set to None then look at them and select
				# them.
				if(objUnit != None):
					CyCamera().LookAtUnit(objUnit)
					if(not CyGame().isNetworkMultiPlayer()):
						CyInterface().selectUnit(objUnit, true, false, false)

				self.currentScreen = MERCENARY_MANAGER
	
				return
				
			# If the function was hire, then hire the mercenary
			if(function == "HireButton"):
				self.hireMercenary(screen, mercenaryid) 

			# If the function was fire, then fire the mercenary
			if(function == "FireButton"):
				self.fireMercenary(screen, mercenaryid) 

			# If the function was show information then populate the
			# mercenary/unit information
			if(function == "UnitInfoButton"):
			
				# Get the player ID
				iPlayer = gc.getGame().getActivePlayer()

				# Get the actual player reference
				player = gc.getPlayer(iPlayer)


				# Convert the unit ID string back into a number
				id = self.alphaToNumber(mercenaryalphaid)
				
				# Get the mercenary 
			#	mercenary = objMercenaryUtils.getMercenary(mercenaryName)

				# If we didn't get a mercenary from the mercenary pool then
				# it is safe to assume that the unit has never been a 
				# mercenary.
			#	if(mercenary == None):
					
					# Create a blank mercenary
			#		mercenary = objMercenaryUtils.createBlankMercenary()

					# Populate the mercenary object with the data from 
					# the unit that we want to look at
			#		mercenary.loadUnitData(player.getUnit(id))
			#		mercenary.setName(mercenaryName)
					
				# Calculate the screen information
				self.calculateScreenWidgetData(screen)

				# Populate the unit information panel with the mercenary/unit
				# information.
				self.clearUnitInformation(screen)
				self.clearMercenaryInformation(screen)
				self.populateUnitInformation(screen,id)					

			# If the function was to contract out a unit then contract out the
			# player's mercenary
			if(function == "CreateContractButton"):
				
				# Set the panel ID as the mercenary name before breaking it up.
				panelID = mercenaryName+"_"+mercenaryalphaid



				# Convert the unit ID string back into a number
				unitID = self.alphaToNumber(mercenaryalphaid)

				# Contract out the unit as a mercenary
				self.contractOutMercenary(screen, panelID, unitID)

			# If the function was to cancel the units contract then cancel 
			# their contract
			if(function == "CancelContractButton"):

				# Set the panel ID as the mercenary name before breaking it up.
				panelID = mercenaryName+"_"+mercenaryalphaid


				
				# Convert the unit ID string back into a number
				unitID = self.alphaToNumber(mercenaryalphaid)

				# Cancel the units contract
				self.cancelContract(screen, unitID)
										
			# If the function was to show the mercenary information then 
			# populate the mercenary information panel.
			if(function == "InfoButton"):
				print "do we get here"
				self.mercenaryName = mercenaryName
				print mercenaryName

				# If the mercenary name was actually set then get their 
				# information from the global mercenary pool.
				if(mercenaryName != None):
					mercenary = gc.getGame().getMercenaryByIndex(mercenaryid)
					# Get the mercenary from the global mercenary pool
				#	mercenary = objMercenaryUtils.getMercenary(mercenaryName)

					# If we couldn't get the mercenary information try to get it
					# from the player's mercenary pool.
				#	if(mercenary == None):
				#		mercenary = objMercenaryUtils.getPlayerMercenary(mercenaryName,gc.getGame().getActivePlayer())

					# Return immediately if we still couldn't get the mercenary information
				#	if(mercenary == None):
				#		return
					# Calculate the screen information
					self.calculateScreenWidgetData(screen)

					# Populate the mercenary information panel
					self.clearUnitInformation(screen)
					self.clearMercenaryInformation(screen)
					self.populateMercenaryInformation(screen, mercenary)
			 									
		return 0
 		
		
	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName
													
	def update(self, fDelta):
		screen = self.getScreen()
		
		
	# Calculates the screens widgets positions, dimensions, text, etc.
	def calculateScreenWidgetData(self, screen):
		' Calculates the screens widgets positions, dimensions, text, etc. '
		
		# The border width should not be a hard coded number
		self.screenWidgetData[BORDER_WIDTH] = 4
		
		self.screenWidgetData[SCREEN_WIDTH] = screen.getXResolution()
		self.screenWidgetData[SCREEN_HEIGHT] = screen.getYResolution()

		strScreenTitle = ""

		if(self.currentScreen == MERCENARY_MANAGER):
			strScreenTitle = localText.getText("TXT_KEY_MERCENARY_SCREEN_TITLE", ()).upper()
		elif(self.currentScreen == MERCENARY_GROUPS_MANAGER):
			strScreenTitle = localText.getText("TXT_KEY_MERCENARY_GROUPS_SCREEN_TITLE", ()).upper()
		elif(self.currentScreen == MERCENARY_CONTRACT_MANAGER):
			strScreenTitle = localText.getText("TXT_KEY_MERCENARY_CONTRACTS_SCREEN_TITLE", ()).upper()
			
		# Screen title panel information
		self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] = 55
		self.screenWidgetData[SCREEN_TITLE_PANEL_X] = 0
		self.screenWidgetData[SCREEN_TITLE_PANEL_Y] = 0
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL] = u"<font=4b>" + localText.getText("TXT_KEY_MERCENARIES_SCREEN_TITLE", ()).upper() + ": " + strScreenTitle + "</font>"
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH]/2
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y] = 8


		# Exit panel information		
		self.screenWidgetData[BOTTOM_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[BOTTOM_PANEL_HEIGHT] = 55
		self.screenWidgetData[BOTTOM_PANEL_X] = 0
		self.screenWidgetData[BOTTOM_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 55

		self.screenWidgetData[MERCENARIES_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_MERCENARY_SCREEN_TITLE", ()).upper() + "</font>"
		self.screenWidgetData[MERCENARIES_TEXT_PANEL_X] = 30
		self.screenWidgetData[MERCENARIES_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_MERCENARY_GROUPS_SCREEN_TITLE", ()).upper() + "</font>"
		self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_X] = 220
		self.screenWidgetData[MERCENARY_GROUPS_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_MERCENARY_CONTRACTS_SCREEN_TITLE", ()).upper() + "</font>"
		# Commented out since mercenary groups are not being implemented in the v0.5 release of the mod.
		#self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_X] = 485
		self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_X] = 220
		self.screenWidgetData[MERCENARY_CONTRACTS_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[EXIT_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.screenWidgetData[EXIT_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] - 30
		self.screenWidgetData[EXIT_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		
		# Available mercenaries panel information
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] = 450
		self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARIES_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_MERCENARIES", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] + 4		
		
		
		# Hired mercenaries panel information
		self.screenWidgetData[HIRED_MERCENARIES_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIRED_MERCENARIES_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_Y] + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIRED_MERCENARIES_PANEL_WIDTH] = 450
		self.screenWidgetData[HIRED_MERCENARIES_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_X] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_WIDTH] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARIES_INNER_PANEL_HEIGHT] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[HIRED_MERCENARIES_PANEL_WIDTH] - (self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_HIRED_MERCENARIES", ()) + "</font>"
		self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_X] = self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[HIRED_MERCENARIES_TEXT_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARIES_TEXT_BACKGROUND_PANEL_Y] + 4
		
		
		# Mercenary information panel information
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[MERCENARY_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_MERCENARY_INFORMATION", ()) + "</font>"
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4
		
		self.screenWidgetData[MERCENARY_ANIMATION_X] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_X]+20
		self.screenWidgetData[MERCENARY_ANIMATION_Y] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_PANEL_Y]+40
		self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] = 303
		self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT] = 200
		self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_X] = -20
		self.screenWidgetData[MERCENARY_ANIMATION_ROTATION_Z] = 30
		self.screenWidgetData[MERCENARY_ANIMATION_SCALE] = 1.0
		
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y] + self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y]
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT]


		# Units contracted out panel information
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] = 450
		self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_WIDTH] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_INNER_PANEL_HEIGHT] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] - (self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_UNITS_CONTRACTED_OUT", ()) + "</font>"
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_TEXT_BACKGROUND_PANEL_Y] + 4		

		
		# Hired mercenaries panel information
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_Y] + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH] = 450
		self.screenWidgetData[AVAILABLE_UNITS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_UNITS_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_UNITS", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_UNITS_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_UNITS_TEXT_BACKGROUND_PANEL_Y] + 4
		
				
		# Unit information panel information
		self.screenWidgetData[UNIT_INFORMATION_PANEL_X] = self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_X] + self.screenWidgetData[UNITS_CONTRACTED_OUT_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_UNIT_INFORMATION", ()) + "</font>"
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4

		self.screenWidgetData[UNIT_ANIMATION_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X]+20
		self.screenWidgetData[UNIT_ANIMATION_Y] = self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y]+40
		self.screenWidgetData[UNIT_ANIMATION_WIDTH] = 303
		self.screenWidgetData[UNIT_ANIMATION_HEIGHT] = 200
		self.screenWidgetData[UNIT_ANIMATION_ROTATION_X] = -20
		self.screenWidgetData[UNIT_ANIMATION_ROTATION_Z] = 30
		self.screenWidgetData[UNIT_ANIMATION_SCALE] = 1.0
		
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[UNIT_ANIMATION_Y] + self.screenWidgetData[UNIT_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[UNIT_ANIMATION_X] + self.screenWidgetData[UNIT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[UNIT_ANIMATION_Y]
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[UNIT_ANIMATION_X] + self.screenWidgetData[UNIT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[UNIT_ANIMATION_HEIGHT]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_TEXT_BACKGROUND_PANEL_X]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y] + self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*18)
		self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] = 128 + (self.screenWidgetData[BORDER_WIDTH]*9)

		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_INFORMATION_PROMOTION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*2)

		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[MERCENARY_ANIMATION_Y]
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[MERCENARY_ANIMATION_X] + self.screenWidgetData[MERCENARY_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH])*6)
		self.screenWidgetData[MERCENARY_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[MERCENARY_ANIMATION_HEIGHT]
		# Available mercenary groups panel information
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] = 450
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_INNER_PANEL_HEIGHT] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_WIDTH] - (self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_AVAILABLE_MERCENARY_GROUPS", ()) + "</font>"
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] + 4		
		
		
		# Hired mercenary groups panel information
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] = self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_Y] + self.screenWidgetData[AVAILABLE_MERCENARY_GROUPS_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] = 450
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))/2
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_X] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_WIDTH] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_INNER_PANEL_HEIGHT] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_Y] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_PANEL_WIDTH] - (self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_HIRED_MERCENARY_GROUPS", ()) + "</font>"
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_X] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_PANEL_Y] = self.screenWidgetData[HIRED_MERCENARY_GROUPS_TEXT_BACKGROUND_PANEL_Y] + 4

		# Mercenary groups information panel information
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X] = self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_X] + self.screenWidgetData[AVAILABLE_MERCENARIES_PANEL_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_MERCENARY_GROUP_INFORMATION", ()) + "</font>"
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[MERCENARY_GROUP_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4


	# Converts a number into its string representation. This is needed since
	# for whatever reason, numbers did not work very well when using them 
	# for all of the different panels in the mercenary manager screen. The
	# unit ID number 382343 is converted to: CHBCDC.
	def numberToAlpha(self, iNum):
		#             1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
		alphaList = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		strNum = str(iNum)
		strAlpha = ""
		
		# Go though the alphaList and convert the numbers to letters
		for i in range (len(strNum)):
			strAlpha = strAlpha + alphaList[int(strNum[i])]
			
		return strAlpha
	
	
	# Converts a number into its string representation. This is needed since
	# for whatever reason, numbers did not work very well when using them 
	# for all of the different panels in the mercenary manager screen. The
	# string "CHBCDC" is converted to: 382343.
	def alphaToNumber(self, strAlpha):
		#             1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26
		alphaList = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		
		strNum = ""

		# Go though the alphaList and convert the letters to numbers
		for i in range (len(strAlpha)):
			strNum = strNum + str(alphaList.index(strAlpha[i]))
		
		return int(strNum)
