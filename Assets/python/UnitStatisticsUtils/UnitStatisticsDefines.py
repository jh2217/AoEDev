# UnitStatisticsDefines.py
# Unit Statistics Mod by Teg_Navanis

#######SD Tool Kit#######

import SdToolKitAdvanced
sdEntityInit   = SdToolKitAdvanced.sdEntityInit
sdEntityExists = SdToolKitAdvanced.sdEntityExists
sdEntityWipe   = SdToolKitAdvanced.sdEntityWipe
sdGetVal       = SdToolKitAdvanced.sdGetVal
sdSetVal       = SdToolKitAdvanced.sdSetVal

sdObjectInit      = SdToolKitAdvanced.sdObjectInit
sdObjectWipe      = SdToolKitAdvanced.sdObjectWipe
sdObjectExists    = SdToolKitAdvanced.sdObjectExists
sdObjectGetVal    = SdToolKitAdvanced.sdObjectGetVal
sdObjectSetVal    = SdToolKitAdvanced.sdObjectSetVal
sdObjectGetAll    = SdToolKitAdvanced.sdObjectGetAll
sdObjectSetAll    = SdToolKitAdvanced.sdObjectSetAll
sdObjectGetDictVal    = SdToolKitAdvanced.sdObjectGetDictVal
sdObjectSetDictVal    = SdToolKitAdvanced.sdObjectSetDictVal

#############################


from CvPythonExtensions import *
import CvUtil
import PyHelpers

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
localText = CyTranslator()
ArtFileMgr = CyArtFileMgr()


# To disable Unit Statistics, please change USE_UNIT_STATISTICS_CALLBACK
# In the PythonCallbackDefines.xml file to 0.

# Change this to either enable or disable unit promotion tracking.
# Default value is True
g_bTrackUnitPromotions = False

# Change this to either enable or disable tracking of your currently best units.
# Default value is True
g_bTrackHighScore = False

# Change this to either enable or disable goody received tracking.
# Default value is True
g_bTrackGoodyReceived = False

# Change this to either enable or disable turn information tracking (amount of turns fortified)
# Default value is False
g_bTrackTurnInformation = False

# Change this to show or hide the number of combats, units killed, units lost and retreats.
# Default value is True
g_bShowCombatCount = False

# Change this to show or hide the unit creation date.
# 0 = no service information
# 1 = "Turns in service: 8 (320 years)"
# 2 = "Years in service: 320 (8 turns)"
# 3 = "Turns in service: 8
# 4 = "Years in service: 320
# Default value is 1
g_iUnitServiceInformation = 1

# Change this to track the distance a unit has moved.
# Default value is False.
g_bTrackMovement = False

# Change this to show or hide the unit event log
# Default value is True
g_bShowUnitEventLog = False

# Change this to display the turn information in the unit events log
# Default value is True
g_bShowLogTurnInformation = False

# Change this to display the year information in the unit events log
# Default value is True
g_bShowLogDateInformation = False

# Change this to switch the order that the turn and year for the logged event
# are displayed. For example if set to False then a unit that was created in
# turn 0 and year 4000BC would be displayed as "Turn 0 (4000BC): <Unit type>
# created".
# Default value is True
g_bShowLogTurnInformationFirst =False

# Change this to display the damage your unit has inflicted/suffered.
# Default value is True
g_bShowDamageInformation = False

# Change this to show or hide combat odds statistics.
# Default value is True
g_bShowOdds = False

# Change this to show or hide unit experience.
# Default value is True
g_bShowExperience = False

# Change this to either enable or disable unit statistics for non-combatants (settlers, workers, missionaries, great people)
# Default value is True
g_bTrackNonCombatants = False

# Change this to either enable or disable unit statistics for all players.
# Other players' statistics will be hidden unless g_bShowAllPlayers is
# Also set to True
# Default value is False
g_bTrackAllPlayers = False

