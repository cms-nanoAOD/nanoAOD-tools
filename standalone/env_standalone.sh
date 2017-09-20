# Please setup python 2.7 and ROOT into your environment first
if [ -f standalone/env_standalone.sh ]; then
    if [ ! -d build ]; then
	echo "Creating build directory..."
	mkdir -p build/lib/python/PhysicsTools
	ln -s ../../../../python build/lib/python/PhysicsTools/NanoAODTools
	touch build/lib/python/__init__.py
	touch build/lib/python/PhysicsTools/__init__.py
	touch python/__init__.py
	touch python/postprocessing/__init__.py
	touch python/postprocessing/framework/__init__.py
	touch python/postprocessing/examples/_init__.py
    else
	echo "Using previously created build directory..."
    fi
    export PYTHONPATH=${PWD}/build/lib/python:${PYTHONPATH}
    echo "Standalone environment set."
else
    echo "Please cd to the NanoAODTools main directory before trying to source standalone/env_standalone.sh"
fi
