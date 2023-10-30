CC=emcc
OUTPUT_FOLDER=./share

build:
	mkdir $(OUTPUT_FOLDER)
	$(CC) ./src/main.c  -s WASM=1 -o $(OUTPUT_FOLDER)/index.html --shell-file ./src/page.html -s NO_EXIT_RUNTIME=1 -s LINKABLE=1 -s EXTRA_EXPORTED_RUNTIME_METHODS='["ccall","UTF8ToString"]'
	wasm2wat $(OUTPUT_FOLDER)/index.wasm -o $(OUTPUT_FOLDER)/index.wat
	truncate -s -2 $(OUTPUT_FOLDER)/index.wat
	echo "\n(start 153))" >> $(OUTPUT_FOLDER)/index.wat
	wat2wasm $(OUTPUT_FOLDER)/index.wat -o $(OUTPUT_FOLDER)/index.wasm
	rm $(OUTPUT_FOLDER)/index.wat
clean:
	rm -rf $(OUTPUT_FOLDER)

