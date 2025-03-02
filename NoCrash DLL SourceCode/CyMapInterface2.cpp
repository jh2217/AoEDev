#include "CvGameCoreDLL.h"
#include "CyMap.h"
#include "CyArea.h"
#include "CyCity.h"
#include "CySelectionGroup.h"
#include "CyUnit.h"
#include "CyPlot.h"
//#include "CvStructs.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyMap
//

void CyMapPythonInterface2(python::class_<CyMap>& x)
{
	OutputDebugString("Python Extension Module - CyMapPythonInterface2\n");

	x
		.def("pointToPlot", &CyMap::pointToPlot, python::return_value_policy<python::manage_new_object>())
		.def("getIndexAfterLastArea", &CyMap::getIndexAfterLastArea, "int () - index for handling NULL areas")
		.def("getNumAreas", &CyMap::getNumAreas, "int () - total areas")
		.def("getNumLandAreas", &CyMap::getNumLandAreas, "int () - total land areas")
		.def("getArea", &CyMap::getArea, python::return_value_policy<python::manage_new_object>(), "CyArea (iID) - get CyArea at iID")
		.def("recalculateAreas", &CyMap::recalculateAreas, "void () - Recalculates the areaID for each plot. Should be preceded by CyMap.setPlotTypes(...)")
		.def("resetPathDistance", &CyMap::resetPathDistance, "void ()")

		.def("calculatePathDistance", &CyMap::calculatePathDistance, "finds the shortest passable path between two CyPlots and returns its length, or returns -1 if no such path exists. Note: the path must be all-land or all-water")
		.def("rebuild", &CyMap::rebuild, "used to initialize the map during WorldBuilder load")
		.def("regenerateGameElements", &CyMap::regenerateGameElements, "used to regenerate everything but the terrain and height maps")
		.def("updateFog", &CyMap::updateFog, "void ()")
		.def("updateMinimapColor", &CyMap::updateMinimapColor, "void ()")
		.def("updateMinOriginalStartDist", &CyMap::updateMinOriginalStartDist, "void (CyArea* pArea)")

/*************************************************************************************************/
/**	FastRebuild								01/14/09								Jean Elcard **/
/**																								**/
/**								Exposes the Functions to Python									**/
/*************************************************************************************************/
		.def("isNeedsRebuilding", &CyMap::isNeedsRebuilding, "bool ()")
		.def("setNeedsRebuilding", &CyMap::setNeedsRebuilding, "void (bool bNewValue)")
		.def("rebuildGraphics", &CyMap::rebuildGraphics, "void () - rebuilds graphics of all plots and updates areas")
/*************************************************************************************************/
/**	FastRebuild								END													**/
/*************************************************************************************************/
		;
}
