## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import string

localText = CyTranslator()

class CvTechSplashScreen:
	"Splash screen for techs"
	def __init__(self, iScreenID):
		self.nScreenId = iScreenID
		self.iTech = -1
		self.nWidgetCount = 0
		# widget names
		self.WIDGET_ID = "TechSplashScreenWidget"
		self.SCREEN_NAME = "TechSplashScreen"
		self.EXIT_ID = "TechSplashExit"

	def interfaceScreen(self, iTech):
		self.EXIT_TEXT = localText.getText("TXT_KEY_SCREEN_CONTINUE", ())
		self.nTechs = CyGlobalContext().getNumTechInfos()
		self.iTech = iTech
		self.nWidgetCount = 0
		
		# Create screen
		
		screen = self.getScreen()
		techInfo = CyGlobalContext().getTechInfo(self.iTech)
		screen.setSound(techInfo.getSound())
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.enableWorldSounds( False )
		screen.showWindowBackground( False )
		Screen_Ronkhar = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		self.W_SCREEN = Screen_Ronkhar.getXResolution() #HD example: 1920
		self.H_SCREEN = Screen_Ronkhar.getYResolution() #HD example: 1200
		# screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setDimensions(0, 0, self.W_SCREEN, self.H_SCREEN)
		
		# Create panels
		
		# Main Panel
		szMainPanel = "TechSplashMainPanel"
		self.W_MAIN_PANEL = max(1024,int(self.W_SCREEN*0.7))
		self.H_MAIN_PANEL = max(768,int(self.H_SCREEN*0.7))
		self.X_MAIN_PANEL = int((self.W_SCREEN - self.W_MAIN_PANEL)/2)
		self.Y_MAIN_PANEL = int((self.H_SCREEN - self.H_MAIN_PANEL)/2)
		screen.addPanel( szMainPanel, "", "", true, true,
			self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		
		# Top Panel
		szHeaderPanel = "TechSplashHeaderPanel"
		self.iMarginSpace = 15
		self.X_UPPER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_UPPER_PANEL = self.Y_MAIN_PANEL + self.iMarginSpace
		self.W_UPPER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_UPPER_PANEL = 300
		screen.addPanel( szHeaderPanel, "", "", true, true,
			self.X_UPPER_PANEL, self.Y_UPPER_PANEL, self.W_UPPER_PANEL, self.H_UPPER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM )
		screen.setStyle(szHeaderPanel, "Panel_DawnBottom_Style")
		
		# Icon Panel
		self.X_ICON_PANEL = self.X_UPPER_PANEL + self.iMarginSpace + 2
		self.H_ICON_PANEL = 135#self.H_MAIN_PANEL - (self.iMarginSpace * 2)
		self.Y_ICON_PANEL = self.Y_UPPER_PANEL + self.iMarginSpace + 33
		self.W_ICON_PANEL = 140
		
		szIconPanel = "IconPanel"
		screen.addPanel( szIconPanel, "", "", true, true,
			self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_UPPER_PANEL-(self.iMarginSpace * 2), self.H_UPPER_PANEL-(self.iMarginSpace * 4), PanelStyles.PANEL_STYLE_MAIN_TAN15 )
		screen.setStyle(szIconPanel, "Panel_TechDiscover_Style")
		
		# Icon Panel
		szIconPanel = "IconPanelGlow"
		screen.addPanel( szIconPanel, "", "", true, true,
			self.X_ICON_PANEL, self.Y_ICON_PANEL, self.W_ICON_PANEL, self.H_ICON_PANEL, PanelStyles.PANEL_STYLE_MAIN_TAN15 )
		screen.setStyle(szIconPanel, "Panel_TechDiscoverGlow_Style")
		

		self.X_LOWER_PANEL = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_LOWER_PANEL = self.Y_UPPER_PANEL + self.H_UPPER_PANEL + self.iMarginSpace - 10
		self.W_LOWER_PANEL = self.W_MAIN_PANEL - (self.iMarginSpace * 2)
		self.H_LOWER_PANEL = 275#self.H_MAIN_PANEL - (self.iMarginSpace * 2)

		# Bottom Panel
		szTextPanel = "TechSplashTextPanel"
		screen.addPanel( szTextPanel, "", "", true, true,
			self.X_LOWER_PANEL+self.iMarginSpace, self.Y_LOWER_PANEL, self.W_LOWER_PANEL-(self.iMarginSpace * 2), self.H_LOWER_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		screen.setStyle(szTextPanel, "Panel_TanT_Style")
		
		self.X_EXIT = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2) - 55
		self.Y_EXIT = self.Y_MAIN_PANEL + self.H_MAIN_PANEL - 45
		self.W_EXIT = 120
		self.H_EXIT = 30
		
		# Exit Button
		screen.setButtonGFC("Exit", localText.getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT , self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		
		self.X_SPECIAL_PANEL = self.X_LOWER_PANEL + self.iMarginSpace
		self.Y_SPECIAL_PANEL = self.Y_LOWER_PANEL + self.iMarginSpace + 25
		self.W_SPECIAL_PANEL = self.W_LOWER_PANEL - (self.iMarginSpace * 2)
		self.H_SPECIAL_PANEL = 250
		
		# Special Panel
		szSpecialPanel = "TechSplashSpecialPanel"
		screen.addPanel( szSpecialPanel, "", "", true, true,
				self.X_SPECIAL_PANEL+self.iMarginSpace, self.Y_SPECIAL_PANEL, self.W_SPECIAL_PANEL-(self.iMarginSpace * 2), self.H_SPECIAL_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(szSpecialPanel, "Panel_Black25_Style")
		
		self.X_ALLOWS_PANEL = self.X_LOWER_PANEL + self.iMarginSpace
		self.Y_ALLOWS_PANEL = self.Y_SPECIAL_PANEL + self.H_SPECIAL_PANEL+ self.iMarginSpace + 15
		self.W_ALLOWS_PANEL = self.W_LOWER_PANEL - (self.iMarginSpace * 2)
		self.H_ALLOWS_PANEL = 80
		
		# Allows Panel
		panelName = self.getNextWidgetName()
		screen.addPanel( panelName, "", "", false, true,
                                 self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL, self.W_ALLOWS_PANEL-(self.iMarginSpace * 2), self.H_ALLOWS_PANEL, PanelStyles.PANEL_STYLE_IN )
		screen.setStyle(panelName, "Panel_Black25_Style")
		
		# Add Contents
		
		# Title
		szTech = techInfo.getDescription()
		self.X_TITLE = self.X_MAIN_PANEL + (self.W_MAIN_PANEL / 2)
		self.Y_TITLE = self.Y_UPPER_PANEL + 12
		self.Z_CONTROLS = -1.3
		
		screen.setLabel(self.getNextWidgetName(), "Background", u"<font=4>" + szTech.upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY,
			self.X_TITLE, self.Y_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		# Tech Icon
		self.W_ICON = 64#90
		self.H_ICON = 64#90
		self.X_ICON = self.X_UPPER_PANEL + 56#23#42
		self.Y_ICON = self.Y_UPPER_PANEL + (self.H_UPPER_PANEL / 2) - (self.H_ICON)# + 17
		screen.addDDSGFC(self.getNextWidgetName(), techInfo.getButton(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, self.iTech, -1 )
		
		# Tech Quote
		if techInfo.getQuote():
			szQuotePanel = "TechSplashQuotePanel"
			#screen.addPanel( szQuotePanel, "", "", true, true,
             #                    self.X_QUOTE, self.Y_QUOTE, self.W_QUOTE, self.H_QUOTE, PanelStyles.PANEL_STYLE_IN )
		
			self.X_QUOTE = self.X_UPPER_PANEL + self.W_ICON_PANEL + (self.iMarginSpace * 2)
			self.Y_QUOTE = self.Y_UPPER_PANEL + self.iMarginSpace + 36
			self.W_QUOTE = self.W_MAIN_PANEL - self.W_ICON_PANEL - 3 * self.iMarginSpace
			self.H_QUOTE = self.H_UPPER_PANEL - (self.iMarginSpace * 2) - 38
		
			screen.addMultilineText( "Text", techInfo.getQuote(),
						 self.X_QUOTE, self.Y_QUOTE + self.iMarginSpace*2, self.W_QUOTE - (self.iMarginSpace * 2), self.H_QUOTE - (self.iMarginSpace * 2), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
		# Special
		szSpecialTitle = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()) + u"</font>"
		szSpecialTitleWidget = "SpecialTitle"
		screen.setText(szSpecialTitleWidget, "", szSpecialTitle, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_SPECIAL_PANEL+self.iMarginSpace, self.Y_SPECIAL_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		listName = self.getNextWidgetName()
		
		szSpecialText = CyGameTextMgr().getTechHelp(self.iTech, True, False, False, True, -1)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANEL+10, self.Y_SPECIAL_PANEL+5, self.W_SPECIAL_PANEL-20, self.H_SPECIAL_PANEL-20, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
		
		# Allows
		szAllowsTitleDesc = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_ALLOWS", ()) + ":" + u"</font>"
		szAllowsTitleWidget = "AllowsTitle"
		screen.setText(szAllowsTitleWidget, "", szAllowsTitleDesc, CvUtil.FONT_LEFT_JUSTIFY,
			       self.X_ALLOWS_PANEL+self.iMarginSpace, self.Y_ALLOWS_PANEL - 20, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		for j in range( CyGlobalContext().getNumUnitClassInfos() ):
			eLoopUnit = CyGlobalContext().getCivilizationInfo(CyGlobalContext().getGame().getActiveCivilizationType()).getCivilizationUnits(j)
			if (eLoopUnit != -1):
				if (isTechRequiredForUnit(self.iTech, eLoopUnit)):
	        			screen.attachImageButton( panelName, "", CyGlobalContext().getActivePlayer().getUnitButton(eLoopUnit), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
								  WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

		for j in range(CyGlobalContext().getNumBuildingClassInfos()):
			bTechFound = 0
			eLoopBuilding = CyGlobalContext().getCivilizationInfo(CyGlobalContext().getGame().getActiveCivilizationType()).getCivilizationBuildings(j)
			if (eLoopBuilding != -1):
				if (isTechRequiredForBuilding(self.iTech, eLoopBuilding)):
	        			screen.attachImageButton( panelName, "", CyGlobalContext().getBuildingInfo(eLoopBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
								  WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, eLoopBuilding, 1, False )

		for j in range(CyGlobalContext().getNumProjectInfos()):
			bTechFound = 0
			if (isTechRequiredForProject(self.iTech, j)):
				screen.attachImageButton( panelName, "", CyGlobalContext().getProjectInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM,
							  WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT, j, 1, False )
							  				

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount * self.nTechs + self.iTech)
		self.nWidgetCount += 1
		return szName
		
	# returns a unique ID for this screen
	def getScreen(self):
		screen = CyGInterfaceScreen(self.SCREEN_NAME + str(self.iTech), self.nScreenId)
		return screen
					
	def handleInput( self, inputClass ):
		if ( inputClass.getData() == int(InputTypes.KB_RETURN) ):
			self.getScreen().hideScreen()
			return 1
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.EXIT_ID):
				self.getScreen().hideScreen()
			return 1
		return 0
		
	def update(self, fDelta):
		return

		
		
