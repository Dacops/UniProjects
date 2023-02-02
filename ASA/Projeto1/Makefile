CFLAGS = -O3 -std=c++11 -g -Wall

proj: proj.cpp
	g++ $(CFLAGS) proj.cpp -lm -o proj
gerador: gerador.cpp
	g++ $(CFLAGS) ladrilho_valido.cpp -lm -o gerador

run: proj
	./proj < input.txt
rung: proj gerador
	./gerador args > testfile
	./proj < testfile
clear:
	rm -f proj gerador testfile


