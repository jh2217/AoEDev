#include "CvGameCoreDLL.h"
#include "CvInfos.h"

//
// Python interface for info classes (formerly structs)
// These are simple enough to be exposed directly - no wrappers
//

void CyInfoPythonInterface3()
{
	OutputDebugString("Python Extension Module - CyInfoPythonInterface3\n");

	python::class_<CvYieldInfo, python::bases<CvInfoBase> >("CvYieldInfo")
		.def("getChar", &CvYieldInfo::getChar, "int ()")
		.def("getHillsChange", &CvYieldInfo::getHillsChange, "int ()")
		.def("getPeakChange", &CvYieldInfo::getPeakChange, "int ()")
		.def("getLakeChange", &CvYieldInfo::getLakeChange, "int ()")
		.def("getCityChange", &CvYieldInfo::getCityChange, "int ()")
		.def("getPopulationChangeOffset", &CvYieldInfo::getPopulationChangeOffset, "int ()")
		.def("getPopulationChangeDivisor", &CvYieldInfo::getPopulationChangeDivisor, "int ()")
		.def("getMinCity", &CvYieldInfo::getMinCity, "int ()")
		.def("getTradeModifier", &CvYieldInfo::getTradeModifier, "int ()")
		.def("getGoldenAgeYield", &CvYieldInfo::getGoldenAgeYield, "int ()")
		.def("getGoldenAgeYieldThreshold", &CvYieldInfo::getGoldenAgeYieldThreshold, "int ()")
		.def("getAIWeightPercent", &CvYieldInfo::getAIWeightPercent, "int ()")
		.def("getColorType", &CvYieldInfo::getColorType, "int ()")
		;

	python::class_<CvTerrainInfo, python::bases<CvInfoBase> >("CvTerrainInfo")

		.def("getMovementCost", &CvTerrainInfo::getMovementCost, "int ()")
		.def("getSeeFromLevel", &CvTerrainInfo::getSeeFromLevel, "int ()")
		.def("getSeeThroughLevel", &CvTerrainInfo::getSeeThroughLevel, "int ()")
		.def("getBuildModifier", &CvTerrainInfo::getBuildModifier, "int ()")
		.def("getDefenseModifier", &CvTerrainInfo::getDefenseModifier, "int ()")

		.def("isWater", &CvTerrainInfo::isWater, "bool ()")
		.def("isImpassable", &CvTerrainInfo::isImpassable, "bool ()")
		.def("isFound", &CvTerrainInfo::isFound, "bool ()")
		.def("isFoundCoast", &CvTerrainInfo::isFoundCoast, "bool ()")
		.def("isFoundFreshWater", &CvTerrainInfo::isFoundFreshWater, "bool ()")
		.def("isHell", &CvTerrainInfo::isHell, "bool ()")

		// Arrays

		.def("getYield", &CvTerrainInfo::getYield, "int (int i)")
		.def("getRiverYieldChange", &CvTerrainInfo::getRiverYieldChange, "int (int i)")
		.def("getHillsYieldChange", &CvTerrainInfo::getHillsYieldChange, "int (int i)")
		;

	// CvInterfaceModeInfo

	python::class_<CvInterfaceModeInfo, python::bases<CvInfoBase> >("CvInterfaceModeInfo")

		.def("getCursorIndex", &CvInterfaceModeInfo::getCursorIndex, "int ()")
		.def("getMissionType", &CvInterfaceModeInfo::getMissionType, "int ()")

		.def("getVisible", &CvInterfaceModeInfo::getVisible, "bool ()")
		.def("getGotoPlot", &CvInterfaceModeInfo::getGotoPlot, "bool ()")
		.def("getHighlightPlot", &CvInterfaceModeInfo::getHighlightPlot, "bool ()")
		.def("getSelectType", &CvInterfaceModeInfo::getSelectType, "bool ()")
		.def("getSelectAll", &CvInterfaceModeInfo::getSelectAll, "bool ()")

		.def("isAltDown", &CvInterfaceModeInfo::isAltDown, "bool ()")
		.def("isShiftDown", &CvInterfaceModeInfo::isShiftDown, "bool ()")
		.def("isCtrlDown", &CvInterfaceModeInfo::isCtrlDown, "bool ()")
		.def("isAltDownAlt", &CvInterfaceModeInfo::isAltDownAlt, "bool ()")
		.def("isShiftDownAlt", &CvInterfaceModeInfo::isShiftDownAlt, "bool ()")
		.def("isCtrlDownAlt", &CvInterfaceModeInfo::isCtrlDownAlt, "bool ()")
		;

	python::class_<CvLeaderHeadInfo, python::bases<CvInfoBase> >("CvLeaderHeadInfo")
		.def("getWonderConstructRand", &CvLeaderHeadInfo::getWonderConstructRand, "int ()")
		.def("getBaseAttitude", &CvLeaderHeadInfo::getBaseAttitude, "int ()")
		.def("getBasePeaceWeight", &CvLeaderHeadInfo::getBasePeaceWeight, "int ()")
		.def("getPeaceWeightRand", &CvLeaderHeadInfo::getPeaceWeightRand, "int ()")
		.def("getWarmongerRespect", &CvLeaderHeadInfo::getWarmongerRespect, "int ()")
		.def("getEspionageWeight", &CvLeaderHeadInfo::getEspionageWeight, "int ()")
		.def("getRefuseToTalkWarThreshold", &CvLeaderHeadInfo::getRefuseToTalkWarThreshold, "int ()")
		.def("getNoTechTradeThreshold", &CvLeaderHeadInfo::getNoTechTradeThreshold, "int ()")
		.def("getTechTradeKnownPercent", &CvLeaderHeadInfo::getTechTradeKnownPercent, "int ()")
		.def("getMaxGoldTradePercent", &CvLeaderHeadInfo::getMaxGoldTradePercent, "int ()")
		.def("getMaxGoldPerTurnTradePercent", &CvLeaderHeadInfo::getMaxGoldPerTurnTradePercent, "int ()")
		.def("getMaxWarRand", &CvLeaderHeadInfo::getMaxWarRand, "int ()")
		.def("getMaxWarNearbyPowerRatio", &CvLeaderHeadInfo::getMaxWarNearbyPowerRatio, "int ()")
		.def("getMaxWarDistantPowerRatio", &CvLeaderHeadInfo::getMaxWarDistantPowerRatio, "int ()")
		.def("getMaxWarMinAdjacentLandPercent", &CvLeaderHeadInfo::getMaxWarMinAdjacentLandPercent, "int ()")
		.def("getLimitedWarRand", &CvLeaderHeadInfo::getLimitedWarRand, "int ()")
		.def("getLimitedWarPowerRatio", &CvLeaderHeadInfo::getLimitedWarPowerRatio, "int ()")
		.def("getDogpileWarRand", &CvLeaderHeadInfo::getDogpileWarRand, "int ()")
		.def("getMakePeaceRand", &CvLeaderHeadInfo::getMakePeaceRand, "int ()")
		.def("getDeclareWarTradeRand", &CvLeaderHeadInfo::getDeclareWarTradeRand, "int ()")
		.def("getDemandRebukedSneakProb", &CvLeaderHeadInfo::getDemandRebukedSneakProb, "int ()")
		.def("getDemandRebukedWarProb", &CvLeaderHeadInfo::getDemandRebukedWarProb, "int ()")
		.def("getRazeCityProb", &CvLeaderHeadInfo::getRazeCityProb, "int ()")
		.def("getBuildUnitProb", &CvLeaderHeadInfo::getBuildUnitProb, "int ()")
		.def("getBaseAttackOddsChange", &CvLeaderHeadInfo::getBaseAttackOddsChange, "int ()")
		.def("getAttackOddsChangeRand", &CvLeaderHeadInfo::getAttackOddsChangeRand, "int ()")
		.def("getWorseRankDifferenceAttitudeChange", &CvLeaderHeadInfo::getWorseRankDifferenceAttitudeChange, "int ()")
		.def("getBetterRankDifferenceAttitudeChange", &CvLeaderHeadInfo::getBetterRankDifferenceAttitudeChange, "int ()")
		.def("getCloseBordersAttitudeChange", &CvLeaderHeadInfo::getCloseBordersAttitudeChange, "int ()")
		.def("getLostWarAttitudeChange", &CvLeaderHeadInfo::getLostWarAttitudeChange, "int ()")
		.def("getAtWarAttitudeDivisor", &CvLeaderHeadInfo::getAtWarAttitudeDivisor, "int ()")
		.def("getAtWarAttitudeChangeLimit", &CvLeaderHeadInfo::getAtWarAttitudeChangeLimit, "int ()")
		.def("getAtPeaceAttitudeDivisor", &CvLeaderHeadInfo::getAtPeaceAttitudeDivisor, "int ()")
		.def("getAtPeaceAttitudeChangeLimit", &CvLeaderHeadInfo::getAtPeaceAttitudeChangeLimit, "int ()")
		.def("getSameReligionAttitudeChange", &CvLeaderHeadInfo::getSameReligionAttitudeChange, "int ()")
		.def("getSameReligionAttitudeDivisor", &CvLeaderHeadInfo::getSameReligionAttitudeDivisor, "int ()")
		.def("getSameReligionAttitudeChangeLimit", &CvLeaderHeadInfo::getSameReligionAttitudeChangeLimit, "int ()")
		.def("getDifferentReligionAttitudeChange", &CvLeaderHeadInfo::getDifferentReligionAttitudeChange, "int ()")
		.def("getDifferentReligionAttitudeDivisor", &CvLeaderHeadInfo::getDifferentReligionAttitudeDivisor, "int ()")
		.def("getDifferentReligionAttitudeChangeLimit", &CvLeaderHeadInfo::getDifferentReligionAttitudeChangeLimit, "int ()")
		.def("getBonusTradeAttitudeDivisor", &CvLeaderHeadInfo::getBonusTradeAttitudeDivisor, "int ()")
		.def("getBonusTradeAttitudeChangeLimit", &CvLeaderHeadInfo::getBonusTradeAttitudeChangeLimit, "int ()")
		.def("getOpenBordersAttitudeDivisor", &CvLeaderHeadInfo::getOpenBordersAttitudeDivisor, "int ()")
		.def("getOpenBordersAttitudeChangeLimit", &CvLeaderHeadInfo::getOpenBordersAttitudeChangeLimit, "int ()")
		.def("getDefensivePactAttitudeDivisor", &CvLeaderHeadInfo::getDefensivePactAttitudeDivisor, "int ()")
		.def("getDefensivePactAttitudeChangeLimit", &CvLeaderHeadInfo::getDefensivePactAttitudeChangeLimit, "int ()")
		.def("getShareWarAttitudeChange", &CvLeaderHeadInfo::getShareWarAttitudeChange, "int ()")
		.def("getShareWarAttitudeDivisor", &CvLeaderHeadInfo::getShareWarAttitudeDivisor, "int ()")
		.def("getShareWarAttitudeChangeLimit", &CvLeaderHeadInfo::getShareWarAttitudeChangeLimit, "int ()")
		.def("getFavoriteCivicAttitudeChange", &CvLeaderHeadInfo::getFavoriteCivicAttitudeChange, "int ()")
		.def("getFavoriteCivicAttitudeDivisor", &CvLeaderHeadInfo::getFavoriteCivicAttitudeDivisor, "int ()")
		.def("getFavoriteCivicAttitudeChangeLimit", &CvLeaderHeadInfo::getFavoriteCivicAttitudeChangeLimit, "int ()")
		.def("getDemandTributeAttitudeThreshold", &CvLeaderHeadInfo::getDemandTributeAttitudeThreshold, "int ()")
		.def("getNoGiveHelpAttitudeThreshold", &CvLeaderHeadInfo::getNoGiveHelpAttitudeThreshold, "int ()")
		.def("getTechRefuseAttitudeThreshold", &CvLeaderHeadInfo::getTechRefuseAttitudeThreshold, "int ()")
		.def("getStrategicBonusRefuseAttitudeThreshold", &CvLeaderHeadInfo::getStrategicBonusRefuseAttitudeThreshold, "int ()")
		.def("getHappinessBonusRefuseAttitudeThreshold", &CvLeaderHeadInfo::getHappinessBonusRefuseAttitudeThreshold, "int ()")
		.def("getHealthBonusRefuseAttitudeThreshold", &CvLeaderHeadInfo::getHealthBonusRefuseAttitudeThreshold, "int ()")
		.def("getMapRefuseAttitudeThreshold", &CvLeaderHeadInfo::getMapRefuseAttitudeThreshold, "int ()")
		.def("getDeclareWarRefuseAttitudeThreshold", &CvLeaderHeadInfo::getDeclareWarRefuseAttitudeThreshold, "int ()")
		.def("getDeclareWarThemRefuseAttitudeThreshold", &CvLeaderHeadInfo::getDeclareWarThemRefuseAttitudeThreshold, "int ()")
		.def("getStopTradingRefuseAttitudeThreshold", &CvLeaderHeadInfo::getStopTradingRefuseAttitudeThreshold, "int ()")
		.def("getStopTradingThemRefuseAttitudeThreshold", &CvLeaderHeadInfo::getStopTradingThemRefuseAttitudeThreshold, "int ()")
		.def("getAdoptCivicRefuseAttitudeThreshold", &CvLeaderHeadInfo::getAdoptCivicRefuseAttitudeThreshold, "int ()")
		.def("getConvertReligionRefuseAttitudeThreshold", &CvLeaderHeadInfo::getConvertReligionRefuseAttitudeThreshold, "int ()")
		.def("getOpenBordersRefuseAttitudeThreshold", &CvLeaderHeadInfo::getOpenBordersRefuseAttitudeThreshold, "int ()")
		.def("getDefensivePactRefuseAttitudeThreshold", &CvLeaderHeadInfo::getDefensivePactRefuseAttitudeThreshold, "int ()")
		.def("getPermanentAllianceRefuseAttitudeThreshold", &CvLeaderHeadInfo::getPermanentAllianceRefuseAttitudeThreshold, "int ()")
		.def("getVassalRefuseAttitudeThreshold", &CvLeaderHeadInfo::getVassalRefuseAttitudeThreshold, "int ()")
		.def("getFavoriteCivic", &CvLeaderHeadInfo::getFavoriteCivic, "int ()")
		.def("getVassalPowerModifier", &CvLeaderHeadInfo::getVassalPowerModifier, "int ()")
		.def("getFreedomAppreciation", &CvLeaderHeadInfo::getFreedomAppreciation, "int ()")

		.def("getArtDefineTag", &CvLeaderHeadInfo::getArtDefineTag, "string ()")

/*************************************************************************************************/
/**	New Tag Defs	(LeaderInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Exposes the Functions to Python									**/
/*************************************************************************************************/
		.def("isFemale", &CvLeaderHeadInfo::isFemale, "bool ()")
		.def("getAlignment", &CvLeaderHeadInfo::getAlignment, "int ()")
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
		.def("getLeaderClass", &CvLeaderHeadInfo::getLeaderClass, "int ()")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
		.def("getAlignmentModifier", &CvLeaderHeadInfo::getAlignmentModifier, "int ()")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		.def("getEthicalAlignment", &CvLeaderHeadInfo::getEthicalAlignment, "int ()")
		.def("getEthicalAlignmentModifier", &CvLeaderHeadInfo::getEthicalAlignmentModifier, "int ()")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
		.def("getProximityMemoryDecayDelay", &CvLeaderHeadInfo::getProximityMemoryDecayDelay, "int ()")
		.def("getProximityMemoryDecayRand", &CvLeaderHeadInfo::getProximityMemoryDecayRand, "int ()")
		.def("getProximityMemoryLimit", &CvLeaderHeadInfo::getProximityMemoryLimit, "int ()")
		.def("getProximityMemoryDecaySpeed", &CvLeaderHeadInfo::getProximityMemoryDecaySpeed, "float ()")
		.def("getDefeatQuote", &CvLeaderHeadInfo::getDefeatQuote, "string ()")
		.def("getImage", &CvLeaderHeadInfo::getImage, "string ()")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 09/02/2007
		.def("getFavoriteWonder", &CvLeaderHeadInfo::getFavoriteWonder, "int ()")
		.def("getPermanentTrait", &CvLeaderHeadInfo::getPermanentTrait, "int ()")
//FfH Card Game: Added by Sto 08/08/2008
		.def("getSomniumAggressiveness", &CvLeaderHeadInfo::getSomniumAggressiveness, "int ()")
//FfH: End Add
//FfH: End Add

/*************************************************************************************************/
/** HatedCivic      Opera       31.05.09                                                        **/
/*************************************************************************************************/
		.def("getHatedCivicAttitudeChange", &CvLeaderHeadInfo::getHatedCivicAttitudeChange, "int ()")
		.def("getHatedCivicAttitudeDivisor", &CvLeaderHeadInfo::getHatedCivicAttitudeDivisor, "int ()")
		.def("getHatedCivicAttitudeChangeLimit", &CvLeaderHeadInfo::getHatedCivicAttitudeChangeLimit, "int ()")
		.def("getHatedCivic", &CvLeaderHeadInfo::getHatedCivic, "int ()")
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

		// Arrays

		.def("hasTrait", &CvLeaderHeadInfo::hasTrait, "bool (int i)")

		.def("getFlavorValue", &CvLeaderHeadInfo::getFlavorValue, "int (int i)")
		.def("getContactRand", &CvLeaderHeadInfo::getContactRand, "int (int i)")
		.def("getContactDelay", &CvLeaderHeadInfo::getContactDelay, "int (int i)")
		.def("getMemoryDecayRand", &CvLeaderHeadInfo::getMemoryDecayRand, "int (int i)")
		.def("getMemoryAttitudePercent", &CvLeaderHeadInfo::getMemoryAttitudePercent, "int (int i)")
		.def("getNoWarAttitudeProb", &CvLeaderHeadInfo::getNoWarAttitudeProb, "int (int i)")
		.def("getUnitAIWeightModifier", &CvLeaderHeadInfo::getUnitAIWeightModifier, "int (int i)")
		.def("getImprovementWeightModifier", &CvLeaderHeadInfo::getImprovementWeightModifier, "int (int i)")
		.def("getDiploPeaceIntroMusicScriptIds", &CvLeaderHeadInfo::getDiploPeaceIntroMusicScriptIds, "int (int i)")
		.def("getDiploPeaceMusicScriptIds", &CvLeaderHeadInfo::getDiploPeaceMusicScriptIds, "int (int i)")
		.def("getDiploWarIntroMusicScriptIds", &CvLeaderHeadInfo::getDiploWarIntroMusicScriptIds, "int (int i)")
		.def("getDiploWarMusicScriptIds", &CvLeaderHeadInfo::getDiploWarMusicScriptIds, "int (int i)")
/*************************************************************************************************/
/** Exposing to python ReligionWeight   Opera       09.06.09                                    **/
/*************************************************************************************************/
		.def("getReligionWeightModifier", &CvLeaderHeadInfo::getReligionWeightModifier, "int (int i)")
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** BonusAttitudeModifier           Opera           30.07.09                                    **/
/*************************************************************************************************/
		.def("getBonusAttitudeModifier", &CvLeaderHeadInfo::getBonusAttitudeModifier, "int (int i)")
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

		// Other

		.def("getLeaderHead", &CvLeaderHeadInfo::getLeaderHead, "string ()")
		.def("getButton", &CvLeaderHeadInfo::getButton, "string ()")
		;

	// CvProcessInfos
	python::class_<CvProcessInfo, python::bases<CvInfoBase> >("CvProcessInfo")
		.def("getTechPrereq", &CvProcessInfo::getTechPrereq, "int ()")

		// Arrays

		.def("getProductionToCommerceModifier", &CvProcessInfo::getProductionToCommerceModifier, "int (int i)")
		;

	python::class_<CvVoteInfo, python::bases<CvInfoBase> >("CvVoteInfo")
		.def("getPopulationThreshold", &CvVoteInfo::getPopulationThreshold, "int ()")
		.def("getStateReligionVotePercent", &CvVoteInfo::getStateReligionVotePercent, "int ()")
		.def("getTradeRoutes", &CvVoteInfo::getTradeRoutes, "int ()")
		.def("getMinVoters", &CvVoteInfo::getMinVoters, "int ()")

		.def("isSecretaryGeneral", &CvVoteInfo::isSecretaryGeneral, "bool ()")
		.def("isVictory", &CvVoteInfo::isVictory, "bool ()")
		.def("isFreeTrade", &CvVoteInfo::isFreeTrade, "bool ()")
		.def("isNoNukes", &CvVoteInfo::isNoNukes, "bool ()")
		.def("isCityVoting", &CvVoteInfo::isCityVoting, "bool ()")
		.def("isCivVoting", &CvVoteInfo::isCivVoting, "bool ()")
		.def("isDefensivePact", &CvVoteInfo::isDefensivePact, "bool ()")
		.def("isOpenBorders", &CvVoteInfo::isOpenBorders, "bool ()")
		.def("isForcePeace", &CvVoteInfo::isForcePeace, "bool ()")
		.def("isForceNoTrade", &CvVoteInfo::isForceNoTrade, "bool ()")
		.def("isForceWar", &CvVoteInfo::isForceWar, "bool ()")
		.def("isAssignCity", &CvVoteInfo::isAssignCity, "bool ()")

//FfH: Added by Kael 11/21/2007
		.def("getPyResult", &CvVoteInfo::getPyResult, "string ()")
//FfH: End Add

		// Arrays

		.def("isForceCivic", &CvVoteInfo::isForceCivic, "bool (int i)")
		.def("isVoteSourceType", &CvVoteInfo::isVoteSourceType, "bool (int i)")
		;

	python::class_<CvProjectInfo, python::bases<CvInfoBase> >("CvProjectInfo")
		.def("getVictoryPrereq", &CvProjectInfo::getVictoryPrereq, "int ()")
		.def("getTechPrereq", &CvProjectInfo::getTechPrereq, "int ()")
		.def("getAnyoneProjectPrereq", &CvProjectInfo::getAnyoneProjectPrereq, "int ()")
		.def("getMaxGlobalInstances", &CvProjectInfo::getMaxGlobalInstances, "int ()")
		.def("getMaxTeamInstances", &CvProjectInfo::getMaxTeamInstances, "int ()")
		.def("getProductionCost", &CvProjectInfo::getProductionCost, "int ()")
		.def("getNukeInterception", &CvProjectInfo::getNukeInterception, "int ()")
		.def("getTechShare", &CvProjectInfo::getTechShare, "int ()")
		.def("getEveryoneSpecialUnit", &CvProjectInfo::getEveryoneSpecialUnit, "int ()")
		.def("getEveryoneSpecialBuilding", &CvProjectInfo::getEveryoneSpecialBuilding, "int ()")

		.def("isSpaceship", &CvProjectInfo::isSpaceship, "bool ()")
		.def("isAllowsNukes", &CvProjectInfo::isAllowsNukes, "bool ()")

		.def("getMovieArtDef", &CvProjectInfo::getMovieArtDef, "string ()")
		.def("getCreateSound", &CvProjectInfo::getCreateSound, "string ()")

//FfH: Added by Kael 10/01/2008
		.def("getNumPrereqCivilizations", &CvProjectInfo::getNumPrereqCivilizations, "int ()")
		.def("getPrereqCivilization", &CvProjectInfo::getPrereqCivilization, "int (int iI)")
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(ProjectInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Exposes the Functions to Python									**/
/*************************************************************************************************/
		.def("getPrereqGlobalCounter", &CvProjectInfo::getPrereqGlobalCounter, "int ()")
		.def("getNumPrereqAlignments", &CvProjectInfo::getNumPrereqAlignments, "int ()")
		.def("getPrereqAlignment", &CvProjectInfo::getPrereqAlignment, "int (int iI)")
		.def("isResetProjects", &CvProjectInfo::isResetProjects, "bool ()")
		.def("isPrereqWar", &CvProjectInfo::isPrereqWar, "bool ()")
		.def("isPrereqBlockBonuses", &CvProjectInfo::isPrereqBlockBonuses, "bool ()")
		.def("getPrereqBroadAlignment", &CvProjectInfo::getPrereqBroadAlignment, "int ()")
		.def("getAlignmentModifier", &CvProjectInfo::getAlignmentModifier, "int ()")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		.def("getNumPrereqEthicalAlignments", &CvProjectInfo::getNumPrereqEthicalAlignments, "int ()")
		.def("getPrereqEthicalAlignment", &CvProjectInfo::getPrereqEthicalAlignment, "int (int iI)")
		.def("getPrereqBroadEthicalAlignment", &CvProjectInfo::getPrereqBroadEthicalAlignment, "int ()")
		.def("getEthicalAlignmentModifier", &CvProjectInfo::getEthicalAlignmentModifier, "int ()")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
		.def("getRevealAllBonuses", &CvProjectInfo::getRevealAllBonuses, "int ()")
		.def("getHideUnits", &CvProjectInfo::getHideUnits, "int ()")
		.def("getSeeInvisible", &CvProjectInfo::getSeeInvisible, "int ()")
		.def("getBlockBonuses", &CvProjectInfo::getBlockBonuses, "int ()")
		.def("getRestoreBonuses", &CvProjectInfo::getRestoreBonuses, "int ()")
		.def("getCooldown", &CvProjectInfo::getCooldown, "int ()")
		.def("isResistable", &CvProjectInfo::isResistable, "bool ()")
		.def("getResistBase", &CvProjectInfo::getResistBase, "int ()")
		.def("getResistMax", &CvProjectInfo::getResistMax, "int ()")
		.def("getResistMin", &CvProjectInfo::getResistMin, "int ()")
		.def("getForcePeaceWithCivilization", &CvProjectInfo::getForcePeaceWithCivilization, "int ()")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

		// Arrays

		.def("getBonusProductionModifier", &CvProjectInfo::getBonusProductionModifier, "int (int i)")
		.def("getVictoryThreshold", &CvProjectInfo::getVictoryThreshold, "int (int i)")
		.def("getVictoryMinThreshold", &CvProjectInfo::getVictoryMinThreshold, "int (int i)")
		.def("getVictoryDelayPercent", &CvProjectInfo::getVictoryDelayPercent, "int ()")
		.def("getSuccessRate", &CvProjectInfo::getSuccessRate, "int ()")
		.def("getProjectsNeeded", &CvProjectInfo::getProjectsNeeded, "int (int i)")
		;

	python::class_<CvReligionInfo, python::bases<CvInfoBase> >("CvReligionInfo")
		.def("getChar", &CvReligionInfo::getChar, "int ()")
		.def("getHolyCityChar", &CvReligionInfo::getHolyCityChar, "int ()")
		.def("getTechPrereq", &CvReligionInfo::getTechPrereq, "int ()")
		.def("getFreeUnitClass", &CvReligionInfo::getFreeUnitClass, "int ()")
		.def("getNumFreeUnits", &CvReligionInfo::getNumFreeUnits, "int ()")
		.def("getSpreadFactor", &CvReligionInfo::getSpreadFactor, "int ()")
		.def("getMissionType", &CvReligionInfo::getMissionType, "int ()")

		.def("getTechButton", &CvReligionInfo::getTechButton, "string ()")
		.def("getGenericTechButton", &CvReligionInfo::getGenericTechButton, "string ()")
		.def("getMovieFile", &CvReligionInfo::getMovieFile, "string ()")
		.def("getMovieSound", &CvReligionInfo::getMovieSound, "string ()")
		.def("getSound", &CvReligionInfo::getSound, "string ()")
		.def("getButtonDisabled", &CvReligionInfo::getButtonDisabled, "string ()")
		.def("getAdjectiveKey", &CvReligionInfo::pyGetAdjectiveKey, "wstring ()")

//FfH: Added by Kael 09/02/2007
		.def("isHidden", &CvReligionInfo::isHidden, "bool ()")
//FfH: End Add

		// Arrays

		.def("getGlobalReligionCommerce", &CvReligionInfo::getGlobalReligionCommerce, "int (int i)")
		.def("getHolyCityCommerce", &CvReligionInfo::getHolyCityCommerce, "int (int i)")
		.def("getStateReligionCommerce", &CvReligionInfo::getStateReligionCommerce, "int (int i)")
/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
		.def("getGlobalReligionYield", &CvReligionInfo::getGlobalReligionYield, "int (int i)")
		.def("getHolyCityYield", &CvReligionInfo::getHolyCityYield, "int (int i)")
		.def("getStateReligionYield", &CvReligionInfo::getStateReligionYield, "int (int i)")
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Religion Based Music					02/09/10									Snarko	**/
/**				Changing music from eras to religions (or eras if no religion)					**/
/*************************************************************************************************/
		.def("getNumSoundtracks", &CvReligionInfo::getNumSoundtracks, "int ()")
		.def("getSoundtracks", &CvReligionInfo::getSoundtracks, "int (int i)")
/*************************************************************************************************/
/**	Religion Based Music						END												**/
/*************************************************************************************************/
		;

	python::class_<CvCorporationInfo, python::bases<CvInfoBase> >("CvCorporationInfo")
		.def("getChar", &CvCorporationInfo::getChar, "int ()")
		.def("getHeadquarterChar", &CvCorporationInfo::getHeadquarterChar, "int ()")
		.def("getTechPrereq", &CvCorporationInfo::getTechPrereq, "int ()")
		.def("getFreeUnitClass", &CvCorporationInfo::getFreeUnitClass, "int ()")
		.def("getSpreadFactor", &CvCorporationInfo::getSpreadFactor, "int ()")
		.def("getSpreadCost", &CvCorporationInfo::getSpreadCost, "int ()")
		.def("getMaintenance", &CvCorporationInfo::getMaintenance, "int ()")
		.def("getMissionType", &CvCorporationInfo::getMissionType, "int ()")

		.def("getMovieFile", &CvCorporationInfo::getMovieFile, "string ()")
		.def("getMovieSound", &CvCorporationInfo::getMovieSound, "string ()")
		.def("getSound", &CvCorporationInfo::getSound, "string ()")

/*************************************************************************************************/
/**	LoadedTGA								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Modifies how the TGA is handled to allow many more religions/corporations/resources easily	**/
/*************************************************************************************************/
		.def("getTGAIndex", &CvReligionInfo::getTGAIndex, "int ()")
/*************************************************************************************************/
/**	LoadedTGA								END													**/
/*************************************************************************************************/
		// Arrays

		.def("getPrereqBonus", &CvCorporationInfo::getPrereqBonus, "int (int i)")
		.def("getHeadquarterCommerce", &CvCorporationInfo::getHeadquarterCommerce, "int (int i)")
		.def("getCommerceProduced", &CvCorporationInfo::getCommerceProduced, "int (int i)")
		.def("getYieldProduced", &CvCorporationInfo::getYieldProduced, "int (int i)")
		;
	python::class_<CvCityClassInfo, python::bases<CvInfoBase> >("CvCityClassInfo")
		.def("getShortDescription", &CvCityClassInfo::getShortDescription, "int ()")
		.def("getCityClassBuildings", &CvCityClassInfo::getCityClassBuildings, "int (int i)")
		.def("getCityClassUnits", &CvCityClassInfo::getCityClassUnits, "int (int i)")

		;
	python::class_<CvTraitInfo, python::bases<CvInfoBase> >("CvTraitInfo")
		.def("getLevel", &CvTraitInfo::getLevel, "int ()")
		.def("getTraitClass", &CvTraitInfo::getTraitClass, "int ()")
		.def("getNextTrait", &CvTraitInfo::getNextTrait,"int()")
		.def("getParentTrait", &CvTraitInfo::getParentTrait, "int()")

		.def("getHealth", &CvTraitInfo::getHealth, "int ()")
		.def("getHappiness", &CvTraitInfo::getHappiness, "int ()")
		.def("getMaxAnarchy", &CvTraitInfo::getMaxAnarchy, "int ()")
		.def("getUpkeepModifier", &CvTraitInfo::getUpkeepModifier, "int ()")
		.def("getLevelExperienceModifier", &CvTraitInfo::getLevelExperienceModifier, "int ()")
		.def("getGreatPeopleRateModifier", &CvTraitInfo::getGreatPeopleRateModifier, "int ()")
		.def("getGreatGeneralRateModifier", &CvTraitInfo::getGreatGeneralRateModifier, "int ()")
		.def("getDomesticGreatGeneralRateModifier", &CvTraitInfo::getDomesticGreatGeneralRateModifier, "int ()")
		.def("getMaxGlobalBuildingProductionModifier", &CvTraitInfo::getMaxGlobalBuildingProductionModifier, "int ()")
		.def("getMaxTeamBuildingProductionModifier", &CvTraitInfo::getMaxTeamBuildingProductionModifier, "int ()")
		.def("getMaxPlayerBuildingProductionModifier", &CvTraitInfo::getMaxPlayerBuildingProductionModifier, "int ()")

		.def("getShortDescription", &CvTraitInfo::getShortDescription, "int (int i)")
		.def("getExtraYieldThreshold", &CvTraitInfo::getExtraYieldThreshold, "int (int i)")
		.def("getTradeYieldModifier", &CvTraitInfo::getTradeYieldModifier, "int (int i)")
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
		.def("getTradeCommerceModifier", &CvTraitInfo::getTradeCommerceModifier, "int (int i)")
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		.def("getCommerceChange", &CvTraitInfo::getCommerceChange, "int (int i)")
		.def("getCommerceModifier", &CvTraitInfo::getCommerceModifier, "int (int i)")

		.def("isFreePromotion", &CvTraitInfo::isFreePromotion, "int (int i)")
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
		.def("getSpecialistYieldChange", &CvTraitInfo::getSpecialistYieldChange, "int (int i, int j)")
		.def("getSpecialistCommerceChange", &CvTraitInfo::getSpecialistCommerceChange, "int (int i, int j)")
		.def("getPeaceCommerceModifier", &CvTraitInfo::getPeaceCommerceModifier, "int (int i)")
		.def("getFeatureProductionChange", &CvTraitInfo::getFeatureProductionChange, "int (int i)")
		.def("getFeatureGrowthChange", &CvTraitInfo::getFeatureGrowthChange, "int (int i)")
		.def("getHurryPopulationModifier", &CvTraitInfo::getHurryPopulationModifier, "int ()")
/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/

//FfH: Added by Kael 10/11/2007
		.def("isSelectable", &CvTraitInfo::isSelectable, "bool ()")
//FfH: End Add

		;

	// CvWorldInfo
	python::class_<CvWorldInfo, python::bases<CvInfoBase> >("CvWorldInfo")
		.def("getDefaultPlayers", &CvWorldInfo::getDefaultPlayers, "int ()")
		.def("getUnitNameModifier", &CvWorldInfo::getUnitNameModifier, "int ()")
		.def("getTargetNumCities", &CvWorldInfo::getTargetNumCities, "int ()")
		.def("getNumFreeBuildingBonuses", &CvWorldInfo::getNumFreeBuildingBonuses, "int ()")
		.def("getBuildingClassPrereqModifier", &CvWorldInfo::getBuildingClassPrereqModifier, "int ()")
		.def("getMaxConscriptModifier", &CvWorldInfo::getMaxConscriptModifier, "int ()")
		.def("getWarWearinessModifier", &CvWorldInfo::getWarWearinessModifier, "int ()")
		.def("getGridWidth", &CvWorldInfo::getGridWidth, "int ()")
		.def("getGridHeight", &CvWorldInfo::getGridHeight, "int ()")
		.def("getTerrainGrainChange", &CvWorldInfo::getTerrainGrainChange, "int ()")
		.def("getFeatureGrainChange", &CvWorldInfo::getFeatureGrainChange, "int ()")
		.def("getResearchPercent", &CvWorldInfo::getResearchPercent, "int ()")
		.def("getTradeProfitPercent", &CvWorldInfo::getTradeProfitPercent, "int ()")
		.def("getDistanceMaintenancePercent", &CvWorldInfo::getDistanceMaintenancePercent, "int ()")
		.def("getNumCitiesMaintenancePercent", &CvWorldInfo::getNumCitiesMaintenancePercent, "int ()")
		.def("getColonyMaintenancePercent", &CvWorldInfo::getColonyMaintenancePercent, "int ()")
		.def("getCorporationMaintenancePercent", &CvWorldInfo::getCorporationMaintenancePercent, "int ()")
		.def("getNumCitiesAnarchyPercent", &CvWorldInfo::getNumCitiesAnarchyPercent, "int ()")
		;

	python::class_<CvClimateInfo, python::bases<CvInfoBase> >("CvClimateInfo")
		.def("getDesertPercentChange", &CvClimateInfo::getDesertPercentChange, "int ()")
		.def("getJungleLatitude", &CvClimateInfo::getJungleLatitude, "int ()")
		.def("getHillRange", &CvClimateInfo::getHillRange, "int ()")
		.def("getPeakPercent", &CvClimateInfo::getPeakPercent, "int ()")

		.def("getSnowLatitudeChange", &CvClimateInfo::getSnowLatitudeChange, "float ()")
		.def("getTundraLatitudeChange", &CvClimateInfo::getTundraLatitudeChange, "float ()")
		.def("getGrassLatitudeChange", &CvClimateInfo::getGrassLatitudeChange, "float ()")
		.def("getDesertBottomLatitudeChange", &CvClimateInfo::getDesertBottomLatitudeChange, "float ()")
		.def("getDesertTopLatitudeChange", &CvClimateInfo::getDesertTopLatitudeChange, "float ()")
		.def("getIceLatitude", &CvClimateInfo::getIceLatitude, "float ()")
		.def("getRandIceLatitude", &CvClimateInfo::getRandIceLatitude, "float ()")
		;

	python::class_<CvSeaLevelInfo, python::bases<CvInfoBase> >("CvSeaLevelInfo")
		.def("getSeaLevelChange", &CvSeaLevelInfo::getSeaLevelChange, "int ()")
		;

	python::class_<CvAssetInfoBase>("CvAssetInfoBase")
		.def("setTag", &CvAssetInfoBase::setTag, "void (string)")
		.def("getTag", &CvAssetInfoBase::getTag, "string ()")
		.def("setPath", &CvAssetInfoBase::setPath, "void (string)")
		.def("getPath", &CvAssetInfoBase::getPath, "string ()")
		;

	python::class_<CvArtInfoAsset, python::bases<CvAssetInfoBase> >("CvArtInfoAsset")
		.def("getButton", &CvArtInfoAsset::getButton, "string ()")
		.def("setNIF", &CvArtInfoAsset::setNIF, "void (string)")
		.def("getNIF", &CvArtInfoAsset::getNIF, "string ()")
		.def("setKFM", &CvArtInfoAsset::setKFM, "void (string)")
		.def("getKFM", &CvArtInfoAsset::getKFM, "string ()")
		;

	python::class_<CvArtInfoScalableAsset, python::bases<CvArtInfoAsset, CvScalableInfo> >("CvArtInfoScalableAsset")
		;

	python::class_<CvArtInfoInterface, python::bases<CvArtInfoAsset> >("CvArtInfoInterface")
		;

	python::class_<CvArtInfoMovie, python::bases<CvArtInfoAsset> >("CvArtInfoMovie")
		;

	python::class_<CvArtInfoMisc, python::bases<CvArtInfoAsset> >("CvArtInfoMisc")
		;

	python::class_<CvArtInfoUnit, python::bases<CvArtInfoScalableAsset> >("CvArtInfoUnit")
		.def("getInterfaceScale", &CvArtInfoUnit::getInterfaceScale, "float ()")
		.def("getKFM", &CvArtInfoUnit::getKFM, "string ()")
		;

	python::class_<CvArtInfoBuilding, python::bases<CvArtInfoScalableAsset> >("CvArtInfoBuilding")
		.def("isAnimated", &CvArtInfoBuilding::isAnimated, "bool ()")
		;

	python::class_<CvArtInfoCivilization, python::bases<CvArtInfoAsset> >("CvArtInfoCivilization")
		.def("isWhiteFlag", &CvArtInfoCivilization::isWhiteFlag, "bool ()")
		;

	python::class_<CvArtInfoLeaderhead, python::bases<CvArtInfoAsset> >("CvArtInfoLeaderhead")
		;

	python::class_<CvArtInfoBonus, python::bases<CvArtInfoScalableAsset> >("CvArtInfoBonus")
		;

	python::class_<CvArtInfoImprovement, python::bases<CvArtInfoScalableAsset> >("CvArtInfoImprovement")
		.def("isExtraAnimations", &CvArtInfoImprovement::isExtraAnimations, "bool ()")
		;

	python::class_<CvArtInfoTerrain, python::bases<CvArtInfoAsset> >("CvArtInfoTerrain")
		;

	python::class_<CvArtInfoFeature, python::bases<CvArtInfoScalableAsset> >("CvArtInfoFeature")
		.def("isAnimated", &CvArtInfoFeature::isAnimated, "bool ()")
		.def("isRiverArt", &CvArtInfoFeature::isRiverArt, "bool ()")
		.def("getFeatureDummyNodeName", &CvArtInfoFeature::getFeatureDummyNodeName, "string (int variety, string tagName)")
		;

	python::class_<CvEmphasizeInfo, python::bases<CvInfoBase> >("CvEmphasizeInfo")
		.def("isAvoidGrowth", &CvEmphasizeInfo::isAvoidGrowth, "bool ()")
		.def("isGreatPeople", &CvEmphasizeInfo::isGreatPeople, "bool ()")

/*************************************************************************************************/
/**	New Tag Defs	(CityAIInfos)			11/15/08								Jean Elcard	**/
/**																								**/
/**								Exposes the Functions to Python									**/
/*************************************************************************************************/
		.def("isAvoidAngryCitizens", &CvEmphasizeInfo::isAvoidAngryCitizens, "bool ()")
		.def("isAvoidUnhealthyCitizens", &CvEmphasizeInfo::isAvoidUnhealthyCitizens, "bool ()")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
		// Arrays

		.def("getYieldChange", &CvEmphasizeInfo::getYieldChange, "int (int i)")
		.def("getCommerceChange", &CvEmphasizeInfo::getCommerceChange, "int (int i)")
		;

	python::class_<CvUpkeepInfo, python::bases<CvInfoBase> >("CvUpkeepInfo")
		.def("getPopulationPercent", &CvUpkeepInfo::getPopulationPercent, "int ()")
		.def("getCityPercent", &CvUpkeepInfo::getCityPercent, "int ()")
		;

	python::class_<CvCultureLevelInfo, python::bases<CvInfoBase> >("CvCultureLevelInfo")
		.def("getCityDefenseModifier", &CvCultureLevelInfo::getCityDefenseModifier, "int ()")

		.def("getSpeedThreshold", &CvCultureLevelInfo::getSpeedThreshold, "int ()")
		;

	python::class_<CvEraInfo, python::bases<CvInfoBase> >("CvEraInfo")
		.def("getStartingUnitMultiplier", &CvEraInfo::getStartingUnitMultiplier, "int () -")
		.def("getStartingDefenseUnits", &CvEraInfo::getStartingDefenseUnits, "int () -")
		.def("getStartingWorkerUnits", &CvEraInfo::getStartingWorkerUnits, "int () -")
		.def("getStartingExploreUnits", &CvEraInfo::getStartingExploreUnits, "int () -")
		.def("getStartingGold", &CvEraInfo::getStartingGold, "int () -")
		.def("getFreePopulation", &CvEraInfo::getFreePopulation, "int () -")
		.def("getStartPercent", &CvEraInfo::getStartPercent, "int () -")
		.def("getGrowthPercent", &CvEraInfo::getGrowthPercent, "int () -")
		.def("getTrainPercent", &CvEraInfo::getTrainPercent, "int () -")
		.def("getConstructPercent", &CvEraInfo::getConstructPercent, "int () -")
		.def("getCreatePercent", &CvEraInfo::getCreatePercent, "int () -")
		.def("getResearchPercent", &CvEraInfo::getResearchPercent, "int () -")
		.def("getBuildPercent", &CvEraInfo::getBuildPercent, "int () -")
		.def("getImprovementPercent", &CvEraInfo::getImprovementPercent, "int () -")
		.def("getGreatPeoplePercent", &CvEraInfo::getGreatPeoplePercent, "int () -")
		.def("getAnarchyPercent", &CvEraInfo::getAnarchyPercent, "int () -")
		.def("getEventChancePerTurn", &CvEraInfo::getEventChancePerTurn, "int () -")
		.def("getSoundtrackSpace", &CvEraInfo::getSoundtrackSpace, "int () -")
		.def("isFirstSoundtrackFirst", &CvEraInfo::isFirstSoundtrackFirst, "int () -")
		.def("getNumSoundtracks", &CvEraInfo::getNumSoundtracks, "int () -")
		.def("getAudioUnitVictoryScript", &CvEraInfo::getAudioUnitVictoryScript, "string () -")
		.def("getAudioUnitDefeatScript", &CvEraInfo::getAudioUnitDefeatScript, "string () -")

		.def("isNoGoodies", &CvEraInfo::isNoGoodies, "bool () -")
		.def("isNoAnimals", &CvEraInfo::isNoAnimals, "bool () -")
		.def("isNoBarbUnits", &CvEraInfo::isNoBarbUnits, "bool () -")
		.def("isNoBarbCities", &CvEraInfo::isNoBarbCities, "bool () -")

		// Arrays

		.def("getSoundtracks", &CvEraInfo::getSoundtracks, "int (int i) -")
		.def("getCitySoundscapeSciptId", &CvEraInfo::getCitySoundscapeSciptId, "int (int i) -")
		;

	python::class_<CvColorInfo, python::bases<CvInfoBase> >("CvColorInfo")
		.def("getColor", &CvColorInfo::getColor,  python::return_value_policy<python::reference_existing_object>())
		;

	python::class_<CvPlayerColorInfo, python::bases<CvInfoBase> >("CvPlayerColorInfo")
		.def("getColorTypePrimary", &CvPlayerColorInfo::getColorTypePrimary, "int ()")
		.def("getColorTypeSecondary", &CvPlayerColorInfo::getColorTypeSecondary, "int ()")
		.def("getTextColorType", &CvPlayerColorInfo::getTextColorType, "int ()")
		;

	python::class_<CvGameText, python::bases<CvInfoBase> >("CvGameText")
		.def("getText", &CvGameText::pyGetText, "wstring ()")
		.def("setText", &CvGameText::setText, "void (wstring)")
		.def("getNumLanguages", &CvGameText::getNumLanguages, "int ()")
		;

	python::class_<CvDiplomacyTextInfo, python::bases<CvInfoBase> >("CvDiplomacyTextInfo")
		.def("getResponse", &CvDiplomacyTextInfo::getResponse,  python::return_value_policy<python::reference_existing_object>(), "Response (int iNum)")
		.def("getNumResponses", &CvDiplomacyTextInfo::getNumResponses, "int ()")

		.def("getCivilizationTypes", &CvDiplomacyTextInfo::getCivilizationTypes, "bool (int i, int j)")
		.def("getLeaderHeadTypes", &CvDiplomacyTextInfo::getLeaderHeadTypes, "bool (int i, int j)")
		.def("getAttitudeTypes", &CvDiplomacyTextInfo::getAttitudeTypes, "bool (int i, int j)")
		.def("getDiplomacyPowerTypes", &CvDiplomacyTextInfo::getDiplomacyPowerTypes, "bool (int i, int j)")

		.def("getNumDiplomacyText", &CvDiplomacyTextInfo::getNumDiplomacyText, "int (int i)")

		.def("getDiplomacyText", &CvDiplomacyTextInfo::getDiplomacyText, "string (int i, int j)")
		;

	python::class_<CvDiplomacyInfo, python::bases<CvInfoBase> >("CvDiplomacyInfo")
		.def("getResponse", &CvDiplomacyInfo::getResponse,  python::return_value_policy<python::reference_existing_object>(), "CvDiplomacyResponse (int iNum)")
		.def("getNumResponses", &CvDiplomacyInfo::getNumResponses, "int ()")

		.def("getCivilizationTypes", &CvDiplomacyInfo::getCivilizationTypes, "bool (int i, int j)")
		.def("getLeaderHeadTypes", &CvDiplomacyInfo::getLeaderHeadTypes, "bool (int i, int j)")
		.def("getAttitudeTypes", &CvDiplomacyInfo::getAttitudeTypes, "bool (int i, int j)")
		.def("getDiplomacyPowerTypes", &CvDiplomacyInfo::getDiplomacyPowerTypes, "bool (int i, int j)")

		.def("getNumDiplomacyText", &CvDiplomacyInfo::getNumDiplomacyText, "int (int i)")

		.def("getDiplomacyText", &CvDiplomacyInfo::getDiplomacyText, "string (int i, int j)")
		;

	python::class_<CvEffectInfo, python::bases<CvInfoBase, CvScalableInfo> >("CvEffectInfo")
		.def("getPath", &CvEffectInfo::getPath, "string ()")
		.def("setPath", &CvEffectInfo::setPath, "void (string)")
		;

	python::class_<CvControlInfo, python::bases<CvInfoBase> >("CvControlInfo")
		.def("getActionInfoIndex", &CvControlInfo::getActionInfoIndex, "int ()")
		;

	python::class_<CvQuestInfo, python::bases<CvInfoBase> >("CvQuestInfo")
		.def("getQuestMessages", &CvQuestInfo::getQuestMessages, "int ()")
		.def("getNumQuestLinks", &CvQuestInfo::getNumQuestLinks, "int ()")
		.def("getNumQuestSounds", &CvQuestInfo::getNumQuestSounds, "int ()")

		.def("getQuestObjective", &CvQuestInfo::getQuestObjective, "string ()")
		.def("getQuestBodyText", &CvQuestInfo::getQuestBodyText, "string ()")
		.def("getNumQuestMessages", &CvQuestInfo::getNumQuestMessages, "string ()")
		.def("getQuestLinkType", &CvQuestInfo::getQuestLinkType, "string ()")
		.def("getQuestLinkName", &CvQuestInfo::getQuestLinkName, "string ()")
		.def("getQuestSounds", &CvQuestInfo::getQuestSounds, "string ()")

		.def("setNumQuestMessages", &CvQuestInfo::setNumQuestMessages, "void (int)")

		.def("setQuestObjective", &CvQuestInfo::setQuestObjective, "void (string)")
		.def("setQuestBodyText", &CvQuestInfo::setQuestBodyText, "void (string)")
		.def("setQuestMessages", &CvQuestInfo::setQuestMessages, "void (int iIndex, string)")
		;

	python::class_<CvTutorialMessage>("CvTutorialMessage")
		.def("getText", &CvTutorialMessage::getText, "string ()")
		.def("getImage", &CvTutorialMessage::getImage, "string ()")
		.def("getSound", &CvTutorialMessage::getSound, "string ()")

		.def("getNumTutorialScripts", &CvTutorialMessage::getNumTutorialScripts, "int ()")
		.def("getTutorialScriptByIndex", &CvTutorialMessage::getTutorialScriptByIndex, "int (int i)")
		;

	python::class_<CvTutorialInfo, python::bases<CvInfoBase> >("CvTutorialInfo")
		.def("getNextTutorialInfoType", &CvTutorialInfo::getNextTutorialInfoType, "string ()")

		.def("getNumTutorialMessages", &CvTutorialInfo::getNumTutorialMessages, "int ()")
		.def("getTutorialMessage", &CvTutorialInfo::getTutorialMessage,  python::return_value_policy<python::reference_existing_object>(), "CvTutorialMessage* (int iIndex)")
		;

	python::class_<CvAutomateInfo, python::bases<CvInfoBase> >("CvAutomateInfo")
		;

	python::class_<CvCommandInfo, python::bases<CvInfoBase> >("CvCommandInfo")
		;

	python::class_<CvGameOptionInfo, python::bases<CvInfoBase> >("CvGameOptionInfo")
		.def("getDefault", &CvGameOptionInfo::getDefault, "bool ()")
		.def("getVisible", &CvGameOptionInfo::getVisible, "bool ()")
		;

	python::class_<CvMPOptionInfo, python::bases<CvInfoBase> >("CvMPOptionInfo")
		.def("getDefault", &CvMPOptionInfo::getDefault, "bool ()")
		;

	python::class_<CvForceControlInfo, python::bases<CvInfoBase> >("CvForceControlInfo")
		.def("getDefault", &CvForceControlInfo::getDefault, "bool ()")
		;

	python::class_<CvPlayerOptionInfo, python::bases<CvInfoBase> >("CvPlayerOptionInfo")
		.def("getDefault", &CvPlayerOptionInfo::getDefault, "bool ()")
		;

	python::class_<CvGraphicOptionInfo, python::bases<CvInfoBase> >("CvGraphicOptionInfo")
		.def("getDefault", &CvGraphicOptionInfo::getDefault, "bool ()")
		;

//FfH Spell System: Added by Kael 07/23/2007
	python::class_<CvSpellInfo, python::bases<CvInfoBase> >("CvSpellInfo")
/*************************************************************************************************/
/**	City Actions	(SpellInfos)			03/28/10								Grey Fox	**/
/*************************************************************************************************/
		.def("isCityAction", &CvSpellInfo::isCityAction, "string ()")
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		.def("getPromotionPrereq1", &CvSpellInfo::getPromotionPrereq1, "string ()")
		.def("getPromotionPrereq2", &CvSpellInfo::getPromotionPrereq2, "string ()")
		.def("getPyResult", &CvSpellInfo::getPyResult, "string ()")
		.def("getPyRequirement", &CvSpellInfo::getPyRequirement, "string ()")
		.def("getPyMiscast", &CvSpellInfo::getPyMiscast, "string ()")

/*************************************************************************************************/
/**	New Tag Defs	(SpellInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Exposes the Functions to Python									**/
/*************************************************************************************************/
		.def("getCreateUnitType", &CvSpellInfo::getCreateUnitType, "int ()")
		.def("isGlobal", &CvSpellInfo::isGlobal, "bool ()")
		.def("isAbility", &CvSpellInfo::isAbility, "bool ()")
		.def("isPrereqNotAttacked", &CvSpellInfo::isPrereqNotAttacked, "bool ()")
		.def("isSetHasAttacked", &CvSpellInfo::isSetHasAttacked, "bool ()")
		.def("isRemoveHasAttacked", &CvSpellInfo::isRemoveHasAttacked, "bool ()")
		.def("isPrereqAvailableCommander", &CvSpellInfo::isPrereqAvailableCommander, "bool ()")
		.def("isPrereqIsNOTMinion", &CvSpellInfo::isPrereqIsNOTMinion, "bool ()")
		.def("isPrereqIsMinion", &CvSpellInfo::isPrereqIsMinion, "bool ()")
		.def("getPrereqBroadAlignment", &CvSpellInfo::getPrereqBroadAlignment, "int ()")
		.def("getAlignmentModifier", &CvSpellInfo::getAlignmentModifier, "int ()")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		.def("getPrereqBroadEthicalAlignment", &CvSpellInfo::getPrereqBroadEthicalAlignment, "int ()")
		.def("getEthicalAlignmentModifier", &CvSpellInfo::getEthicalAlignmentModifier, "int ()")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
		.def("isSummonMaster", &CvSpellInfo::isSummonMaster, "bool ()")
		.def("getPromotionDuration", &CvSpellInfo::getPromotionDuration, "int ()")
		.def("getQuote", &CvSpellInfo::getQuote, "string ()")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//InterfaceUpgrade: Better Pedia - Added by Grey Fox 04/18/2008
		.def("isGlobal", &CvSpellInfo::isGlobal, "bool ()")
		.def("getCivilizationPrereq", &CvSpellInfo::getCivilizationPrereq, "int ()")
//Interface Upgrade: Better Pedia - End Add
/*************************************************************************************************/
/**	Tech Spell Help								07/16/10							Grey Fox	**/
/*************************************************************************************************/
		.def("getTechPrereq", &CvSpellInfo::getTechPrereq, "int ()")
/*************************************************************************************************/
/**	Tech Spell Help								 END											**/
/*************************************************************************************************/

		;


	python::class_<CvLeaderClassInfo, python::bases<CvInfoBase> >("CvLeaderClassInfo")

		.def("getLeaderStatus", &CvLeaderClassInfo::getLeaderStatus, "int ()")
		.def("getMaxTraitsPerClass", CvLeaderClassInfo::getMaxTraitsPerClass, "int (int i)")
	;
	python::class_<CvFlagInfo, python::bases<CvInfoBase> >("CvFlagInfo")

	;
//FfH: End Add
}

