// *******************************************************************************************************************************
// *******************************************************************************************************************************
//
//		Name:		hardware.c
//		Purpose:	Hardware Emulation
//		Created:	25th October 2024
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// *******************************************************************************************************************************
// *******************************************************************************************************************************

#include "sys_processor.h"
#include "hardware.h"
#include "gfx.h"
#include <stdio.h>

// *******************************************************************************************************************************
//												Reset Hardware
// *******************************************************************************************************************************

void HWReset(void) {
}

// *******************************************************************************************************************************
//												  Reset CPU
// *******************************************************************************************************************************

void HWSync(void) {
}

// *******************************************************************************************************************************
//										     Receive PS/2 events
// *******************************************************************************************************************************

void HWQueueKeyboardEvent(int scanCode) {
}

// *******************************************************************************************************************************
//									Track keystrokes to the keyboard port
// *******************************************************************************************************************************

int HWKeymap(int k,int r) {
	int ascii = GFXToASCII(k,-1);
	if (ascii != 0) {
		CPUAccessMemory()[0xC000] = 0x80|ascii;
		//printf("%c %d %d\n",GFXToASCII(k,1),GFXToASCII(k,1),k);
	}
	return k;
}
