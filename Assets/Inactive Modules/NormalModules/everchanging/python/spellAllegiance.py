
from CvPythonExtensions import *
gc = CyGlobalContext()

def postCombatAllegiance(pCaster, pOpponent):
	player = pOpponent.getOwner()
	pPlayer = gc.getPlayer(player)
	pCity = pPlayer.getCapitalCity()
	iMoreStrength = pCaster.getStrBoost()	
	if pCity.isNone():
		OpPlotX = pOpponent.getX()
		OpPlotY = pOpponent.getY()
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SAILA'), OpPlotX, OpPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.changeStrBoost(iMoreStrength+1)
		for i in range(gc.getNumPromotionInfos()):
			if not gc.getPromotionInfo(i).isEquipment():
				newUnit.setHasPromotion(i, pCaster.isHasPromotion(i))
		newUnit.setLevel(pCaster.getLevel())
		newUnit.setExperienceTimes100(pCaster.getExperienceTimes100(), -1)
		newUnit.finishMoves()
		
	else:
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SAILA'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.changeStrBoost(iMoreStrength+1)
		for i in range(gc.getNumPromotionInfos()):
			if not gc.getPromotionInfo(i).isEquipment() and not gc.getPromotionInfo(i).isMustMaintain():
				newUnit.setHasPromotion(i, pCaster.isHasPromotion(i))
		newUnit.setLevel(pCaster.getLevel())
		newUnit.setExperienceTimes100(pCaster.getExperienceTimes100(), -1)
		newUnit.finishMoves()
	for iPlayer in range(gc.getMAX_PLAYERS()):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SAILA_FIRST", ()),'',1,'Art/Modules/Everchanging/Buttons/saila.dds',ColorTypes(8),pOpponent.getX(),pOpponent.getY(),True,True)	
	
