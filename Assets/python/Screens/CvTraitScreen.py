#
# Rise from Erebus v1.4 / v2.0
#
# Interface for DynTraits
# by ArcticNightWolf  
# DynTraits developped by GreyFox, into rife dll moved/implemented by Valkrionn
#
#  7th / X   / 2011 - ANW - initial version
# 10th / XII / 2011 - ANW - the interface
# 16th / XII / 2011 - ANW - implementing sort functions
#
# Code might be un-optimized, since I was creating it in on-the-fly python mode
#   which changes the behaviour of the code - needs optimalization!
#

from CvPythonExtensions import *
import CvScreenEnums
import ScreenInput
import CvUtil
import Popup as PyPopup

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()

def showTraitPopup(argsList):
	add = argsList[0]
	rem = argsList[1]
	
	if add == "" and rem == "":
		return
	
	popup = PyPopup.PyPopup(-1)

	szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), false)
	if not szTitle == "":
		popup.setHeaderString(szTitle)

	imageH = 48   # Height of the image
	imageW = 344  # Width of the image
	imageY = 0    # Y position of the image
	if not add == "":
		popup.addDDS(ArtFileMgr.getInterfaceArtInfo("INTERFACE_DYNAMIC_TRAITS_GAIN").getPath(), 0, imageY, imageH, imageW)
		imageY += imageH
		addedTraits = add.split()
		bAddCR = False
		szAdd = ""
		for trait in addedTraits:
			if bAddCR:
				szAdd += "\n"
			# If this is in a chain show the parent and the level
			if gc.getTraitInfo(int(trait)).getLevel() > 1:
				szAdd += str(gc.getTraitInfo(gc.getTraitInfo(int(trait)).getParentTrait()).getText()) + " Lvl: " + str(gc.getTraitInfo(int(trait)).getLevel())
			else:
				szAdd += str(gc.getTraitInfo(int(trait)).getText())
			bAddCR = True
			imageY +=5
		popup.setBodyString(szAdd)
	
	if not rem == "":
		popup.addDDS(ArtFileMgr.getInterfaceArtInfo("INTERFACE_DYNAMIC_TRAITS_LOSE").getPath(), 0, imageY, imageH, imageW)
		removedTraits = rem.split()
		bAddCR = False
		szRemove = ""
		for trait in removedTraits:
			if bAddCR:
				szRemove += "\n"
			szRemove += str(gc.getTraitInfo(int(trait)).getText())
			bAddCR = True
		popup.setBodyString(szRemove)

	popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)

