#pragma once

#ifndef CySnarkoProfiler_h
#define CySnarkoProfiler_h

//
// Python wrapper class for CvSnarkoProfiler
//

class CvSnarkoProfiler;
class CySnarkoProfiler
{
public:

	CySnarkoProfiler();
	CySnarkoProfiler(CvSnarkoProfiler* pSnarkoProfiler);					// Call from C++
	CvSnarkoProfiler* getSnarkoProfiler() { return m_pSnarkoProfiler;	}	// Call from C++
	bool isNone() { return (m_pSnarkoProfiler==NULL); }


	bool profile(char* szFunc, bool bStopLogging);

protected:

	CvSnarkoProfiler* m_pSnarkoProfiler;
};

#endif	// #ifndef CySnarkoProfiler