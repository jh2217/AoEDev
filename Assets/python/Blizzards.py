## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

#Blizzards Modcomp by TC01
#	initConstants() contains all the constant values used in this file, for ease of access
#	doBlizzardTurn() is called every game turn and moves, kills, or spawns blizzards randomly
#	moveBlizzard(pPlot, iDirection) moves a blizzard to pPlot depending on iDirection
#	canBlizzard(pPlot, bNew) checks if pPlot can have a blizzard move onto it or (if bNew = true) if a blizzard can be spawned there
#	doBlizzard() applies the effects of a blizzard

#	All of these functions can be modified to add your own effects. I suggest not modifying doBlizzardTurn or moveBlizzard, but instead modifying the constants defined at in initConstants, as
#they affect the behavior of the movement, creation, and killing of blizzards. canBlizzard can be altered to change whether a blizzard can move onto or spawn on a plot. doBlizzard can be
#modified to cause different features or terrains to appear in different conditions.

#	 You can use this modcomp with any mod. Follow the instructions in Merging Guide.txt or in the forum thread to merge it. Be aware that it has been included in my Frozen civilization and
#in Rise of Erebus by Valkrionn (formerly FF+).

class Blizzards:

	def initConstants(self):
		self.iBlizzardMoveChance = 30
		self.iBlizzardKillChance = 30			#Chance a blizzard expires
		self.iBlizzardKillChancePlus = 70		#Chance a blizzard expires outside of Illian or Frozen territory
		self.iBlizzardChance = 10				#Chance a blizzard spawns
		self.iBlizzardIceChance = 10			#Chance a blizzard turns an adjacent water plot into ice
		self.iPermanentSnowChance = -1			#Chance a blizzard turns land plots into permanent snow

		self.iMaxBlizzardsInRange = 1			#Maximum number of blizzards that can be around a newly created blizzard

	def doBlizzardTurn(self):

		self.initConstants()

		iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
		iIllians = gc.getInfoTypeForString('CIVILIZATION_ILLIANS')
		iFrozen = gc.getInfoTypeForString('CIVILIZATION_FROZEN')
		iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
		iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')

		for i in range(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getFeatureType() == iBlizzard:
				iBlizzardDirectionRand = CyGame().getSorenRandNum(100, "Blizzard")
				iBlizzardKillRand = CyGame().getSorenRandNum(100, "Kill Blizzard")

				#Moves a blizzard
				if(iBlizzardDirectionRand<=self.iBlizzardMoveChance):
					self.moveBlizzard(pPlot)

				#Kills a blizzard (has an effect only if moveBlizzard didn't move the blizzard)
				else:
					if pPlot.getOwner() in [iIllians,iFrozen]:
						if iBlizzardKillRand <= self.iBlizzardKillChance:
							pPlot.setFeatureType(-1,-1)
					else:
						if iBlizzardKillRand <= self.iBlizzardKillChancePlus:
							pPlot.setFeatureType(-1, -1)

			#Creates a blizzard
			else:
				if pPlot.getTerrainType() in [iTundra,iGlacier]:
					if self.canBlizzard(pPlot, true):
						if CyGame().getSorenRandNum(100, "Blizzard") < self.iBlizzardChance:
							pPlot.setFeatureType(iBlizzard,0)
							self.doBlizzard(pPlot)

	def moveBlizzard(self, pOldPlot):
		iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
		iWinter = gc.getInfoTypeForString('FEATURE_WINTER')
		iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')
		iFrozen = gc.getInfoTypeForString('CIVILIZATION_FROZEN')
		iRnd = CyGame().getSorenRandNum(7, "Blizzards") # destination is equally chosen among the 8 surrounding tiles
		xMov,yMov = SURROUND1[iRnd]
		newPlot = CyMap().plot(pOldPlot.getX() + xMov, pOldPlot.getY() + yMov)

		if self.canBlizzard(newPlot, false): # if new plot is valid for blizzard
			newPlot.setFeatureType(iBlizzard,0) #add blizzard at new plot
			self.doBlizzard(newPlot) # activate blizzard effects on new plot
			# if the territory belongs to frozen civ and player already cast global spell wintering, tile becomes winter
			# TODO Ronkhar this code portion should be made modular. 1) add for module in... at the end of the function 2) move this condition to frozen module python files
			pOldPlot.setFeatureType(-1,-1) #remove blizzard at old plot. If frozen and wintering has occurred, transform into winter

			if pOldPlot.getOwner() != -1:
				pPlayer = gc.getPlayer(pOldPlot.getOwner())
				if (pPlayer.getCivilizationType() == iFrozen and pPlayer.isFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL) and pOldPlot.getTerrainType() == iGlacier):
					pOldPlot.setFeatureType(iWinter,-1)
					
	def canBlizzard(self, pPlot, bNew):
		iFrozen = gc.getInfoTypeForString('CIVILIZATION_FROZEN')
		iIllian = gc.getInfoTypeForString('CIVILIZATION_ILLIANS')
		iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
		if pPlot.isNone() == False:

			#General rules, always followed for both movement and creation
			if pPlot.isPeak():
				return False
			if pPlot.getFeatureType() != -1:
				return False
			if pPlot.isWater():
				return False

			#If we're creating a new blizzard, apply extra restrictions:
			if bNew == true:
				if pPlot.getOwner() != -1:
					if (gc.getPlayer(pPlot.getOwner()).getCivilizationType() not in (iFrozen,iIllian)):
						return False
				if pPlot.getOwner() == -1:
					return False
				if pPlot.isCity():
					return False

				iNumBlizzards = 0
				for iX in range(pPlot.getX()-1, pPlot.getX()+2, 1):
					for iY in range(pPlot.getY()-1, pPlot.getY()+2, 1):
						pRange = CyMap().plot(iX, iY)
						if pRange.getFeatureType() == iBlizzard:
							iNumBlizzards += 1
				if iNumBlizzards > self.iMaxBlizzardsInRange:
					return false

		return True

	def doBlizzard(self, pPlot):

		self.initConstants()

		iGlacier = gc.getInfoTypeForString('TERRAIN_GLACIER')
		iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
		iTaiga = gc.getInfoTypeForString('TERRAIN_TAIGA')
		iIce = gc.getInfoTypeForString('FEATURE_ICE') # in water
		iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
		iFloodPlains = gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')
		iForest = gc.getInfoTypeForString('FEATURE_FOREST')
		iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
		iScrub = gc.getInfoTypeForString('FEATURE_SCRUB')
		iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
		iGrain = gc.getInfoTypeForString('BONUSCLASS_GRAIN')
		iLivestock = gc.getInfoTypeForString('BONUSCLASS_LIVESTOCK')
		iDeer = gc.getInfoTypeForString('BONUS_DEER')
		iArcticDeer = gc.getInfoTypeForString('BONUS_DEER_ARCTIC')
		iCow = gc.getInfoTypeForString('BONUS_COW')
		iBison = gc.getInfoTypeForString('BONUS_BISON')
		iFur = gc.getInfoTypeForString('BONUS_FUR')
		bValid = False
		iX = pPlot.getX()
		iY = pPlot.getY()
		
		getPlot	= CyMap().plot
		for iiX,iiY in RANGE1:
			targetPlot = getPlot(iX+iiX,iY+iiY)
			if not targetPlot.isNone():
				if not targetPlot.isWater():
					if (targetPlot.getRealTerrainType() == iTaiga or (targetPlot.getTerrainType()==iTaiga) and targetPlot.getRealTerrainType()==-1): #Taiga becomes permanent tundra terrain automatically
						targetPlot.setTerrainType(iTundra,true,true)
						if pPlot.getBonusType(-1) == iDeer: # If bonus deer, change to arctic deer
							pPlot.setBonusType(iArcticDeer)
						elif pPlot.getBonusType(-1) == iCow: # If bonus cow, change to bison
							pPlot.setBonusType(iBison)
					elif (targetPlot.getRealTerrainType() == iTundra or(targetPlot.getTerrainType()==iTundra) and targetPlot.getRealTerrainType()==-1) : # Tundra becomes permanent glacier automatically
						targetPlot.setTerrainType(iGlacier,true,true)
						if pPlot.getBonusType(-1) == iDeer: # If bonus deer, change to arctic deer
							pPlot.setBonusType(iArcticDeer)
						elif pPlot.getBonusType(-1) == iCow: # If bonus cow, change to bison
							pPlot.setBonusType(iBison)
					elif (targetPlot.getRealTerrainType() != iGlacier and targetPlot.getTerrainType()!=iGlacier):  #Other (non glacier) plots will randomly be set to either permanent or temporary taiga terrain
						iPermanentRand = CyGame().getSorenRandNum(100, "Temp Terrain")
						if iPermanentRand < self.iPermanentSnowChance:
							targetPlot.setTerrainType(iTaiga,true,true)
						else:
							iTempRand = CyGame().getSorenRandNum(5, "Bob") + 10
							targetPlot.setTempTerrainType(iTaiga, iTempRand)
							#Removes livestock and grain bonuses temporarily.
							if targetPlot.getBonusType(-1) not in (-1,iDeer,iBison,iFur): # if deer or bison or fur, immune
								if (gc.getBonusInfo(targetPlot.getBonusType(-1)).getBonusClassType() == iGrain or gc.getBonusInfo(targetPlot.getBonusType(-1)).getBonusClassType() == iLivestock):
									targetPlot.setTempBonusType(-1, iTempRand)
						#Specified features (and smoke) are destroyed/terraformed into something else
						if targetPlot.getImprovementType() == iSmoke:
							targetPlot.setImprovementType(-1)
						if targetPlot.getFeatureType() == iForest:
							targetPlot.setFeatureType(iForest, 2)
						if targetPlot.getFeatureType() == iJungle:
							targetPlot.setFeatureType(iForest, 2)
						if targetPlot.getFeatureType() == iFlames:
							targetPlot.setFeatureType(-1, -1)
						if targetPlot.getFeatureType() == iFloodPlains:
							targetPlot.setFeatureType(-1, -1)
						if targetPlot.getFeatureType() == iScrub:
							targetPlot.setFeatureType(-1, -1)



					#If the blizzard is by the coast, turn that coast into Ice. (Permanent or not).
					if targetPlot.isWater():
						if targetPlot.getFeatureType() != iIce:
							targetPlot.setTempFeatureType(iIce, 0, CyGame().getSorenRandNum(5, "Bob") + 10)