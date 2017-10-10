(*

DYMO Label Software v8 SDK

This example demonstrates how to create an address label from scratch by adding a new Address Object and setting its attributes.

*)

on run argv
	tell application "DYMO Label"
		
		openLabel in "/Users/qasimabbas/Documents/HackRU-QRU/label-maker-backend/qrLabel.label"
		
		printLabel
		
	end tell
end run