class CvTraitScreen:
	"DynTraits's screen"
	def __init__(self):
	
		self.SCREEN_NAME            = "DynTraitScreen"
		self.SCREEN_TITLE           = u"TRAIT OVERVIEW"
		self.MANAGER_SCREEN_ID      = self.SCREEN_NAME + "MainWindow"
		
		self.BACKGROUND_ID          = self.SCREEN_NAME + "BackgroundImage"
		self.TOP_BG_PANEL_ID        = self.SCREEN_NAME + "TopBGPanel"
		self.BOTTOM_BG_PANEL_ID     = self.SCREEN_NAME + "BottomBGPanel"
		
		self.HEADER_ID              = self.SCREEN_NAME + "Header"
		self.EXIT_ID                = self.SCREEN_NAME + "ExitButton"
		
		self.SCROLL_AREA_ID         = self.SCREEN_NAME + "ScrollArea"
		self.PANEL_LIST_ID          = self.SCREEN_NAME + "MainPanel"
		self.PANEL_TRAIT_INFO_ID    = self.SCREEN_NAME + "TraitInfoPanel"
		self.PANEL_LH_INFO_ID       = self.SCREEN_NAME + "LeaderheadInfoPanel"
		
		self.SELECTED_TRAIT_NAME_ID = self.SCREEN_NAME + "SelTraitName"
		self.SELECTED_TRAIT_LEVL_ID = self.SCREEN_NAME + "SelTraitLevl"
		self.SELECTED_TRAIT_PROG_ID = self.SCREEN_NAME + "SelTraitProg"
		self.SELECTED_TRAIT_PANE_ID = self.SCREEN_NAME + "SelTraitPane"
		self.SELECTED_TRAIT_TEXT_ID = self.SCREEN_NAME + "SelTraitText"
		
		self.TRAIT_NAME_ID          = self.SCREEN_NAME + "TraitName" # + trait number
		self.TRAIT_LEVEL_ID         = self.SCREEN_NAME + "TraitLevel" # + trait number
		self.TRAIT_PROGRESS_ID      = self.SCREEN_NAME + "TraitProgress" # + trait number
		
		self.TRAIT_NAME_LABEL_ID    = self.SCREEN_NAME + "TraitColTitleName"
		self.TRAIT_LEVEL_LABEL_ID   = self.SCREEN_NAME + "TraitColTitleLevel"
		self.TRAIT_PROGR_LABEL_ID   = self.SCREEN_NAME + "TraitColTitleProgress"
		
		self.LH_NAME_ID             = self.SCREEN_NAME + "LeaderHeadName"
		self.LH_STATUS_ID           = self.SCREEN_NAME + "LeaderHeadStatus"
		self.LH_IMAGE_ID            = self.SCREEN_NAME + "LeaderHeadImage"
		self.CIV_NAME_ID            = self.SCREEN_NAME + "CivName"
		
		self.X_SCREEN           = 500
		self.Y_SCREEN           = 396
		self.W_SCREEN           = 1024
		self.H_SCREEN           = 768
		
		## Depth
		self.Z_BACKGROUND       = -2.1
		self.Z_CONTROLS         = self.Z_BACKGROUND - 0.2
		self.DZ                 = -0.2
		
		self.X_TITLE            = self.X_SCREEN
		self.Y_TITLE            = 12
		
		self.X_EXIT             = 994
		self.Y_EXIT             = 726
		
		## The panel with list of traits
		self.X_PANEL_LIST       = 16
		self.Y_PANEL_LIST       = 64
		self.W_PANEL_LIST       = self.W_SCREEN - 432 - 32
		self.H_PANEL_LIST       = self.H_SCREEN - 128

		## The scrolling box with list of traits
		self.X_SCROLL_AREA      = self.X_PANEL_LIST
		self.Y_SCROLL_AREA      = self.Y_PANEL_LIST + 40
		self.W_SCROLL_AREA      = self.W_PANEL_LIST - 22
		self.H_SCROLL_AREA      = self.H_PANEL_LIST - 80
		
		self.TRAIT_PADDING      = 20 # space between traits in the list
		self.X_TRAIT_OFFSET     = 0
		self.Y_TRAIT_OFFSET     = 0
		self.SEL_FORMAT         = u"2b" # formatting of the selected tag - <font=XXX>
		
		self.X_TRAIT_COL_OFFSET = 16 # offset of column labels
		self.Y_TRAIT_COL_TITLE  = 16 # offset of column labels
		self.X_TRAIT_NAME_COL   = 10
		self.X_TRAIT_LEVEL_COL  = self.X_TRAIT_NAME_COL  + 160 # 175
		self.X_TRAIT_PROGR_COL  = self.X_TRAIT_LEVEL_COL + 130 # 320
		
		## Information box about the current trait
		self.X_PANEL_TRAIT_INFO = self.X_PANEL_LIST + self.W_PANEL_LIST + 16;
		self.Y_PANEL_TRAIT_INFO = 64 + 224
		self.W_PANEL_TRAIT_INFO = self.W_SCREEN - (self.W_SCREEN - 400 - 32) - 16
		self.H_PANEL_TRAIT_INFO = self.H_SCREEN - 128 - 224
		
		self.X_ALIGN_TRAIT      = self.X_PANEL_TRAIT_INFO + 32
		self.X_TRAIT_INFO_NAME  = self.X_ALIGN_TRAIT
		self.Y_TRAIT_INFO_NAME  = self.Y_PANEL_TRAIT_INFO + 22
		self.X_TRAIT_INFO_LEVL  = self.X_ALIGN_TRAIT
		self.Y_TRAIT_INFO_LEVL  = self.Y_TRAIT_INFO_NAME + 36
		self.X_TRAIT_INFO_PROG  = self.X_ALIGN_TRAIT
		self.Y_TRAIT_INFO_PROG  = self.Y_TRAIT_INFO_LEVL + 18
		self.X_TRAIT_INFO_TEXT  = self.X_ALIGN_TRAIT
		self.Y_TRAIT_INFO_TEXT  = self.Y_TRAIT_INFO_PROG + 36
		
		self.DEF_TRAIT_NAME     = u"No trait selected"
		self.DEF_TRAIT_PROG     = u"Your level: ??   Maximum level: ??"
		self.DEF_TRAIT_LEVL     = u"Your progress: ??    Goal: ??  ( ?? % )"
		self.DEF_TRAIT_TEXT     = u"Select trait to show info"
		self.DEF_NO_TRAIT_TEXT  = u"No help info available"
		
		## Information about the leader
		self.X_PANEL_LH_INFO    = self.X_PANEL_LIST + self.W_PANEL_LIST + 16;
		self.Y_PANEL_LH_INFO    = 64
		self.W_PANEL_LH_INFO    = self.W_SCREEN - (self.W_SCREEN - 400 - 32) - 16
		self.H_PANEL_LH_INFO    = 208
		
		self.X_LH_IMAGE         = self.X_PANEL_LH_INFO + 16
		self.Y_LH_IMAGE         = self.Y_PANEL_LH_INFO + 16
		self.W_LH_IMAGE         = self.H_PANEL_LH_INFO - 32
		self.H_LH_IMAGE         = self.H_PANEL_LH_INFO - 32
		self.X_LH_NAME          = self.X_LH_IMAGE + self.W_LH_IMAGE + 8
		self.Y_LH_NAME          = self.Y_LH_IMAGE + 18
		self.Y_CIV_NAME         = self.Y_LH_NAME + 24
		
		self.TraitLabelMap    = [ self.TRAIT_NAME_ID, self.TRAIT_LEVEL_ID, self.TRAIT_PROGRESS_ID ]

		self.TraitCount       = 0; # gc.getNumTraitInfos();
		self.RawTraitList     = [()] # /list/: INDEX: iTrait VALUE: /array/ ( eTrait, sz eTrait.getDescription(), iLevel, iLevelMax, iProgress, iProgressGoal , iIndex)
		
		self.SORT_SYMBOL      = u" ^"
		self.REVSORT_SYMBOL   = u" ^*"

		self.UserClicked      = False; # Did user click ? ( Click on already sorted column will reverse the list )
		self.SortingBy        = 0; # 0 Name / 1 Level / 2 Progress
		self.ReverseSort      = False; # Reverse sort ? ( ascending  / descending sort )
		self.SortedTraitList  = [()] # /list/: INDEX: index of trait on screen VALUE: /array/ ( sortingValue, iTrait )
		self.SelectedTrait    = -1 # selected trait 
		self.SelectedTraitP   = -1 # previously selected trait ( for un-highlighting purposes )
		
		## DEBUG: 80 random values
		self.RandomListLVCAP  = (3 , 3 , 2 , 2 , 2 , 0 , 4 , 3 , 2 , 0 , 0 , 3 , 5 , 5 , 2 , 5 , 3 , 5 , 0 , 2 , 4 , 0 , 5 , 4 , 1 , 5 , 1 , 5 , 4 , 0 , 3 , 2 , 0 , 5 , 3 , 3 , 2 , 3 , 4 , 1 , 0 , 4 , 1 , 0 , 3 , 4 , 0 , 5 , 0 , 1 , 4 , 3 , 0 , 2 , 3 , 0 , 1 , 2 , 4 , 0 , 2 , 2 , 3 , 1 , 4 , 0 , 2 , 5 , 5 , 4 , 1 , 2 , 5 , 0 , 0 , 4 , 4 , 4 , 4 , 5)
		self.RandomListLV     = (0 , 0 , 2 , 1 , 1 , 0 , 4 , 0 , 2 , 0 , 0 , 2 , 4 , 1 , 1 , 0 , 0 , 4 , 0 , 2 , 3 , 0 , 2 , 2 , 0 , 3 , 0 , 5 , 4 , 0 , 2 , 2 , 0 , 2 , 3 , 3 , 0 , 3 , 4 , 1 , 0 , 3 , 0 , 0 , 1 , 0 , 0 , 4 , 0 , 0 , 0 , 0 , 0 , 1 , 2 , 0 , 1 , 1 , 4 , 0 , 1 , 0 , 2 , 1 , 1 , 0 , 0 , 3 , 2 , 0 , 0 , 0 , 1 , 0 , 0 , 2 , 1 , 0 , 3 , 2)
		self.RandomListXPC    = (3000 , 3000 , 9000 , 6000 , 6000 , 3000 , 15000 , 3000 , 9000 , 3000 , 3000 , 9000 , 15000 , 6000 , 6000 , 3000 , 3000 , 15000 , 3000 , 9000 , 12000 , 3000 , 9000 , 9000 , 3000 , 12000 , 3000 , 18000 , 15000 , 3000 , 9000 , 9000 , 3000 , 9000 , 12000 , 12000 , 3000 , 12000 , 15000 , 6000 , 3000 , 12000 , 3000 , 3000 , 6000 , 3000 , 3000 , 15000 , 3000 , 3000 , 3000 , 3000 , 3000 , 6000 , 9000 , 3000 , 6000 , 6000 , 15000 , 3000 , 6000 , 3000 , 9000 , 6000 , 6000 , 3000 , 3000 , 12000 , 9000 , 3000 , 3000 , 3000 , 6000 , 3000 , 3000 , 9000 , 6000 , 3000 , 12000 , 9000)
		self.RandomListXP     = (951 , 687 , 454 , 3170 , 3983 , 481 , 14750 , 1586 , 6015 , 1335 , 302 , 1223 , 3733 , 2690 , 5249 , 85 , 2463 , 11207 , 1941 , 5795 , 10419 , 2574 , 6148 , 6994 , 2106 , 663 , 2609 , 9550 , 8277 , 2015 , 8240 , 5387 , 1673 , 3606 , 11682 , 7936 , 2243 , 5207 , 12017 , 5809 , 864 , 11268 , 1297 , 835 , 1628 , 596 , 1630 , 14972 , 850 , 1884 , 129 , 2062 , 42 , 3875 , 4888 , 268 , 2344 , 4874 , 3328 , 2626 , 2992 , 666 , 7591 , 2715 , 1247 , 1480 , 46 , 8687 , 364 , 1409 , 1296 , 411 , 4331 , 2821 , 1956 , 558 , 4543 , 2127 , 9606 , 89)

	def interfaceScreen (self):
		### Generic stuff
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True)
		screen.showWindowBackground(True)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)		
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		### Static stuff ( background, exit buttons, panels etc )
		screen.addDDSGFC( self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel(  self.TOP_BG_PANEL_ID,     u"", u"", True, False, 0, 0,       self.W_SCREEN, 55,    PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel(  self.BOTTOM_BG_PANEL_ID,  u"", u"", True, False, 0, 713,     self.W_SCREEN, 55,    PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.setText(   self.EXIT_ID,   self.BACKGROUND_ID, u"<font=4>EXIT</font>",                   CvUtil.FONT_RIGHT_JUSTIFY,  self.X_EXIT,   self.Y_EXIT,  self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
		screen.setText(   self.HEADER_ID, self.BACKGROUND_ID, u"<font=4b>"+self.SCREEN_TITLE+"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE,  self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL,      -1, -1)
		
		screen.addPanel(  self.PANEL_LIST_ID,       u"", u"", True, False, self.X_PANEL_LIST,       self.Y_PANEL_LIST,          self.W_PANEL_LIST,       self.H_PANEL_LIST,          PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(  self.PANEL_TRAIT_INFO_ID, u"", u"", True, False, self.X_PANEL_TRAIT_INFO, self.Y_PANEL_TRAIT_INFO,    self.W_PANEL_TRAIT_INFO, self.H_PANEL_TRAIT_INFO,    PanelStyles.PANEL_STYLE_MAIN)
		screen.addPanel(  self.PANEL_LH_INFO_ID,    u"", u"", True, False, self.X_PANEL_LH_INFO,    self.Y_PANEL_LH_INFO,       self.W_PANEL_LH_INFO,    self.H_PANEL_LH_INFO,       PanelStyles.PANEL_STYLE_MAIN)
		
		screen.addScrollPanel( self.SCROLL_AREA_ID, self.BACKGROUND_ID, self.X_SCROLL_AREA, self.Y_SCROLL_AREA, self.W_SCROLL_AREA, self.H_SCROLL_AREA, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.setActivation( self.SCROLL_AREA_ID, ActivationTypes.ACTIVATE_NORMAL )

		### Traits
		screen.setText(   self.SELECTED_TRAIT_NAME_ID , self.BACKGROUND_ID, u"<font=4>"+self.DEF_TRAIT_NAME+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_INFO_NAME, self.Y_TRAIT_INFO_NAME, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(   self.SELECTED_TRAIT_LEVL_ID , self.BACKGROUND_ID, u"<font=2b>"+self.DEF_TRAIT_LEVL+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_INFO_LEVL, self.Y_TRAIT_INFO_LEVL, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(   self.SELECTED_TRAIT_PROG_ID , self.BACKGROUND_ID, u"<font=2b>"+self.DEF_TRAIT_PROG+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_INFO_PROG, self.Y_TRAIT_INFO_PROG, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel(  self.SELECTED_TRAIT_PANE_ID, "", "", true, true, self.X_TRAIT_INFO_TEXT, self.Y_TRAIT_INFO_TEXT, 350, 280, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setText(   self.SELECTED_TRAIT_TEXT_ID , self.BACKGROUND_ID, u"<font=2>"+self.DEF_TRAIT_TEXT+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_INFO_TEXT, self.Y_TRAIT_INFO_TEXT, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		screen.setTextAt(self.TRAIT_NAME_LABEL_ID ,  self.PANEL_LIST_ID, u"<font=2b>Trait</font>",    CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_NAME_COL +  self.X_TRAIT_COL_OFFSET,  self.Y_TRAIT_COL_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setTextAt(self.TRAIT_LEVEL_LABEL_ID,  self.PANEL_LIST_ID, u"<font=2b>Level</font>",    CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_LEVEL_COL + self.X_TRAIT_COL_OFFSET,  self.Y_TRAIT_COL_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setTextAt(self.TRAIT_PROGR_LABEL_ID,  self.PANEL_LIST_ID, u"<font=2b>Progress</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_PROGR_COL + self.X_TRAIT_COL_OFFSET,  self.Y_TRAIT_COL_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		
		### Leader / Civilization
		player        = gc.getPlayer(CyGame().getActivePlayer())
		pLH           = gc.getLeaderHeadInfo(player.getLeaderType())
		pCiv          = gc.getCivilizationInfo(player.getCivilizationType())
		
		screen.setText(self.LH_NAME_ID, self.BACKGROUND_ID, u"<font=3b>"+pLH.getDescription()+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LH_NAME, self.Y_LH_NAME, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.CIV_NAME_ID, self.BACKGROUND_ID, u"<font=2>"+pCiv.getDescription()+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_LH_NAME, self.Y_CIV_NAME, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addDDSGFC(self.LH_IMAGE_ID, str(pLH.getButton()), self.X_LH_IMAGE, self.Y_LH_IMAGE, self.W_LH_IMAGE, self.H_LH_IMAGE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		### Dynamic stuff
		self.loadItems()
		self.sortBy(self.SortingBy)
		self.drawTraits()
		
	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.TRAITS_SCREEN)
		
	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()
		return None
		
	def update(self, fDelta):
		return None
		
	def drawTraits(self):
	
		self.SelectedTrait = -1;
		self.SelectedTraitP = -1;
	
		numInfos = self.TraitCount;
		
		for i in range(numInfos):
		
			iTrait = self.SortedTraitList[i][1]
			self.drawTraitEntry(iTrait, i, False, False)

		return
		
	def drawTraitEntry(self, piTrait, pId, pReplace, pHighlight):

		player        = gc.getPlayer(CyGame().getActivePlayer())
		pLH           = gc.getLeaderHeadInfo(player.getLeaderType())
		pCiv          = gc.getCivilizationInfo(player.getCivilizationType())
		
		screen = self.getScreen()
		traitData = self.RawTraitList[piTrait]
	
		szInfo =  traitData[1]   #pTrait.getDescription()
		szInfo2 = str(traitData[2]) + " / Max: " + str(traitData[3])   #"1 / 5"
		if (traitData[5]!=0):
			szInfo3 = str(traitData[4]) + " / Goal: " + str(traitData[5]) + " ( "+str(traitData[4]*100/traitData[5])+"% )"  #"1575 / 21000 ( 13.3% )"
		else:
			szInfo3 = "Static Trait"
		szi = str(pId)
		
		if (pReplace == True):
			screen.deleteWidget(self.TRAIT_NAME_ID    +szi)
			screen.deleteWidget(self.TRAIT_LEVEL_ID   +szi)
			screen.deleteWidget(self.TRAIT_PROGRESS_ID+szi)
		
			
		szHighlight = ""
		if (pHighlight == True):
			szHighlight = self.SEL_FORMAT
		else:
			szHighlight = "2"
			
		screen.setTextAt(self.TRAIT_NAME_ID    +szi,  self.SCROLL_AREA_ID, u"<font="+szHighlight+u">"+szInfo+ u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TRAIT_NAME_COL + self.X_TRAIT_OFFSET,  (pId*self.TRAIT_PADDING) + self.Y_TRAIT_OFFSET, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_TRAIT,gc.getInfoTypeForString(traitData[0].getType()), player.getCivilizationType() )
		screen.setTextAt(self.TRAIT_LEVEL_ID   +szi,  self.SCROLL_AREA_ID, u"<font="+szHighlight+u">"+szInfo2+u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TRAIT_LEVEL_COL + self.X_TRAIT_OFFSET, (pId*self.TRAIT_PADDING) + self.Y_TRAIT_OFFSET, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setTextAt(self.TRAIT_PROGRESS_ID+szi,  self.SCROLL_AREA_ID, u"<font="+szHighlight+u">"+szInfo3+u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TRAIT_PROGR_COL + self.X_TRAIT_OFFSET, (pId*self.TRAIT_PADDING) + self.Y_TRAIT_OFFSET, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		return None
		
	def updateTraitInfo(self):
		screen = self.getScreen()
		self.loadItems()
		self.UserClicked = False
		self.sortBy(self.SortingBy)
		if (self.SelectedTrait != -1):
			eSelected = self.RawTraitList[self.SortedTraitList[self.SelectedTrait][1]]
	
			szInfo =  eSelected[1]   #pTrait.getDescription()
			szInfo2 = "Your level: "+str(eSelected[2]) + "   Maximum level: " + str(eSelected[3])   #"1 / 5"
			if (eSelected[5]!=0):
				szInfo3 = "Your progress: "+ str(eSelected[4]) + "    Goal: " + str(eSelected[5]) + "  ( "+str(eSelected[4]*100/eSelected[5])+"% )"  #"1575 / 21000 ( 13.3% )"
			else:
				szInfo3 ="Static Trait"
			screen.deleteWidget(self.SELECTED_TRAIT_NAME_ID)
			screen.setText( self.SELECTED_TRAIT_NAME_ID , self.BACKGROUND_ID, u"<font=4><b>"+szInfo+           u"</b></font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_INFO_NAME, self.Y_TRAIT_INFO_NAME,self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.deleteWidget(self.SELECTED_TRAIT_LEVL_ID)
			screen.setText(   self.SELECTED_TRAIT_LEVL_ID , self.BACKGROUND_ID, u"<font=2b>"+szInfo2+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_INFO_LEVL, self.Y_TRAIT_INFO_LEVL, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.deleteWidget(self.SELECTED_TRAIT_PROG_ID)
			screen.setText(   self.SELECTED_TRAIT_PROG_ID , self.BACKGROUND_ID, u"<font=2b>"+szInfo3+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_INFO_PROG, self.Y_TRAIT_INFO_PROG, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			screen.deleteWidget(self.SELECTED_TRAIT_TEXT_ID)
			screen.deleteWidget(self.SELECTED_TRAIT_PANE_ID)
			screen.addPanel(  self.SELECTED_TRAIT_PANE_ID, "", "", true, true, self.X_TRAIT_INFO_TEXT, self.Y_TRAIT_INFO_TEXT, 350, 280, PanelStyles.PANEL_STYLE_BLUE50 )
			screen.attachMultilineText( self.SELECTED_TRAIT_PANE_ID, self.SELECTED_TRAIT_TEXT_ID , u"<font=2>"+   CyGameTextMgr().parseTraitReqs(eSelected[6])+ u"</font>", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
			if (self.SelectedTraitP != -1):
				thing = self.SortedTraitList[self.SelectedTraitP][1]
				eSelectedP = self.RawTraitList[thing]
				self.drawTraitEntry(self.SortedTraitList[self.SelectedTraitP][1], self.SelectedTraitP, True, False)

			self.drawTraitEntry(self.SortedTraitList[self.SelectedTrait][1], self.SelectedTrait, True, True)
			
			self.SelectedTraitP = self.SelectedTrait	
		return
	
	def loadItems(self):
		randNum = CyGame().getSorenRandNum
		NumDisplayTraits = 0
		NumTotalTraits = gc.getNumTraitInfos()
		player = gc.getPlayer(CyGame().getActivePlayer())		
		leaderhead = gc.getLeaderHeadInfo(player.getLeaderType())
		leaderclass = gc.getLeaderClassInfo(leaderhead.getLeaderClass())
		bupdate=False
		for i in range(NumTotalTraits):
			kTrait = gc.getTraitInfo(i)
			if kTrait.getLevel() > 1: continue
			if kTrait.getTraitClass()<0: continue
			if player.getNumMaxTraitPerClass(kTrait.getTraitClass())<=0 : continue
			if player.getNumTraitPerClass(kTrait.getTraitClass())>=player.getNumMaxTraitPerClass(kTrait.getTraitClass()) and not player.hasTrait(i):continue
			if (player.getMinRequiredPoints(i)==0 and not player.hasTrait(i)): continue
			if kTrait.getTraitClass()==gc.getInfoTypeForString("TRAITCLASS_EMERGENT") and not player.hasTrait(i) : continue
			# TODO: Load hidden trait into display if it is actually acquired. Currentlty, it's always hidden:
			if kTrait.isGraphicalOnly(): continue
			if self.SelectedTrait==-1 : 
				self.SelectedTrait=0
				bupdate=True
			NumDisplayTraits += 1

		self.TraitCount = NumDisplayTraits
		self.RawTraitList = [( None , "", 0, 0, 0, 0)] * self.TraitCount
		#player = gc.getPlayer(CyGame().getActivePlayer())		
		traitIndex = 0
		for i in range(NumTotalTraits):
			kTrait = gc.getTraitInfo(i)
			if kTrait.getLevel() > 1: continue
			if kTrait.getTraitClass()<0: continue
			if player.getNumMaxTraitPerClass(kTrait.getTraitClass())<=0 : continue
			if player.getNumTraitPerClass(kTrait.getTraitClass())>=player.getNumMaxTraitPerClass(kTrait.getTraitClass()) and not player.hasTrait(i):continue
			if (player.getMinRequiredPoints(i)==0 and not player.hasTrait(i)): continue
			if kTrait.getTraitClass()==gc.getInfoTypeForString("TRAITCLASS_EMERGENT") and not player.hasTrait(i) : continue
			# TODO: Load hidden trait into display if it is actually acquired. Currentlty, it's always hidden:
			if kTrait.isGraphicalOnly(): continue
			
			iLv = self.getKnownLevel(i)
			iLvM = self.calculateMaxLevel(kTrait)
			
			iXp = player.getTraitPoints(i)
			iXpC = player.getMinRequiredPointsNextTrait(i)

			self.RawTraitList[traitIndex] = (kTrait, kTrait.getDescription(), iLv, iLvM, iXp, iXpC, i)
			traitIndex += 1
		
		if bupdate:
			self.updateTraitInfo()
		return
		
	def calculateMaxLevel(self, kTrait):
		
		eLastTrait = self.getLastTrait(kTrait)
		
		iLvM = eLastTrait.getLevel()
		if iLvM == 0:
			iLvM = 1
		
		return iLvM
			
	def getLastTrait(self, kTrait):
		
		kLastTrait = kTrait
		if kTrait.getNextTrait() != -1:
			kLastTrait = self.getLastTrait(gc.getTraitInfo(kTrait.getNextTrait()))
		
		return kLastTrait
			
	def getKnownLevel(self, eTrait):
		
		iKnownLevel = 0
		player = gc.getPlayer(CyGame().getActivePlayer())
		while player.hasTrait(eTrait):
			iKnownLevel += 1
			eTrait = gc.getTraitInfo(eTrait).getNextTrait()
			if eTrait == -1:
				break
		
		return iKnownLevel
			
	def getMinTrait(self):
		player = gc.getPlayer(CyGame().getActivePlayer())
		iMinTrait = 0
		
		for i in range(self.TraitCount):
			kTrait = gc.getTraitInfo(i)
			
			if player.hasTrait(i):
				if not kTrait.isCoreTrait():
					if player.getTraitPoints(i) < iMinTrait or iMinTrait == 0:
						iMinTrait = player.getTraitPoints(i)
		return iMinTrait
		
	def sortBy(self, piSortType):
		if (self.SortingBy == piSortType and self.UserClicked): 
			self.ReverseSort = not self.ReverseSort
			self.UserClicked = False;
		
		self.SortingBy = piSortType
		
		if (self.ReverseSort == True):
			mark = self.REVSORT_SYMBOL
		else:
			mark = self.SORT_SYMBOL
		
		self.loadItems()
		screen = self.getScreen()
		
		screen.deleteWidget(self.TRAIT_NAME_LABEL_ID)
		screen.deleteWidget(self.TRAIT_LEVEL_LABEL_ID)
		screen.deleteWidget(self.TRAIT_PROGR_LABEL_ID)
		if (piSortType == 0): 
			tMark = mark
			self.SortedTraitList = [("", 0)] * self.TraitCount
			for i in range(self.TraitCount):
				self.SortedTraitList[i] = (self.RawTraitList[i][1], i)
			self.SortedTraitList.sort()
		else: tMark = ""
		screen.setTextAt(self.TRAIT_NAME_LABEL_ID ,  self.PANEL_LIST_ID, u"<font=2b>Trait"+tMark+u"</font>",    CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_NAME_COL +  self.X_TRAIT_COL_OFFSET,  self.Y_TRAIT_COL_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		if (piSortType == 1): 
			tMark = mark
			self.SortedTraitList = [(0, 0)] * self.TraitCount
			for i in range(self.TraitCount):
				self.SortedTraitList[i] = (self.RawTraitList[i][2]*(-1000)+(self.RawTraitList[i][4]*100/max(1,self.RawTraitList[i][5]))*(-1), i) 
			self.SortedTraitList.sort()
		else: tMark = ""
		screen.setTextAt(self.TRAIT_LEVEL_LABEL_ID,  self.PANEL_LIST_ID, u"<font=2b>Level"+tMark+u"</font>",    CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_LEVEL_COL + self.X_TRAIT_COL_OFFSET,  self.Y_TRAIT_COL_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		if (piSortType == 2):
			tMark = mark
			self.SortedTraitList = [("", 0)] * self.TraitCount
			for i in range(self.TraitCount):
				self.SortedTraitList[i] = (self.RawTraitList[i][4]*100/max(1,self.RawTraitList[i][5]), i)
			self.SortedTraitList.sort()	
		else: tMark = ""
		screen.setTextAt(self.TRAIT_PROGR_LABEL_ID,  self.PANEL_LIST_ID, u"<font=2b>Progress"+tMark+u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_TRAIT_PROGR_COL + self.X_TRAIT_COL_OFFSET,  self.Y_TRAIT_COL_TITLE, self.Z_CONTROLS, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		
		if (self.ReverseSort == True):
			self.SortedTraitList.reverse()

	def handleInput(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			fctName = inputClass.getFunctionName()
			if (fctName == self.EXIT_ID ):	
				screen.hideScreen()
				return 1
			if (fctName == self.TRAIT_NAME_LABEL_ID):
				self.UserClicked = True;
				self.sortBy(0)
				self.drawTraits()
				return 1
			if (fctName == self.TRAIT_LEVEL_LABEL_ID):
				self.UserClicked = True;
				self.sortBy(1)
				self.drawTraits()
				return 1
			if (fctName == self.TRAIT_PROGR_LABEL_ID):
				self.UserClicked = True;
				self.sortBy(2)
				self.drawTraits()
				return 1
			if (fctName in self.TraitLabelMap):
				self.SelectedTrait = inputClass.getID()
				self.updateTraitInfo()
				return 1
		return 0
		
