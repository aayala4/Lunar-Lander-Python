# By: Alex Ayala
# 12/10/16
# Makefile
# Makefile for Lunar Lander Project

CMP = g++ -Wall -std=c++11
CLASS1 = ship
CLASS2 = terrain
MAIN = final
EXEC = $(MAIN)
FLAGX = -lX11

$(EXEC): $(MAIN).o $(CLASS1).o $(CLASS2).o
	$(CMP) $(MAIN).o $(CLASS1).o $(CLASS2).o gfxnew.o $(FLAGX) -o $(EXEC)

$(CLASS1).o: $(CLASS1).cpp $(CLASS1).h
	$(CMP) -c $(CLASS1).cpp -o $(CLASS1).o

$(CLASS2).o: $(CLASS2).cpp $(CLASS2).h
	$(CMP) -c $(CLASS2).cpp -o $(CLASS2).o

$(MAIN).o: $(MAIN).cpp $(CLASS1).h $(CLASS2).h
	$(CMP) -c $(MAIN).cpp -o $(MAIN).o

clean:
	rm $(EXEC) $(MAIN).o $(CLASS1).o $(CLASS2).o
