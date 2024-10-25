// *******************************************************************************************************************************
// *******************************************************************************************************************************
//
//		Name:		sys_debugger.c
//		Purpose:	Debugger Code (System Dependent)
//		Created:	25th October 2024
//		Author:		Paul Robson (paul@robsons->org.uk)
//
// *******************************************************************************************************************************
// *******************************************************************************************************************************

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "gfx.h"
#include "sys_processor.h"
#include "debugger.h"
#include "hardware.h"

#include "4502/__4502mnemonics.h"

#include "__font5x7.h"

#define DBGC_ADDRESS 	(0x0F0)														// Colour scheme.
#define DBGC_DATA 		(0x0FF)														// (Background is in main.c)
#define DBGC_HIGHLIGHT 	(0xFF0)

static int renderCount = 0;

// *******************************************************************************************************************************
//											This renders the debug screen
// *******************************************************************************************************************************

static const char *labels[] = { "A","X","Y","Z","PC","SP","N","V","B","D","I","Z","C", NULL };

void DBGXRender(int *address,int showDisplay) {
	int n = 0;
	char buffer[32];
	CPUSTATUS *s = CPUGetStatus();

	GFXSetCharacterSize(36,24);
	DBGVerticalLabel(21,0,labels,DBGC_ADDRESS,-1);									// Draw the labels for the register

	#define DN(v,w) GFXNumber(GRID(24,n++),v,16,w,GRIDSIZE,DBGC_DATA,-1)			// Helper macro

	DN(s->a,2);DN(s->x,2);DN(s->y,2);DN(s->z,2);DN(s->pc,4);DN(s->sp+0x100,4);
	DN(s->sign,1);DN(s->overflow,1);DN(s->brk,1);DN(s->decimal,1);DN(s->interruptDisable,1);DN(s->zero,1);DN(s->carry,1);

	n = 0;
	int a = address[1];																// Dump Memory.
	for (int row = 15;row < 23;row++) {
		GFXNumber(GRID(0,row),a,16,4,GRIDSIZE,DBGC_ADDRESS,-1);
		for (int col = 0;col < 8;col++) {
			int c = CPUReadMemory(a);
			GFXNumber(GRID(5+col*3,row),c,16,2,GRIDSIZE,DBGC_DATA,-1);
			c = (c & 0x7F);if (c < ' ') c = '.';
			GFXCharacter(GRID(30+col,row),c,GRIDSIZE,DBGC_DATA,-1);
			a = (a + 1) & 0xFFFF;
		}		
	}

	int p = address[0];																// Dump program code. 
	int opc;

	for (int row = 0;row < 14;row++) {
		int isPC = (p == ((s->pc) & 0xFFFF));										// Tests.
		int isBrk = (p == address[3]);
		GFXNumber(GRID(0,row),p,16,4,GRIDSIZE,isPC ? DBGC_HIGHLIGHT:DBGC_ADDRESS,	// Display address / highlight / breakpoint
																	isBrk ? 0xF00 : -1);
		opc = CPUReadMemory(p);p = (p + 1) & 0xFFFF;								// Read opcode.
		strcpy(buffer,_mnemonics[opc]);												// Work out the opcode.
		char *at = strchr(buffer,'@');												// Look for '@'
		if (at != NULL) {															// Operand ?
			char hex[6],temp[32];	
			if (at[1] == '1') {
				sprintf(hex,"%02x",CPUReadMemory(p));
				p = (p+1) & 0xFFFF;
			}
			if (at[1] == '2') {
				sprintf(hex,"%02x%02x",CPUReadMemory(p+1),CPUReadMemory(p));
				p = (p+2) & 0xFFFF;
			}
			if (at[1] == 'r') {
				int addr = CPUReadMemory(p);
				p = (p+1) & 0xFFFF;
				if ((addr & 0x80) != 0) addr = addr-256;
				sprintf(hex,"%04x",addr+p);
			}
			strcpy(temp,buffer);
			strcpy(temp+(at-buffer),hex);
			strcat(temp,at+2);
			strcpy(buffer,temp);
		}
		GFXString(GRID(5,row),buffer,GRIDSIZE,isPC ? DBGC_HIGHLIGHT:DBGC_DATA,-1);	// Print the mnemonic
	}

	renderCount++;
	if (showDisplay != 0) {
		int xc = 64*6;int yc = 32*8;
		int xs = 3;int ys = 3;
		SDL_Rect r;
		r.w = xs*xc;r.h = ys*yc;
		r.x = WIN_WIDTH/2-r.w/2;r.y = WIN_HEIGHT/2-r.h/2;
		SDL_Rect rc2;rc2 = r;
		rc2.w += 8;rc2.h += 8;rc2.x -=4;rc2.y -= 4;
		GFXRectangle(&rc2,0);
		GFXRectangle(&r,0);
	}
}
