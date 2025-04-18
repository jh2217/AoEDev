## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# Fullscreen, by Ronkhar 2013-08
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvScreensInterface
import CvEventInterface

PIXEL_INCREMENT = 7
BOX_INCREMENT_WIDTH = 29 # Used to be 33 #Should be a multiple of 3...
# TW: Keep BOX_INCREMENT_HEIGHT / BOX_INCREMENT_Y_SPACING = 1.5
BOX_INCREMENT_HEIGHT = 12 #Should be a multiple of 3...
BOX_INCREMENT_Y_SPACING = 8 #Should be a multiple of 3...
BOX_INCREMENT_X_SPACING = 3 #Should be a multiple of 3...

# 
NUM_SECONDARY_BUTTONS_IN_ROW = 7

TEXTURE_SIZE = 24
X_START = 6
X_INCREMENT = 27
Y_INCREMENT = 25

CIV_HAS_TECH = 0
CIV_IS_RESEARCHING = 1
CIV_NO_RESEARCH = 2
CIV_TECH_AVAILABLE = 3
CIV_UNIQUE_TECH = 4
CIV_HAS_UNIQUE_TECH = 5

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvTechChooser:
	"Tech Chooser Screen"

	def __init__(self):
		self.nWidgetCount = 0
		self.iCivSelected = 0
		self.aiCurrentState = []

		# Advanced Start
		self.m_iSelectedTech = -1
		self.m_bSelectedTechDirty = false
		self.m_bTechRecordsDirty = false

	def hideScreen (self):

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		# Hide the screen
		screen.hideScreen()

	# Screen construction function
	def interfaceScreen(self):

		if ( CyGame().isPitbossHost() ):
			return

		# Create a new screen, called TechChooser, using the file CvTechChooser.py for input
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )
		screen.setRenderInterfaceOnly(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		screen.hide("AddTechButton")
		screen.hide("ASPointsLabel")
		screen.hide("SelectedTechLabel")

		if ( CyGame().isDebugMode() ):
			screen.addDropDownBoxGFC( "CivDropDown", 22, 12, 192, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.SMALL_FONT )
			screen.setActivation( "CivDropDown", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString( "CivDropDown", gc.getPlayer(j).getName(), j, j, False )
		else:
			screen.hide( "CivDropDown" )

		if ( screen.isPersistent() and self.iCivSelected == gc.getGame().getActivePlayer()):
			self.updateTechRecords(false)
			return

		self.nWidgetCount = 0
		self.iCivSelected = gc.getGame().getActivePlayer()
		self.aiCurrentState = []
		screen.setPersistent( True )

		# Find out the game resolution and give the same to tech screen (full screen research)
		Screen_Ronkhar = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		W_SCREEN = Screen_Ronkhar.getXResolution() #HD example: 1920
		H_SCREEN = Screen_Ronkhar.getYResolution() #HD example: 1200

		# Advanced Start
		if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() >= 0):

			self.m_bSelectedTechDirty = true
			self.X_ADD_TECH_BUTTON = 10
			self.H_ADD_TECH_BUTTON = 30
			self.Y_ADD_TECH_BUTTON = H_SCREEN - 40 #same as quit button
			self.W_ADD_TECH_BUTTON = 150
			self.X_ADVANCED_START_TEXT = self.X_ADD_TECH_BUTTON + self.W_ADD_TECH_BUTTON + 20

			szText = localText.getText("TXT_KEY_WB_AS_ADD_TECH", ())
			screen.setButtonGFC( "AddTechButton", szText, "", self.X_ADD_TECH_BUTTON, self.Y_ADD_TECH_BUTTON, self.W_ADD_TECH_BUTTON, self.H_ADD_TECH_BUTTON, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
			screen.hide("AddTechButton")


		# Here we set the background widget and exit button, and we show the screen
		screen.showWindowBackground( False )
		screen.setDimensions(0,0, W_SCREEN, H_SCREEN)
		screen.addDDSGFC("TechBG", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG").getPath(), 0, 0, W_SCREEN, H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, -3, W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, H_SCREEN-58, W_SCREEN, 58, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText( "TechChooserExit", "Background", u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, W_SCREEN-14, H_SCREEN-40, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		screen.setActivation( "TechChooserExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

		# Header...
		szText = u"<font=4>"
		szText = szText + localText.getText("TXT_KEY_TECH_CHOOSER_TITLE", ()).upper()
		szText = szText + u"</font>"
		screen.setLabel( "TechTitleHeader", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, W_SCREEN/2, 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Make the scrollable area for the city list...  ?! city ?! (by Ronkhar)
		screen.addScrollPanel( "TechList", u"", -9, 39, W_SCREEN+19, H_SCREEN-111, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.setActivation( "TechList", ActivationTypes.ACTIVATE_NORMAL )
		screen.hide( "TechList" )

		# Add the Highlight
		#screen.addDDSGFC( "TechHighlight", ArtFileMgr.getInterfaceArtInfo("TECH_HIGHLIGHT").getPath(), 0, 0, self.getXStart() + 6, 12 + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#screen.hide( "TechHighlight" )

		# Place the tech blocks
		self.placeTechs()
		# Draw the arrows
		self.drawArrows()
		screen.moveToFront( "CivDropDown" )
		screen.moveToFront( "AddTechButton" )

	def stopDisplayTech(self,eTech):
		pPlayer = gc.getPlayer(self.iCivSelected)
		Manager		= CvEventInterface.getEventManager()
		Civ			= Manager.Civilizations
		Trait		= Manager.Traits
		Alignment	= Manager.Alignments
		Tech		= Manager.Techs
		Option		= Manager.GameOptions
		Unit		= Manager.Units
		hasTrait	= pPlayer.hasTrait
		eAlignment	= pPlayer.getAlignment()
		eCiv		= pPlayer.getCivilizationType()
		bAI			= pPlayer.isHuman() == False
		bAgnostic	= pPlayer.isAgnostic()

		if eTech == gc.getInfoTypeForString('TECH_NEVER'):
			return True

		if eTech == Tech["Orders from Heaven"]:
			if Option["No Order"]: return True
			if bAgnostic: return True

		elif eTech == Tech["White Hand"]:
			if bAgnostic: return True

		elif eTech == Tech["Way of the Earthmother"]:
			if Option["No RoK"]: return True
			if bAgnostic: return True

		elif eTech == Tech["Arete"]:
			if Option["No RoK"]: return True
			if bAgnostic: return True

		elif eTech == Tech["Way of the Forests"]:
			if Option["No Leaves"]: return True
			if bAgnostic: return True
			
		elif eTech == Tech["Hidden Paths"]:
			if Option["No Leaves"]: return True
			if bAgnostic: return True

		elif eTech == Tech["Message from the Deep"]:
			if Option["No OO"]: return True
			if bAgnostic: return True

		elif eTech == Tech["Mind Stapling"]:
			if Option["No OO"]: return True
			if bAgnostic: return True
			
		elif eTech == Tech["Corruption of Spirit"]:
			if Option["No Veil"]: return True
			if bAgnostic: return True
			
		elif eTech == Tech["Infernal Pact"]:
			if Option["No Veil"]: return True
			if bAgnostic: return True

		elif eTech == Tech["Honor"]:
			if bAgnostic: return True

		elif eTech == Tech["Deception"]:
			if bAgnostic: return True

		elif eTech == Tech["Seafaring"]:
			if eCiv != Civ["Lanun"]: return True

		elif eTech == Tech["Steam Power"]:
			if eCiv != Civ["Mechanos"]: return True

		elif eTech == Tech["Alchemy"]:
			if eCiv != Civ["Mechanos"] and Unit["Generic"]["Wandering Sage"]==-1 : return True
			
		elif eTech == Tech["Swampdwelling"]:
			if eCiv != Civ["Cualli"] and eCiv != Civ["Mazatl"]: return True
			
		elif eTech == Tech["The Gift"]: 
			if eCiv != Civ["Scions"]: return True
			
		elif eTech == Tech["Traditions"]: 
			if eCiv != Civ["Jotnar"]: return True
			
		elif eTech == Tech["Dunespeakers"]: 
			if eCiv != Civ["Malakim"]: return True
			
		elif eTech == Tech["Dark Secrets"]: 
			if eCiv != Civ["D'Tesh"]: return True
		else:
			return False
	
	def placeTechs (self):

		iMaxX = 0
		iMaxY = 0

		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		iLeader = pPlayer.getLeaderType()
		iCivilization = pPlayer.getCivilizationType()
		pCapital = pPlayer.getCapitalCity()

		# If we are the Pitboss, we don't want to put up an interface at all
		if ( CyGame().isPitbossHost() ):
			return

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		# Get a list of techs that are required for the Civ's Unique Spell, Unique starting techs
		lUniqueTech = self.getUniqueTech()

		# Go through all the techs
		for i in range(gc.getNumTechInfos()):
			if (self.stopDisplayTech(i)): 
				self.aiCurrentState.append(CIV_NO_RESEARCH)
				continue
			# Added by Grey Fox July 16th 2010
			bFirstToTech = (CyGame().countKnownTechNumTeams(i) == 0)
			# End Add

			# Create and place a tech in its proper location
			iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT ) )
			iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT ) + 5
			szTechRecord = "TechRecord" + str(i)

			if ( iMaxX < iX + self.getXStart() ):
				iMaxX = iX + self.getXStart()
			if ( iMaxY < iY + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ) ):
				iMaxY = iY + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT )

			screen.attachPanelAt( "TechList", szTechRecord, u"", u"", True, False, PanelStyles.PANEL_STYLE_TECH, iX - 6, iY - 6, self.getXStart() + 6, 12 + ( BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ), WidgetTypes.WIDGET_TECH_TREE, i, -1 )
			screen.setActivation( szTechRecord, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)
			screen.hide( szTechRecord )

			#reset so that it offsets from the tech record's panel
			iX = 6
			iY = 6

			if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ) and i in lUniqueTech:
				screen.setPanelColor(szTechRecord, 175, 145, 70)
				self.aiCurrentState.append(CIV_HAS_UNIQUE_TECH)
			elif ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
				screen.setPanelColor(szTechRecord, 85, 150, 87)
				self.aiCurrentState.append(CIV_HAS_TECH)
			elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
				screen.setPanelColor(szTechRecord, 104, 158, 165)
				self.aiCurrentState.append(CIV_IS_RESEARCHING)
			elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
				screen.setPanelColor(szTechRecord, 104, 158, 165)
				self.aiCurrentState.append(CIV_IS_RESEARCHING)
			elif i in lUniqueTech:
				screen.setPanelColor(szTechRecord, 154, 78, 174)
				self.aiCurrentState.append(CIV_UNIQUE_TECH)
			elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
				screen.setPanelColor(szTechRecord, 100, 104, 160)
				self.aiCurrentState.append(CIV_NO_RESEARCH)
			else:
				screen.setPanelColor(szTechRecord, 206, 65, 69)
				self.aiCurrentState.append(CIV_TECH_AVAILABLE)

			szTechID = "TechID" + str(i)
			szTechString = "<font=1>"
			if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
				szTechString = szTechString + str(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "
			szTechString += gc.getTechInfo(i).getDescription()
			szTechString = szTechString + "</font>"
			screen.setTextAt( szTechID, szTechRecord, szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + X_INCREMENT, iY + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )
			screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

			szTechButtonID = "TechButtonID" + str(i)
			screen.addDDSGFCAt( szTechButtonID, szTechRecord, gc.getTechInfo(i).getButton(), iX + 6, iY + 4, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_TECH_TREE, i, -1, False )

			iButton = 0

			j = 0
			k = 0

			# Unlockable units...
			for j in range( gc.getNumUnitClassInfos() ):
				eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(j)
				if iLeader == gc.getInfoTypeForString("LEADER_SAUROS"):
					if pCapital != - 1:
						eLoopUnit = pCapital.getCityUnits(j)
				if (eLoopUnit != -1):
					if (gc.getUnitInfo(eLoopUnit).getPrereqAndTech() == i):
						szUnitButton = "Unit" + str(j)
						iActivePlayer =gc.getGame().getActivePlayer()
						pActivePlayer =gc.getPlayer(iActivePlayer)
						#print eLoopUnit
						#print gc.getUnitInfo(eLoopUnit).getDescription()
						#print str(gc.getUnitInfo(eLoopUnit).getType())
						#print str(gc.getTechInfo(i).getType())
						newbutton = pActivePlayer.getUnitButton(eLoopUnit)
						screen.addDDSGFCAt( szUnitButton, szTechRecord, newbutton, iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, True )
						iButton += 1

			j = 0
			k = 0

			# Unlockable Buildings...
			for j in range(gc.getNumBuildingClassInfos()):
				bTechFound = 0
				eLoopBuilding = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationBuildings(j)
				if iLeader == gc.getInfoTypeForString("LEADER_SAUROS"):
					if pCapital != - 1:
						eLoopUnit = pCapital.getCityBuildings(j)
				if (eLoopBuilding != -1):
					if (gc.getBuildingInfo(eLoopBuilding).getPrereqAndTech() == i):
						szBuildingButton = "Building" + str(j)
						screen.addDDSGFCAt( szBuildingButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, True )
						iButton += 1

			j = 0
			k = 0

			# Obsolete Buildings...
			for j in range(gc.getNumBuildingClassInfos()):
				eLoopBuilding = gc.getCivilizationInfo(gc.getPlayer(self.iCivSelected).getCivilizationType()).getCivilizationBuildings(j)

				if (eLoopBuilding != -1):
					if (gc.getBuildingInfo(eLoopBuilding).getObsoleteTech() == i):
						# Add obsolete picture here...
						szObsoleteButton = "Obsolete" + str(j)
						szObsoleteX = "ObsoleteX" + str(j)
						screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBuildingInfo(eLoopBuilding).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
						screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE, eLoopBuilding, -1, False )
						iButton += 1

			j = 0
			k = 0

			# Obsolete Bonuses...
			for j in range(gc.getNumBonusInfos()):
				if (gc.getBonusInfo(j).getTechObsolete() == i):
					# Add obsolete picture here...
					szObsoleteButton = "ObsoleteBonus" + str(j)
					szObsoleteX = "ObsoleteXBonus" + str(j)
					screen.addDDSGFCAt( szObsoleteButton, szTechRecord, gc.getBonusInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
					screen.addDDSGFCAt( szObsoleteX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_BONUS, j, -1, False )
					iButton += 1

			j = 0
			k = 0

			# Obsolete Monastaries...
			for j in range (gc.getNumSpecialBuildingInfos()):
				if (gc.getSpecialBuildingInfo(j).getObsoleteTech() == i):
						# Add obsolete picture here...
						szObsoleteSpecialButton = "ObsoleteSpecial" + str(j)
						szObsoleteSpecialX = "ObsoleteSpecialX" + str(j)
						screen.addDDSGFCAt( szObsoleteSpecialButton, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
						screen.addDDSGFCAt( szObsoleteSpecialX, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_RED_X").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OBSOLETE_SPECIAL, j, -1, False )
						iButton += 1

			j = 0
			k = 0

			# Route movement change
			for j in range(gc.getNumRouteInfos()):
				if ( gc.getRouteInfo(j).getTechMovementChange(i) != 0 ):
					szMoveButton = "Move" + str(j)
					screen.addDDSGFCAt( szMoveButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MOVE_BONUS").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MOVE_BONUS, i, -1, False )
					iButton += 1

			j = 0
			k = 0

			# Promotion Info
			for j in range( gc.getNumPromotionInfos() ):
				lPromoPrereq = []
				lMekaraPromotions = [gc.getInfoTypeForString('PROMOTION_OVERSEER_SCORCH'), gc.getInfoTypeForString('PROMOTION_OVERSEER_SPRING'), gc.getInfoTypeForString('PROMOTION_OVERSEER_BLOOM')]
				if gc.getPromotionInfo(j).getNumPrereqCivilizations() > 0:
					for k in range(gc.getPromotionInfo(j).getNumPrereqCivilizations()):
						lPromoPrereq.append(gc.getPromotionInfo(j).getPrereqCivilization(k))
				if gc.getPromotionInfo(j).getMinLevel() < 0 or gc.getPromotionInfo(j).isNoXP():
					continue
				if lPromoPrereq and not iCivilization in lPromoPrereq:
					continue
				if gc.getPromotionInfo(j).getNumPrereqUnits() > 0:
					continue
				if j in lMekaraPromotions and iCivilization != gc.getInfoTypeForString('CIVILIZATION_MEKARA'):
					continue
				if ( gc.getPromotionInfo(j).getTechPrereq() == i ):
					szPromotionButton = "Promotion" + str(j)
					screen.addDDSGFCAt( szPromotionButton, szTechRecord, gc.getPromotionInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, j, -1, False )
					iButton += 1

			j = 0
			k = 0

			# Modified by Grey Fox July 16th 2010
			# Free unit
			if bFirstToTech:
				if ( gc.getTechInfo(i).getFirstFreeUnitClass() != UnitClassTypes.NO_UNITCLASS ):
					szFreeUnitButton = "FreeUnit" + str(i)

					eLoopUnit = gc.getCivilizationInfo(gc.getGame().getActiveCivilizationType()).getCivilizationUnits(gc.getTechInfo(i).getFirstFreeUnitClass())
					if (eLoopUnit != -1):
						screen.addDDSGFCAt( szFreeUnitButton, szTechRecord, gc.getPlayer(gc.getGame().getActivePlayer()).getUnitButton(eLoopUnit), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_UNIT, eLoopUnit, i, False )
						iButton += 1
			# End Modify

			j = 0
			k = 0

			# Feature production modifier
			if ( gc.getTechInfo(i).getFeatureProductionModifier() != 0 ):
				szFeatureProductionButton = "FeatureProduction" + str(i)
				screen.addDDSGFCAt( szFeatureProductionButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FEATURE_PRODUCTION").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FEATURE_PRODUCTION, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Worker speed
			if ( gc.getTechInfo(i).getWorkerSpeedModifier() != 0 ):
				szWorkerModifierButton = "Worker" + str(i)
				screen.addDDSGFCAt( szWorkerModifierButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WORKER_SPEED").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WORKER_RATE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Trade Routes per City change
			if ( gc.getTechInfo(i).getTradeRoutes() != 0 ):
				szTradeRouteButton = "TradeRoutes" + str(i)
				screen.addDDSGFCAt( szTradeRouteButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TRADE_ROUTES").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TRADE_ROUTES, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Health Rate bonus from this tech...
			if ( gc.getTechInfo(i).getHealth() != 0 ):
				szHealthRateButton = "HealthRate" + str(i)
				screen.addDDSGFCAt( szHealthRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HEALTH").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HEALTH_RATE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Happiness Rate bonus from this tech...
			if ( gc.getTechInfo(i).getHappiness() != 0 ):
				szHappinessRateButton = "HappinessRate" + str(i)
				screen.addDDSGFCAt( szHappinessRateButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_HAPPINESS").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_HAPPINESS_RATE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Modified by Grey Fox July 16th 2010
			# Free Techs
			if bFirstToTech:
				if ( gc.getTechInfo(i).getFirstFreeTechs() > 0 ):
					szFreeTechButton = "FreeTech" + str(i)
					screen.addDDSGFCAt( szFreeTechButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_FREETECH").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FREE_TECH, i, -1, False )
					iButton += 1
			# End Modify

			j = 0
			k = 0
			# DynTraits Start
			if (not gc.isNoCrash()):
				# Free Temporary Traits
				for j in xrange( gc.getNumTraitInfos() ):
				
					iTraitPoints = gc.getTechInfo(i).getTraitCounterModifier(j)
					iTraitPointsFirstTo = gc.getTechInfo(i).getFirstTraitCounterModifier(j)
					iTemporaryTrait = gc.getTechInfo(i).getTraitGainTemporary(j)
					iTemporaryTraitFirstTo = gc.getTechInfo(i).getFirstTraitGainTemporary(j)
					
					if (bFirstToTech and iTraitPointsFirstTo != 0) or iTraitPoints != 0:
						if (iTraitPointsFirstTo + iTraitPoints) > 0:
							szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_DYNAMIC_TRAITS_COUNTER_POSITIVE").getPath()
						else:
							szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_DYNAMIC_TRAITS_COUNTER_NEGATIVE").getPath()
							
						szTraitButton = "Tech" + str(i) + "TraitPoints" + str(j)
						screen.addDDSGFCAt( szTraitButton, szTechRecord, szButton, iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TRAITCOUNTER, j, i, True )
						iButton += 1
						
					if iTemporaryTrait > 0 or (iTemporaryTraitFirstTo > 0 and bFirstToTech):
						szButton = gc.getTraitInfo(j).getButton()
						if not szButton:
							szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_DYNAMIC_TRAITS_TEMP_GAIN").getPath()

						szTraitButton = "Tech" + str(i) + "TemporaryTrait" + str(j)
						screen.addDDSGFCAt( szTraitButton, szTechRecord, szButton, iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TEMPORARY_TRAIT_GAIN, j, i, True )
						iButton += 1
					
			j = 0
			k = 0
			# DynTraits End
			# Line of Sight bonus...
			if ( gc.getTechInfo(i).isExtraWaterSeeFrom() ):
				szLOSButton = "LOS" + str(i)
				screen.addDDSGFCAt( szLOSButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_LOS").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_LOS_BONUS, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Map Center Bonus...
			if ( gc.getTechInfo(i).isMapCentering() ):
				szMapCenterButton = "MapCenter" + str(i)
				screen.addDDSGFCAt( szMapCenterButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPCENTER").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_CENTER, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Map Reveal...
			if ( gc.getTechInfo(i).isMapVisible() ):
				szMapRevealButton = "MapReveal" + str(i)
				screen.addDDSGFCAt( szMapRevealButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPREVEAL").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_REVEAL, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Map Trading
			if ( gc.getTechInfo(i).isMapTrading() == True ):
				szMapTradeButton = "MapTrade" + str(i)
				screen.addDDSGFCAt( szMapTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_MAPTRADING").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_MAP_TRADE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Tech Trading
			if ( gc.getTechInfo(i).isTechTrading() ):
				szTechTradeButton = "TechTrade" + str(i)
				screen.addDDSGFCAt( szTechTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_TECHTRADING").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_TRADE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Gold Trading
			if ( gc.getTechInfo(i).isGoldTrading() ):
				szGoldTradeButton = "GoldTrade" + str(i)
				screen.addDDSGFCAt( szGoldTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_GOLDTRADING").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_GOLD_TRADE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Open Borders
			if ( gc.getTechInfo(i).isOpenBordersTrading() ):
				szOpenBordersButton = "OpenBorders" + str(i)
				screen.addDDSGFCAt( szOpenBordersButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_OPENBORDERS").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_OPEN_BORDERS, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Defensive Pact
			if ( gc.getTechInfo(i).isDefensivePactTrading() ):
				szDefensivePactButton = "DefensivePact" + str(i)
				screen.addDDSGFCAt( szDefensivePactButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_DEFENSIVEPACT").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DEFENSIVE_PACT, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Permanent Alliance
			if ( gc.getTechInfo(i).isPermanentAllianceTrading() ):
				szPermanentAllianceButton = "PermanentAlliance" + str(i)
				screen.addDDSGFCAt( szPermanentAllianceButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_PERMALLIANCE").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PERMANENT_ALLIANCE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Vassal States
			if ( gc.getTechInfo(i).isVassalStateTrading() ):
				szVassalStateButton = "VassalState" + str(i)
				screen.addDDSGFCAt( szVassalStateButton , szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_VASSAL").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_VASSAL_STATE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Bridge Building
			if ( gc.getTechInfo(i).isBridgeBuilding() ):
				szBuildBridgeButton = "BuildBridge" + str(i)
				screen.addDDSGFCAt( szBuildBridgeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_BRIDGEBUILDING").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BUILD_BRIDGE, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Irrigation unlocked...
			if ( gc.getTechInfo(i).isIrrigation() ):
				szIrrigationButton = "Irrigation" + str(i)
				screen.addDDSGFCAt( szIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_IRRIGATION").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IRRIGATION, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Ignore Irrigation unlocked...
			if ( gc.getTechInfo(i).isIgnoreIrrigation() ):
				szIgnoreIrrigationButton = "IgnoreIrrigation" + str(i)
				screen.addDDSGFCAt( szIgnoreIrrigationButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_NOIRRIGATION").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IGNORE_IRRIGATION, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Coastal Work unlocked...
			if ( gc.getTechInfo(i).isWaterWork() ):
				szWaterWorkButton = "WaterWork" + str(i)
				screen.addDDSGFCAt( szWaterWorkButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERWORK").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_WATER_WORK, i, -1, False )
				iButton += 1

			j = 0
			k = 0

			# Improvements
			for j in range(gc.getNumBuildInfos()):
				bTechFound = 0

				if (gc.getBuildInfo(j).getTechPrereq() == -1):
					bTechFound = 0
					for k in range(gc.getNumFeatureInfos()):
						if (gc.getBuildInfo(j).getFeatureTech(k) == i):
							bTechFound = 1
				else:
					if (gc.getBuildInfo(j).getTechPrereq() == i):
						bTechFound = 1

				if (bTechFound == 1):
					szImprovementButton = "Improvement" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szImprovementButton, szTechRecord, gc.getBuildInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_IMPROVEMENT, i, j, False )
					iButton += 1

			j = 0
			k = 0

			# Added by Grey Fox July 16th 2010
			# City Actions and Worldspells (Spells) available
			for j in xrange ( gc.getNumSpellInfos() ):
				if (gc.getSpellInfo(j).getTechPrereq() == i) and (gc.getSpellInfo(j).isGlobal() or gc.getSpellInfo(j).isCityAction()):
					if (gc.getSpellInfo(j).getCivilizationPrereq() == -1 or gc.getSpellInfo(j).getCivilizationPrereq() == gc.getGame().getActiveCivilizationType()):
						szButton = gc.getSpellInfo(j).getButton()
						szCityActionButton = "CityAction" + str( ( i * 1000 ) + j )
						screen.addDDSGFCAt( szCityActionButton, szTechRecord, szButton, iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL, j, i, False )
						iButton += 1

			j = 0
			k = 0
			# End Add

			# Domain Extra Moves
			for j in range( DomainTypes.NUM_DOMAIN_TYPES ):
				if (gc.getTechInfo(i).getDomainExtraMoves(j) != 0):
					szDomainExtraMovesButton = "DomainExtraMoves" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szDomainExtraMovesButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERMOVES").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_DOMAIN_EXTRA_MOVES, i, j, False )
					iButton += 1

			j = 0
			k = 0

			# Adjustments
			for j in range( CommerceTypes.NUM_COMMERCE_TYPES ):
				if (gc.getTechInfo(i).isCommerceFlexible(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isCommerceFlexible(j))):
					szAdjustButton = "AdjustButton" + str( ( i * 1000 ) + j )
					if ( j == CommerceTypes.COMMERCE_CULTURE ):
						szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_CULTURE").getPath()
					elif ( j == CommerceTypes.COMMERCE_ESPIONAGE ):
						szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_ESPIONAGE").getPath()
					else:
						szFileName = ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_QUESTIONMARK").getPath()
					screen.addDDSGFCAt( szAdjustButton, szTechRecord, szFileName, iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_ADJUST, i, j, False )
					iButton += 1

			j = 0
			k = 0

			# Terrain opens up as a trade route
			for j in range( gc.getNumTerrainInfos() ):
				if (gc.getTechInfo(i).isTerrainTrade(j) and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isTerrainTrade(j))):
					szTerrainTradeButton = "TerrainTradeButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_WATERTRADE").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
					iButton += 1

			j = gc.getNumTerrainInfos()
			if (gc.getTechInfo(i).isRiverTrade() and not (gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isRiverTrade())):
				szTerrainTradeButton = "TerrainTradeButton" + str( ( i * 1000 ) + j )
				screen.addDDSGFCAt( szTerrainTradeButton, szTechRecord, ArtFileMgr.getInterfaceArtInfo("INTERFACE_TECH_RIVERTRADE").getPath(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TERRAIN_TRADE, i, j, False )
				iButton += 1

			j = 0
			k = 0

			# Special buildings like monestaries...
			for j in range( gc.getNumSpecialBuildingInfos() ):
				if (gc.getSpecialBuildingInfo(j).getTechPrereq() == i):
					szSpecialBuilding = "SpecialBuildingButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szSpecialBuilding, szTechRecord, gc.getSpecialBuildingInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_SPECIAL_BUILDING, i, j, False )
					iButton += 1

			j = 0
			k = 0

			# Yield change
			for j in range( gc.getNumImprovementInfos() ):
				bFound = False

				#FfH: Modified by Kael 01/05/2009
				# for k in range( YieldTypes.NUM_YIELD_TYPES ):
				# 	if (gc.getImprovementInfo(j).getTechYieldChanges(i, k)):
				# 		if ( bFound == False ):
				# 			szYieldChange = "YieldChangeButton" + str( ( i * 1000 ) + j )
				# 			screen.addDDSGFCAt( szYieldChange, szTechRecord, gc.getImprovementInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, i, j, False )
				# 			iButton += 1
				# 			bFound = True
				if not gc.getImprovementInfo(j).isUnique():
					for k in range( YieldTypes.NUM_YIELD_TYPES ):
						if (gc.getImprovementInfo(j).getTechYieldChanges(i, k)):
							if ( bFound == False ):
								szYieldChange = "YieldChangeButton" + str( ( i * 1000 ) + j )
								screen.addDDSGFCAt( szYieldChange, szTechRecord, gc.getImprovementInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_YIELD_CHANGE, i, j, False )
								iButton += 1
								bFound = True
				#FfH: End Modify

			j = 0
			k = 0

			# Bonuses revealed
			for j in range( gc.getNumBonusInfos() ):
				if (gc.getBonusInfo(j).getTechReveal() == i):
					szBonusReveal = "BonusRevealButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szBonusReveal, szTechRecord, gc.getBonusInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_BONUS_REVEAL, i, j, False )
					iButton += 1

			j = 0
			k = 0

			# Civic options
			for j in range( gc.getNumCivicInfos() ):
				if (gc.getCivicInfo(j).getTechPrereq() == i):

					#FfH: Modified by Kael 07/03/2009
					# szCivicReveal = "CivicRevealButton" + str( ( i * 1000 ) + j )
					# screen.addDDSGFCAt( szCivicReveal, szTechRecord, gc.getCivicInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_CIVIC_REVEAL, i, j, False )
					# iButton += 1
					if (gc.getCivicInfo(j).getPrereqCivilization() == -1 or gc.getCivicInfo(j).getPrereqCivilization() == gc.getGame().getActiveCivilizationType()):
						szCivicReveal = "CivicRevealButton" + str( ( i * 1000 ) + j )
						screen.addDDSGFCAt( szCivicReveal, szTechRecord, gc.getCivicInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_CIVIC_REVEAL, i, j, False )
						iButton += 1
					#FfH: End Modify

			j = 0
			k = 0

			# Projects possible
			for j in range( gc.getNumProjectInfos() ):
				if (gc.getProjectInfo(j).getTechPrereq() == i):

					#FfH: Modified by Kael 10/01/2008
					# szProjectInfo = "ProjectInfoButton" + str( ( i * 1000 ) + j )
					# screen.addDDSGFCAt( szProjectInfo, szTechRecord, gc.getProjectInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
					# iButton += 1
					if (gc.getProjectInfo(j).getNumPrereqCivilizations() == 0):
						szProjectInfo = "ProjectInfoButton" + str( ( i * 1000 ) + j )
						screen.addDDSGFCAt( szProjectInfo, szTechRecord, gc.getProjectInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
						iButton += 1
					if (gc.getProjectInfo(j).getNumPrereqCivilizations() > 0):
						for i in range( gc.getProjectInfo(j).getNumPrereqCivilizations() ):
							if (gc.getProjectInfo(j).getPrereqCivilization(i) == gc.getGame().getActiveCivilizationType()):
								szProjectInfo = "ProjectInfoButton" + str( ( i * 1000 ) + j )
								screen.addDDSGFCAt( szProjectInfo, szTechRecord, gc.getProjectInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
								iButton += 1
					#FfH: End Modify

			j = 0
			k = 0

			# Processes possible
			for j in range( gc.getNumProcessInfos() ):
				if (gc.getProcessInfo(j).getTechPrereq() == i):
					szProcessInfo = "ProcessInfoButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szProcessInfo, szTechRecord, gc.getProcessInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_PROCESS_INFO, i, j, False )
					iButton += 1

			j = 0
			k = 0

			# Religions unlocked
			for j in range( gc.getNumReligionInfos() ):
				if ( gc.getReligionInfo(j).getTechPrereq() == i ):
					szFoundReligion = "FoundReligionButton" + str( ( i * 1000 ) + j )
					if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
						szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_POPUPBUTTON_RELIGION").getPath()
					else:
						szButton = gc.getReligionInfo(j).getButton()
					screen.addDDSGFCAt( szFoundReligion, szTechRecord, szButton, iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_RELIGION, i, j, False )
					iButton += 1


			for j in range( gc.getNumCorporationInfos() ):
				if ( gc.getCorporationInfo(j).getTechPrereq() == i ):
					szFoundCorporation = "FoundCorporationButton" + str( ( i * 1000 ) + j )
					screen.addDDSGFCAt( szFoundCorporation, szTechRecord, gc.getCorporationInfo(j).getButton(), iX + X_START + (iButton % NUM_SECONDARY_BUTTONS_IN_ROW) * X_INCREMENT, iY + 4 + ( ( iButton / NUM_SECONDARY_BUTTONS_IN_ROW ) + 1 ) * Y_INCREMENT, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_FOUND_CORPORATION, i, j, False )
					iButton += 1

			screen.show( szTechRecord )


		screen.attachPanelAt("TechList", "TiersTopPanel", u"", u"", True, True, PanelStyles.PANEL_STYLE_TOPBAR, 0, 0, iMaxX, 55, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		lTiers = [1, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 7.5, 8]

		for i in xrange(len(lTiers)):
			szTierName = "TableHeaderTop" + str(i)
			szText = "Tier " + str(lTiers[i])
			screen.setLabelAt( szTierName, "TiersTopPanel", u"<font=4>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, ( i + 1 ) * ( BOX_INCREMENT_WIDTH + BOX_INCREMENT_X_SPACING ) * PIXEL_INCREMENT - ( ( BOX_INCREMENT_WIDTH + BOX_INCREMENT_X_SPACING ) * PIXEL_INCREMENT ) / 2 + 8, 8, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		screen.setViewMin( "TechList", iMaxX + 20, iMaxY + 20 )
		screen.show( "TechList" )
		screen.setFocus( "TechList" )


	# Will update the tech records based on color, researching, researched, queued, etc.
	def updateTechRecords (self, bForce):

		# If we are the Pitboss, we don't want to put up an interface at all
		if ( CyGame().isPitbossHost() ):
			return

		# Get a list of techs that are required for the Civ's Unique Spell, Unique starting techs
		lUniqueTech = self.getUniqueTech()

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		abChanged = []
		bAnyChanged = 0

		# Go through all the techs
		for i in range(gc.getNumTechInfos()):
			abChanged.append(0)
			if (self.stopDisplayTech(i)): continue

			if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ) and i in lUniqueTech:
				if ( self.aiCurrentState[i] != CIV_HAS_UNIQUE_TECH ):
					self.aiCurrentState[i] = CIV_HAS_UNIQUE_TECH
					abChanged[i] = 1
					bAnyChanged = 1
			elif ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
				if ( self.aiCurrentState[i] != CIV_HAS_TECH ):
					self.aiCurrentState[i] = CIV_HAS_TECH
					abChanged[i] = 1
					bAnyChanged = 1
			elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
				if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
					self.aiCurrentState[i] = CIV_IS_RESEARCHING
					abChanged[i] = 1
					bAnyChanged = 1
			elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
				if ( self.aiCurrentState[i] != CIV_IS_RESEARCHING ):
					self.aiCurrentState[i] = CIV_IS_RESEARCHING
					abChanged[i] = 1
					bAnyChanged = 1
			elif i in lUniqueTech :
				if ( self.aiCurrentState[i] != CIV_UNIQUE_TECH ):
					self.aiCurrentState[i] = CIV_UNIQUE_TECH
					abChanged[i] = 1
					bAnyChanged = 1
			elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
				if ( self.aiCurrentState[i] != CIV_NO_RESEARCH ):
					self.aiCurrentState[i] = CIV_NO_RESEARCH
					abChanged[i] = 1
					bAnyChanged = 1
			else:
				if ( self.aiCurrentState[i] != CIV_TECH_AVAILABLE ):
					self.aiCurrentState[i] = CIV_TECH_AVAILABLE
					abChanged[i] = 1
					bAnyChanged = 1

		for i in range(gc.getNumTechInfos()):
			if (self.stopDisplayTech(i)): continue
			if (abChanged[i] or bForce or (bAnyChanged and gc.getPlayer(self.iCivSelected).isResearchingTech(i))):
				# Create and place a tech in its proper location
				szTechRecord = "TechRecord" + str(i)
				szTechID = "TechID" + str(i)
				szTechString = "<font=1>"

				if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
					szTechString = szTechString + unicode(gc.getPlayer(self.iCivSelected).getQueuePosition(i)) + ". "

				iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT ) )
				iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT ) + 5

				szTechString += gc.getTechInfo(i).getDescription()
				if ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
					szTechString += " ("
					szTechString += str(gc.getPlayer(self.iCivSelected).getResearchTurnsLeft(i, ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i )))
					szTechString += ")"
				szTechString = szTechString + "</font>"
				screen.setTextAt( szTechID, "TechList", szTechString, CvUtil.FONT_LEFT_JUSTIFY, iX + 6 + X_INCREMENT, iY + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_TECH_TREE, i, -1 )
				screen.setActivation( szTechID, ActivationTypes.ACTIVATE_MIMICPARENTFOCUS )

				if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ) and i in lUniqueTech:
					screen.setPanelColor(szTechRecord, 175, 145, 70)
				elif ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):
					screen.setPanelColor(szTechRecord, 85, 150, 87)
				elif ( gc.getPlayer(self.iCivSelected).getCurrentResearch() == i ):
					screen.setPanelColor(szTechRecord, 104, 158, 165)
				elif ( gc.getPlayer(self.iCivSelected).isResearchingTech(i) ):
					screen.setPanelColor(szTechRecord, 104, 158, 165)
				elif i in lUniqueTech :
					screen.setPanelColor(szTechRecord, 154, 78, 174)
				elif ( gc.getPlayer(self.iCivSelected).canEverResearch(i) ):
					screen.setPanelColor(szTechRecord, 100, 104, 160)
				else:
					screen.setPanelColor(szTechRecord, 206, 65, 69)

	# Will draw the arrows
	def drawArrows (self):

		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		iLoop = 0
		self.nWidgetCount = 0

		ARROW_X = ArtFileMgr.getInterfaceArtInfo("ARROW_X").getPath()
		ARROW_Y = ArtFileMgr.getInterfaceArtInfo("ARROW_Y").getPath()
		ARROW_MXMY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXMY").getPath()
		ARROW_XY = ArtFileMgr.getInterfaceArtInfo("ARROW_XY").getPath()
		ARROW_MXY = ArtFileMgr.getInterfaceArtInfo("ARROW_MXY").getPath()
		ARROW_XMY = ArtFileMgr.getInterfaceArtInfo("ARROW_XMY").getPath()
		ARROW_HEAD = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD").getPath()
		ARROW_HEAD_UP = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD_UP").getPath()
		ARROW_HEAD_DN = ArtFileMgr.getInterfaceArtInfo("ARROW_HEAD_DN").getPath()

		for i in range(gc.getNumTechInfos()):
			if (self.stopDisplayTech(i)): continue
			bFirst = 1

			fX = (BOX_INCREMENT_WIDTH * PIXEL_INCREMENT) - 8

			for j in range( gc.getNUM_AND_TECH_PREREQS() ):

				eTech = gc.getTechInfo(i).getPrereqAndTechs(j)

				if ( eTech > -1  and not self.stopDisplayTech(eTech) ):

					fX = fX - X_INCREMENT

					iX = 30 + ( (gc.getTechInfo(i).getGridX() - 1) * ( ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT ) )
					iY = ( gc.getTechInfo(i).getGridY() - 1 ) * ( BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT ) + 5

					szTechPrereqID = "TechPrereqID" + str((i * 1000) + j)
					screen.addDDSGFCAt( szTechPrereqID, "TechList", gc.getTechInfo(eTech).getButton(), iX + fX, iY + 4, TEXTURE_SIZE, TEXTURE_SIZE, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

					#szTechPrereqBorderID = "TechPrereqBorderID" + str((i * 1000) + j)
					#screen.addDDSGFCAt( szTechPrereqBorderID, "TechList", ArtFileMgr.getInterfaceArtInfo("TECH_TREE_BUTTON_BORDER").getPath(), iX + fX + 4, iY + 22, 32, 32, WidgetTypes.WIDGET_HELP_TECH_PREPREQ, eTech, -1, False )

			j = 0

			for j in range( gc.getNUM_OR_TECH_PREREQS() ):

				eTech = gc.getTechInfo(i).getPrereqOrTechs(j)

				if ( eTech > -1 and not self.stopDisplayTech(eTech) ):

					# iX is left of tech box
					iX = 24 + ( (gc.getTechInfo(eTech).getGridX() - 1) * ( ( BOX_INCREMENT_X_SPACING + BOX_INCREMENT_WIDTH ) * PIXEL_INCREMENT ) )
					# iY is top of tech box
					iY = ( gc.getTechInfo(eTech).getGridY() - 1 ) * ( BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT ) + 5
					# dY is Y spacing between boxes
					dY = BOX_INCREMENT_Y_SPACING * PIXEL_INCREMENT
					# bY is the vertical size of the tech box
					bY = dY + 18

					# j is the pre-req, i is the tech...
					xDiff = gc.getTechInfo(i).getGridX() - gc.getTechInfo(eTech).getGridX()
					yDiff = gc.getTechInfo(i).getGridY() - gc.getTechInfo(eTech).getGridY()

					# screen.addDDSGFCAt(	self.getNextWidgetName(), "TechList", 'ui element', 		'x start position (left edge of icon)',						'y start position (top edge of icon)', 					'x width', 						'y height',						WidgetTypes.WIDGET_GENERAL, -1, -1, False)
					if (yDiff == 0):
						screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, 				iX + self.getXStart(), 										iY + self.getYStart(3), 								self.getWidth(xDiff), 			8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, 			iX + self.getXStart() + self.getWidth(xDiff), 				iY + self.getYStart(3), 								8, 								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					elif (yDiff < 0):
						if (xDiff == 0):
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, 			iX + self.getXStart()/2 - 4, 								iY + dY * yDiff + bY + 16,								8, 								-dY * yDiff - bY - 14,	 		WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD_UP,	iX + self.getXStart()/2 - 4,								iY + dY * yDiff + bY + 8,								8, 								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						else:
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, 			iX + self.getXStart(), 										iY + self.getYStart(1), 								self.getWidth(xDiff) / 2, 		8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XY, 		iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), 		iY + self.getYStart(1), 								8, 								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, 			iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), 		iY + self.getYStart(1) + 8 - self.getHeight(yDiff, 3), 	8, 								self.getHeight(yDiff, 3) - 8, 	WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_XMY, 		iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ), 		iY + self.getYStart(1) - self.getHeight(yDiff, 3), 		8, 								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X, 			iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ), 	iY + self.getYStart(1) - self.getHeight(yDiff, 3), 		( self.getWidth(xDiff) / 2 )-4,	8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD, 		iX + self.getXStart() + self.getWidth(xDiff), 				iY + self.getYStart(1) - self.getHeight(yDiff, 3), 		8, 								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
					elif (yDiff > 0):
						if (xDiff == 0):
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y, 			iX + self.getXStart()/2 - 4, 								iY + bY + 8,		 									8, 								dY * yDiff - bY - 12, 			WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD_DN, 	iX + self.getXStart()/2 - 4,								iY + dY * yDiff - 4,									8, 								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
						else:
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X,			iX + self.getXStart(),										iY + self.getYStart(5),									self.getWidth(xDiff) / 2,		8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXMY,		iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ),		iY + self.getYStart(5),									8,								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_Y,			iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ),		iY + self.getYStart(5) + 8,								8,								self.getHeight(yDiff, 3) - 8, 	WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_MXY,		iX + self.getXStart() + ( self.getWidth(xDiff) / 2 ),		iY + self.getYStart(5) + self.getHeight(yDiff, 3),		8,								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_X,			iX + 8 + self.getXStart() + ( self.getWidth(xDiff) / 2 ),	iY + self.getYStart(5) + self.getHeight(yDiff, 3),		( self.getWidth(xDiff) / 2 )-4,	8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )
							screen.addDDSGFCAt( self.getNextWidgetName(), "TechList", ARROW_HEAD,		iX + self.getXStart() + self.getWidth(xDiff),				iY + self.getYStart(5) + self.getHeight(yDiff, 3),		8,								8, 								WidgetTypes.WIDGET_GENERAL, -1, -1, False )

		return

	def TechRecord (self, inputClass):
		return 0

	# Clicked the parent?
	def ParentClick (self, inputClass):
		return 0

	def CivDropDown( self, inputClass ):

		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )
			iIndex = screen.getSelectedPullDownID("CivDropDown")
			self.iCivSelected = screen.getPullDownData("CivDropDown", iIndex)
			self.updateTechRecords(false)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		# Advanced Start Stuff

		pPlayer = gc.getPlayer(self.iCivSelected)
		if (pPlayer.getAdvancedStartPoints() >= 0):

			# Add tech button
			if (inputClass.getFunctionName() == "AddTechButton"):
				if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, true) != -1):
					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_TECH, self.iCivSelected, -1, -1, self.m_iSelectedTech, true)	#Action, Player, X, Y, Data, bAdd
					self.m_bTechRecordsDirty = true
					self.m_bSelectedTechDirty = true

			# Tech clicked on
			elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
				if (inputClass.getButtonType() == WidgetTypes.WIDGET_TECH_TREE):
					self.m_iSelectedTech = inputClass.getData1()
					self.updateSelectedTech()

		' Calls function mapped in TechChooserInputMap'
		# only get from the map if it has the key
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED ):
			self.CivDropDown( inputClass )
			return 1
		return 0

	def getNextWidgetName(self):
		szName = "TechArrow" + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def getXStart(self):
		return ( BOX_INCREMENT_WIDTH * PIXEL_INCREMENT )

	def getXSpacing(self):
		return ( BOX_INCREMENT_X_SPACING * PIXEL_INCREMENT )

	def getYStart(self, iY):
		""" '3' is box vertical center, lower iY -> starting higher on box"""
		return int((((BOX_INCREMENT_HEIGHT * PIXEL_INCREMENT ) / 6.0) * iY) - PIXEL_INCREMENT )

	def getWidth(self, xDiff):
		return ( ( xDiff * self.getXSpacing() ) + ( ( xDiff - 1 ) * self.getXStart() ) )

	def getHeight(self, yDiff, nFactor):
		return ( ( nFactor + ( ( abs( yDiff ) - 1 ) * BOX_INCREMENT_Y_SPACING ) ) * PIXEL_INCREMENT )

	def getUniqueTech(self):
		iPlayer = CyGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)
		iLeader = pPlayer.getLeaderType()
		iCivilization = pPlayer.getCivilizationType()
		pCapital = pPlayer.getCapitalCity()

		# Tech blocked by civ prereq
		lUniqueTech = [gc.getInfoTypeForString('TECH_SEAFARING'), gc.getInfoTypeForString('TECH_STEAM_POWER'), gc.getInfoTypeForString('TECH_SWAMPDWELLING'), gc.getInfoTypeForString('TECH_THE_GIFT'), gc.getInfoTypeForString('TECH_JO1'), gc.getInfoTypeForString('TECH_DESERTPEOPLE'), gc.getInfoTypeForString('TECH_DARK_SECRETS')]

		# Global Spells Tech
		for iSpell in xrange (gc.getNumSpellInfos()):
			if gc.getSpellInfo(iSpell).isGlobal() and (gc.getSpellInfo(iSpell).getCivilizationPrereq() == -1 or gc.getSpellInfo(iSpell).getCivilizationPrereq() == iCivilization):
				iSpellPrereq = gc.getSpellInfo(iSpell).getTechPrereq()
				if iSpellPrereq != -1:
					lUniqueTech.append(iSpellPrereq)

		# Heroes Tech
		iHeroClass = CvEventInterface.getEventManager().cf.getHero(pPlayer)
		if iHeroClass != - 1:
			iHero = gc.getCivilizationInfo(iCivilization).getCivilizationUnits(iHeroClass)
			iHeroPrereq = gc.getUnitInfo(iHero).getPrereqAndTech()
			if iHeroPrereq != -1:
				lUniqueTech.append(iHeroPrereq)

		return lUniqueTech

	def update(self, fDelta):

		if (CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT)):
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, false)

			if (self.m_bSelectedTechDirty):
				self.m_bSelectedTechDirty = false
				self.updateSelectedTech()

			if (self.m_bTechRecordsDirty):
				self.m_bTechRecordsDirty = false
				self.updateTechRecords(true)

			if (gc.getPlayer(self.iCivSelected).getAdvancedStartPoints() < 0):
				# hide the screen
				screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )
				screen.hide("AddTechButton")
				screen.hide("ASPointsLabel")
				screen.hide("SelectedTechLabel")

		return

	def updateSelectedTech(self):
		pPlayer = gc.getPlayer(CyGame().getActivePlayer())

		# Get the screen
		screen = CyGInterfaceScreen( "TechChooser", CvScreenEnums.TECH_CHOOSER )

		szName = ""
		iCost = 0

		if (self.m_iSelectedTech != -1):
			szName = gc.getTechInfo(self.m_iSelectedTech).getDescription()
			iCost = gc.getPlayer(CyGame().getActivePlayer()).getAdvancedStartTechCost(self.m_iSelectedTech, true)

		if iCost > 0:
			szText = u"<font=4>" + localText.getText("TXT_KEY_WB_AS_SELECTED_TECH_COST", (iCost, pPlayer.getAdvancedStartPoints())) + u"</font>"
			screen.setLabel( "ASPointsLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		else:
			screen.hide("ASPointsLabel")

		szText = u"<font=4>"
		szText += localText.getText("TXT_KEY_WB_AS_SELECTED_TECH", (szName,))
		szText += u"</font>"
		screen.setLabel( "SelectedTechLabel", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, self.X_ADVANCED_START_TEXT + 250, self.Y_ADD_TECH_BUTTON + 3, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		# Want to add
		if (pPlayer.getAdvancedStartTechCost(self.m_iSelectedTech, true) != -1):
			screen.show("AddTechButton")
		else:
			screen.hide("AddTechButton")

	def onClose(self):
		pPlayer = gc.getPlayer(self.iCivSelected)
		if (pPlayer.getAdvancedStartPoints() >= 0):
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, true)
		return 0

class TechChooserMaps:

	TechChooserInputMap = {
		'TechRecord'			: CvTechChooser().TechRecord,
		'TechID'				: CvTechChooser().ParentClick,
		'TechPane'				: CvTechChooser().ParentClick,
		'TechButtonID'			: CvTechChooser().ParentClick,
		'TechButtonBorder'		: CvTechChooser().ParentClick,
		'Unit'					: CvTechChooser().ParentClick,
		'Building'				: CvTechChooser().ParentClick,
		'Obsolete'				: CvTechChooser().ParentClick,
		'ObsoleteX'				: CvTechChooser().ParentClick,
		'Move'					: CvTechChooser().ParentClick,
		'FreeUnit'				: CvTechChooser().ParentClick,
		'FeatureProduction'		: CvTechChooser().ParentClick,
		'Worker'				: CvTechChooser().ParentClick,
		'TradeRoutes'			: CvTechChooser().ParentClick,
		'HealthRate'			: CvTechChooser().ParentClick,
		'HappinessRate'			: CvTechChooser().ParentClick,
		'FreeTech'				: CvTechChooser().ParentClick,
		'LOS'					: CvTechChooser().ParentClick,
		'MapCenter'				: CvTechChooser().ParentClick,
		'MapReveal'				: CvTechChooser().ParentClick,
		'MapTrade'				: CvTechChooser().ParentClick,
		'TechTrade'				: CvTechChooser().ParentClick,
		'OpenBorders'			: CvTechChooser().ParentClick,
		'BuildBridge'			: CvTechChooser().ParentClick,
		'Irrigation'			: CvTechChooser().ParentClick,
		'Improvement'			: CvTechChooser().ParentClick,
		'DomainExtraMoves'		: CvTechChooser().ParentClick,
		'AdjustButton'			: CvTechChooser().ParentClick,
		'TerrainTradeButton'	: CvTechChooser().ParentClick,
		'SpecialBuildingButton'	: CvTechChooser().ParentClick,
		'YieldChangeButton'		: CvTechChooser().ParentClick,
		'BonusRevealButton'		: CvTechChooser().ParentClick,
		'CivicRevealButton'		: CvTechChooser().ParentClick,
		'ProjectInfoButton'		: CvTechChooser().ParentClick,
		'ProcessInfoButton'		: CvTechChooser().ParentClick,
		'FoundReligionButton'	: CvTechChooser().ParentClick,
		'CivDropDown'			: CvTechChooser().CivDropDown,
		}

