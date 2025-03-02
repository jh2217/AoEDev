//
// Python wrapper class for CvSnarkoProfiler
//
#include "CvGameCoreDLL.h"

#include "CySnarkoProfiler.h"
#include "CvSnarkoProfiler.h"



CySnarkoProfiler::CySnarkoProfiler() : m_pSnarkoProfiler(NULL)
{
	m_pSnarkoProfiler = &GC.getProfiler();
}

CySnarkoProfiler::CySnarkoProfiler(CvSnarkoProfiler* pSnarkoProfiler) : m_pSnarkoProfiler(pSnarkoProfiler)
{
}

bool CySnarkoProfiler::profile(char* szFunc, bool bStopLogging)
{
	if (m_pSnarkoProfiler)
	{
		m_pSnarkoProfiler->profile(szFunc, bStopLogging);
		return true;
	}
	else
	{
		return false;
	}
}