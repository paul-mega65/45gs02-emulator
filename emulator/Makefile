# *******************************************************************************************
# *******************************************************************************************
#
#		Name : 		Makefile
#		Purpose :	Build Emulator
#		Date :		25th October 2024
#		Author : 	Paul Robson (paul@robsons.org.uk)
#
# *******************************************************************************************
# *******************************************************************************************

include ../build_env/common.make

APPNAME = m4502

SOURCES = 	src/core/sys_processor.o  src/framework/main.o src/framework/gfx.o src/framework/debugger.o \
			src/core/sys_debugger.o src/core/hardware.o \
  			
CC = g++

.PHONY: all clean emulator prebuild release run

all: emulator

run: emulator
	../bin/$(APPNAME)
	
emulator: prebuild $(APPNAME)
	cp $(APPNAME) ../bin
	
%.o:%.cpp
	$(CC) `sdl2-config --cflags` $(CXXFLAGS) -D INCLUDE_DEBUGGING_SUPPORT -I cpu -I framework -I include -I .  -c -o $@ $<

clean:
	rm -f $(APPNAME) 
	rm -f src/*.o 
	rm -f src/core/*.o 
	rm -f src/framework/*.o

$(APPNAME): $(SOURCES)
	$(CC) $(SOURCES) $(LDFLAGS) `sdl2-config --libs` -o $@

prebuild:
	make -C processor
	make -C font

