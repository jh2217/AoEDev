#pragma once

// gameAI.h

#ifndef CIV4_GAME_AI_H
#define CIV4_GAME_AI_H

#include "CvGame.h"

class CvGameAI : public CvGame
{

public:

  CvGameAI();
  virtual ~CvGameAI();

  void AI_init();
  void AI_uninit();
	void AI_reset();

	void AI_makeAssignWorkDirty();
	void AI_updateAssignWork();

	int AI_combatValue(UnitTypes eUnit);

	int AI_turnsPercent(int iTurns, int iPercent);

	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);

/*************************************************************************************************/
/**	AI anti barb force				12/04/11											Snarko	**/
/**					Helping the AI take out barbs, one unit at the time...						**/
/*************************************************************************************************/
	int getAIBarbWeight();
/*************************************************************************************************/
/**	AI anti barb force						END													**/
/*************************************************************************************************/

protected:

  int m_iPad;
/*************************************************************************************************/
/**	AI anti barb force				12/04/11											Snarko	**/
/**					Helping the AI take out barbs, one unit at the time...						**/
/*************************************************************************************************/
  int iAIBarbWeight;

private:
	void AI_calcBarbWeight();
/*************************************************************************************************/
/**	AI anti barb force						END													**/
/*************************************************************************************************/

};

#endif
