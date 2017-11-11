vpath %.cpp src
CC=g++
CFLAGS=-c -Wall -g
LDFLAGS= -Wall -g
SOURCES=main.cpp
INCLUDE=-Iinclude
LIBS=-lm
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=HiMCM.exe

all: $(SOURCES) $(EXECUTABLE)
    
$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(INCLUDE) $(LIBS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $(INCLUDE) $(LIBS) $< -o $@

.PHONY : clean

clean:
	rm -f *.o *~ $(EXECUTABLE)
