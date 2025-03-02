//
// published python interface for CySnarkoProfiler
//
#include "CvGameCoreDLL.h"
#include "CySnarkoProfiler.h"

void CySnarkoProfilerPythonInterface()
{
	OutputDebugString("Python Extension Module - CySnarkoProfilerPythonInterface\n");

	python::class_<CySnarkoProfiler>("CySnarkoProfiler")
		.def("isNone", &CySnarkoProfiler::isNone, "bool () - Returns whether the pointer points to a real SnarkoProfiler") //How could it not? Still, I'll leave it in.
		.def("profile", &CySnarkoProfiler::profile, "void (string szFunc, bool bStopLogging) - Logs how long between this call and the last");
	;
}