# Change this to either enable or disable the display of other players' unit statistics
# Leave disabled if you don't want any additional information about enemy units.
# Requires g_bTrackAllPlayers to be set to True.
# Default value is False
g_bShowAllPlayers = False

# If this is enabled, all players share one high score list (g_bTrackAllPlayers required for this to have effect)
# Default value is False
g_bGlobalHighScore = False

# Change this to either enable or disable help panes in the unit statistics screens
# Default value is True
g_bShowHelp = False

# Change this to either enable or disable Fall from Heaven Mode.
# Default value is False
g_bFfHMode = False

# Determines whether spells and summons (fireballs, meteors etc.) are treated as normal units
# They tend to have a major (negative) impact on player statistics, hence they are disabled by default.
# Default value is False
g_bFfHTrackSpells = False

# If you want to use other buttons than the default ones, add the corresponding string here. So far included:
# "" = standard set
#"xienwolf" = xienwolf's buttons for Fall From Heaven
# Default value is ""
g_strAlternativeButtons = "xienwolf_"

COMBATCOUNT = "CombatCount"
BODYCOUNT = "BodyCount"
BATTLECOUNT = "BattleCount"
ATTACK = "Attack"
DEFENSE = "Defense"
AIRATTACK = "AirAttack"
AIRDEFENSE = "AirDefense"
AIRSTRIKE = "AirStrike"
COLLATERAL = "Collateral"
LIST = "List"
TYPENUMBER = "TypeNumber"
STARTTURN = "StartTurn"
MOVEMENT_COUNTER = "MoveCounter"
CARGO_COUNTER = "CargoCounter"
MOVEMENT_COUNTER_ENEMY = "MoveCounterEnemy"
PLOT= "Plot"
WARP = "Warp"
TRANSPORT = "Transport"
DAMAGETYPE = ["DamageInflicted",
			  "DamageInflictedDefending",
			  "DamageInflictedAttacking",
			  "CollateralDamageInflicted",
			  "FlankingDamageInflicted",
			  "AirStrikeDamageInflicted",
			  "OtherDamageInflicted",
			  "DamageSuffered",
			  "DamageSufferedAttacking",
			  "DamageSufferedDefending",
			  "CollateralDamageSuffered",
			  "FlankingDamageSuffered",
			  "AirStrikeDamageSuffered",
			  "OtherDamageSuffered"]
DAMAGESTATS = "DamageStats"
EXPERIENCE = "Experience"
BESTODDS = "BestOdds"
ODDSDATA = "OddsData"
AVERAGEODDS = "AverageOdds"
AVERAGEODDSHIGHEST = "AverageOddsHighest"
AVERAGEODDSLOWEST = "AverageOddsLowest"
LIFEODDS = "LifeOdds"
GOODIES = "Goodies"
TURNINFORMATION = "TurnInformation"
TOTALTURNSFORTIFIED = "TotalTurnsFortified"
MAXTURNSFORTIFIED = "MaxTurnsFortified"
CAPTURECOUNT = "CaptureCount"
GRAVEYARD = "GraveYard"
GRAVEYARDLIST = "GraveYardList"
UNITTYPE = "UnitType"
UNITID = "UnitID"
UNITAGE = "UnitAge"
COMMANDO = "Commando"
PROMOTION_LIST = "Promotion_List"
HIGHEST_DEFEAT_ODDS = "HIGHEST_DEFEAT_ODDS"
SPELLCOUNT = "SpellCount"
INFLICTED = "Inflicted"
SUFFERED = "Suffered"
OTHER = "Other"
FLANKING = "Flanking"
CASTCOUNT = "CastCount"
HEROCOUNT = "HeroCount"

