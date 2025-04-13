## Arachnophobia CvSpellInterface.py
## By LeastCraft 05/08/2023

from CvPythonExtensions import *
from BasicFunctions import *
from CvSpellInterface import *
import PyHelpers
import CvEventInterface
import CvUtil

# Globals
PyPlayer			= PyHelpers.PyPlayer
gc					= CyGlobalContext()
localText			= CyTranslator()
getInfoType			= gc.getInfoTypeForString

Manager             = CvEventInterface.getEventManager()
Bonus               = Manager.Resources
Civ                 = Manager.Civilizations
Trait               = Manager.Traits
Buildings           = Manager.Buildings
UnitCombat          = Manager.UnitCombats
Race                = Manager.Promotions["Race"]
GenericPromo        = Manager.Promotions["Generic"]
Effect              = Manager.Promotions["Effects"]

def reqGiantSpiderUpgradeAlt(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if (pPlayer.getNumCities() > 0):
		pNest = pPlayer.getCapitalCity()
		iNestPop = pNest.getPopulation()
		if iNestPop >= 11:
			return True
	return False

# Symbiotic Communion Spells Start
def WorstSpiderByPromo(player, location, promo):
	pPlot = location
	pWorstUnit = -1
	fWorstValue = 99999999 # Nothing returned could be higher than this value, so the first unit will always be the worst to begin with.
	for i in range(pPlot.getNumUnits()):
		fValue = 999999
		pUnit = pPlot.getUnit(i)
		if (promo == -1 or pUnit.isHasPromotion(promo)) and pUnit.getSummoner() == -1: # Used by Symbiotic Communions only. We want real units only (not summons)
			if pUnit.getOwner() == player:
				iLevel = pUnit.getLevel()
				iStrength = pUnit.baseCombatStr()
				fStrength = iStrength * (1.0 - (pUnit.getDamage() / 100)) # Find the unit's actual strength by factoring in its damage
				fModifier = iLevel / 2.0 + 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_HERO')) or pUnit.isHasPromotion(getInfoType('PROMOTION_ADVENTURER')):
					fModifier += 9999 # Heroes should never be chosen
				if pUnit.isHasPromotion(getInfoType('PROMOTION_HEROIC')):
					fModifier += 9999 # Nor should battle-hardened units
				if pUnit.getUnitCombatType() == getInfoType('UNITCOMBAT_BEAST'):
					fModifier += 99 # Nor should beast units, i.e. giant spiders
				if pUnit.isHasPromotion(getInfoType('PROMOTION_WEAK')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_STRONG')):
					fModifier += 2.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_CRAZED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_DISEASED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_ENRAGED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_UNDISCIPLINED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_PLAGUED')):
					fModifier -= 1.0

				fValue = fStrength * fModifier
				if fValue < fWorstValue:
					fWorstValue = fValue
					pWorstUnit = pUnit

	return pWorstUnit

def reqCommunion(caster, spider_type):
	iSpider = getInfoType('PROMOTION_SPIDER_RHAGODESSA')
	
	if spider_type == 1:
		iSpider = getInfoType('PROMOTION_SPIDER_RHAGODESSA')
	if spider_type == 2:
		iSpider = getInfoType('PROMOTION_SPIDER_TEXTUS')
	if spider_type == 3:
		iSpider = getInfoType('PROMOTION_SPIDER_MUCRO')
	if spider_type == 4:
		iSpider = getInfoType('PROMOTION_SPIDER_ARGYRONETA')
	if spider_type == 5:
		iSpider = getInfoType('PROMOTION_SPIDER_VENENUM')
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.isHasPromotion(iSpider):
			return True
	return False

def spellCommunion(caster, spider_type):
	iSpider = getInfoType('PROMOTION_SPIDER_RHAGODESSA')
	iMutation = getInfoType('PROMOTION_SPIDERMUTATION_VENOM_SECRETION')

	if spider_type == 1:
		iSpider = getInfoType('PROMOTION_SPIDER_RHAGODESSA')
		iMutation = getInfoType('PROMOTION_SPIDERMUTATION_VENOM_SECRETION')
	if spider_type == 2:
		iSpider = getInfoType('PROMOTION_SPIDER_TEXTUS')
		iMutation = getInfoType('PROMOTION_SPIDERMUTATION_JOINTED_LIMBS')
	if spider_type == 3:
		iSpider = getInfoType('PROMOTION_SPIDER_MUCRO')
		iMutation = getInfoType('PROMOTION_SPIDERMUTATION_CHITIN_CARAPACE')
	if spider_type == 4:
		iSpider = getInfoType('PROMOTION_SPIDER_ARGYRONETA')
		iMutation = getInfoType('PROMOTION_SPIDERMUTATION_TRAIL_PHEROMONE')
	if spider_type == 5:
		iSpider = getInfoType('PROMOTION_SPIDER_VENENUM')
		iMutation = getInfoType('PROMOTION_SPIDERMUTATION_SPITTER_GLAND')
		

	#Sacrifice weakest spider
	iOwner = caster.getOwner()
	pPlot = caster.plot()
	pVictim = -1
	pVictim = WorstSpiderByPromo(iOwner, pPlot, iSpider)
	if pVictim != -1:
		pVictim.kill(True, 0)
		
		#Grant Mutation
		iMelee = getInfoType('UNITCOMBAT_MELEE')
		iRecon = getInfoType('UNITCOMBAT_RECON')
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitCombatType() == iMelee or pUnit.getUnitCombatType() == iRecon:
				pUnit.setHasPromotion(iMutation, True)
# Symbiotic Communion Spells End

# Spider Summoning Spells Start
def setSpiderPromo(spawnUnit, pPlayer, pCity):
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

def spellCallBabySpider(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	iSpider = getInfoType('UNIT_BABY_SPIDER')

	spawnUnit = pPlayer.initUnit(iSpider, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	setSpiderPromo(spawnUnit, pPlayer, pCity)

	iBroodActivity = pPlayer.getCivCounter()
	iCost = 2500
	pPlayer.setCivCounter(iBroodActivity - iCost)

def reqCallBabySpider(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())

	return pCity.getPopulation() >= 1 and pPlayer.getCivCounter() >= 2500

def spellCallSpider(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	iSpider = getInfoType('UNIT_SPIDER')

	spawnUnit = pPlayer.initUnit(iSpider, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	setSpiderPromo(spawnUnit, pPlayer, pCity)
	
	iBroodActivity = pPlayer.getCivCounter()
	iCost = 7500
	pPlayer.setCivCounter(iBroodActivity - iCost)

def reqCallSpider(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())

	return pCity.getPopulation() >= 6 and pPlayer.getCivCounter() >= 7500

def spellCallGiantSpider(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	iSpider = getInfoType('UNIT_GIANT_SPIDER')

	spawnUnit = pPlayer.initUnit(iSpider, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	setSpiderPromo(spawnUnit, pPlayer, pCity)
	
	iBroodActivity = pPlayer.getCivCounter()
	iCost = 15000
	pPlayer.setCivCounter(iBroodActivity - iCost)

def reqCallGiantSpider(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())

	return pCity.getPopulation() >= 11 and pPlayer.getCivCounter() >= 17500

# Spider Summoning Spells End

def spellDietOfWorms(caster):
	pPlayer = gc.getPlayer(caster.getOwner())

	iBroodActivity = pPlayer.getCivCounter()
	iCost = 10000
	pPlayer.setCivCounter(iBroodActivity - iCost)

def reqDietOfWorms(caster):
	pPlayer = gc.getPlayer(caster.getOwner())

	return pPlayer.getCivCounter() >= 10000

def spellPsalmForTheSwarm(caster):
	pPlayer = gc.getPlayer(caster.getOwner())

	iBroodActivity = pPlayer.getCivCounter()
	iValue = 5000
	pPlayer.setCivCounter(iBroodActivity + iValue)

def spellSmearPoison(caster):
	pVictim = -1
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if pUnit.getUnitType() == getInfoType('UNIT_BABY_SPIDER') and not pUnit.isHasPromotion(getInfoType('PROMOTION_GROWTH_SPURTS')):
				if (pVictim == -1 or pVictim.getLevel() > pUnit.getLevel()):
					pVictim = pUnit
	if pVictim != -1:
		pVictim.kill(True, 0)

def reqSmearPoison(caster):
	iPoisonedBlade = getInfoType('PROMOTION_POISONED_BLADE')
	pPoisonedBlade = gc.getPromotionInfo(iPoisonedBlade)
	# Check that PROMOTION_POISONED_BLADE is eligible for the unit
	if caster.getUnitCombatType()!=-1 and pPoisonedBlade.getUnitCombat(caster.getUnitCombatType()):
		# Check that there is a baby spider that has not entered Growth Spurts
		pPlot = caster.plot()
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getOwner() == caster.getOwner():
				if pUnit.getUnitType() == getInfoType('UNIT_BABY_SPIDER') and not pUnit.isHasPromotion(getInfoType('PROMOTION_GROWTH_SPURTS')):
					return True
	return False

def spellCannibalize(caster):
	caster.setDamage(caster.getDamage() - 15, caster.getOwner())
	pVictim = -1
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if pUnit.getUnitType() == getInfoType('UNIT_BABY_SPIDER') and not pUnit.isHasPromotion(getInfoType('PROMOTION_GROWTH_SPURTS')):
				if (pVictim == -1 or pVictim.getLevel() > pUnit.getLevel()):
					pVictim = pUnit
	if pVictim != -1:
		pVictim.kill(True, 0)
		
def reqCannibalize(caster):
	eligibleUnits = [getInfoType('UNIT_SPIDER'), getInfoType('UNIT_GIANT_SPIDER'), getInfoType('UNIT_NESTING_SPIDER'), getInfoType('UNIT_MOTHER_SPIDER')]
	if caster.getUnitType() not in eligibleUnits: return False
	if caster.getDamage() == 0: return False
	
	# Check that there is a baby spider that has not entered Growth Spurts
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if pUnit.getUnitType() == getInfoType('UNIT_BABY_SPIDER') and not pUnit.isHasPromotion(getInfoType('PROMOTION_GROWTH_SPURTS')):
				return True
	return False

def onMoveMazeOfWebs(caster, pPlot):
	immuneUnits = [getInfoType('UNIT_BABY_SPIDER'), getInfoType('UNIT_SPIDER'), getInfoType('UNIT_GIANT_SPIDER'), getInfoType('UNIT_NESTING_SPIDER'), getInfoType('UNIT_MOTHER_SPIDER')]
	if caster.getUnitType() not in immuneUnits:
		if gc.getPlayer(caster.getOwner()).getCivilizationType() != Civ["Archos"]:
			iHasted = getInfoType('PROMOTION_HASTED')
			caster.safeRemovePromotion(iHasted)
			iSlow = getInfoType('PROMOTION_SLOW')
			caster.setHasPromotion(iSlow, True)