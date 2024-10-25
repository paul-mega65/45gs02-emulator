
include ../build_env/common.make

all: assemble 

.any:

	
assemble: .any
	$(ACME) --cpu m65 -l test.sym -r test.rep test.asm

run: assemble
	$(XEMU) -prg test.prg

reset: .any
	$(M65) -F

hrun: assemble
	$(M65) -r test.prg