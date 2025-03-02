## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import types
from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls
import CvEventInterface
import random

PyPlayer = PyHelpers.PyPlayer

def doChanceArchosReplacement(self, iPlayer):
	gc = CyGlobalContext()
	if iPlayer == -1:
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
	else:
		pPlayer = gc.getPlayer(iPlayer)

	iNumCities = pPlayer.getNumCities()
	if iNumCities > 0:
		UnitClass		= self.UnitClasses
		Building		= self.Buildings
		Trait			= self.Traits
		pNest 			= pPlayer.getCapitalCity()
		iNestPop 		= pNest.getPopulation()
		iNumGroves 		= pPlayer.countNumBuildings(Building["Dark Weald"])
		getUCC			= pPlayer.getUnitClassCount
		iNumSpiders		= ((getUCC(UnitClass["Baby Spider"]) * 0.5) + getUCC(UnitClass["Spider"]) + (getUCC(UnitClass["Giant Spider"]) * 2))
		
		iNumSpiderCities = len(PyPlayer(iPlayer).getCityList())

		fSpiderkin = 1
		if pPlayer.hasTrait(Trait["Spiderkin"]):
			fSpiderkin = 1.30

		iSpiderSpawnChance = ((iNestPop + (iNumSpiderCities*2) + (iNumGroves*4)) * fSpiderkin) - iNumSpiders
		iSpiderSpawnChance = (iSpiderSpawnChance * 100)
		iSpiderSpawnChance = scaleInverse(iSpiderSpawnChance)

		pPlayer.setCivCounter(iSpiderSpawnChance)
		#No scorpions
		pPlayer.setCivCounterMod(0)

def onLoadGame(self, argsList):
	self.cf.doChanceArchos = types.MethodType(doChanceArchosReplacement, self.cf)


def onGameStart(self, argsList):
	self.cf.doChanceArchos = types.MethodType(doChanceArchosReplacement, self.cf)


def onUnitCreated(self, argsList):
	'Unit Completed'
	pUnit = argsList[0]
	self.verifyLoaded()
	gc 					= CyGlobalContext()
	getInfoType			= gc.getInfoTypeForString
	cf					= self.cf
	game 				= CyGame()
	player 				= PyPlayer(pUnit.getOwner())
	getPlayer 			= gc.getPlayer
	pPlayer 			= getPlayer(pUnit.getOwner())
	Civ					= self.Civilizations
	Promo				= self.Promotions["Effects"]
	Generic				= self.Promotions["Generic"]
	Race				= self.Promotions["Race"]
	Equipment			= self.Promotions["Equipment"]
	UnitCombat			= self.UnitCombats
	Tech				= self.Techs
	Mana				= self.Mana
	setPromo 			= pUnit.setHasPromotion
	hasTrait 			= pPlayer.hasTrait
	Trait				= self.Traits
	iUnitType 			= pUnit.getUnitType()
	iUnitCombat 		= pUnit.getUnitCombatType()
	initUnit 			= pPlayer.initUnit
	getNumAvailBonuses 	= pPlayer.getNumAvailableBonuses
	getTeam 			= gc.getTeam
	hasPromo 			= pUnit.isHasPromotion
	randNum 			= game.getSorenRandNum
	iNoAI				= UnitAITypes.NO_UNITAI
	iSouth 				= DirectionTypes.DIRECTION_SOUTH
	pPlot 				= pUnit.plot()
	iX = pPlot.getX(); iY = pPlot.getY()

	iMelee = getInfoType('UNITCOMBAT_MELEE')
	iRecon = getInfoType('UNITCOMBAT_RECON')

	if pUnit.getUnitCombatType() == iMelee or pUnit.getUnitCombatType() == iRecon:
		iSpiderRed = getInfoType('PROMOTION_SPIDER_RHAGODESSA')
		iMutationRed = getInfoType('PROMOTION_SPIDERMUTATION_VENOM_SECRETION')
		iSpiderYellow = getInfoType('PROMOTION_SPIDER_TEXTUS')
		iMutationYellow = getInfoType('PROMOTION_SPIDERMUTATION_JOINTED_LIMBS')
		iSpiderGrey = getInfoType('PROMOTION_SPIDER_MUCRO')
		iMutationGrey = getInfoType('PROMOTION_SPIDERMUTATION_CHITIN_CARAPACE')
		iSpiderBlue = getInfoType('PROMOTION_SPIDER_ARGYRONETA')
		iMutationBlue = getInfoType('PROMOTION_SPIDERMUTATION_TRAIL_PHEROMONE')
		iSpiderGreen = getInfoType('PROMOTION_SPIDER_VENENUM')
		iMutationGreen = getInfoType('PROMOTION_SPIDERMUTATION_SPITTER_GLAND')

		redCount = 0
		yellowCount = 0
		greyCount = 0
		blueCount = 0
		greenCount = 0

		for i in range(pPlot.getNumUnits()):
			pUnitInStack = pPlot.getUnit(i)
			if pUnitInStack.isHasPromotion(iSpiderRed):
				redCount += 1
			if pUnitInStack.isHasPromotion(iSpiderYellow):
				yellowCount += 1
			if pUnitInStack.isHasPromotion(iSpiderGrey):
				greyCount += 1
			if pUnitInStack.isHasPromotion(iSpiderBlue):
				blueCount += 1
			if pUnitInStack.isHasPromotion(iSpiderGreen):
				greenCount += 1

		if (random.randint(1,100) <= redCount * 10):
			pUnit.setHasPromotion(iMutationRed, True)
		if (random.randint(1,100) <= yellowCount * 10):
			pUnit.setHasPromotion(iMutationYellow, True)
		if (random.randint(1,100) <= greyCount * 10):
			pUnit.setHasPromotion(iMutationGrey, True)
		if (random.randint(1,100) <= blueCount * 10):
			pUnit.setHasPromotion(iMutationBlue, True)
		if (random.randint(1,100) <= greenCount * 10):
			pUnit.setHasPromotion(iMutationGreen, True)