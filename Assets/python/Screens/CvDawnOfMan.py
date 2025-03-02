## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# FlavourMod: Changed by Jean Elcard 03/20/2009
# Ronkhar 2013-08-20
import CvUtil
from CvPythonExtensions import *

ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
gc = CyGlobalContext()

class CvDawnOfMan:
	"Dawn of man screen"
	def __init__(self, iScreenID):
		self.iScreenID = iScreenID

		self.EXT_SPACING = 28 # same as pediamain. See if the var can be called from here instead of recreating it
		self.INT_SPACING = 14 # same as pediamain. See if the var can be called from here instead of recreating it
		self.S_FANCY_ICON = 64 # icon size is 64x64
		self.W_LEADERHEAD = 320 # width of the dds file
		self.H_LEADERHEAD = 384 # height of the dds file

	def interfaceScreen(self):
		'Use a popup to display the opening text'
		if ( CyGame().isPitbossHost() ):
			return

		#self.calculateSizesAndPositions()

		self.player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.EXIT_TEXT = localText.getText("TXT_KEY_SCREEN_CONTINUE", ())

		# Create screen

		screen = CyGInterfaceScreen( "CvDawnOfMan", self.iScreenID )
		# Find out the game resolution
		self.W_SCREEN = screen.getXResolution() #HD example: 1920
		self.H_SCREEN = screen.getYResolution() #HD example: 1200
		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground( False )
		screen.setDimensions(0, 0, self.W_SCREEN, self.H_SCREEN)
		screen.enableWorldSounds( false )

		# Create panels

		# Main
		szMainPanel = "DawnOfManMainPanel"

		self.W_MAIN_PANEL = self.W_SCREEN - 2 * self.EXT_SPACING
		self.H_MAIN_PANEL = self.H_SCREEN - 2 * self.EXT_SPACING
		self.X_MAIN_PANEL = self.EXT_SPACING
		self.Y_MAIN_PANEL = self.EXT_SPACING
		screen.addPanel( szMainPanel, "", "", true, true,
			self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )

		# Top
		szHeaderPanel = "DawnOfManHeaderPanel"
		self.X_HEADER_PANEL = self.X_MAIN_PANEL + self.INT_SPACING
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + self.INT_SPACING
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - self.INT_SPACING*2
		# self.H_HEADER_PANEL = self.H_LEADERHEAD + self.INT_SPACING*2
		self.H_HEADER_PANEL = int(self.H_SCREEN*0.6) # test Ronkhar 2013-08-30
		screen.addPanel( szHeaderPanel, "", "", true, false,
			self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNTOP )

		# Bottom
		szTextPanel = "DawnOfManTextPanel"
		self.X_TEXT_PANEL = self.X_HEADER_PANEL
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + self.H_HEADER_PANEL + self.INT_SPACING   - 10 #10 is the fudge factor
		self.W_TEXT_PANEL = self.W_HEADER_PANEL
		self.H_TEXT_PANEL = self.H_MAIN_PANEL   - self.H_HEADER_PANEL - self.INT_SPACING*3 + 10 #10 is the fudge factor
		screen.addPanel( szTextPanel, "", "", true, true,
			self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )

		# Add contents

		# Leaderhead graphic
		szLeaderPanel = "DawnOfManLeaderPanel"

		self.X_LEADERHEAD = self.X_HEADER_PANEL + self.INT_SPACING
		self.Y_LEADERHEAD = self.Y_HEADER_PANEL + self.INT_SPACING
		#screen.addPanel( szLeaderPanel, "", "", true, false,self.X_LEADERHEAD - 3, self.Y_LEADERHEAD - 5, self.W_LEADERHEAD + 6, self.H_LEADERHEAD + 8, PanelStyles.PANEL_STYLE_DAWNTOP )
		screen.addLeaderheadGFC("LeaderHead", self.player.getLeaderType(), AttitudeTypes.ATTITUDE_PLEASED,
			self.X_LEADERHEAD + 5, self.Y_LEADERHEAD + 5, self.W_LEADERHEAD - 10, self.H_LEADERHEAD - 10, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Info/"Stats" text

		self.X_FANCY_ICON1 = self.X_LEADERHEAD + self.W_LEADERHEAD + self.INT_SPACING
		self.X_FANCY_ICON2 = self.X_HEADER_PANEL + self.W_HEADER_PANEL - self.INT_SPACING - self.S_FANCY_ICON
		self.Y_FANCY_ICON = (self.Y_HEADER_PANEL + self.INT_SPACING + 6) - 6
		# Fancy icon things
		civ_button = ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.player.getCivilizationType()).getArtDefineTag()).getButton()
		screen.addDDSGFC( "IconLeft",  civ_button, self.X_FANCY_ICON1 , self.Y_FANCY_ICON , self.S_FANCY_ICON, self.S_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDDSGFC( "IconRight", civ_button, self.X_FANCY_ICON2 , self.Y_FANCY_ICON , self.S_FANCY_ICON, self.S_FANCY_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		szNameText = "<color=255,255,0,255>" + u"<font=3b>" + gc.getLeaderHeadInfo(self.player.getLeaderType()).getDescription().upper() + u"</font>"
		szNameText += "\n- " + self.player.getCivilizationDescription(0) + " -\n"
		szNameText += u"<font=2>" + CyGameTextMgr().parseLeaderTraits(self.player.getLeaderType(), self.player.getCivilizationType(), True, False) + u"</font>"
		self.X_LEADER_TITLE_TEXT = (self.X_FANCY_ICON1+self.S_FANCY_ICON)+((self.X_FANCY_ICON2 - (self.X_FANCY_ICON1+self.S_FANCY_ICON))/2) - ((self.W_HEADER_PANEL / 3)/2)
		self.Y_LEADER_TITLE_TEXT = self.Y_HEADER_PANEL + self.INT_SPACING + 6
		self.W_LEADER_TITLE_TEXT = self.W_HEADER_PANEL / 3
		self.H_LEADER_TITLE_TEXT = self.H_HEADER_PANEL / 2
		screen.addMultilineText( "NameText", szNameText, self.X_LEADER_TITLE_TEXT, self.Y_LEADER_TITLE_TEXT, self.W_LEADER_TITLE_TEXT, self.H_LEADER_TITLE_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)


		self.X_STATS_TEXT = self.X_FANCY_ICON1# + self.W_LEADERHEAD + (self.INT_SPACING * 2) + 5
		self.Y_STATS_TEXT = self.Y_LEADER_TITLE_TEXT + 75
		self.W_STATS_TEXT = int(self.W_HEADER_PANEL * (5 / 7.0)) + 2 * self.INT_SPACING
		self.H_STATS_TEXT = int(self.H_HEADER_PANEL * (3 / 5.0)) - 2 * self.INT_SPACING
		screen.addMultilineText( "HeaderText2", localText.getText("TXT_KEY_FREE_TECHS", ()) + ":", self.X_STATS_TEXT, self.Y_STATS_TEXT+15, self.W_STATS_TEXT, self.H_STATS_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		self.W_TECH = 425
		self.H_TECH = 80
		screen.addPanel( "HeaderText3", "", "", false, true,
				 self.X_STATS_TEXT, self.Y_STATS_TEXT+30, self.W_TECH, self.H_TECH, PanelStyles.PANEL_STYLE_EMPTY )

		for iTech in range(gc.getNumTechInfos()):
			if (gc.getCivilizationInfo(self.player.getCivilizationType()).isCivilizationFreeTechs(iTech)):
				screen.attachImageButton( "HeaderText3", "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

		self.Text_BoxText = CyGameTextMgr().parseCivInfos(self.player.getCivilizationType(), True)

		screen.addMultilineText( "HeaderText4", self.Text_BoxText, self.X_STATS_TEXT, self.Y_STATS_TEXT+30+self.H_TECH, self.W_STATS_TEXT - 3 * self.INT_SPACING, self.H_STATS_TEXT - 4 * self.INT_SPACING, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)


		# Main Body text
		szDawnTitle = u"<font=3>" + localText.getText("TXT_KEY_DAWN_OF_MAN_SCREEN_TITLE", ()).upper() + u"</font>"
		screen.setLabel("DawnTitle", "Background", szDawnTitle, CvUtil.FONT_CENTER_JUSTIFY,
				self.X_TEXT_PANEL + (self.W_TEXT_PANEL / 2), self.Y_TEXT_PANEL + 15, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )


		'''
		bodyString = localText.getText("TXT_KEY_DAWN_OF_MAN_TEXT", (CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn(), false), self.player.getCivilizationAdjectiveKey(), self.player.getNameKey()))
		'''
		pCivilization = gc.getCivilizationInfo(self.player.getCivilizationType())
		dawnString = "TXT_KEY_CIV_" + pCivilization.getType()[len("CIVILIZATION_"):] + "_STRATEGY"
		bodyString = localText.getText(dawnString, (CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn(), false), self.player.getCivilizationAdjectiveKey(), self.player.getNameKey())).lstrip()
		if bodyString == dawnString:
			bodyString = localText.getText("TXT_KEY_DAWN_OF_MAN_TEXT", (CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn(), false), self.player.getCivilizationAdjectiveKey(), self.player.getNameKey()))

		self.iTEXT_PANEL_MARGIN = 35
		screen.addMultilineText( "BodyText", bodyString, self.X_TEXT_PANEL + self.INT_SPACING, self.Y_TEXT_PANEL + self.INT_SPACING + self.iTEXT_PANEL_MARGIN, self.W_TEXT_PANEL - (self.INT_SPACING * 2), self.H_TEXT_PANEL - (self.INT_SPACING * 2) - 75, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		self.W_EXIT = 120
		self.H_EXIT = 30
		self.X_EXIT = (self.W_SCREEN/2) - (self.W_EXIT/2) # Centred
		self.Y_EXIT = self.Y_TEXT_PANEL + self.H_TEXT_PANEL - self.H_EXIT
		screen.setButtonGFC("Exit", self.EXIT_TEXT, "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

		pActivePlayer = gc.getPlayer(CyGame().getActivePlayer())
		pLeaderHeadInfo = gc.getLeaderHeadInfo(pActivePlayer.getLeaderType())
		screen.setSoundId(CyAudioGame().Play2DSoundWithId(pLeaderHeadInfo.getDiploPeaceMusicScriptIds(0)))

	def handleInput( self, inputClass ):
		return 0

	def update(self, fDelta):
		return

	def onClose(self):
		CyInterface().setSoundSelectionReady(true)
		return 0