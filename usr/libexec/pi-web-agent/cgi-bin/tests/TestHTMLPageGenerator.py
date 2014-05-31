#!/usr/bin/python
import sys
import os
import PiWebAgentTestSuite
import HTMLPageGenerator
from HTMLPageGenerator import *
import unittest

class TestHTMLPageGenerator(unittest.TestCase):

	def setUp(self):
		self.radioWidgets = InputWidgetGroup()

	def test_radio_widget(self):
		fo = open("TestRadioForm.test", "r")
		expectedResult = fo.read(125)
		fo.close()
		r1=InputWidget("radio","sex", "male", "Male")
		r2=InputWidget("radio","sex","female", "Female")		
		self.radioWidgets.addInputWidget(r1)
		self.radioWidgets.addInputWidget(r2)
		result = createForm("", "", "", self.radioWidgets)
		self.assertEqual(expectedResult, result)
		


if __name__ == '__main__':
    unittest.main()
