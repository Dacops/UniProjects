CFLAGS = -O3 -std=c++11 -g -Wall

proj: proj.cpp
	g++ $(CFLAGS) proj.cpp -lm -o proj

run: proj
	./proj < input.txt

clear:
	rm -f proj