HighScoreTypes = {
								  BODYCOUNT: 0,
								  BATTLECOUNT: 0,
								  SPELLCOUNT: 0,
								  CASTCOUNT: 0,
								  HEROCOUNT: 0,
								DAMAGETYPE[0]: 0,
								DAMAGETYPE[1]: 0,
								DAMAGETYPE[2]: 0,
								DAMAGETYPE[3]: 0,
								DAMAGETYPE[4]: 0,
								DAMAGETYPE[5]: 0,
								DAMAGETYPE[6]: 0,
								DAMAGETYPE[7]: 0,
								DAMAGETYPE[8]: 0,
								DAMAGETYPE[9]: 0,
								DAMAGETYPE[10]: 0,
								DAMAGETYPE[11]: 0,
								DAMAGETYPE[12]: 0,
								DAMAGETYPE[13]: 0,
								MOVEMENT_COUNTER: 0,
								CARGO_COUNTER: 0,
								  WARP: 0,
								  UNITAGE: 0,
								  BESTODDS: 101,
								  AVERAGEODDSHIGHEST: -1,
								  AVERAGEODDSLOWEST: 101,
								  LIFEODDS: 101,
								  EXPERIENCE: 0,
								  TOTALTURNSFORTIFIED: 0,
								  MAXTURNSFORTIFIED: 0,
								  COMMANDO: 0
								  }

# COMBATCOUNT: [iBattles, iKills, iLosses, iWithdrawals (for normal battles) / iEnemyAttacks (for air strikes, collateral damage etc.))
UnitStatsData = {
							COMBATCOUNT: {ATTACK: [0, 0, 0, 0], DEFENSE: [0, 0, 0, 0], AIRATTACK: [0, 0, 0, 0], AIRDEFENSE: [0, 0, 0, 0], AIRSTRIKE: [0, 0, 0, 0], FLANKING: [0, 0, 0, 0],COLLATERAL: [0, 0, 0, 0], OTHER: [0, 0, 0, 0]},
							SPELLCOUNT: 0,
							CASTCOUNT: 0,
							HEROCOUNT: 0,
							TURNINFORMATION: [0, 0, 0, 0],
							STARTTURN: 0,
							UNITAGE: 0,
							CARGO_COUNTER: 0,
							MOVEMENT_COUNTER: 0,
							PLOT: [0, 0],
							WARP: 0,
							TRANSPORT: 0,
							DAMAGESTATS: {INFLICTED: [0, 0, 0, 0, 0, 0, 0], SUFFERED: [0, 0, 0, 0, 0, 0, 0]},
							BESTODDS: -1,
							EXPERIENCE: 0,
							AVERAGEODDS: -1,
							LIFEODDS: 101,
							ODDSDATA: [0, 0, "", 101],
							 CAPTURECOUNT: 0,
							 GRAVEYARD: 0,
							 UNITTYPE: 0,
							 UNITID: 0,
							 PROMOTION_LIST: [],
							LIST: "" }

PlayerStatsData = {
							COMBATCOUNT: {ATTACK: [0, 0, 0, 0], DEFENSE: [0, 0, 0, 0], AIRATTACK: [0, 0, 0], AIRDEFENSE: [0, 0, 0], AIRSTRIKE: [0, 0, 0, 0], FLANKING: [0, 0, 0, 0],COLLATERAL: [0, 0, 0, 0], OTHER: [0, 0, 0, 0]},
							SPELLCOUNT: 0,
							CASTCOUNT: 0,
							HEROCOUNT: 0,
							TURNINFORMATION: [0, 0, 0],
							CARGO_COUNTER: 0,
							MOVEMENT_COUNTER: 0,
							WARP: 0,
							TRANSPORT: 0,
							DAMAGESTATS: {INFLICTED: [0, 0, 0, 0, 0, 0, 0], SUFFERED: [0, 0, 0, 0, 0, 0, 0]},
							EXPERIENCE: 0,
							ODDSDATA: 0,
							CAPTURECOUNT: 0,
							GOODIES: 0,
							HIGHEST_DEFEAT_ODDS: 0,
							GRAVEYARDLIST: []
										   }

