# this makefile is intended for g++ on Linux

CC = g++
UNAME_S := $(shell uname -s)

CFLAGS = -c -Wall -O3 -fpermissive
ifeq ($(UNAME_S),Linux)
    LDFLAGS += -lglut -lGLU -lGL -lXext -lX11 -lm -lasound
endif
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -framework GLUT
endif

# CFLAGS = -c
LDFLAGS += -pthread
INCLUDE = -I include/

MODULES = main \
		  audioOut \
		  synthAPI

OBJECTS := $(addprefix build/,$(addsuffix .o,$(MODULES)))

EXECUTABLE = application


all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $^ -o $@ $(LDFLAGS)

build/%.o: app/%.c*
	$(CC) $(INCLUDE) $(word 1,$^) -o $@ $(CFLAGS)


clean:
	-rm $(OBJECTS)
