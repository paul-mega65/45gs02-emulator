# *******************************************************************************************
# *******************************************************************************************
#
#		Name : 		process.py
#		Purpose :	Generate 4502 emulation code.
#		Date :		25th October 2024
#		Author : 	Paul Robson (paul@robsons.org.uk)
#
# *******************************************************************************************
# *******************************************************************************************

import re

#
#		Create an array of modes. Each entry has code to calculate the effective
#		address, the number of additional cycles, and how it is physically displayed.
#
modes = {}
#
#		Absolute modes
#
modes["a"] = { "eac":"FetchWord();eac = temp16;", "cycles":0, "desc":"@2" }
modes["ax"] = { "eac":"FetchWord();eac = (temp16+x) & 0xFFFF;", "cycles":0, "desc":"@2,X" }
modes["ay"] = { "eac":"FetchWord();eac = (temp16+y) & 0xFFFF;", "cycles":0, "desc":"@2,Y" }
#
#		Zero Page modes
#
modes["bp"] = { "eac":"eac = Fetch();", "cycles":-1, "desc":"@1" }
modes["bx"] = { "eac":"eac = (Fetch()+basePage);", "cycles":0, "desc":"@1,X" }
modes["by"] = { "eac":"eac = (Fetch()+basePage);", "cycles":0, "desc":"@1,Y" }
#
#		Immediate modes.
#
modes["i"] = { "eac":"", "cycles":-2, "desc":"#@1" }
modes["iw"] = { "eac":"eac = pc;pc += 2", "cycles":-2, "desc":"#@2" }
#
#		Indirect mode.
#
modes["id"] = { "eac":"FetchWord();eac = ReadWord(temp16);", "cycles":2, "desc":"(@2)" }
modes["ix"] = { "eac":"temp8 = (Fetch()+x) & 0xFF;eac = ReadWord(temp8);", "cycles":3, "desc":"(@1,X)" }
modes["iy"] = { "eac":"temp8 = Fetch();eac = (ReadWord(temp8)+y) & 0xFFFF;", "cycles":2, "desc":"(@1),Y" }
modes["iz"] = { "eac":"temp8 = Fetch();eac = (ReadWord(temp8)+z) & 0xFFFF;", "cycles":2, "desc":"(@1),Z" }
modes["sp"] = { "eac":"temp8 = Fetch();eac = (ReadWord(temp8+stackBaseAddress+s)+y) & 0xFFFF;", "cycles":2, "desc":"(@1,SP),Y" }
modes["iax"] = { "eac":"FetchWord();temp16 = (temp16+x) & 0xFFFF;eac = ReadWord(temp16)","cycles":2,"desc":"(@2,x)"}
#
#		BBranch modes.
#
modes["br"] = { "eac":"eac = Fetch();if (eac & 0x80) eac |= 0xFF00;eac = (pc+eac) & 0xFFFF;", "cycles":-1, "desc":"@1,@R" }
modes["zr"] = { "eac":"eac = Fetch();if (eac & 0x80) eac |= 0xFF00;eac = (pc+eac) & 0xFFFF;", "cycles":-1, "desc":"@R" }
modes["ar"] = { "eac":"FetchWord();eac = (temp16 + pc - 1) & 0xFFFF;", "cycles":-1, "desc":"@S" }
#
#		Contains the mnemonics and the code for each instruction.
#
mnemonics = [ None ] * 256
codeList =  [ None ] * 256

#
#		Define an opcode.
#
def defineOpcode(opcode,mnemonic,code,cycles):
	assert mnemonics[opcode] is None
	mnemonics[opcode] = mnemonic.lower() 
	codeList[opcode] = "Cycles({0});{1}".format(cycles,code)
	#print("{1:02x} {0} {2}".format(mnemonics[opcode],opcode,codeList[opcode]))

#
#		Open the 4502 definition file, read and pre-process it.
#
src = open("4502.def").readlines()
src = [x if x.find("//") < 0 else x[:x.find("//")] for x in src]
src = [x.strip().replace("\t"," ").replace("\n"," ") for x in src if x.strip() != ""]

#
#		Output all lines beginning with ':' to the support file.
#
open("__4502support.h","w").write("\n".join([x[1:] for x in src if x[0] == ':']))

#
#		Remove all those lines. Put | before lines beginning with "
#
src = [x for x in src if x[0] != ':']
src = ["~"+x if x.startswith('"') else x for x in src]
#
#		Join together and split on tilde.
#
src = [x.strip() for x in " ".join(src).split("~") if x.strip() != ""]
#
#		For each line.
#
for l in src:
	print(l)
	#
	#		Decompose into Mnemonic cycles opcodes c-code
	#
	m = re.match("^\"([\w\s\#\%@]+)\"\s+(\d+)\s+([\(\)\w\:\,]+)\s+(.+)",l)
	assert m is not None,"Line "+l
	#
	#		Simple opcode, so 2 digits long.
	#
	if len(m.group(3)) == 2:
		defineOpcode(int(m.group(3),16),m.group(1),m.group(4),int(m.group(2)))
	#
	#		Multiple opcodes for instruction.
	#
	else:
		opcodes = re.match("^\((.*)\)$",m.group(3))
		#
		#		For each opcode, 
		#
		for mode in opcodes.group(1).split(","):
			m2 = re.match("^(\w+)\:([0-9A-F]+)$",mode)							# the opcode.
			assert(m2 is not None)
			mode = m2.group(1).lower()											# addressing mode.
			body = m.group(4)													# code.
			assert mode in modes

			if mode[0] == 'z':													# if zero page use fast access
				body = body.replace("Read(","Read(").replace("Write(","Write(")
			if mode == 'i':														# immediate mode.
				body = body.replace("Read(eac)","Fetch()")

			mnemonic = m.group(1).replace("@O",modes[mode]["desc"])				# construct the assembler mnemonic
			body = body.replace("@EAC",modes[mode]["eac"],int(m.group(2))) 		# insert EAC code.
			if mnemonic.find("%") >= 0:
				for i in range(0,8):
					defineOpcode(int(m2.group(2),16)+i*16,mnemonic.replace("%",str(i)),body.replace("%",str(i)),int(m.group(2))+modes[mode]["cycles"])
			else:
				defineOpcode(int(m2.group(2),16),mnemonic,body,int(m.group(2))+modes[mode]["cycles"])

#
#		Fill in undefined with byte
#
for i in range(0,256):
	if mnemonics[i] is None:
		mnemonics[i] = "byte {0:02x}".format(i)

#
#		Write out the mnemonic table.
#
m = ['"'+m.lower()+'"' for m in mnemonics]
open("__4502mnemonics.h","w").write("static const char *_mnemonics[] = { "+",".join(m) + "};")

#
#		Write out instruction code.
#
handle = open("__4502opcodes.h","w")
unused = []
for i in range(0,256):
	if codeList[i] is not None:
		handle.write("case 0x{0:02x}: /* ${0:02x} {1} */\n".format(i,mnemonics[i]))
		handle.write("\t{0};break;\n".format(codeList[i]).replace(";;",";"))
	else:
		if i < 256:
			unused.append(i)

print("Successfully generated 45GS02 opcodes.")
print(" ".join(["{0:02x}".format(n) for n in unused]))