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

# Globals
PyPlayer			= PyHelpers.PyPlayer
gc					= CyGlobalContext()
localText			= CyTranslator()
getInfoType			= gc.getInfoTypeForString


def setSpiderPromo(cf, spawnUnit, pPlayer, pCity):
	Effect      = cf.Promotions["Effects"]
	Buildings   = cf.Buildings
	Trait       = cf.Traits
	if spawnUnit:
		setPromo = spawnUnit.setHasPromotion
		pNest       = pPlayer.getCapitalCity()
		iNestPop    = pNest.getPopulation()
		getNum      = pNest.getNumBuilding
		if pPlayer.hasTrait(Trait["Spiderkin"]):
			if iNestPop >= 9:
				setPromo( Effect["Spiderkin"], True)

		if iNestPop >= 16:
			setPromo( Effect["Strong"], True)

		if pCity:
			pCity.applyBuildEffects(spawnUnit)

		if   getNum( Buildings["Nest Addon1"]) > 0:
			iBroodStrength = 1
		elif getNum( Buildings["Nest Addon2"]) > 0:
			iBroodStrength = 2
		elif getNum( Buildings["Nest Addon3"]) > 0:
			iBroodStrength = 3
		elif getNum( Buildings["Nest Addon4"]) > 0:
			iBroodStrength = 4
		else:
			iBroodStrength = 0
		spawnUnit.changeFreePromotionPick(iBroodStrength)


def spawnCocoon(pPlayer, pPlot):
	# Spawn cocoon if one does not exist
	initUnit 	= pPlayer.initUnit
	iCocoon     = getInfoType('UNIT_COCOON')
	iNoAI       = UnitAITypes.NO_UNITAI
	iWest       = DirectionTypes.DIRECTION_WEST
	
	bHasCocoon = False
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == iCocoon:
			bHasCocoon = True
	if not bHasCocoon:
		initUnit(iCocoon, pPlot.getX(), pPlot.getY(), iNoAI, iWest)


def doTurnArchosReplacement(self, iPlayer):
	pPlayer         = gc.getPlayer(iPlayer)
	if pPlayer.getNumCities() <= 0:
		pPlayer.setCivCounter(0)
	else:
		pNest       = pPlayer.getCapitalCity()
		iNestPop    = pNest.getPopulation()
		Unit        = self.Units["Archos"]
		iNoAI       = UnitAITypes.NO_UNITAI
		iSouth      = DirectionTypes.DIRECTION_SOUTH
		iX = pNest.getX(); iY = pNest.getY()
		initUnit 	= pPlayer.initUnit

		map 		= CyMap()
		plotByIndex = map.plotByIndex
		randNum 	= CyGame().getSorenRandNum

		# Set CivCounterMod as both the spider spawn chance and the Brood Activity increase per turn
		iSpawnChance = self.doChanceArchos(iPlayer)
		pPlayer.setCivCounterMod(iSpawnChance)

		iBroodActivity = pPlayer.getCivCounter() + iSpawnChance
		# Set CivCounter as the cumulative Brood Activity
		pPlayer.setCivCounter(iBroodActivity)

		# Spawn spiders from capital
		if randNum(10000, "Spawn Roll") < iSpawnChance:
			if iNestPop >= 11 and iBroodActivity >= 80000:
				spawnUnit = initUnit( Unit["Giant Spider"], iX, iY, iNoAI, iSouth)
			elif iNestPop >= 6 and iBroodActivity >= 40000:
				spawnUnit = initUnit( Unit["Spider"], iX, iY, iNoAI, iSouth)
			elif iNestPop >= 1 and iBroodActivity >= 20000:
				spawnUnit = initUnit( Unit["Baby Spider"], iX, iY, iNoAI, iSouth)
			else:
				spawnUnit = None
			setSpiderPromo(self, spawnUnit, pPlayer, pNest)
			if spawnUnit:
				spawnUnit.setHasPromotion(getInfoType('PROMOTION_HATCHING'), True)
				spawnCocoon(pPlayer, pNest.plot())
		
		# Spawn spiders from feeding pens
		for i in xrange(map.numPlots()):
			pPlot = plotByIndex(i)
			if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_FEEDING_PEN'):
				if pPlot.getOwner() == iPlayer:
					if randNum(10000, "Spawn Roll") < iSpawnChance:
						# Spawn baby spider
						spawnUnit = initUnit(Unit["Baby Spider"], pPlot.getX(), pPlot.getY(), iNoAI, iSouth)
						setSpiderPromo(self, spawnUnit, pPlayer, None)
						spawnUnit.setHasPromotion(getInfoType('PROMOTION_HATCHING'), True)
						spawnCocoon(pPlayer, pPlot)


def doChanceArchosReplacement(self, iPlayer):
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
		iNumSpiders		= (getUCC(UnitClass["Spider"]) * 2 + (getUCC(UnitClass["Giant Spider"]) * 4))

		map 		= CyMap()
		plotByIndex = map.plotByIndex

		iNumFeedingPen = 0
		for i in xrange(map.numPlots()):
			pPlot = plotByIndex(i)
			if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_FEEDING_PEN'):
				if pPlot.getOwner() == iPlayer:
					iNumFeedingPen += 1

		fSpiderkin = 1
		if pPlayer.hasTrait(Trait["Spiderkin"]):
			fSpiderkin = 1.30

		iSpiderSpawnChance = ((iNestPop + (iNumGroves*2) + iNumFeedingPen) * fSpiderkin) - iNumSpiders
		iSpiderSpawnChance = (iSpiderSpawnChance * 100)
		iSpiderSpawnChance = scaleInverse(iSpiderSpawnChance)

		return iSpiderSpawnChance


def onLoadGame(self, argsList):
	self.cf.doChanceArchos = types.MethodType(doChanceArchosReplacement, self.cf)
	self.cf.doTurnArchos = types.MethodType(doTurnArchosReplacement, self.cf)


def onGameStart(self, argsList):
	self.cf.doChanceArchos = types.MethodType(doChanceArchosReplacement, self.cf)
	self.cf.doTurnArchos = types.MethodType(doTurnArchosReplacement, self.cf)


def onUnitCreated(self, argsList):
	'Unit Completed'
	pUnit = argsList[0]
	self.verifyLoaded()
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

	# When a spider with variant promotion is stationed in a city, +10% chance to grant the respective mutation to newly created melee and recon units in the city.
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