## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
#
# CIV Python Tools Code
#
import CvUtil
import PyHelpers
import Popup as PyPopup
import CvScreenEnums
from CvPythonExtensions import *

PyPlayer = PyHelpers.PyPlayer
PyGame = PyHelpers.PyGame

# globals
gc = CyGlobalContext()
iLastSelectedObject = -1
gSetUnit = 0

def toggleDebugMode():
	return

def adjustUnitMovement(iPlayer, iUnitType, iNumMoves):
	player = PyPlayer(iPlayer)
	for unit in player.getUnitList():
		if ( int(unit.getUnitType()) == iUnitType ):
			unit.setMoves(iNumMoves)

def giveUnitsLotsOfMoves():
	playerTeam = gc.getActivePlayer().getTeam(0)
	playerTeam.changeExtraMoves(DomainTypes.DOMAIN_LAND, 1000)
	playerTeam.changeExtraMoves(DomainTypes.DOMAIN_SEA, 1000)
	playerTeam.changeExtraMoves(DomainTypes.DOMAIN_AIR, 1000)
	
############################### DEBUG TOOLS ####################################
class CvDebugTools:
	def __init__(self):
		self._bDebugMode = False
		self.iActiveEffect = -1
		self.pEffectPlot = None
	
	def getDebugMode( self ):
		return self._bDebugMode
		
	def setDebugMode( self, bVal ):
		self._bDebugMode = bVal		
		CyInterface().addImmediateMessage( "CvDebugTools.setDebugMode set to %s" % self.bDebugMode, "" )

	def notifyInput( self, argsList ):
		#print "Python Debug Mode Notify"
		return 0
	
	def initEffectViewer( self, argsList ):
		px,py = argsList
		pPlot = CyMap().plot(px,py)
		popup = PyPopup.PyPopup( CvUtil.PopupTypeEffectViewer, EventContextTypes.EVENTCONTEXT_SELF )
		popup.setSize(550,300)
		popup.setUserData( (px,py) )
		popup.setHeaderString( "Python Debug Tools: Object Placer" )
		# Pulldown0 - Player Selection
		numEffects = gc.getNumEffectInfos()	# get total # of units from Game
		
		popup.createPythonPullDown("Choose an Effect")
		for i in range(gc.getNumEffectInfos()):
			popup.addPullDownString(gc.getEffectInfo(i).getType(), i)
		
		popup.createPythonEditBox( "Default", "Modify the scale of the effect" )
		popup.createPythonEditBox( "Default", "Modify the update rate" )
		
		# Launch Popup
		popup.launch()
		return 0
	
	def applyEffectViewer(self, playerID, userData, popupReturn):
		px,py = userData
		self.pEffectPlot = CyMap().plot(px,py)
		
		if self.pEffectPlot.isNone():
			return 0
		
		self.iActiveEffect = popupReturn.getSelectedPullDownValue( 0 )
		
		CyEngine().triggerEffect(self.iActiveEffect, self.pEffectPlot.getPoint())
		#scale = popupReturn.getSelectedListBoxValue( 0 )
		#updateRate = int( popupReturn.getEditBoxString( 0 ) )

	############################
	## UNIT / CITY PLAYER 
	############################
	def initUnitPicker( self, argsList ):
		'initUnitPicker - for placing units & cities'
		px,py = argsList
		pPlot = CyMap().plot(px,py)
		popup = PyPopup.PyPopup( CvUtil.EventPlaceObject, EventContextTypes.EVENTCONTEXT_ALL )
		popup.setSize(400,600)
		popup.setPosition(600,25)
		popup.setUserData( (px,py) )
		popup.setHeaderString( "Python Debug Tools: Object Placer" )
		#popup.setBodyString( "Choose Player:" )

		# Pulldown0 - Player Selection
		iNumUnits = gc.getNumUnitInfos()	# get total # of units from Game
		iOwner = pPlot.getOwner()
		if ( iOwner == PlayerTypes.NO_PLAYER ):
			iOwner = gc.getGame().getActivePlayer()
		popup.createPythonPullDown("Choose a Player")
		popup.addPullDownString(gc.getPlayer(iOwner).getName(), iOwner)
		for i in range(gc.getMAX_PLAYERS()):
			if (gc.getPlayer(i).isEverAlive()):
				if (i != iOwner):
					popup.addPullDownString(gc.getPlayer(i).getName(), i)

		popup.addSeparator()
		
		# ListBox0 - Unit List w/ City also selectable
		#popup.setBodyString( "Select Game Object to Add:" )

		popup.createPythonListBox( "" )
		popup.addListBoxString( 'Nothing', iNumUnits + 1 )   # for clean exit
		popup.addSeparator()
		lastSelection = u""
		if ( iLastSelectedObject == -1 ):
			pass
		elif ( iLastSelectedObject == iNumUnits+1 ):
			lastSelection = u'Nothing'
		elif ( iLastSelectedObject == iNumUnits ):
			lastSelection = u'City'
		else:
			lastSelection = gc.getUnitInfo(iLastSelectedObject).getDescription()
		if ( not iLastSelectedObject == -1 ):
			popup.addListBoxString( lastSelection, iLastSelectedObject )
		popup.addListBoxString( u'City', iNumUnits )    	# list City first

		# sort units alphabetically
		unitsList=[(0,0)]*iNumUnits
		for j in range( iNumUnits ):
			unitsList[j] = (gc.getUnitInfo(j).getDescription(), j)
		unitsList.sort()	

		for j in range( iNumUnits ):			
			popup.addListBoxString( unitsList[j][0], unitsList[j][1])
		
		# EditBox0 - Customize how many units to build
		#popup.setBodyString( "How many objects?" )
		popup.createPythonEditBox( "1", "This allows you to create multiple units." )
		
		# Launch Popup
		#popup.setSize( 400, 600 )
		popup.launch()
		return 0
	
	def applyUnitPicker( self, argsList ):
		'Apply Unit Picker'
		popupReturn, userData = argsList
		px,py = userData
		pPlot = CyMap().plot(px,py)
		
		if pPlot.isNone():
			return 0
		
		# UNIT DEBUG MENU
		playerID = popupReturn.getSelectedPullDownValue( 0 )
		selectedObject = popupReturn.getSelectedListBoxValue( 0 )
		iSpawnNum = int( popupReturn.getEditBoxString( 0 ) )
		
		player = PyPlayer( playerID )
		if ( player.isNone() ):
			return -1   # Error
			
		iNumUnits = gc.getNumUnitInfos()
		global iLastSelectedObject
		iLastSelectedObject = selectedObject
		if ( selectedObject != iNumUnits + 1 ):# Nothing
			
			if ( selectedObject == iNumUnits ):# City"
				player.initCity( px,py )
			
			else:
				player.initUnit( selectedObject, px, py, iSpawnNum )
		else:
			iLastSelectedObject = -1
				
		return 0	
	def cheatEvents ( self ):
		'Cheat an Event in'
		popup = PyPopup.PyPopup( CvUtil.EventCheat, EventContextTypes.EVENTCONTEXT_ALL )
		popup.setHeaderString( "Event Cheat!" )
		# Loop through Event Infos and add names
		for i in range(gc.getNumEventTriggerInfos()):
			trigger = gc.getEventTriggerInfo(i)
			popup.addButton(str(trigger.getType()))
        
		popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)

	def applyCheatEvent(self, argsList ):
		'Apply Event Cheat'
		popupReturn = argsList
		id = popupReturn.getButtonClicked()
        #message = "DEBOOTY Event: %s (%s)" %(id, gc.getActivePlayer().getName())
        #CvUtil.pyPrint(message)
        #iData1 = argsList[1]
		pPlayer = gc.getGame().getActivePlayer()
        #player = PyPlayer( pPlayer )
		player = gc.getPlayer(pPlayer)
        #player.changeGold(id)
		player.trigger(id)
	############################
	## TECH / GOLD CHEAT POPUP
	############################
	def cheatTechs( self ):
		'Cheat techs and gold to the players'
		popup = PyPopup.PyPopup( CvUtil.EventAwardTechsAndGold, EventContextTypes.EVENTCONTEXT_ALL )
		popup.setHeaderString( "Tech & Gold Cheat!" )
		popup.createPullDown()
		popup.addPullDownString( "All", gc.getMAX_CIV_PLAYERS() )
		for i in range( gc.getMAX_CIV_PLAYERS() ):
			if ( gc.getPlayer(i).isAlive() ):
				popup.addPullDownString( gc.getPlayer(i).getName(), i )
		popup.setBodyString( "Modify Player %s:" %( CvUtil.getIcon('gold'),) )
		popup.createPythonEditBox( "0", "Integer value (positive or negative)" )
		
		# Loop through Era Infos and add names
		for i in range(gc.getNumEraInfos()):
			popup.addButton(gc.getEraInfo(i).getDescription())
		
		popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)
	
	def applyTechCheat( self, argsList ):
		'Apply Tech Cheat'
		popupReturn = argsList
		playerID = popupReturn.getSelectedPullDownValue( 0 )
		bAll = 0
		if playerID == gc.getMAX_CIV_PLAYERS():
			bAll = 1
			player = PyGame().getCivPlayerList()
		else:
			player = PyPlayer( playerID )
		era = popupReturn.getButtonClicked()
		
		try:
			goldChange = int( popupReturn.getEditBoxString( 0 ) )
		except:
			return 0
			
		if goldChange:
			if not bAll:
				player.changeGold(goldChange)
			else:
				for i in range(len(player)):
					player[i].changeGold(goldChange)

		for tech in PyGame().getEraTechList(era):
			id = tech.getID()
			if not bAll:
				player.setHasTech( id )
			else:
				for j in range(len(player)):
					player[j].setHasTech( id )
	def RotateUnit(self, Direction, px, py ):
		if ( px != -1 and py != -1 ):
			unit = CyMap().plot(px, py).getUnit(0)
			if ( not unit.isNone() ):
				unitEntity = CyUnitEntity(unit)
				dir = unitEntity.GetUnitFacingDirection( )
				dir += Direction * 0.05;
				unitEntity.SetUnitFacingDirection( dir )

	def resetUnitMovement( self ):
		global g_bDebugMode
		if g_bDebugMode == 0:
			return			
		for i in range(gc.getMAX_PLAYERS()):
			(unit, iter) = gc.getPlayer(i).firstUnit(false)
			while (unit):
				unit.setMoves(0)
				(unit, iter) = gc.getPlayer(i).nextUnit(iter, false)

	def allUnits( self ):
		self.putOneOfEveryUnit();
		
	def allBonuses( self ):
		iNBonuses = gc.getNumBonusInfos()
		map = CyMap()
		if ( iNBonuses < map.getGridWidth() * map.getGridHeight() ):
			for x in range(map.getGridWidth()):
				for y in range((iNBonuses/map.getGridWidth())+1):
					map.plot(x,y).setBonusType( (x + y * map.getGridWidth())%iNBonuses );
		
	def allImprovements( self ):
		iNImprovements = gc.getNumImprovementInfos()
		map = CyMap()
		if ( iNImprovements < map.getGridWidth() * map.getGridHeight() ):
			for x in range(map.getGridWidth()):
				for y in range((iNImprovements/map.getGridWidth())+1):
					map.plot(x,y).setImprovementType( (x + y * map.getGridWidth())%iNImprovements );
		
	def putOneOfEveryUnit( self ):
		pass
		iNUnits = gc.getNumUnitInfos()
		map = CyMap()
		player = gc.getPlayer(0)
		if ( iNUnits < map.getGridWidth() * map.getGridHeight() ):
			for x in range(map.getGridWidth()):
				for y in range((iNUnits/map.getGridWidth())+1):
					player.initUnit( (x + y * map.getGridWidth())%iNUnits, x, y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION )

	def wonderMovie( self ):
		'ShowWonder Movie'
		
		popup = PyPopup.PyPopup( CvUtil.EventShowWonder, EventContextTypes.EVENTCONTEXT_ALL )
		popup.setHeaderString( "Wonder Movie" )
		popup.createPullDown()
		for i in range(gc.getNumBuildingInfos()):
			szMovieFile = gc.getBuildingInfo(i).getMovie()
			if (szMovieFile != None and len(szMovieFile) > 0):
				popup.addPullDownString( gc.getBuildingInfo(i).getDescription(), i )

		for i in range(gc.getNumProjectInfos()):
			szMovieFile = None
			szArtDef = gc.getProjectInfo(i).getMovieArtDef()
			if (len(szArtDef) > 0):
				szMovieFile = CyArtFileMgr().getMovieArtInfo(szArtDef).getPath()
			if (szMovieFile != None and len(szMovieFile) > 0):
				popup.addPullDownString( gc.getProjectInfo(i).getDescription(), gc.getNumBuildingInfos() + i )
			
		popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)
	
	def applyWonderMovie( self, argsList ):
		'Apply Wonder Movie'
		popupReturn = argsList
		wonderID = popupReturn.getSelectedPullDownValue( 0 )
					
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
		popupInfo.setData2(-1)
		popupInfo.setText(u"showWonderMovie")
		
		if wonderID < gc.getNumBuildingInfos():
			popupInfo.setData3(0)
			popupInfo.setData1(wonderID)
		else:
			popupInfo.setData3(2)
			popupInfo.setData1(wonderID - gc.getNumBuildingInfos())

		popupInfo.addPopup(0)

	def cheatEvents2(self):
		"Initiate list of events"
		szText		= "List of available Events."
		iPlayer		= CyGame().getActivePlayer()
		pPlayer		= gc.getPlayer(iPlayer)
		totalWeight	= 0
		popupInfo	= CyPopupInfo()
		popupInfo.setData1(iPlayer)
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("applyCheatEvents2")
		lEvents = []
		for i in xrange(gc.getNumEventTriggerInfos()):
			iPrereq = gc.getEventTriggerInfo(i).getNumPrereqEvents()
			if iPrereq > 0:
				continue
			triggerData = pPlayer.initTriggeredData(i, false, -1, -1, -1, -1, -1, -1, -1, -1, -1)
			if triggerData == None:
				continue
			iWeight = pPlayer.getEventTriggerWeight(i)
			if iWeight <= 0:
				continue
			szButtonText = str(gc.getEventTriggerInfo(i).getType())							# EVENTTRIGGER_AFFLUENT_DUKE
			if szButtonText.startswith("EVENTTRIGGER_"):									# AFFLUENT_DUKE
				szButtonText = szButtonText[13:]
			szButtonText = szButtonText.replace("_"," ")									# AFFLUENT DUKE
			szButtonText = szButtonText.title()												# Affluent Duke
			szButtonText = str(i) + ". " + szButtonText + ", Weight: " + str(iWeight)		# 1. Affluent Duke, Weight: 40
			popupInfo.addPythonButton(szButtonText,"")
			totalWeight += iWeight
			lEvents.append(i)
		if totalWeight > 0:
			szText	+= "\n" + "Total Weight: " + str(totalWeight) + "\n" + "Chance to trigger an event per turn: " + str(gc.getDefineINT("EVENT_CHANCE_PER_TURN")) + "%"
		szText += "\n" + str(lEvents)
		popupInfo.setText(szText)
		popupInfo.addPopup(iPlayer)

	def debugRemoveAIUnits(self):
		"Remove AI units by unitcombat"
		szText		= "Remove AI units by UnitCombat" + "\n" + "(try removing Naval units on infinite load)"
		iPlayer		= CyGame().getActivePlayer()
		popupInfo	= CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("applyRemoveAIUnits")
		popupInfo.addPythonButton("Cancel","")
		popupInfo.addPythonButton("Remove all AI Units","")
		popupInfo.addPythonButton("Remove 50% of the AI Units","")
		for i in xrange(gc.getNumUnitCombatInfos()):
			szButtonText = "Remove all AI " + str(gc.getUnitCombatInfo(i).getDescription())
			popupInfo.addPythonButton(szButtonText,"")
		popupInfo.setText(szText)
		popupInfo.addPopup(iPlayer)

g_CvDebugTools = CvDebugTools()

# def applyCheatEvents2(argsList):
	# gc				= CyGlobalContext()
	# iButtonId		= argsList[0]
	# iPlayer			= argsList[1]
	# pPlayer			= gc.getPlayer(iPlayer)
	# lEvents			= []
	# for i in xrange(gc.getNumEventTriggerInfos()):
		# iPrereq = gc.getEventTriggerInfo(i).getNumPrereqEvents()
		# if iPrereq > 0:
			# continue
		# triggerData = pPlayer.initTriggeredData(i, false, -1, -1, -1, -1, -1, -1, -1, -1, -1)
		# if triggerData == None:
			# continue
		# iWeight = pPlayer.getEventTriggerWeight(i)
		# if iWeight <= 0:
			# continue
		# lEvents.append(i)
	# if lEvents:
		# ### TEST
		# print lEvents
		# pPlayer.trigger(lEvents[iButtonId])

# CvScreensInterface.applyCheatEvents2 = applyCheatEvents2