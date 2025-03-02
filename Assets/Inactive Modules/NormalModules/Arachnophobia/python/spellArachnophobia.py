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
git					= gc.getInfoTypeForString

# Symbiotic Communion Spells Start

def WorstUnitByPromo(player, location, promo):
	py = player
	pPlot = location
	pWorstUnit = -1
	fWorstValue = 9999999999999999999999999999 #Nothing returned could be higher than this value, so the first unit will always be the worst to begin with.
	for i in range(pPlot.getNumUnits()):
		fValue = 999999999999999999
		pUnit = pPlot.getUnit(i)
		if (promo == -1 or pUnit.isHasPromotion(promo)) and pUnit.getSummoner() == -1: #used by Symbiotic Communions only. We want real units only (not summons)
			if pUnit.getOwner() == player:
				iLevel = pUnit.getLevel()
				iStrength = pUnit.baseCombatStr()
				fStrength = iStrength * (1.0 - (pUnit.getDamage() / 100))#Find the unit's actual strength by factoring in its damage
				fModifier = iLevel / 2
				if pUnit.isHasPromotion(getInfoType('PROMOTION_HERO')) or pUnit.isHasPromotion(getInfoType('PROMOTION_ADVENTURER')):
					fModifier += 999999999999 #Heroes should never be chosen
				if pUnit.isHasPromotion(getInfoType('PROMOTION_HEROIC')):
					fModifier += 999999999999 #Nor should Battle-Hardened units
				if pUnit.getUnitCombatType() == getInfoType('UNITCOMBAT_BEAST'): #Nor should beast units, i.e. giant spiders
					fModifier += 99
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
	pVictim = WorstUnitByPromo(iOwner, pPlot, iSpider)
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
