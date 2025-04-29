#!/bin/sh

install() {
    pip3 install -r requirements.txt
}

run() {
    python3 main.py
}

run-web() {
    rm -rf build
	mkdir -p build/web
	cp -rf assets build/web || true
	cp -rf esper build/web || true
	PYGBAG=1 pygbag main.py || echo "pygbag build completed"
}