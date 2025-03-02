# TabElements.py
# Based on EmperorFools work on BUG
# 2009 Fredrik 'Grey Fox' Henriksson

"""
	Screen is the CyGTabCtrl object you want to add the element to
	Example code to create a new Tab Control window:
		self.pTabControl = CyGTabCtrl(title, True, True)
		tab = self.pTabControl
		tab.setModal(0)
		tab.setSize(self.width, self.height)
		tab.setControlsExpanding(False)
		tab.setColumnLength(self.iScreenHeight)
"""

def addLabel (screen, panel, name, title=None, tooltip=None):
	"""
	Adds a label to the panel
	"""
	if (title):
		screen.attachLabel(panel, name, title)
		screen.setControlFlag(name, "CF_LABEL_SMALLSIZE")
		if (tooltip):
			screen.setToolTip(name, tooltip)
		return name
	return None

def addTextEdit (screen, labelPanel, controlPanel, name, value):
	"""
	Adds a Text Edit to the panel

	"""
	if (labelPanel == controlPanel):
		box = name + "HBox"
		screen.attachHBox(labelPanel, box)
		screen.setLayoutFlag(box, "LAYOUT_SIZE_HPREFERREDEXPANDING")
		labelPanel = box
		controlPanel = box
	if (labelPanel is not None):
		label = name + "Label"
		screen.attachLabel(labelPanel, label, name)
		screen.setControlFlag(label, "CF_LABEL_DEFAULTSIZE")
		screen.setLayoutFlag(label, "LAYOUT_RIGHT")
	control = name + "Edit"
	screen.attachEdit(controlPanel, control, value, self.callbackIFace, "handleIrcTextEditChange", name)
	screen.setToolTip(control, name)
	screen.setLayoutFlag(control, "LAYOUT_SIZE_HPREFERREDEXPANDING")
	return control


def addSpacer (tab, panel, name, size=1):
	spacer = name + "_Spacer"
	tab.attachLabel(panel, spacer, " " * size)
	tab.setControlFlag(spacer, "CF_LABEL_DEFAULTSIZE")
