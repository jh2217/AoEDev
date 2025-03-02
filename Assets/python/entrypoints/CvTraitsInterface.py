# ######################################################
# Dynamic Traits specific callbacks
# Author: Grey Fox
# ######################################################

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import CvEventInterface
import sys
import PyHelpers

PyInfo = PyHelpers.PyInfo
PyPlayer = PyHelpers.PyPlayer

from FoxTools import *

# Only used if USE_ON_TRAIT_GAINED_CALLBACK
# is set to 1 in PythonCallbackDefines.xml
def onTraitGained(argsList):
	eTrait, bParent, iPlayer = argsList
	gc 				= CyGlobalContext()
	Manager		 	= CvEventInterface.getEventManager()

	if Manager.Tools == None: return

	getInfoType 	= gc.getInfoTypeForString
	pPlayer 		= gc.getPlayer(iPlayer)
	game 			= CyGame()
	iGameTurn 		= game.getGameTurn()

	iTraitClass = gc.getTraitInfo(eTrait).getTraitClass()
	if (iTraitClass == getInfoType('CIVILIZATION_TRAIT')) or (iTraitClass == getInfoType('TECH_TRAIT')):
		szName = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDescription()
	else:
		szName = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription()

	if gc.getTraitInfo(eTrait).getParentTrait() == -1:
		szDesc = gc.getTraitInfo(eTrait).getDescription()
		szText = CyTranslator().getText("TXT_KEY_GAINED_TRAIT",(szName, szDesc,))
	else:
		eParentTrait = gc.getTraitInfo(eTrait).getParentTrait()
		szDesc = gc.getTraitInfo(eParentTrait).getDescription()
		iLevel = gc.getTraitInfo(eTrait).getLevel()
		szText = CyTranslator().getText("TXT_KEY_GAINED_LEVEL_TRAIT",(szName, iLevel, szDesc,))

	if gc.getTraitInfo(eTrait).getImage() != "":
		szArt = gc.getTraitInfo(eTrait).getImage()
	else:
		szArt = 'art/interface/popups/TraitsGained.dds'


	if pPlayer.isHuman() and iGameTurn > 1:
		Manager.Tools.addPopupMsg("Gained", szText, szArt)

	DbgWnd = Manager.DbgWnd
	szMsg = "Turn(%d): %s [NEWLINE]" % (iGameTurn, szText)
	DbgWnd.addLine("Trait Gains", iPlayer, szMsg )


# Only used if USE_ON_TRAIT_LOST_CALLBACK
# is set to 1 in PythonCallbackDefines.xml
def onTraitLost(argsList):
	eTrait, bParent, iPlayer = argsList
	gc 				= CyGlobalContext()
	Manager		 	= CvEventInterface.getEventManager()

	if Manager.Tools == None: return

	getInfoType 	= gc.getInfoTypeForString
	pPlayer 		= gc.getPlayer(iPlayer)
	game 			= CyGame()
	iGameTurn 		= game.getGameTurn()

	iTraitClass = gc.getTraitInfo(eTrait).getTraitClass()
	if (iTraitClass == getInfoType('CIVILIZATION_TRAIT')) or (iTraitClass == getInfoType('TECH_TRAIT')):
		szName = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDescription()
	else:
		szName = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDescription()

	if gc.getTraitInfo(eTrait).getParentTrait() == -1:
		szDesc = gc.getTraitInfo(eTrait).getDescription()
		szText = CyTranslator().getText("TXT_KEY_LOST_TRAIT",(szName, szDesc,))
	else:
		eParentTrait = gc.getTraitInfo(eTrait).getParentTrait()
		szDesc = gc.getTraitInfo(eParentTrait).getDescription()
		iLevel = gc.getTraitInfo(eTrait).getLevel()
		szText = CyTranslator().getText("TXT_KEY_LOST_LEVEL_TRAIT",(szName, iLevel, szDesc,))

	if gc.getTraitInfo(eTrait).getImage() != "":
		szArt = gc.getTraitInfo(eTrait).getImage()
	else:
		szArt = 'art/interface/popups/TraitsLost.dds'


	if pPlayer.isHuman() and iGameTurn > 1:
		Manager.Tools.addPopupMsg("Lost", szText, szArt)

	DbgWnd = Manager.DbgWnd
	szMsg = "Turn(%d): %s [NEWLINE]" % (iGameTurn, szText)
	DbgWnd.addLine("Trait Losses", iPlayer, szMsg )
	