## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# part of Unit Statistics Mod
#  by
# Teg_Navanis
# based on CvMercenaryManager.py, part of Mercenaries Mod by TheLopez



import ScreenInput
import CvScreenEnums
import ScreenInput
import UnitStatisticsTools
from CvStatisticsScreensEnums import *
from UnitStatisticsDefines import *


# globals

objUnitStatisticsTools = UnitStatisticsTools.UnitStatisticsTools()



class CvStatisticsScreen:

	def __init__(self):

		self.WIDGET_ID = "UnitStatsWidget"
		self.screenWidgetData = {}
		self.nWidgetCount = 0
		self.Z_BACKGROUND = -2.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.currentScreen = UNIT_STATISTICS
		self.currentHighScore = "BodyCount"
		self.EventKeyDown=6
		self.currentUnit=0


	# This function is called from 'outside', namely from the event manager.
	# strScreen is the argument that defines which screen is to be shown first
	def startScreen(self, objUnit, strScreen):
		self.currentUnit = objUnit
		iPlayer = gc.getGame().getActivePlayer()

		if (strScreen == "unit"):
			self.currentScreen = UNIT_STATISTICS
		if (strScreen == "player"):
			self.currentScreen = PLAYER_STATISTICS
		if (strScreen == "highscores"):
			self.currentScreen = HIGHSCORES
		if (strScreen == "graveyard"):
			self.currentScreen = GRAVEYARD

		self.interfaceScreen(iPlayer)


	"Statistics Screen"
	def interfaceScreen(self, iPlayer):

		screen = self.getScreen()

		# Get the screen height, width etc.
		self.calculateScreenWidgetData(screen)

		objUnit = self.currentUnit

		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)


		# draws the top and bottom panel of the screen
		self.drawScreenTop(screen)
		self.drawScreenBottom(screen)

		# Draws the main part of the screen (depending on which screen is to be drawn)
		if(self.currentScreen == UNIT_STATISTICS):
			if (objUnit != None):
				self.drawUnitScreen(screen, objUnit)
			else:
				self.drawPlayerScreen(screen)
		elif(self.currentScreen == PLAYER_STATISTICS):
			self.drawPlayerScreen(screen, iPlayer)
		elif(self.currentScreen == HIGHSCORES or self.currentScreen == CURRHIGHSCORES):
			self.drawHighScoresScreen(screen, "highscore")
		elif(self.currentScreen == GRAVEYARD):
			self.drawGraveYardScreen(screen)
		elif(self.currentScreen == HALLOFFAME):
			self.drawHighScoresScreen(screen, "halloffame")
		elif(self.currentScreen == TOP10 or self.currentScreen == "TOPLISTA"):
			self.drawHighScoresScreen(screen, "top10")


	# Returns the instance of the unit statistics screen.
	def getScreen(self):
		if (self.currentScreen == HIGHSCORES or self.currentScreen == CURRHIGHSCORES):
			return CyGInterfaceScreen("HighScoresScreen", CvScreenEnums.HIGHSCORES_SCREEN)
		elif (self.currentScreen == UNIT_STATISTICS):
			return CyGInterfaceScreen("UnitStatisticsScreen", CvScreenEnums.UNITSTATS_SCREEN)
		elif (self.currentScreen == PLAYER_STATISTICS):
			return CyGInterfaceScreen("PlayerStatisticsScreen", CvScreenEnums.PLAYERSTATS_SCREEN)
		elif (self.currentScreen == GRAVEYARD):
			return CyGInterfaceScreen("GraveYardScreen", CvScreenEnums.GRAVEYARD_SCREEN)
		elif (self.currentScreen == HALLOFFAME):
			return CyGInterfaceScreen("HallOfFameScreen", CvScreenEnums.HALLOFFAME_SCREEN)
		elif (self.currentScreen == TOP10):
			return CyGInterfaceScreen("Top10Screen1", CvScreenEnums.TOP10_SCREEN1)
		elif (self.currentScreen == "TOPLISTA"):
			return CyGInterfaceScreen("Top10Screen2", CvScreenEnums.TOP10_SCREEN2)
		else:
			return False

	def drawUnitScreen(self, screen, objUnit):

		# Create an empty data sheet for the unit
		# if for some reason we haven't been logging it
		if(sdObjectExists("UnitStats", objUnit) == False):
			objUnitStatisticsTools.setupUnitStats(objUnit)

		# Defines the structure of the screen
		screen.addPanel(UNIT_INFORMATION_PANEL_ID, u"", u"", True, False, self.screenWidgetData[UNIT_INFORMATION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(UNIT_INFORMATION_INNER_PANEL_ID, u"", u"", True, False, self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.addPanel(UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(UNIT_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel(UNIT_INFORMATION_PROMOTION_PANEL_ID, localText.getText("TXT_KEY_WB_PROMOTIONS", ()), u"", True, False, self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addScrollPanel(UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID, u"", self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)

		isDead = 0
		# This test handles all dead units (graveyard)
		try:
			# Build the unit XP string
			strXP = u"%.2f/%.2f" %(objUnit.getExperience(), objUnit.experienceNeeded())
		except:
			isDead = 1


		HSList = objUnitStatisticsTools.getAllHighScores()

		if isDead:
			unittype = sdObjectGetVal("UnitStats", objUnit, UNITTYPE)
			highscoreTitle = localText.getText("TXT_KEY_HALLOFFAME_SMALL", ())
			HSUnitList = objUnitStatisticsTools.getHighScoresCurrentUnit(objUnit, "halloffame")
			promotionList = sdObjectGetVal("UnitStats", objUnit, PROMOTION_LIST)

		else:
			unittype = objUnit.getUnitType()
			highscoreTitle = localText.getText("TXT_KEY_HIGHSCORES_SMALL", ())
			promotionList = []
			for i in range(gc.getNumPromotionInfos()):
				# If the unit has the promotion add it to the promotion list
				if(objUnit.isHasPromotion(i)):
					promotionList.append(i)
			HSUnitList = objUnitStatisticsTools.getHighScoresCurrentUnit(objUnit, "highscore")

		screen.addPanel(UNIT_INFORMATION_HIGHSCORE_PANEL_ID, highscoreTitle, u"", True, False, self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addScrollPanel(UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_ID, u"", self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_HEIGHT] / 2, PanelStyles.PANEL_STYLE_EMPTY)


		screen.addPanel(UNIT_INFORMATION_DETAILS_PANEL_ID, u"", u"", True, False, self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.attachListBoxGFC( UNIT_INFORMATION_DETAILS_PANEL_ID, UNIT_INFORMATION_DETAILS_LIST_ID, "", TableStyles.TABLE_STYLE_EMPTY )
		screen.enableSelect(UNIT_INFORMATION_DETAILS_LIST_ID, False)

		if not isDead:

			# Build the unit stats string
			if (objUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
				fUnitHealth = int(objUnit.airBaseCombatStr()) * float(objUnit.currHitPoints()) / float(objUnit.maxHitPoints())
				fMaxHealth = int(objUnit.airBaseCombatStr())
			else:
				fUnitHealth = int(objUnitStatisticsTools.combatStrFunction(objUnit, true)) * float(objUnit.currHitPoints()) / float(objUnit.maxHitPoints())
				fMaxHealth = int(objUnitStatisticsTools.combatStrFunction(objUnit, true))

			if ( (objUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0 ):
				iDenom = 1
			else:
				iDenom = 0
			iCurrMoves = ((objUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
			TurnsinService = localText.getText("TXT_KEY_TURNS_IN_SERVICE", ()) + " " + str(gc.getGame().getGameTurn() - sdObjectGetVal("UnitStats", objUnit, "StartTurn"))
			strStats = u"%.2f/%.2f%c    %d/%d%c" %(fUnitHealth, fMaxHealth, CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR),iCurrMoves, objUnit.baseMoves(),CyGame().getSymbolID(FontSymbols.MOVES_CHAR))

			# Show the unit information (Unit Type, Level, Health, Turns in service)
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, objUnit.getNameNoDesc(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, localText.getText("TXT_KEY_UNITSTATS_UNITTYPE", ()) + " " + PyInfo.UnitInfo(objUnit.getUnitType()).getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, localText.getText("INTERFACE_PANE_LEVEL", ()) + " " + str(objUnit.getLevel()) + "     XP: " + strXP, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "" + strStats + "\n", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, TurnsinService, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			screen.appendListBoxString( UNIT_INFORMATION_DETAILS_LIST_ID, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		else:
			screen.addMultilineText(UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_ID, "<font=4>" +localText.getText("TXT_KEY_UNITSTATS_DEAD", ()) + "</font>", self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X] + 8, self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y] + 82, self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH] - 8, 40, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)


		position = 0
		for i in promotionList:
			Promotion = gc.getPromotionInfo(i)
			screen.setImageButtonAt("Promotion" + str(i), UNIT_INFORMATION_INNER_PROMOTION_PANEL_ID, Promotion.getButton(), (position % 6) * 64, (position / 6) * 64, 64, 64, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, gc.getInfoTypeForString(Promotion.getType()), -1)
			position += 1

		# Add all of the high scores the unit has.

		for HighScore in HSUnitList:
			index = HSUnitList.index(HighScore)
			screen.setImageButtonAt(HighScore + "_HSBox"  + str(HSList.index(HighScore)), UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_ID, "Art/Interface/Buttons/HighScores/" + g_strAlternativeButtons+ HighScore +".dds", (index % 6) * 64, (index / 6) * 64, 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.addUnitGraphicGFC(UNIT_GRAPHIC, unittype, self.screenWidgetData[UNIT_ANIMATION_X], self.screenWidgetData[UNIT_ANIMATION_Y], self.screenWidgetData[UNIT_ANIMATION_WIDTH], self.screenWidgetData[UNIT_ANIMATION_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1, self.screenWidgetData[UNIT_ANIMATION_ROTATION_X], self.screenWidgetData[UNIT_ANIMATION_ROTATION_Z], self.screenWidgetData[UNIT_ANIMATION_SCALE], True)
		screen.attachMultilineText(UNIT_INFORMATION_INNER_PANEL_ID, "Stats", objUnitStatisticsTools.getUnitStatisticsString(objUnit), WidgetTypes.WIDGET_GENERAL, -1, -1, -1)


	def drawPlayerScreen(self, screen, iPlayer):

		# Defines the structure of the screen
		screen.addPanel(UNIT_INFORMATION_PANEL_ID, u"", u"", True, True, self.screenWidgetData[UNIT_INFORMATION_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(PLAYER_INFORMATION_INNER_PANEL_ID, u"", u"", True, True, self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_X], self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_Y], self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_WIDTH], self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_EMPTY)
		screen.addPanel(UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(UNIT_INFORMATION_TEXT_PANEL_ID, "Background", self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL2], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_X], self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.attachMultilineText(PLAYER_INFORMATION_INNER_PANEL_ID, "Stats", objUnitStatisticsTools.getPlayerStatisticsString(iPlayer), WidgetTypes.WIDGET_GENERAL, -1, -1, -1)

		self.X_LEADERS = 20
		self.Y_LEADERS = 600
		self.W_LEADERS = screen.getXResolution() - 40
		self.H_LEADERS = 90
		self.LEADER_BUTTON_SIZE = 64
		self.LEADER_MARGIN = 12
		self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))

		if (g_bShowAllPlayers and (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer())):

			# Set scrollable area for leaders
			screen.addPanel("LEADER_PANEL_ID", "", "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN)

			listLeaders = []
			for iLoopPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iLoopPlayer)
				if (player.isEverAlive()):
					listLeaders.append(iLoopPlayer)

			iNumLeaders = len(listLeaders)
			if iNumLeaders >= self.LEADER_COLUMNS:
				iButtonSize = self.LEADER_BUTTON_SIZE / 2
			else:
				iButtonSize = self.LEADER_BUTTON_SIZE

			iColumns = int(self.W_LEADERS / (iButtonSize + self.LEADER_MARGIN))

			# loop through all players and display leaderheads
			for iIndex in range(iNumLeaders):
				iLoopPlayer = listLeaders[iIndex]
				player = gc.getPlayer(iLoopPlayer)

				x = self.X_LEADERS + self.LEADER_MARGIN + (iIndex % iColumns) * (iButtonSize + self.LEADER_MARGIN)
				y = self.Y_LEADERS + self.LEADER_MARGIN + (iIndex // iColumns) * (iButtonSize + self.LEADER_MARGIN)

				if iLoopPlayer == gc.getORC_PLAYER():
					szButton = "Art/Interface/Buttons/Civilizations/Orc.dds"
				elif iLoopPlayer == gc.getANIMAL_PLAYER():
					szButton = "Art/Interface/Buttons/Civilizations/Animal.dds"
				elif iLoopPlayer == gc.getDEMON_PLAYER():
					szButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					szButton = gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton()
				screen.addCheckBoxGFC(PLAYER_STATISTICS_NEW_PLAYER_TEXT_PANEL_ID + str(iLoopPlayer), szButton, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setState(PLAYER_STATISTICS_NEW_PLAYER_TEXT_PANEL_ID + str(iLoopPlayer), (iPlayer == iLoopPlayer))


	def drawHighScoresScreen(self, screen, strHSorHOF):


		#Draws the lefthand part of the screen and the bottom of the screen
		self.drawHighScoreList(screen, strHSorHOF)
		self.drawHighScoreBottom(screen)

		# Defines the structure of the screen
		screen.addPanel(HIGHSCORE_PAGE_PANEL_ID, u"", u"", True, False, self.screenWidgetData[HIGHSCORE_PAGE_PANEL_X], self.screenWidgetData[HIGHSCORE_PAGE_PANEL_Y], self.screenWidgetData[HIGHSCORE_PAGE_PANEL_WIDTH], self.screenWidgetData[HIGHSCORE_PAGE_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(HIGHSCORE_PAGE_INNER_PANEL_ID, u"", u"", True, True, self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_X], self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_Y], self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_WIDTH], self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )
		screen.setText(HIGHSCORE_PAGE_TEXT_PANEL_ID, "Background", self.screenWidgetData[HIGHSCORE_PAGE_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[HIGHSCORE_PAGE_TEXT_PANEL_X], self.screenWidgetData[HIGHSCORE_PAGE_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# This draws the righthand part of the screen
		i = 0
		for highscore in objUnitStatisticsTools.getAllHighScores():
			i += 1


			# 1, 3, 5 etc. are shown on the left...
			if (i % 2 != 0):
				screen.attachPanel(HIGHSCORE_PAGE_INNER_PANEL_ID, "highscore" + str(i) + "1", "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				#screen.addPanel("highscore" + str(i) + "1", "", "", False, False, self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_X], self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_Y] + (i // 2) * 72, self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_WIDTH], 72, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachPanel("highscore" + str(i) + "1", highscore, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)

			# ... 2, 4, 6 etc. on the right.
			else:
				screen.attachPanel("highscore" + str(i - 1) + "1", highscore, "", "", False, False, PanelStyles.PANEL_STYLE_DAWN)

			if	(strHSorHOF != "top10"):
				# Adds the button for the highscore
				screen.attachImageButton( highscore, highscore + "_HighScoreButton98",
											"Art/Interface/Buttons/Highscores/"+g_strAlternativeButtons+highscore+".dds", GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
				# disable the button if there is no unit holding that high score
				if (isinstance(objUnitStatisticsTools.getHSUnit(highscore, strHSorHOF), (int))):
					screen.enable(highscore + "_HighScoreButton98", False)

			else:
				# Adds the button for the highscore
				screen.attachCheckBoxGFC( highscore, highscore + "_TopListButton",
											"Art/Interface/Buttons/Highscores/"+g_strAlternativeButtons+highscore+".dds", ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 64, 64, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				screen.setState(highscore + "_TopListButton", self.currentHighScore == highscore)

				# disable the button if there is no unit holding that high score
				if (isinstance(objUnitStatisticsTools.getHSUnit(highscore, strHSorHOF), (int))):
					screen.enable(highscore + "_TopListButton", False)

			# get the string with the current and hall of fame high scores and add it to the screen
			strHighscore = objUnitStatisticsTools.getHSString(highscore, "player")
			screen.attachPanel(highscore, highscore+"Text", "", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
			screen.attachMultilineText(highscore+"Text", highscore+"Text1", strHighscore, WidgetTypes.WIDGET_GENERAL, -1, -1, -1)

	# Draws the lefthand part of the high scores screen
	def drawHighScoreList(self, screen, strHSorHOF):

		if strHSorHOF == "top10":
			htype = self.currentHighScore
			HSUnitList, HSValList = objUnitStatisticsTools.checkTop10(htype, gc.getGame().getActivePlayer())

		else:
			# Get the list of all units with at least one high score
			HSUnitList = objUnitStatisticsTools.getHighScoreUnits(strHSorHOF)

		# Define the height of the lefthand list depending on the number of highscore units
		HEIGHT = min(len(HSUnitList) * 70 + 70, self.screenWidgetData[HIGHSCORE_LIST_PANEL_HEIGHT])
		HEIGHT2 = HEIGHT - (14*self.screenWidgetData[BORDER_WIDTH])

		# Defines the structure of the screen
		screen.addPanel(HIGHSCORE_LIST_PANEL_ID, u"", u"", True, False, self.screenWidgetData[HIGHSCORE_LIST_PANEL_X], self.screenWidgetData[HIGHSCORE_LIST_PANEL_Y], self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH], HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(HIGHSCORE_LIST_INNER_PANEL_ID, u"", u"", True, True, self.screenWidgetData[HIGHSCORE_LIST_INNER_PANEL_X], self.screenWidgetData[HIGHSCORE_LIST_INNER_PANEL_Y], self.screenWidgetData[HIGHSCORE_LIST_INNER_PANEL_WIDTH], HEIGHT2, PanelStyles.PANEL_STYLE_IN)
		screen.addPanel(HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_ID, u"", u"", True, False, self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_X], self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_Y], self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_WIDTH], self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_MAIN )

		if strHSorHOF == "highscore":
			screen.setText(HIGHSCORE_LIST_TEXT_PANEL_ID, "Background", "<font=3b>" + localText.getText("TXT_KEY_HIGHSCORE_UNITS", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_X], self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		elif strHSorHOF == "halloffame":
			screen.setText(HIGHSCORE_LIST_TEXT_PANEL_ID, "Background", "<font=3b>" + localText.getText("TXT_KEY_HALLOFFAME_UNITS", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_X], self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		elif strHSorHOF == "top10":
			screen.setText(HIGHSCORE_LIST_TEXT_PANEL_ID, "Background", "<font=3b>" + localText.getText("TXT_KEY_TOP10_UNITS", ()) + "</font>", CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_X], self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


		if strHSorHOF == "halloffame":
			# Get the list of dead units
			graveyardlist = []
			if ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) and g_bShowAllPlayers):
				for iPlayer in range(gc.getMAX_PLAYERS()):
					if (gc.getPlayer(iPlayer).isEverAlive()):
						newlist = sdObjectGetVal("UnitStats", gc.getPlayer(iPlayer), "GraveYardList")
						if (len(newlist) > 0):
							graveyardlist.extend(newlist)
			else:
				graveyardlist = sdObjectGetVal("UnitStats", gc.getActivePlayer(), "GraveYardList")


		# For each unit with at least one highscore, a little panel is added
		for id in HSUnitList:
			iUnitID, iPlayer, unit = objUnitStatisticsTools.unitIDToObject(id)
			try:
				unittype = unit.getUnitType()
				if unittype == -1:
					unittype = sdObjectGetVal("UnitStats", unit, "UnitType")
			except:
				unittype = sdObjectGetVal("UnitStats", unit, "UnitType")

			UnitID = objUnitStatisticsTools.numberToAlpha(iUnitID)+ "-" + objUnitStatisticsTools.numberToAlpha(iPlayer)
			screen.attachPanel(HIGHSCORE_LIST_INNER_PANEL_ID, UnitID, u"", u"", False, False, PanelStyles.PANEL_STYLE_DAWN)

			# Adds a button to the unit's panel
			screen.attachImageButton(UnitID, UnitID + "_UnitButton98",
										gc.getUnitInfo(unittype).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_GENERAL, -1, -1, False )


			# Some structural panels to make it look right
			if strHSorHOF != "top10":
				screen.attachPanel(UnitID, UnitID+"RightPanel", "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachPanel(UnitID+"RightPanel", UnitID+"Buttons","", "", True, False, PanelStyles.PANEL_STYLE_EMPTY)
			else:
				if (not isinstance(HSValList[HSUnitList.index(id)], (int))):
					valstring = "%.2f" %(HSValList[HSUnitList.index(id)])
					if (htype == LIFEODDS or htype == AVERAGEODDSLOWEST or htype == AVERAGEODDSHIGHEST or htype == BESTODDS):
						valstring = valstring + "%"
				else:
					valstring = str(HSValList[HSUnitList.index(id)])
				screen.attachPanel(UnitID, UnitID+"RightPanel", " ", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachPanel(UnitID+"RightPanel", UnitID+"Buttons", valstring, "", True, False, PanelStyles.PANEL_STYLE_EMPTY)

			# Add a 'find' button. Clicking on it closes the screen and selects the unit (see handleinput if you want to change this)
			screen.attachImageButton( UnitID, UnitID+"_FindButton99",
										"Art/Interface/Buttons/Actions/Wake.dds", GenericButtonSizes.BUTTON_SIZE_32, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, False )



			if strHSorHOF != "top10":
				# Add all of the high scores the unit has.
				HSList = objUnitStatisticsTools.getAllHighScores()
				highscoreList = objUnitStatisticsTools.getHighScoresCurrentUnit(unit, strHSorHOF)
				for highscore in highscoreList:
					index = highscoreList.index(highscore)
					screen.setImageButtonAt(UnitID + "_HSButton"  + str(HSList.index(highscore)), UnitID+"Buttons", "Art/Interface/Buttons/HighScores/" +g_strAlternativeButtons+ highscore +".dds", (index % 5) * 24, (index / 5) * 24, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1)
					if (iPlayer != gc.getGame().getActivePlayer() and not g_bShowAllPlayers):
						screen.enable(UnitID + "_HSButton"  + str(HSList.index(highscore)), False)


			if (iPlayer != gc.getGame().getActivePlayer() and not g_bShowAllPlayers):
				screen.enable(UnitID + "_UnitButton98", False)
				screen.enable(UnitID + "_FindButton99", False)


			# If the unit is dead, disable the FindButton
			try:
				unit.getExperience()
			except:
				screen.enable(UnitID + "_FindButton99", False)

		self.drawMiniMap(screen, strHSorHOF)


	# Draws the minimap for the "High Scores" screen
	def drawMiniMap(self, screen, strHSorHOF):


		# Get the list of all units with at least one high score
		if strHSorHOF == "highscore" or strHSorHOF == "halloffame":
			HSUnitList = objUnitStatisticsTools.getHighScoreUnits("highscore")
		elif strHSorHOF == "top10":
			HSUnitList, HSValList = objUnitStatisticsTools.checkTop10(self.currentHighScore, gc.getGame().getActivePlayer())

		# Create a minimap
		screen.addPanel("MiniMapPanel", u"", "", False, False, self.screenWidgetData[MINIMAP_X], self.screenWidgetData[MINIMAP_Y], self.screenWidgetData[MINIMAP_WIDTH], self.screenWidgetData[MINIMAP_HEIGHT], PanelStyles.PANEL_STYLE_MAIN)
		screen.initMinimap(self.screenWidgetData[MINIMAP_X] + self.screenWidgetData[MINIMAP_BORDER], self.screenWidgetData[MINIMAP_X] + self.screenWidgetData[MINIMAP_WIDTH] - self.screenWidgetData[MINIMAP_BORDER], self.screenWidgetData[MINIMAP_Y] + self.screenWidgetData[MINIMAP_BORDER], self.screenWidgetData[MINIMAP_Y] + self.screenWidgetData[MINIMAP_HEIGHT] - self.screenWidgetData[MINIMAP_BORDER], self.Z_CONTROLS)
		screen.updateMinimapSection(False, False)

		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_MILITARY, 0.3)

		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)
		screen.bringMinimapToFront()
		screen.updateMinimapVisibility()




		# Show all high score units on the minimap
		for id in HSUnitList:
			iUnitID, iPlayer, loopUnit = objUnitStatisticsTools.unitIDToObject(id)
			if (iPlayer != gc.getGame().getActivePlayer() and not g_bShowAllPlayers):
				continue
			else:
				player = PyPlayer(iPlayer)
				iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()
				screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, loopUnit.getX(), loopUnit.getY(), iColor, 0.6)

	# Draws the bottom bar of the "High Score" screen
	def drawHighScoreBottom(self, screen):
		screen.addPanel(HSBOTTOM_PANEL_ID, u"", u"", True, True, self.screenWidgetData[HSBOTTOM_PANEL_X], self.screenWidgetData[HSBOTTOM_PANEL_Y], self.screenWidgetData[HSBOTTOM_PANEL_WIDTH], self.screenWidgetData[HSBOTTOM_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_BOTTOMBAR)

		szText1 = self.screenWidgetData[TOP10_TEXT_PANEL]
		szText2 = self.screenWidgetData[HALLOFFAME_TEXT_PANEL]
		szText3 = self.screenWidgetData[CURRHIGHSCORES_TEXT_PANEL]

		color2 = gc.getInfoTypeForString("COLOR_PLAYER_PURPLE")

		if (self.currentScreen == TOP10 or self.currentScreen == "TOPLISTA" ):
			szText1 = localText.changeTextColor(szText1, color2)
		elif (self.currentScreen == HALLOFFAME):
			szText2 = localText.changeTextColor(szText2, color2)
		elif (self.currentScreen == CURRHIGHSCORES or self.currentScreen == HIGHSCORES):
			szText3 = localText.changeTextColor(szText3, color2)

		screen.setText(HALLOFFAME_TEXT_PANEL_ID, "Background", szText2, CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[HALLOFFAME_TEXT_PANEL_X], self.screenWidgetData[HALLOFFAME_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(CURRHIGHSCORES_TEXT_PANEL_ID, "Background", szText3, CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[CURRHIGHSCORES_TEXT_PANEL_X], self.screenWidgetData[CURRHIGHSCORES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(TOP10_TEXT_PANEL_ID, "Background", szText1, CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[TOP10_TEXT_PANEL_X], self.screenWidgetData[TOP10_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide(BOTTOM_PANEL_ID)
		screen.moveToFront(UNIT_STATISTICS_TEXT_PANEL_ID)
		screen.moveToFront(HIGHSCORES_TEXT_PANEL_ID)
		screen.moveToFront(PLAYER_STATISTICS_TEXT_PANEL_ID)
		screen.moveToFront(EXIT_TEXT_PANEL_ID)

	# Draws the top bar of the "Unit Statistics" screens
	def drawScreenTop(self, screen):
		screen.setDimensions(0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT])
		screen.addDrawControl(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_OPAQUE").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC(BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.screenWidgetData[SCREEN_WIDTH], self.screenWidgetData[SCREEN_HEIGHT], WidgetTypes.WIDGET_GENERAL, -1, -1 )

		screen.addPanel(SCREEN_TITLE_PANEL_ID, u"", u"", True, False, self.screenWidgetData[SCREEN_TITLE_PANEL_X], self.screenWidgetData[SCREEN_TITLE_PANEL_Y], self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH], self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_TOPBAR )
		screen.setText(SCREEN_TITLE_TEXT_PANEL_ID, "Background", self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL], CvUtil.FONT_CENTER_JUSTIFY, self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X], self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


	# Draws the bottom bar of the "Unit Statistics" screens
	def drawScreenBottom(self, screen):
		screen.addPanel(BOTTOM_PANEL_ID, u"", u"", True, True, self.screenWidgetData[BOTTOM_PANEL_X], self.screenWidgetData[BOTTOM_PANEL_Y], self.screenWidgetData[BOTTOM_PANEL_WIDTH], self.screenWidgetData[BOTTOM_PANEL_HEIGHT], PanelStyles.PANEL_STYLE_BOTTOMBAR )

		szText1 = self.screenWidgetData[UNIT_STATISTICS_TEXT_PANEL]
		szText2 = self.screenWidgetData[HIGHSCORES_TEXT_PANEL]
		szText3 = self.screenWidgetData[PLAYER_STATISTICS_TEXT_PANEL]

		color1 = gc.getInfoTypeForString("COLOR_GREY")
		color2 = gc.getInfoTypeForString("COLOR_PLAYER_PURPLE")
		if (self.currentUnit == "" or self.currentUnit == None or isinstance(self.currentUnit, (int))):
			szText1 = localText.changeTextColor(szText1, color1)
		if (self.currentScreen == UNIT_STATISTICS):
			szText1 = localText.changeTextColor(szText1, color2)
		elif (self.currentScreen == HIGHSCORES or self.currentScreen == CURRHIGHSCORES or self.currentScreen == TOP10 or self.currentScreen == "TOPLISTA" or self.currentScreen == HALLOFFAME):
			szText2 = localText.changeTextColor(szText2, color2)
		elif (self.currentScreen == PLAYER_STATISTICS):
			szText3 = localText.changeTextColor(szText3, color2)

		screen.setText(UNIT_STATISTICS_TEXT_PANEL_ID, "Background", szText1, CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[UNIT_STATISTICS_TEXT_PANEL_X], self.screenWidgetData[UNIT_STATISTICS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(HIGHSCORES_TEXT_PANEL_ID, "Background", szText2, CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[HIGHSCORES_TEXT_PANEL_X], self.screenWidgetData[HIGHSCORES_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(PLAYER_STATISTICS_TEXT_PANEL_ID, "Background", szText3, CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[PLAYER_STATISTICS_TEXT_PANEL_X], self.screenWidgetData[PLAYER_STATISTICS_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#screen.setText(GRAVEYARD_TEXT_PANEL_ID, "Background", self.screenWidgetData[GRAVEYARD_TEXT_PANEL], CvUtil.FONT_LEFT_JUSTIFY, self.screenWidgetData[GRAVEYARD_TEXT_PANEL_X], self.screenWidgetData[GRAVEYARD_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setText(EXIT_TEXT_PANEL_ID, "Background", self.screenWidgetData[EXIT_TEXT_PANEL], CvUtil.FONT_RIGHT_JUSTIFY, self.screenWidgetData[EXIT_TEXT_PANEL_X], self.screenWidgetData[EXIT_TEXT_PANEL_Y], self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )


	def closeScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	# handles the display of the units info pane
	def showHSInfoPane(self, id):

		screen = self.getScreen()

		self.calculateScreenWidgetData(screen)

		screen.addPanel( HIGHSCORE_INFO_PANE_ID, u"", u"", True, True, \
						self.screenWidgetData[HIGHSCORE_INFO_PANE_X], self.screenWidgetData[HIGHSCORE_INFO_PANE_Y] ,self.screenWidgetData[HIGHSCORE_INFO_PANE_WIDTH], self.screenWidgetData[HIGHSCORE_INFO_PANE_HEIGHT], \
						PanelStyles.PANEL_STYLE_HUD_HELP )


		HSList = objUnitStatisticsTools.getAllHighScores()

		szText = objUnitStatisticsTools.getHSString(HSList[id], "unit")

		szTextSized = "<font=2>"+ szText +"</font=2>"

		# create shadow text
		szTextBlack = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_BLACK"))

		szTextBlackSized = "<font=2>"+ szTextBlack +"</font=2>"

		# display shadow text
		screen.addMultilineText( "UNIT_INFO_TEXT_SHADOW", szTextBlackSized, \
								self.screenWidgetData[HIGHSCORE_INFO_PANE_X] + 6, self.screenWidgetData[HIGHSCORE_INFO_PANE_Y] +6, \
								self.screenWidgetData[HIGHSCORE_INFO_PANE_WIDTH] -3, self.screenWidgetData[HIGHSCORE_INFO_PANE_HEIGHT] - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)
		# display text
		screen.addMultilineText( "UNIT_INFO_TEXT", szTextSized, \
								self.screenWidgetData[HIGHSCORE_INFO_PANE_X] + 5, self.screenWidgetData[HIGHSCORE_INFO_PANE_Y] +5, \
								self.screenWidgetData[HIGHSCORE_INFO_PANE_WIDTH] -3, self.screenWidgetData[HIGHSCORE_INFO_PANE_HEIGHT] - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)

	def hideHSInfoPane(self):
		screen = self.getScreen()
		screen.hide("UNIT_INFO_TEXT")
		screen.hide("UNIT_INFO_TEXT_SHADOW")
		screen.hide(HIGHSCORE_INFO_PANE_ID)

	# handles the display of the button info pane
	def showButtonInfoPane(self, id):

		if not g_bShowHelp:
			return

		screen = self.getScreen()

		self.calculateScreenWidgetData(screen)

		screen.addPanel( BUTTON_INFO_PANE_ID, u"", u"", True, True, \
						self.screenWidgetData[BUTTON_INFO_PANE_X], self.screenWidgetData[BUTTON_INFO_PANE_Y] ,self.screenWidgetData[BUTTON_INFO_PANE_WIDTH], self.screenWidgetData[BUTTON_INFO_PANE_HEIGHT], \
						PanelStyles.PANEL_STYLE_HUD_HELP )

		if (id == 98):
			szText = localText.getText("TXT_KEY_UNITSTATS_UNITBUTTON", ())
		elif (id == 99):
			szText = localText.getText("TXT_KEY_UNITSTATS_FINDBUTTON", ())
		else:
			HSList = objUnitStatisticsTools.getAllHighScores()
			szText = objUnitStatisticsTools.getHSString(HSList[id], "unit")


		szTextSized = "<font=2>"+ szText +"</font=2>"

		# create shadow text
		szTextBlack = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_BLACK"))

		szTextBlackSized = "<font=2>"+ szTextBlack +"</font=2>"

		# display shadow text
		screen.addMultilineText( "UNIT_INFO_TEXT_SHADOW", szTextBlackSized, \
								self.screenWidgetData[BUTTON_INFO_PANE_X] + 6, self.screenWidgetData[BUTTON_INFO_PANE_Y] +6, \
								self.screenWidgetData[BUTTON_INFO_PANE_WIDTH] -3, self.screenWidgetData[BUTTON_INFO_PANE_HEIGHT] - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)
		# display text
		screen.addMultilineText( "UNIT_INFO_TEXT", szTextSized, \
								self.screenWidgetData[BUTTON_INFO_PANE_X] + 5, self.screenWidgetData[BUTTON_INFO_PANE_Y] +5, \
								self.screenWidgetData[BUTTON_INFO_PANE_WIDTH] -3, self.screenWidgetData[BUTTON_INFO_PANE_HEIGHT] - 3, \
								WidgetTypes.WIDGET_GENERAL, -1, -1, \
								CvUtil.FONT_LEFT_JUSTIFY)

	def hideButtonInfoPane(self):

		if not g_bShowHelp:
			return

		screen = self.getScreen()
		screen.hide("UNIT_INFO_TEXT")
		screen.hide("UNIT_INFO_TEXT_SHADOW")
		screen.hide(BUTTON_INFO_PANE_ID)

	# If you hover your mouse over a unit button, its location on the map begins to blink
	def setFlashPlot (self, screen, strName, strOnOrOff):

		# Get the unit object
		iUnitID, iPlayer, objUnit = objUnitStatisticsTools.unitIDToObject(strName)

		if (objUnit == None or isinstance(objUnit, (int))):
			return

		if (iPlayer != gc.getGame().getActivePlayer() and not g_bShowAllPlayers):
			return

		# Get the color
		self.iActivePlayer = gc.getGame().getActivePlayer()
		player = PyPlayer(iPlayer)
		iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()

		if (player.getTeam().isAtWar(gc.getPlayer(self.iActivePlayer).getTeam())):
			iColor = gc.getInfoTypeForString("COLOR_RED")
		elif (gc.getPlayer(iPlayer).getTeam() != gc.getPlayer(self.iActivePlayer).getTeam()):
			iColor = gc.getInfoTypeForString("COLOR_YELLOW")
		else:
			iColor = gc.getInfoTypeForString("COLOR_WHITE")

		# If the mouse is moving on the button, the unit's plot starts to blink
		if (strOnOrOff == "on"):
			screen.minimapFlashPlot(objUnit.getX(), objUnit.getY(), iColor, -1)

		# If the mouse is moving off the button, the blinking stops
		if (strOnOrOff == "off"):
			screen.minimapClearAllFlashingTiles()

	def minimapClicked(self):
		self.hideScreen()
		self.currentScreen = UNIT_STATISTICS

	# Will handle the input for this screen...
	def handleInput (self, inputClass):

		screen = self.getScreen()

		# Get the data
		theKey = int(inputClass.getData())


		# If the escape key was pressed then set the current screen to unit statistics
		if (inputClass.getNotifyCode() == self.EventKeyDown and theKey == int(InputTypes.KB_ESCAPE)):
			self.currentScreen = UNIT_STATISTICS

		# If the exit text was pressed then set the current screen to unit statistics.
		if(inputClass.getFunctionName() == EXIT_TEXT_PANEL_ID):
			self.currentScreen = UNIT_STATISTICS

		# Handles the info panes that appear if you hover your mouse over a high score button
		# on the unit screen and the flashing of the minimap
		id = inputClass.getID()
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON  ):
			if (inputClass.getFunctionName().endswith("HSBox")):
				self.showHSInfoPane(id)
			elif (inputClass.getFunctionName().endswith("UnitButton") or inputClass.getFunctionName().endswith("FindButton")):
				strName, function = inputClass.getFunctionName().split("_")
				self.setFlashPlot(screen, strName, "on")
				self.showButtonInfoPane(id)
			elif (inputClass.getFunctionName().endswith("HSButton")):
				strName, function = inputClass.getFunctionName().split("_")
				self.setFlashPlot(screen, strName, "on")
				self.showButtonInfoPane(id)
			elif (inputClass.getFunctionName().endswith("HighScoreButton")):
				htype, function = inputClass.getFunctionName().split("_")
				iUnitID, iPlayer, objUnit = objUnitStatisticsTools.unitIDToObject(objUnitStatisticsTools.getHSUnit(htype, "highscore"))
				if (not isinstance(objUnit, (int))):
					strName = objUnitStatisticsTools.numberToAlpha(objUnit.getID()) + "-" + objUnitStatisticsTools.numberToAlpha(objUnit.getOwner())
					self.setFlashPlot(screen, strName, "on")
					self.showButtonInfoPane(id)
			elif (inputClass.getFunctionName().endswith("FindButton")):
				strName, function = inputClass.getFunctionName().split("_")
				self.setFlashPlot(screen, strName, "on")
				self.showButtonInfoPane(id)
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ):
			if (inputClass.getFunctionName().endswith("HSBox")):
				self.hideHSInfoPane()
			elif (inputClass.getFunctionName().endswith("UnitButton") or inputClass.getFunctionName().endswith("FindButton")):
				strName, function = inputClass.getFunctionName().split("_")
				self.setFlashPlot(screen, strName, "off")
				self.hideButtonInfoPane()
			elif (inputClass.getFunctionName().endswith("HSButton")):
				strName, function = inputClass.getFunctionName().split("_")
				self.setFlashPlot(screen, strName, "off")
				self.hideButtonInfoPane()
			elif (inputClass.getFunctionName().endswith("HighScoreButton")):
				htype, function = inputClass.getFunctionName().split("_")
				iUnitID, iPlayer, objUnit = objUnitStatisticsTools.unitIDToObject(objUnitStatisticsTools.getHSUnit(htype, "highscore"))
				if (not isinstance(objUnit, (int))):
					strName = objUnitStatisticsTools.numberToAlpha(objUnit.getID()) + "-" + objUnitStatisticsTools.numberToAlpha(objUnit.getOwner())
					self.setFlashPlot(screen, strName, "off")
				self.hideButtonInfoPane()


		# Handles all the links at the bottom of the page. If a button is pressed, check whether
		# the selected page is already open. If it isn't, mark it as active and redraw
		# the screen
		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName().endswith("LINK")):
			strName, function = inputClass.getFunctionName().split("_")
			if strName == PLAYER_STATISTICS_NEW_PLAYER:
				self.currentScreen = PLAYER_STATISTICS
				self.hideScreen()
				self.interfaceScreen(inputClass.getID())
			elif strName == UNIT_STATISTICS:
				if (self.currentUnit == None or isinstance(self.currentUnit, (int))):
					return
				else:
					self.currentScreen = UNIT_STATISTICS
					self.hideScreen()
					self.interfaceScreen(gc.getGame().getActivePlayer())
			elif (self.currentScreen != strName):
				self.currentScreen = strName
				self.hideScreen()
				self.interfaceScreen(gc.getGame().getActivePlayer())
			return


		# If someone pressed one of the buttons in the screen then handle the
		# action
		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName().endswith("Button")):
			# Split up the function name into the unit ID string and the actual
			# action that was performed
			strName, function = inputClass.getFunctionName().split("_")

			# If the function was unit, then close the screen and find the unit
			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and function == "UnitButton"):
				iUnitID, iPlayer, objUnit = objUnitStatisticsTools.unitIDToObject(strName)
				if (objUnit == None or isinstance(objUnit, (int))):
					return
				if(iPlayer != gc.getGame().getActivePlayer() and not g_bShowAllPlayers):
					return
				self.currentUnit = objUnit
				self.currentScreen = UNIT_STATISTICS
				self.hideScreen()
				self.interfaceScreen(gc.getGame().getActivePlayer())

			# If the function was graveyard, then close the screen and find the unit
			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and function == "GraveYardUnitButton"):
				iUnitID, iPlayer, objPlot = objUnitStatisticsTools.unitIDToObject(strName)
				if (objPlot == None or isinstance(objPlot, (int))):
					return
				self.currentUnit = objPlot
				self.currentScreen = UNIT_STATISTICS
				self.hideScreen()
				self.interfaceScreen(gc.getGame().getActivePlayer())

			# If the function was highscore, then open the unit screen for the corresponding unit
			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and function == "TopListButton" and self.currentHighScore != strName):
				self.currentHighScore = strName
				if (self.currentScreen == TOP10):
					self.currentScreen = "TOPLISTA"
				elif (self.currentScreen == "TOPLISTA"):
					self.currentScreen = TOP10
				self.hideScreen()
				self.interfaceScreen(gc.getGame().getActivePlayer())

			# If the function was highscore, then open the unit screen for the corresponding unit
			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and function == "HighScoreButton"):

				if self.currentScreen == HIGHSCORES:
					strHSorHOF = "highscore"
				elif self.currentScreen == HALLOFFAME:
					strHSorHOF = "halloffame"
				iUnitID, iPlayer, objUnit = objUnitStatisticsTools.unitIDToObject(objUnitStatisticsTools.getHSUnit(strName, strHSorHOF))

				if (objUnit == None or isinstance(objUnit, (int))):
					return
				try:
					objUnit.getExperience()
				except:
					if (objUnit.getY() != gc.getGame().getActivePlayer() and not g_bShowAllPlayers):
						return
					self.currentUnit = objUnit
					self.currentScreen = UNIT_STATISTICS
					self.hideScreen()
					self.interfaceScreen(gc.getGame().getActivePlayer())
				if(objUnit.getOwner() != gc.getGame().getActivePlayer() and not g_bShowAllPlayers):
					return
				self.currentUnit = objUnit
				self.currentScreen = UNIT_STATISTICS
				self.hideScreen()
				self.interfaceScreen(gc.getGame().getActivePlayer())

			# If the function was find, then close the screen and find the unit
			if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and function == "FindButton"):

				iUnitID, iPlayer, objUnit = objUnitStatisticsTools.unitIDToObject(strName)

				# If the unit is not set to None then look at them and select
				# them.
				if(objUnit != None):
					CyCamera().JustLookAtPlot(objUnit.plot())
					if(not CyGame().isNetworkMultiPlayer()):
						CyInterface().selectUnit(objUnit, true, false, false)

				self.currentScreen = UNIT_STATISTICS

				return

		return 0

	def update(self, fDelta):
		return

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	# Calculates the screens widgets positions, dimensions, text, etc.
	def calculateScreenWidgetData(self, screen):
		' Calculates the screens widgets positions, dimensions, text, etc. '

		# The border width should not be a hard coded number
		self.screenWidgetData[BORDER_WIDTH] = 4

		self.screenWidgetData[SCREEN_WIDTH] = screen.getXResolution()
		self.screenWidgetData[SCREEN_HEIGHT] = screen.getYResolution()


		# Screen title panel information
		self.screenWidgetData[SCREEN_TITLE_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] = 55
		self.screenWidgetData[SCREEN_TITLE_PANEL_X] = 0
		self.screenWidgetData[SCREEN_TITLE_PANEL_Y] = 0
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL] = u"<font=4b>" + localText.getText("TXT_KEY_UNIT_STATISTICS", ()) + "</font>"
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH]/2
		self.screenWidgetData[SCREEN_TITLE_TEXT_PANEL_Y] = 8


		# Exit panel information
		self.screenWidgetData[BOTTOM_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[BOTTOM_PANEL_HEIGHT] = 55
		self.screenWidgetData[BOTTOM_PANEL_X] = 0
		self.screenWidgetData[BOTTOM_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 55

		self.screenWidgetData[UNIT_STATISTICS_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_UNIT_STATISTICS", ())+ "</font>"
		self.screenWidgetData[UNIT_STATISTICS_TEXT_PANEL_X] = 30
		self.screenWidgetData[UNIT_STATISTICS_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[HIGHSCORES_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_HIGHSCORES", ()) + "</font>"
		self.screenWidgetData[HIGHSCORES_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] * 1/4 + 30
		self.screenWidgetData[HIGHSCORES_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[PLAYER_STATISTICS_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_PLAYER_STATISTICS", ()) + "</font>"
		self.screenWidgetData[PLAYER_STATISTICS_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] * 2/4 - 30
		self.screenWidgetData[PLAYER_STATISTICS_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[GRAVEYARD_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_GRAVEYARD", ()) + "</font>"
		self.screenWidgetData[GRAVEYARD_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] * 3/4 - 40
		self.screenWidgetData[GRAVEYARD_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42

		self.screenWidgetData[HSBOTTOM_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH]
		self.screenWidgetData[HSBOTTOM_PANEL_HEIGHT] = 90
		self.screenWidgetData[HSBOTTOM_PANEL_X] = 0
		self.screenWidgetData[HSBOTTOM_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - self.screenWidgetData[HSBOTTOM_PANEL_HEIGHT]

		self.screenWidgetData[HALLOFFAME_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_HALLOFFAME", ()) + "</font>"
		self.screenWidgetData[HALLOFFAME_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] * 1/4 + 30
		self.screenWidgetData[HALLOFFAME_TEXT_PANEL_Y] = self.screenWidgetData[HSBOTTOM_PANEL_Y] +13

		self.screenWidgetData[CURRHIGHSCORES_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_CURRHIGHSCORES", ()) + "</font>"
		self.screenWidgetData[CURRHIGHSCORES_TEXT_PANEL_X] = 30
		self.screenWidgetData[CURRHIGHSCORES_TEXT_PANEL_Y] = self.screenWidgetData[HSBOTTOM_PANEL_Y] +13

		self.screenWidgetData[TOP10_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_TOP10", ()) + "</font>"
		self.screenWidgetData[TOP10_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] * 2/4 + 30
		self.screenWidgetData[TOP10_TEXT_PANEL_Y] = self.screenWidgetData[HSBOTTOM_PANEL_Y] +13


		self.screenWidgetData[EXIT_TEXT_PANEL] = u"<font=4>" + localText.getText("TXT_KEY_UNITSTATS_EXIT", ()) + "</font>"
		self.screenWidgetData[EXIT_TEXT_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] - 30
		self.screenWidgetData[EXIT_TEXT_PANEL_Y] = self.screenWidgetData[SCREEN_HEIGHT] - 42



		# Unit screen information
		self.screenWidgetData[UNIT_INFORMATION_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*2) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BOTTOM_PANEL_HEIGHT]))
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*6)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_Y] + 4

		self.screenWidgetData[UNIT_ANIMATION_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X]+ self.screenWidgetData[BORDER_WIDTH]*4
		self.screenWidgetData[UNIT_ANIMATION_Y] = self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL_Y]+40
		self.screenWidgetData[UNIT_ANIMATION_WIDTH] = 303
		self.screenWidgetData[UNIT_ANIMATION_HEIGHT] = 200
		self.screenWidgetData[UNIT_ANIMATION_ROTATION_X] = -20
		self.screenWidgetData[UNIT_ANIMATION_ROTATION_Z] = 30
		self.screenWidgetData[UNIT_ANIMATION_SCALE] = 1.0

		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] = 440
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] = 185
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X] = self.screenWidgetData[SCREEN_WIDTH] - self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*4)
		self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] = self.screenWidgetData[UNIT_ANIMATION_Y]

		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]*2
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] + 33
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH] - 20
		self.screenWidgetData[UNIT_INFORMATION_INNER_PROMOTION_PANEL_HEIGHT] = 114

		self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_X]
		self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_Y] + self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_HEIGHT] = 185

		self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]*2
		self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_Y] + 33
		self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_WIDTH] - 20
		self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_HEIGHT] = 234


		self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]*3
		self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_Y] = self.screenWidgetData[UNIT_ANIMATION_Y] + self.screenWidgetData[UNIT_ANIMATION_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_INNER_PANEL_HEIGHT] = self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT] - self.screenWidgetData[BORDER_WIDTH] - self.screenWidgetData[UNIT_ANIMATION_Y] - self.screenWidgetData[UNIT_ANIMATION_HEIGHT]

		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_UNIT_OVERVIEW", ()) + "</font>"
		self.screenWidgetData[UNIT_INFORMATION_TEXT_PANEL2] = "<font=3b>" + localText.getText("TXT_KEY_PLAYER_OVERVIEW", ()) + "</font>"
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X] = self.screenWidgetData[UNIT_ANIMATION_X] + self.screenWidgetData[UNIT_ANIMATION_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_Y] = self.screenWidgetData[UNIT_ANIMATION_Y]
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - (self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH])*2 + self.screenWidgetData[UNIT_INFORMATION_PROMOTION_PANEL_WIDTH])
		self.screenWidgetData[UNIT_INFORMATION_DETAILS_PANEL_HEIGHT] = self.screenWidgetData[UNIT_ANIMATION_HEIGHT]

		# Player screen information
		self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_X] = self.screenWidgetData[UNIT_INFORMATION_PANEL_X] + self.screenWidgetData[BORDER_WIDTH]*3
		self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_Y] = self.screenWidgetData[UNIT_INFORMATION_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]*4 + self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT]
		self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_WIDTH] = self.screenWidgetData[UNIT_INFORMATION_PANEL_WIDTH] - (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[PLAYER_INFORMATION_INNER_PANEL_HEIGHT] = self.screenWidgetData[UNIT_INFORMATION_PANEL_HEIGHT] - (self.screenWidgetData[BORDER_WIDTH]*9) - self.screenWidgetData[UNIT_INFORMATION_TEXT_BACKGROUND_PANEL_HEIGHT]

		# High Score screen information
		self.screenWidgetData[HIGHSCORE_LIST_PANEL_X] = self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIGHSCORE_LIST_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH] = 310
		self.screenWidgetData[HIGHSCORE_LIST_INNER_PANEL_X] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIGHSCORE_LIST_INNER_PANEL_Y] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIGHSCORE_LIST_INNER_PANEL_WIDTH] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH] - (self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[BORDER_WIDTH]*2))
		self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_X] = self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[HIGHSCORE_LIST_TEXT_PANEL_Y] = self.screenWidgetData[HIGHSCORE_LIST_TEXT_BACKGROUND_PANEL_Y] + 4

		self.screenWidgetData[MINIMAP_X] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_X]
		self.screenWidgetData[MINIMAP_WIDTH] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH]
		self.screenWidgetData[MINIMAP_HEIGHT_MAX] = 300
		self.screenWidgetData[MINIMAP_BORDER] = 20
		self.screenWidgetData[MINIMAP_HEIGHT] = (self.screenWidgetData[MINIMAP_WIDTH] * CyMap().getGridHeight()) / CyMap().getGridWidth()
		if (self.screenWidgetData[MINIMAP_HEIGHT] > self.screenWidgetData[MINIMAP_HEIGHT_MAX]):
			self.screenWidgetData[MINIMAP_WIDTH] = (self.screenWidgetData[MINIMAP_HEIGHT_MAX] * CyMap().getGridWidth()) / CyMap().getGridHeight()
			self.screenWidgetData[MINIMAP_HEIGHT] = self.screenWidgetData[MINIMAP_HEIGHT_MAX]
		self.screenWidgetData[MINIMAP_Y] = self.screenWidgetData[SCREEN_HEIGHT] - self.screenWidgetData[BORDER_WIDTH]*2 - self.screenWidgetData[MINIMAP_HEIGHT] - self.screenWidgetData[HSBOTTOM_PANEL_HEIGHT]


		self.screenWidgetData[HIGHSCORE_LIST_PANEL_HEIGHT] = self.screenWidgetData[MINIMAP_Y] - (self.screenWidgetData[HIGHSCORE_LIST_PANEL_Y])
		self.screenWidgetData[HIGHSCORE_LIST_INNER_PANEL_HEIGHT] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])

		self.screenWidgetData[HIGHSCORE_PAGE_PANEL_X] = self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH]
		self.screenWidgetData[HIGHSCORE_PAGE_PANEL_Y] = self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIGHSCORE_PAGE_PANEL_WIDTH] = self.screenWidgetData[SCREEN_WIDTH] - self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH] - self.screenWidgetData[BORDER_WIDTH]*2
		self.screenWidgetData[HIGHSCORE_PAGE_PANEL_HEIGHT] = (self.screenWidgetData[SCREEN_HEIGHT] - ((self.screenWidgetData[BORDER_WIDTH]*3) + self.screenWidgetData[SCREEN_TITLE_PANEL_HEIGHT])) - self.screenWidgetData[HSBOTTOM_PANEL_HEIGHT]
		self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_X] = self.screenWidgetData[HIGHSCORE_PAGE_PANEL_X] + (4*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_Y] = self.screenWidgetData[HIGHSCORE_PAGE_PANEL_Y] + (10*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_WIDTH] = self.screenWidgetData[HIGHSCORE_PAGE_PANEL_WIDTH] - (8*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIGHSCORE_PAGE_INNER_PANEL_HEIGHT] = self.screenWidgetData[HIGHSCORE_PAGE_PANEL_HEIGHT] - (14*self.screenWidgetData[BORDER_WIDTH])
		self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_X] = self.screenWidgetData[HIGHSCORE_PAGE_PANEL_X] + self.screenWidgetData[BORDER_WIDTH] + (self.screenWidgetData[BORDER_WIDTH]*2)
		self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_Y] = self.screenWidgetData[HIGHSCORE_PAGE_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH] + self.screenWidgetData[BORDER_WIDTH]
		self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_WIDTH] = self.screenWidgetData[HIGHSCORE_PAGE_PANEL_WIDTH] - self.screenWidgetData[BORDER_WIDTH]*6
		self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_HEIGHT] = 30
		self.screenWidgetData[HIGHSCORE_PAGE_TEXT_PANEL] = "<font=3b>" + localText.getText("TXT_KEY_HIGHSCORES_SMALL", ()) + "</font>"
		self.screenWidgetData[HIGHSCORE_PAGE_TEXT_PANEL_X] = self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_X] + (self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_WIDTH]/2)
		self.screenWidgetData[HIGHSCORE_PAGE_TEXT_PANEL_Y] = self.screenWidgetData[HIGHSCORE_PAGE_TEXT_BACKGROUND_PANEL_Y] + 4

		self.screenWidgetData[HIGHSCORE_INFO_PANE_WIDTH] = 250
		self.screenWidgetData[HIGHSCORE_INFO_PANE_HEIGHT] = 69
		self.screenWidgetData[HIGHSCORE_INFO_PANE_X] = self.screenWidgetData[UNIT_INFORMATION_HIGHSCORE_PANEL_X] - self.screenWidgetData[HIGHSCORE_INFO_PANE_WIDTH]
		self.screenWidgetData[HIGHSCORE_INFO_PANE_Y] = self.screenWidgetData[UNIT_INFORMATION_INNER_HIGHSCORE_PANEL_Y] + self.screenWidgetData[BORDER_WIDTH]*5

		self.screenWidgetData[BUTTON_INFO_PANE_WIDTH] = 250
		self.screenWidgetData[BUTTON_INFO_PANE_HEIGHT] = 69
		self.screenWidgetData[BUTTON_INFO_PANE_X] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_X] + self.screenWidgetData[HIGHSCORE_LIST_PANEL_WIDTH]
		self.screenWidgetData[BUTTON_INFO_PANE_Y] = self.screenWidgetData[HIGHSCORE_LIST_PANEL_Y]
