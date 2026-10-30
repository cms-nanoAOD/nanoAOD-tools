PYTHON=python
PYEXT=$(shell $(PYTHON)-config --extension-suffix 2>/dev/null || echo ".so")
PYINC=$(shell $(PYTHON)-config --includes)
DARWIN := $(shell uname|grep Darwin)
ifdef DARWIN
	LIBLDFLAG=-install_name @rpath/libcorrectionlib.so
	PYLDFLAG=-undefined dynamic_lookup -Wl,-rpath,'@loader_path/lib'
else
	LIBLDFLAG=
	PYLDFLAG=-Wl,-rpath,'$$ORIGIN/lib'
endif
OSXFLAG=$(shell uname|grep -q Darwin && echo "-undefined dynamic_lookup")
CFLAGS=--std=c++17 -O3 -Wall -fPIC -Irapidjson/include -Ipybind11/include -Icpp-peglib $(PYINC) -Iinclude
PREFIX ?= correctionlib
STRVER=$(shell git describe --tags)
MAJOR=$(shell git describe --tags|sed -n "s/v\([0-9]\+\)\..*/\1/p")
MINOR=$(shell git describe --tags|sed -n "s/v[0-9]\+\.\([0-9]\+\)\..*/\1/p")

.PHONY: build all clean install pythonbinding

all: pythonbinding

include/correctionlib_version.h: include/version.h.in
	sed "s/@CORRECTIONLIB_VERSION@/$(STRVER)/;s/@correctionlib_VERSION_MAJOR@/$(MAJOR)/;s/@correctionlib_VERSION_MINOR@/$(MINOR)/" $< > $@

build/%.o: src/%.cc include/correctionlib_version.h
	mkdir -p build
	$(CXX) $(CFLAGS) -c $< -o $@

lib/libcorrectionlib.so: build/correction.o build/formula_ast.o
	mkdir -p lib
	$(CXX) -pthread -lz -fPIC -shared $(LIBLDFLAG) $^ -o $@

pythonbinding: build/python.o lib/libcorrectionlib.so
	$(CXX) -fPIC -shared $(PYLDFLAG) $< -Llib -lcorrectionlib -o _core$(PYEXT)
	touch __init__.py

install: pythonbinding
	mkdir -p $(PREFIX)/include
	mkdir -p $(PREFIX)/lib
	install -m 644 include/correction.h $(PREFIX)/include
	install -m 644 include/correctionlib_version.h $(PREFIX)/include
	install -m 755 _core$(PYEXT) $(PREFIX)
	install -m 755 lib/libcorrectionlib.so $(PREFIX)/lib
	install -m 644 __init__.py $(PREFIX)

clean:
	rm -rf build
	rm -f demo
	rm -f data/examples.json*
	rm -f include/correctionlib_version.h
	rm -f __init__.py _core*
