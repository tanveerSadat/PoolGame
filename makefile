export LD_LIBRARY_PATH=`pwd`

# PYTHON_INCLUDE_PATH = /usr/include/python3.11
# PYTHON_LIB_PATH = /usr/lib/python3.11x

# My computer
PYTHON_INCLUDE_PATH = /opt/homebrew/Frameworks/Python.framework/Versions/Current/include/python3.11
PYTHON_LIB_PATH = /opt/homebrew/Frameworks/Python.framework/Versions/Current/lib

all: libphylib.so _phylib.so

libphylib.so: phylib.o
	clang -std=c99 -Wall -pedantic -lm phylib.o -shared -o libphylib.so

phylib.o: phylib.c phylib.h
	clang -std=c99 -Wall -pedantic -g -c phylib.c

phylib_wrap.c: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	clang -Wall -pedantic -std=c99 -c phylib_wrap.c -I$(PYTHON_INCLUDE_PATH) -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	clang -Wall -pedantic -std=c99 -shared phylib_wrap.o -L. -L$(PYTHON_LIB_PATH) -lpython3.11 -lphylib -o _phylib.so

clean:
	rm -f *.o *.so *.svg A1 phylib_wrap.c phylib.py
