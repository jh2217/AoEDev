#pragma once

#ifndef CyGameTextMgr_h
#define CyGameTextMgr_h

//
// Python wrapper class for CyGameTextMgr
//

class CvGameTextMgr;
class CyCity;
class CyUnit;
class CyDeal;
struct TradeData;
class CyGameTextMgr
{
public:
	CyGameTextMgr();
	CyGameTextMgr(CvGameTextMgr* m_pGameTextMgr);			// Call from C++
	bool isNone() { return (m_pGameTextMgr==NULL); }

	void Reset();

	std::wstring getTimeStr(int iGameTurn, bool bSave);
	std::wstring getDateStr(int iGameTurn, bool bSave, int /*CalendarTypes*/ eCalendar, int iStartYear, int /*GameSpeedTypes*/ eSpeed);
	std::wstring getInterfaceTimeStr(int /*PlayerTypes*/ iPlayer);
	std::wstring getGoldStr(int /*PlayerTypes*/ iPlayer);
	std::wstring getResearchStr(int /*PlayerTypes*/ iPlayer);
	std::wstring getOOSSeeds(int /*PlayerTypes*/ iPlayer);
	std::wstring getNetStats(int /*PlayerTypes*/ iPlayer);
	std::wstring getTechHelp(int iTech, bool bCivilopediaText, bool bPlayerContext, bool bStrategyText, bool bTreeInfo, int iFromTech);
	std::wstring getUnitHelp(int iUnit, bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CyCity* pCity);
	std::wstring getSpecificUnitHelp(CyUnit* pUnit, bool bOneLine, bool bShort);
	std::wstring getBuildingHelp(int iBuilding, bool bCivilopediaText, bool bStrategyText, bool bTechChooserText, CyCity* pCity,bool bInGame);
	std::wstring getProjectHelp(int iProject, bool bCivilopediaText, CyCity* pCity);
	std::wstring getPromotionHelp(int iPromotion, bool bCivilopediaText);

//FfH Spell System: Added by Kael 07/23/2007
	std::wstring getSpellHelp(int iSpell, bool bCivilopediaText);
//FfH: End Add

	std::wstring getBonusHelp(int iBonus, bool bCivilopediaText);
	std::wstring getReligionHelpCity(int iReligion, CyCity* pCity, bool bCityScreen, bool bForceReligion, bool bForceState, bool bNoStateReligion);
	std::wstring getCorporationHelpCity(int iCorporation, CyCity* pCity, bool bCityScreen, bool bForceCorporation);
	std::wstring getImprovementHelp(int iImprovement, bool bCivilopediaText);
	std::wstring getTerrainHelp(int iTerrain, bool bCivilopediaText);
	std::wstring getFeatureHelp(int iFeature, bool bCivilopediaText);
	std::wstring getPlotEffectHelp(int iFeature, bool bCivilopediaText);
	std::wstring getCityClassHelp(int iFeature, bool bCivilopediaText);
	std::wstring getRouteHelp(int iFeature, bool bCivilopediaText);
	std::wstring parseCivicInfo(int /*CivicTypes*/ iCivicType, bool bCivilopediaText, bool bPlayerContext, bool bSkipName);
/*************************************************************************************************/
/**	Xienwolf Tweak							07/12/09											**/
/**																								**/
/**		Allowed for "prettier" display of Civic Information in the Pedia by splitting it in 2	**/
/*************************************************************************************************/
	std::wstring parseCivicInfoRequires(int /*CivicTypes*/ iCivicType, bool bCivilopediaText, bool bPlayerContext, bool bSkipName);
	std::wstring parseCivicInfoHelp(int /*CivicTypes*/ iCivicType, bool bCivilopediaText, bool bPlayerContext, bool bSkipName);
	std::wstring parseTraits(int /*TraitTypes*/ iTrait, int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	std::wstring parseSpawnGroups(int /*SpawnGroupTypes*/ iSpawnGroup);
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	std::wstring parseAffinities(int /*AffinityTypes*/ iAffinity);
	std::wstring parseAffinitiesReqs(int /*AffinityTypes*/ iAffinity);
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	std::wstring parseReligionInfo(int /*ReligionTypes*/ iReligionType, bool bCivilopediaText);
	std::wstring parseCorporationInfo(int /*CorporationTypes*/ iCorporationType, bool bCivilopediaText);
	std::wstring parseCivInfos(int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan);
/*************************************************************************************************/
/** InterfaceComfort					Opera													**/
/*************************************************************************************************/
	std::wstring parseMoreCivInfos(int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan, bool bLinks, bool bCivilopediaText);
/*************************************************************************************************/
/** InterfaceComfort					END														**/
/*************************************************************************************************/
	std::wstring parseLeaderTraits(int /*LeaderHeadTypes*/ iLeader, int /*CivilizationTypes*/ iCivilization, bool bDawnOfMan, bool bCivilopediaText);
	std::wstring getTradeString(TradeData* pTradeData, int iPlayer1, int iPlayer2);
	std::wstring getSpecialistHelp(int iSpecialist, bool bCivilopediaText);
	std::wstring buildHintsList();
	std::wstring getAttitudeString(int iPlayer, int iTargetPlayer);
	std::wstring setConvertHelp(int iPlayer, int iReligion);
	std::wstring setRevolutionHelp(int iPlayer);
	std::wstring setVassalRevoltHelp(int iMaster, int iVassal);
	std::wstring getActiveDealsString(int iThisPlayer, int iOtherPlayer);
	std::wstring getDealString(CyDeal* pDeal, int iPlayerPerspective);
	// DynTraits Start
	std::wstring parseTraitReqs(int /*TraitTypes*/ iTrait);
	// DynTraits End


protected:
	CvGameTextMgr* m_pGameTextMgr;
};

#endif	// #ifndef CyGameTextMgr_h
