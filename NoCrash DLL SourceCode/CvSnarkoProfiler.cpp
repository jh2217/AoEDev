#include "CvGameCoreDLL.h"

#include "time.h"
#include "CvSnarkoProfiler.h"
#include "CvGlobals.h"	// for gDLL

CvSnarkoProfiler::CvSnarkoProfiler()
{
	szLastFunc = NULL;
}

CvSnarkoProfiler::~CvSnarkoProfiler()
{
}

void CvSnarkoProfiler::profile(char* szFunc, bool bStopLogging)
{
	int iNewTime = clock();
	if (szLastFunc != NULL)
	{
		int iTimeDiff = iNewTime - iLastTime;
		if (iTimeDiff > 1)
		{
			CvString szTimer;
			szTimer.Format("last func: %s new func: %s Time elapsed: %i", szLastFunc, szFunc, iTimeDiff);
			gDLL->logMsg("Profilenew.log", szTimer);
		}
	}
	if (bStopLogging)
	{
		szLastFunc = NULL;
	}
	else
	{
		szLastFunc = szFunc;
		iLastTime = clock();
	}
}