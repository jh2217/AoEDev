import os
import _winreg # access windows registry
import traceback
from CvPythonExtensions import *


gc = CyGlobalContext()

iMaxFilenameTries = 100

bWroteLog = False

SEPERATOR = "-----------------------------------------------------------------\n"


# Simply checks every game turn for OOS. If it finds it, writes the
# info contained in the sync checksum to a log file, then sets the bWroteLog
# variable so that it only happens once.
def doGameUpdate():
	global bWroteLog
	bOOS = CyInterface().isOOSVisible()

	if (bOOS and not bWroteLog):
		writeLog()
		bWroteLog = True

def getDocFolder():
	try:
		userFolder = regRead(_winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders", "Personal")
		if not userFolder : return ""
		finalFolder =  os.path.join(userFolder, "My Games", "Beyond the Sword", "Ashes of Erebus")
		return finalFolder
	except:
		print " FfH2 -> can t join FfH doc Folders :"
		print traceback.format_exc()
		return ""

def regRead(registry, path, field):
	pathKey = _winreg.OpenKey(registry, path)
	docPath = ""
	try:
		docPath = _winreg.QueryValueEx(pathKey, field)[0]
	except:
		print " FfH2 -> can t get doc path :"
		print traceback.format_exc()
	pathKey.Close()
	return docPath

def writeLog():
	folder = getDocFolder()
	szNewFilename = "%s - Player %s - " % (gc.getPlayer(gc.getGame().getActivePlayer()).getName(), gc.getGame().getActivePlayer()) + "OOSLog - Turn " + "%s" % (gc.getGame().getGameTurn()) + ".txt"
	filePath = os.path.join(folder, szNewFilename)
	pFile = open(filePath, "w")

	#
	# Global data
	#
	pFile.write(SEPERATOR)
	pFile.write(SEPERATOR)

	pFile.write("  GLOBALS  \n")

	pFile.write(SEPERATOR)
	pFile.write(SEPERATOR)
	pFile.write("\n\n")

	pFile.write("Next Map Rand Value: %d\n" % CyGame().getMapRand().get(10000, "OOS Log"))
	pFile.write("Next Soren Rand Value: %d\n" % CyGame().getSorenRand().get(10000, "OOS Log"))

	pFile.write("Total num cities: %d\n" % CyGame().getNumCities() )
	pFile.write("Total population: %d\n" % CyGame().getTotalPopulation() )
	pFile.write("Total Deals: %d\n" % CyGame().getNumDeals() )

	pFile.write("Total owned plots: %d\n" % CyMap().getOwnedPlots() )
	pFile.write("Total num areas: %d\n" % CyMap().getNumAreas() )

	pFile.write("\n\n")

	#
	# Player data
	#
	iPlayer = 0
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isEverAlive()):
			pFile.write(SEPERATOR)
			pFile.write(SEPERATOR)

			string = "  PLAYER %d: %s  \n" % (iPlayer, pPlayer.getName())
			pFile.write(string.encode('utf8'))
			string = "  Civilizations: %s  \n" % (pPlayer.getCivilizationDescription(0))
			pFile.write(string.encode('utf8'))

			pFile.write(SEPERATOR)
			pFile.write(SEPERATOR)
			pFile.write("\n\n")

			pFile.write("Basic data:\n")
			pFile.write("-----------\n")
			pFile.write("Player %d Score: %d\n" % (iPlayer, gc.getGame().getPlayerScore(iPlayer) ))

			pFile.write("Player %d Population: %d\n" % (iPlayer, pPlayer.getTotalPopulation() ) )
			pFile.write("Player %d Total Land: %d\n" % (iPlayer, pPlayer.getTotalLand() ) )
			pFile.write("Player %d Gold: %d\n" % (iPlayer, pPlayer.getGold() ) )
			pFile.write("Player %d Assets: %d\n" % (iPlayer, pPlayer.getAssets() ) )
			pFile.write("Player %d Power: %d\n" % (iPlayer, pPlayer.getPower() ) )
			pFile.write("Player %d Num Cities: %d\n" % (iPlayer, pPlayer.getNumCities() ) )
			pFile.write("Player %d Num Units: %d\n" % (iPlayer, pPlayer.getNumUnits() ) )
			pFile.write("Player %d Num Selection Groups: %d\n" % (iPlayer, pPlayer.getNumSelectionGroups() ) )

			pFile.write("\n\n")

			pFile.write("Yields:\n")
			pFile.write("-------\n")
			for iYield in range( int(YieldTypes.NUM_YIELD_TYPES) ):
				pFile.write("Player %d %s Total Yield: %d\n" % (iPlayer, gc.getYieldInfo(iYield).getDescription(), pPlayer.calculateTotalYield(iYield) ))

			pFile.write("\n\n")

			pFile.write("Commerce:\n")
			pFile.write("---------\n")
			for iCommerce in range( int(CommerceTypes.NUM_COMMERCE_TYPES) ):
				pFile.write("Player %d %s Total Commerce: %d\n" % (iPlayer, gc.getCommerceInfo(iCommerce).getDescription(), pPlayer.getCommerceRate(CommerceTypes(iCommerce)) ))

			pFile.write("\n\n")

			pFile.write("Bonus Info:\n")
			pFile.write("-----------\n")
			for iBonus in range(gc.getNumBonusInfos()):
				string = "Player %d, %s, Number Available: %d\n" % (iPlayer, gc.getBonusInfo(iBonus).getDescription(), pPlayer.getNumAvailableBonuses(iBonus) )
				pFile.write(string.encode('utf8')) # this solves all problems with non ascii characters.
				string = "Player %d, %s, Import: %d\n" % (iPlayer, gc.getBonusInfo(iBonus).getDescription(), pPlayer.getBonusImport(iBonus) )
				pFile.write(string.encode('utf8'))
				string = "Player %d, %s, Export: %d\n" % (iPlayer, gc.getBonusInfo(iBonus).getDescription(), pPlayer.getBonusExport(iBonus) )
				pFile.write(string.encode('utf8'))
				pFile.write("\n")

			pFile.write("\n\n")

			pFile.write("Improvement Info:\n")
			pFile.write("-----------------\n")
			for iImprovement in range(gc.getNumImprovementInfos()):
				string = "Player %d, %s, Improvement count: %d\n" % (iPlayer, gc.getImprovementInfo(iImprovement).getDescription(), pPlayer.getImprovementCount(iImprovement) )
				pFile.write(string.encode('utf8'))

			pFile.write("\n\n")

			pFile.write("Building Class Info:\n")
			pFile.write("--------------------\n")
			for iBuildingClass in range(gc.getNumBuildingClassInfos()):
				string = "Player %d, %s, Building class count plus building: %d\n" % (iPlayer, gc.getBuildingClassInfo(iBuildingClass).getDescription(), pPlayer.getBuildingClassCountPlusMaking(iBuildingClass) )
				pFile.write(string.encode('utf8'))

			pFile.write("\n\n")

			pFile.write("Unit Class Info:\n")
			pFile.write("--------------------\n")
			for iUnitClass in range(gc.getNumUnitClassInfos()):
				string = "Player %d, %s, Unit class count plus training: %d\n" % (iPlayer, gc.getUnitClassInfo(iUnitClass).getDescription(), pPlayer.getUnitClassCountPlusMaking(iUnitClass) )
				pFile.write(string.encode('utf8'))

			pFile.write("\n\n")

			pFile.write("UnitAI Types Info:\n")
			pFile.write("------------------\n")
			for iUnitAIType in range(int(UnitAITypes.NUM_UNITAI_TYPES)):
				string = "Player %d, %s, Unit AI Type count: %d\n" % (iPlayer, gc.getUnitAIInfo(iUnitAIType).getDescription(), pPlayer.AI_totalUnitAIs(UnitAITypes(iUnitAIType)) )
				pFile.write(string.encode('utf8'))


			pFile.write("\n\n")

			pFile.write("City Info:\n")
			pFile.write("----------\n")
			iNumCities = pPlayer.getNumCities()

			if (iNumCities == 0):
				pFile.write("No Cities")
			else:
				pLoopCityTuple = pPlayer.firstCity(False)
				while (pLoopCityTuple[0] != None):
					pCity = pLoopCityTuple[0]
					pFile.write("Player %d, City ID: %d, %s, Plot Radius: %d\n" % (iPlayer, pCity.getID(), pCity.getName(), pCity.getPlotRadius() ))

					pFile.write("X: %d, Y: %d\n" % (pCity.getX(), pCity.getY()) )
					pFile.write("Founded: %d\n" % pCity.getGameTurnFounded() )
					pFile.write("Population: %d\n" % pCity.getPopulation() )
					pFile.write("Buildings: %d\n" % pCity.getNumBuildings() )
					pFile.write("Improved Plots: %d\n" % pCity.countNumImprovedPlots() )
					string = "Producing: %s\n" % pCity.getProductionName()
					pFile.write(string.encode('utf8'))
					pFile.write("%d Tiles Worked, %d Specialists, %d Great People\n" % (pCity.getWorkingPopulation(), pCity.getSpecialistPopulation(), pCity.getNumGreatPeople()) )
					pFile.write("Tiles being Worked: ")
					for iLoop in range(pCity.getNumCityPlots()):
						if pCity.isWorkingPlotByIndex(iLoop):
							pFile.write("%d, " % iLoop )
					pFile.write("\n")

					pLoopCityTuple = pPlayer.nextCity(pLoopCityTuple[1], False)
					pFile.write("\n")


			pFile.write("\n\n")

			pFile.write("Unit Info:\n")
			pFile.write("----------\n")
			iNumUnits = pPlayer.getNumUnits()

			if (iNumUnits == 0):
				pFile.write("No Units")
			else:
				pLoopUnitTuple = pPlayer.firstUnit(False)
				while (pLoopUnitTuple[0] != None):
					pUnit = pLoopUnitTuple[0]
					string = "Player %d, Unit ID: %d, %s\n" % (iPlayer, pUnit.getID(), pUnit.getName() )
					pFile.write(string.encode('utf8'))
					pFile.write("X: %d, Y: %d\n" % (pUnit.getX(), pUnit.getY()) )
					pFile.write("Damage: %d\n" % pUnit.getDamageReal() )
					pFile.write("Experience: %d\n" % pUnit.getExperienceTimes100() )
					pFile.write("Level: %d\n" % pUnit.getLevel() )

					pLoopUnitTuple = pPlayer.nextUnit(pLoopUnitTuple[1], False)
					pFile.write("\n")


			# Space at end of player's info
			pFile.write("\n\n")

	# Close file

	pFile.close()
