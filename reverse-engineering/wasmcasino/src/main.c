#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <emscripten/emscripten.h>

static int money_val = 69;
static long int win_lose;
static const char WIN[] = "You win!";
static const char LOSE[] = "You lose!";
// Have we stored log in assert?
static int log_stored = 0;

/**
 * (c) 2019, Jacob Baines.
 * 
 * Executes the debugger keyword in javascript. If the console is up then it
 * will cause the program to pause and the user will have to click through. If
 * we detect this behavior, restore the default console.log
 * 
 */
static int debugger_check()
{
    int before = time(NULL);

    EM_ASM(
    {
        debugger;
    }, NULL);

    int after = time(NULL);
    if ((after - before) != 0)
    {
        if (log_stored == 1)
        {
            EM_ASM(
            {
                delete window['console']['log'];
                window['console']['log'] = window['console']['assert'];
            }, NULL);
        }
        return 1;
    }
    return 0;
}

static void refresh_state() {
    if (money_val == 69) {
        srandom((int) emscripten_get_now());
        money_val = (random() % 100) * 10;
    } else if (money_val <= 0){
        money_val = 0;
    }
    EM_ASM(
    {
        money($0);
    }, money_val);
}

/**
 * (c) 2019, Jacob Baines, with slight modification.
 * 
 * restart is the first function to execute. It fires before main(). It has three
 * key responsibilities:
 *
 * 1. Check for the developer console via the javascript debugger keyword.
 * 2. Inspect the function that executes debugger to see if its been modified.
 * 3. Overwrite console.log to point to f_af9a16d2279f483ab0687076b7badd6c.
 *
 * This function is also called when the attacker fails to guess the correct win-lose pattern. 
 * I imagine subversion of this function would be quite bad.
 * 
 * (export "restart" (func 153))
 * (call 1145)
 */
static void restart()
{
    win_lose = 0;

    refresh_state();

    rand();

    // check for dev console.
    if (debugger_check() == 1)
    {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, "debug check failed");
        return;
    }

    // the expected value of ASM_CONSTS[0].
    // char expected[] = "function() {debugger;}";

    // check to see if the debugger logic was modified
    // int result = EM_ASM_INT(
    // {
    //     var check_js = ASM_CONSTS[1445].toString();
    //     var expected = AsciiToString($0);
    //     return check_js == expected;
    // }, expected);

    if (0)//result != 1)
    {
        if (log_stored == 1)
        {
            EM_ASM(
            {
                delete window['console']['log'];
                window['console']['log'] = window['console']['assert'];
            }, NULL);
        }
        return;
    }

    // reset console.log
    log_stored = 1;

    EM_ASM(
    {
        window['console']['assert'] = window['console']['log'];
        window['console']['log'] = function(param)
        {
            var result = Module.ccall('f_af9a16d2279f483ab0687076b7badd6c', 'void', ['number'], [param]);
        }
    }, NULL);
}


void EMSCRIPTEN_KEEPALIVE f_af9a16d2279f483ab0687076b7badd6c(int param) {

    EM_ASM({
        Module.print($0)
    }, param);

    if(param <= 0) {
        restart();
        return;
    }

    money_val -= param;
    refresh_state();

    // define WASM_EXPORT __attribute__((visibility("default")))
    // include <stdlib.h>

    // WASM_EXPORT
    // int f_45a9216c9dba493e853c3ce88432b1f5 (int val)
    // {
    // return rand_r(&val) % 2 == 0;
    // }

    int n = EM_ASM_INT({
        var wasm = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 9, 2, 96, 0, 0, 96, 1, 127, 1, 127, 3, 4, 3, 0, 1, 1, 4, 5, 1, 112, 1, 1, 1, 5, 3, 1, 0, 2, 6, 21, 3, 127, 1, 65, 128, 136, 4, 11, 127, 0, 65, 128, 136, 4, 11, 127, 0, 65, 128, 8, 11, 7, 74, 4, 34, 102, 95, 52, 53, 97, 57, 50, 49, 54, 99, 57, 100, 98, 97, 52, 57, 51, 101, 56, 53, 51, 99, 51, 99, 101, 56, 56, 52, 51, 50, 98, 49, 102, 53, 0, 1, 6, 109, 101, 109, 111, 114, 121, 2, 0, 11, 95, 95, 104, 101, 97, 112, 95, 98, 97, 115, 101, 3, 1, 10, 95, 95, 100, 97, 116, 97, 95, 101, 110, 100, 3, 2, 10, 127, 3, 2, 0, 11, 44, 1, 1, 127, 35, 0, 65, 16, 107, 34, 1, 36, 0, 32, 1, 32, 0, 54, 2, 12, 32, 1, 65, 12, 106, 16, 2, 33, 0, 32, 1, 65, 16, 106, 36, 0, 32, 0, 65, 127, 115, 65, 1, 113, 11, 77, 1, 1, 127, 32, 0, 32, 0, 40, 2, 0, 65, 237, 156, 153, 142, 4, 108, 65, 185, 224, 0, 106, 34, 1, 54, 2, 0, 32, 1, 65, 11, 118, 32, 1, 115, 34, 0, 65, 7, 116, 65, 128, 173, 177, 233, 121, 113, 32, 0, 115, 34, 0, 65, 15, 116, 65, 128, 128, 152, 254, 126, 113, 32, 0, 115, 34, 0, 65, 18, 118, 32, 0, 115, 65, 1, 118, 11]);
        
        var module = new WebAssembly.Module(wasm);
        var module_instance = new WebAssembly.Instance(module);
        var result = module_instance.exports.f_45a9216c9dba493e853c3ce88432b1f5($0);
        return result;
    }, param);

    win_lose = (win_lose * 10) + n;

    if(n) {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, WIN);


        EM_ASM({
            window['console']['log'] = function(param)
            {
                var result = Module.ccall('f_ff1e1c7c1efc46c3a4b529818f8045ab', 'void', ['number'], [param]);
            }
        }, NULL);
    } else {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, LOSE);

        restart();
    }
}

void EMSCRIPTEN_KEEPALIVE f_ff1e1c7c1efc46c3a4b529818f8045ab (int param) {
    if(param <= 0) {
        restart();
        return;
    }

    money_val -= param;
    refresh_state();


    // define WASM_EXPORT __attribute__((visibility("default")))
    // include <stdlib.h>

    // WASM_EXPORT
    // int f_0fed8e8028554911a6fc04a81d588027 (int val)
    // {
    //   int n = rand_r(&val);
    //   int x = rand_r(&n);
    //   n = rand_r(&n);
    //   for(int i = 0; i < x % 23; i++) {
    //     n = rand_r(&n);
    //   }
    //   return n % 2 == 1;
    // }

    unsigned char meh[] = {
        0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x09, 0x02, 0x60,
        0x00, 0x00, 0x60, 0x01, 0x7f, 0x01, 0x7f, 0x03, 0x04, 0x03, 0x00, 0x01,
        0x01, 0x04, 0x05, 0x01, 0x70, 0x01, 0x01, 0x01, 0x05, 0x03, 0x01, 0x00,
        0x02, 0x06, 0x15, 0x03, 0x7f, 0x01, 0x41, 0x80, 0x88, 0x04, 0x0b, 0x7f,
        0x00, 0x41, 0x80, 0x88, 0x04, 0x0b, 0x7f, 0x00, 0x41, 0x80, 0x08, 0x0b,
        0x07, 0x4a, 0x04, 0x22, 0x66, 0x5f, 0x30, 0x66, 0x65, 0x64, 0x38, 0x65,
        0x38, 0x30, 0x32, 0x38, 0x35, 0x35, 0x34, 0x39, 0x31, 0x31, 0x61, 0x36,
        0x66, 0x63, 0x30, 0x34, 0x61, 0x38, 0x31, 0x64, 0x35, 0x38, 0x38, 0x30,
        0x32, 0x37, 0x00, 0x01, 0x06, 0x6d, 0x65, 0x6d, 0x6f, 0x72, 0x79, 0x02,
        0x00, 0x0b, 0x5f, 0x5f, 0x68, 0x65, 0x61, 0x70, 0x5f, 0x62, 0x61, 0x73,
        0x65, 0x03, 0x01, 0x0a, 0x5f, 0x5f, 0x64, 0x61, 0x74, 0x61, 0x5f, 0x65,
        0x6e, 0x64, 0x03, 0x02, 0x0a, 0xc2, 0x01, 0x03, 0x02, 0x00, 0x0b, 0x6f,
        0x01, 0x02, 0x7f, 0x23, 0x00, 0x41, 0x10, 0x6b, 0x22, 0x01, 0x24, 0x00,
        0x20, 0x01, 0x20, 0x00, 0x36, 0x02, 0x0c, 0x20, 0x01, 0x20, 0x01, 0x41,
        0x0c, 0x6a, 0x10, 0x02, 0x36, 0x02, 0x08, 0x20, 0x01, 0x41, 0x08, 0x6a,
        0x10, 0x02, 0x21, 0x00, 0x20, 0x01, 0x20, 0x01, 0x41, 0x08, 0x6a, 0x10,
        0x02, 0x22, 0x02, 0x36, 0x02, 0x08, 0x02, 0x40, 0x20, 0x00, 0x41, 0x17,
        0x6f, 0x22, 0x00, 0x41, 0x01, 0x48, 0x0d, 0x00, 0x03, 0x40, 0x20, 0x01,
        0x20, 0x01, 0x41, 0x08, 0x6a, 0x10, 0x02, 0x22, 0x02, 0x36, 0x02, 0x08,
        0x20, 0x00, 0x41, 0x7f, 0x6a, 0x22, 0x00, 0x0d, 0x00, 0x0b, 0x0b, 0x20,
        0x01, 0x41, 0x10, 0x6a, 0x24, 0x00, 0x20, 0x02, 0x41, 0x02, 0x6f, 0x41,
        0x01, 0x46, 0x0b, 0x4d, 0x01, 0x01, 0x7f, 0x20, 0x00, 0x20, 0x00, 0x28,
        0x02, 0x00, 0x41, 0xed, 0x9c, 0x99, 0x8e, 0x04, 0x6c, 0x41, 0xb9, 0xe0,
        0x00, 0x6a, 0x22, 0x01, 0x36, 0x02, 0x00, 0x20, 0x01, 0x41, 0x0b, 0x76,
        0x20, 0x01, 0x73, 0x22, 0x00, 0x41, 0x07, 0x74, 0x41, 0x80, 0xad, 0xb1,
        0xe9, 0x79, 0x71, 0x20, 0x00, 0x73, 0x22, 0x00, 0x41, 0x0f, 0x74, 0x41,
        0x80, 0x80, 0x98, 0xfe, 0x7e, 0x71, 0x20, 0x00, 0x73, 0x22, 0x00, 0x41,
        0x12, 0x76, 0x20, 0x00, 0x73, 0x41, 0x01, 0x76, 0x0b
    };


    int n = EM_ASM_INT(
    {
        var arr = new Uint8Array($2);
        for (var i = 0; i < $2; i++)
        {
            arr[i] = getValue($1 + i);
        }

        var module = new WebAssembly.Module(arr);
        var module_instance = new WebAssembly.Instance(module);
        var result = module_instance.exports.f_0fed8e8028554911a6fc04a81d588027($0);
        return result;
    }, param, meh, 333);

    win_lose = (win_lose * 10) + n;

    if (n == 0) {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, LOSE);
        EM_ASM({
            window['console']['log'] = function(param)
            {
                var result = Module.ccall('f_21651e0c254e4a879d13b0b92ea561e4', 'void', ['number'], [param]);
            }
        }, NULL);
    } else {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, WIN);
        restart();
    }
}

void EMSCRIPTEN_KEEPALIVE f_21651e0c254e4a879d13b0b92ea561e4 (int param) {
    if(param <= 0) {
        restart();
        return;
    }

    money_val -= param;
    refresh_state();

    // define WASM_EXPORT __attribute__((visibility("default")))
    // include <stdlib.h>

    // WASM_EXPORT
    // int f_8e1409b6e03b4923af45422bdeaf1ed8 (int val)
    // {
    //   int n = rand_r(&val);
    //   int x = rand_r(&n);
    //   n = rand_r(&n);
    //   for(int i = 0; i < x % 20; i++) {
    //     n = rand_r(&n);
    //   }
    //   return n % 2 == 0;
    // }

    unsigned char moo[] = {
        0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x09, 0x02, 0x60,
        0x00, 0x00, 0x60, 0x01, 0x7f, 0x01, 0x7f, 0x03, 0x04, 0x03, 0x00, 0x01,
        0x01, 0x04, 0x05, 0x01, 0x70, 0x01, 0x01, 0x01, 0x05, 0x03, 0x01, 0x00,
        0x02, 0x06, 0x15, 0x03, 0x7f, 0x01, 0x41, 0x80, 0x88, 0x04, 0x0b, 0x7f,
        0x00, 0x41, 0x80, 0x88, 0x04, 0x0b, 0x7f, 0x00, 0x41, 0x80, 0x08, 0x0b,
        0x07, 0x4a, 0x04, 0x22, 0x66, 0x5f, 0x38, 0x65, 0x31, 0x34, 0x30, 0x39,
        0x62, 0x36, 0x65, 0x30, 0x33, 0x62, 0x34, 0x39, 0x32, 0x33, 0x61, 0x66,
        0x34, 0x35, 0x34, 0x32, 0x32, 0x62, 0x64, 0x65, 0x61, 0x66, 0x31, 0x65,
        0x64, 0x38, 0x00, 0x01, 0x06, 0x6d, 0x65, 0x6d, 0x6f, 0x72, 0x79, 0x02,
        0x00, 0x0b, 0x5f, 0x5f, 0x68, 0x65, 0x61, 0x70, 0x5f, 0x62, 0x61, 0x73,
        0x65, 0x03, 0x01, 0x0a, 0x5f, 0x5f, 0x64, 0x61, 0x74, 0x61, 0x5f, 0x65,
        0x6e, 0x64, 0x03, 0x02, 0x0a, 0xc2, 0x01, 0x03, 0x02, 0x00, 0x0b, 0x6f,
        0x01, 0x02, 0x7f, 0x23, 0x00, 0x41, 0x10, 0x6b, 0x22, 0x01, 0x24, 0x00,
        0x20, 0x01, 0x20, 0x00, 0x36, 0x02, 0x0c, 0x20, 0x01, 0x20, 0x01, 0x41,
        0x0c, 0x6a, 0x10, 0x02, 0x36, 0x02, 0x08, 0x20, 0x01, 0x41, 0x08, 0x6a,
        0x10, 0x02, 0x21, 0x00, 0x20, 0x01, 0x20, 0x01, 0x41, 0x08, 0x6a, 0x10,
        0x02, 0x22, 0x02, 0x36, 0x02, 0x08, 0x02, 0x40, 0x20, 0x00, 0x41, 0x14,
        0x6f, 0x22, 0x00, 0x41, 0x01, 0x48, 0x0d, 0x00, 0x03, 0x40, 0x20, 0x01,
        0x20, 0x01, 0x41, 0x08, 0x6a, 0x10, 0x02, 0x22, 0x02, 0x36, 0x02, 0x08,
        0x20, 0x00, 0x41, 0x7f, 0x6a, 0x22, 0x00, 0x0d, 0x00, 0x0b, 0x0b, 0x20,
        0x01, 0x41, 0x10, 0x6a, 0x24, 0x00, 0x20, 0x02, 0x41, 0x7f, 0x73, 0x41,
        0x01, 0x71, 0x0b, 0x4d, 0x01, 0x01, 0x7f, 0x20, 0x00, 0x20, 0x00, 0x28,
        0x02, 0x00, 0x41, 0xed, 0x9c, 0x99, 0x8e, 0x04, 0x6c, 0x41, 0xb9, 0xe0,
        0x00, 0x6a, 0x22, 0x01, 0x36, 0x02, 0x00, 0x20, 0x01, 0x41, 0x0b, 0x76,
        0x20, 0x01, 0x73, 0x22, 0x00, 0x41, 0x07, 0x74, 0x41, 0x80, 0xad, 0xb1,
        0xe9, 0x79, 0x71, 0x20, 0x00, 0x73, 0x22, 0x00, 0x41, 0x0f, 0x74, 0x41,
        0x80, 0x80, 0x98, 0xfe, 0x7e, 0x71, 0x20, 0x00, 0x73, 0x22, 0x00, 0x41,
        0x12, 0x76, 0x20, 0x00, 0x73, 0x41, 0x01, 0x76, 0x0b
    };



    bool n = EM_ASM_INT(
    {
        var arr = new Uint8Array($2);
        for (var i = 0; i < $2; i++)
        {
            arr[i] = getValue($1 + i);
        }

        var module = new WebAssembly.Module(arr);
        var module_instance = new WebAssembly.Instance(module);
        var result = module_instance.exports.f_8e1409b6e03b4923af45422bdeaf1ed8($0);
        return result;
    }, param, moo, 333);

    win_lose = (win_lose * 10) + n;

    if(!n) {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, LOSE);
        EM_ASM({
            window['console']['log'] = function(param)
            {
                var result = Module.ccall('f_b284669ad59c4be4a92e162e9f5eee6a', 'void', ['number'], [param]);
            }
        }, NULL);
    } else {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, WIN);
        restart();
    }   
}

void EMSCRIPTEN_KEEPALIVE f_b284669ad59c4be4a92e162e9f5eee6a (int param) {
    if(param <= 0) {
        restart();
        return;
    }

    money_val -= param;
    refresh_state();

    // define WASM_EXPORT __attribute__((visibility("default")))
    // include <stdlib.h>

    // WASM_EXPORT
    // int f_78cd7618730c4df39c6b525af3bb93c2 (int val)
    // {
    //   int n = rand_r(&val);
    //   int x = rand_r(&n);
    //   for(int i = 0; i < x % 22; i++) {
    //     n = rand_r(&n);
    //   }
    //   return n % 2 == 0;
    // }

    int n = EM_ASM_INT(
    {
        var wasm = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 9, 2, 96, 0, 0, 96, 1, 127, 1, 127, 3, 4, 3, 0, 1, 1, 4, 5, 1, 112, 1, 1, 1, 5, 3, 1, 0, 2, 6, 21, 3, 127, 1, 65, 128, 136, 4, 11, 127, 0, 65, 128, 136, 4, 11, 127, 0, 65, 128, 8, 11, 7, 74, 4, 34, 102, 95, 55, 56, 99, 100, 55, 54, 49, 56, 55, 51, 48, 99, 52, 100, 102, 51, 57, 99, 54, 98, 53, 50, 53, 97, 102, 51, 98, 98, 57, 51, 99, 50, 0, 1, 6, 109, 101, 109, 111, 114, 121, 2, 0, 11, 95, 95, 104, 101, 97, 112, 95, 98, 97, 115, 101, 3, 1, 10, 95, 95, 100, 97, 116, 97, 95, 101, 110, 100, 3, 2, 10, 188, 1, 3, 2, 0, 11, 105, 1, 2, 127, 35, 0, 65, 16, 107, 34, 1, 36, 0, 32, 1, 32, 0, 54, 2, 12, 32, 1, 32, 1, 65, 12, 106, 16, 2, 54, 2, 8, 2, 64, 2, 64, 32, 1, 65, 8, 106, 16, 2, 65, 22, 111, 34, 0, 65, 1, 72, 13, 0, 3, 64, 32, 1, 32, 1, 65, 8, 106, 16, 2, 34, 2, 54, 2, 8, 32, 0, 65, 127, 106, 34, 0, 13, 0, 12, 2, 11, 11, 32, 1, 40, 2, 8, 33, 2, 11, 32, 1, 65, 16, 106, 36, 0, 32, 2, 65, 127, 115, 65, 1, 113, 11, 77, 1, 1, 127, 32, 0, 32, 0, 40, 2, 0, 65, 237, 156, 153, 142, 4, 108, 65, 185, 224, 0, 106, 34, 1, 54, 2, 0, 32, 1, 65, 11, 118, 32, 1, 115, 34, 0, 65, 7, 116, 65, 128, 173, 177, 233, 121, 113, 32, 0, 115, 34, 0, 65, 15, 116, 65, 128, 128, 152, 254, 126, 113, 32, 0, 115, 34, 0, 65, 18, 118, 32, 0, 115, 65, 1, 118, 11]);
        
        var module = new WebAssembly.Module(wasm);
        var module_instance = new WebAssembly.Instance(module);
        var result = module_instance.exports.f_78cd7618730c4df39c6b525af3bb93c2($0);
        return result;
    }, param);

    win_lose = (win_lose * 10) + n;

    if(n) {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, WIN);
        EM_ASM({
            window['console']['log'] = function(param)
            {
                var result = Module.ccall('f_2d1c11d799f84e7ab30acd417c057968', 'void', ['number'], [param]);
            }
        }, NULL);
    } else {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, LOSE);
        restart();
    }
}

int lol (int param) {

    int nyeh[] = {
        0x72, 0x7f, 0x7d, 0x61, 0x76, 0x74, 0x63, 0x64, 0x00, 0x02, 0x4a, 0x47, 
        0x04, 0x04, 0x5d, 0x6e, 0x54, 0x03, 0x53, 0x52, 0x44, 0x06, 0x01, 0x5f, 
        0x06, 0x6e, 0x00, 0x42, 0x6e, 0x05, 0x01, 0x5d, 0x03, 0x06, 0x58, 0x00, 
        0x5e, 0x06, 0x6e, 0x01, 0x55, 0x5b, 0x6f, 0x5f, 0x03, 0x47, 0x03, 0x42, 
        0x6e, 0x40, 0x5d, 0x04, 0x49, 0x02, 0x54, 0x6e, 0x01, 0x07, 0x6e, 0x5c, 
        0x01, 0x5c, 0x6f, 0x07, 0x09, 0x6e, 0x54, 0x51, 0x01, 0x01, 0x06, 0x06, 
        0x04, 0x02, 0x07, 0x02, 0x4d, 0x75, 0x74, 0x75
    };

    int flag[] = {
        0x43, 0x4f, 0x4d, 0x50, 0x46, 0x45, 0x53, 0x54, 0x31, 0x32, 0x7b, 0x77,
        0x34, 0x35, 0x6d, 0x5f, 0x64, 0x33, 0x62, 0x62, 0x75, 0x36, 0x31, 0x6e, 
        0x36, 0x5f, 0x30, 0x72, 0x5f, 0x35, 0x30, 0x6d, 0x33, 0x37, 0x68, 0x31, 
        0x6e, 0x36, 0x5f, 0x31, 0x64, 0x6b, 0x5f, 0x6e, 0x33, 0x76, 0x33, 0x72, 
        0x5f, 0x70, 0x6c, 0x34, 0x79, 0x33, 0x64, 0x5f, 0x31, 0x37, 0x5f, 0x6c, 
        0x30, 0x6c, 0x5f, 0x36, 0x39, 0x5f, 0x64, 0x61, 0x30, 0x31, 0x37, 0x36, 
        0x34, 0x33, 0x37, 0x33, 0x7d
    };

    EM_ASM({
        Module.print($0)
    }, flag);

    int nyeh_size = sizeof(nyeh);

    char * nyeh2 = malloc(nyeh_size + 1);
    char pass[5];

    sprintf(pass, "%d", param);

    for (int i = 0; i < sizeof(nyeh); i++) {
        nyeh2[i] = ((char) nyeh[i]) ^ pass[i % 5];
    }

    return flag;
}

void EMSCRIPTEN_KEEPALIVE f_2d1c11d799f84e7ab30acd417c057968 (int param) {
    if(param <= 0) {
        restart();
        return;
    }

    money_val -= param;
    refresh_state();

    // define WASM_EXPORT __attribute__((visibility("default")))
    // include <stdlib.h>

    // WASM_EXPORT
    // int f_f92e4801599f4fb494315621cfbfd8b3 (int val)
    // {
    //   int n = rand_r(&val);
    //   return rand_r(&n) % 2 == 0;
    // }

    int n = EM_ASM_INT({
        var wasm = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 9, 2, 96, 0, 0, 96, 1, 127, 1, 127, 3, 4, 3, 0, 1, 1, 4, 5, 1, 112, 1, 1, 1, 5, 3, 1, 0, 2, 6, 21, 3, 127, 1, 65, 128, 136, 4, 11, 127, 0, 65, 128, 136, 4, 11, 127, 0, 65, 128, 8, 11, 7, 74, 4, 34, 102, 95, 102, 57, 50, 101, 52, 56, 48, 49, 53, 57, 57, 102, 52, 102, 98, 52, 57, 52, 51, 49, 53, 54, 50, 49, 99, 102, 98, 102, 100, 56, 98, 51, 0, 1, 6, 109, 101, 109, 111, 114, 121, 2, 0, 11, 95, 95, 104, 101, 97, 112, 95, 98, 97, 115, 101, 3, 1, 10, 95, 95, 100, 97, 116, 97, 95, 101, 110, 100, 3, 2, 10, 139, 1, 3, 2, 0, 11, 56, 1, 1, 127, 35, 0, 65, 16, 107, 34, 1, 36, 0, 32, 1, 32, 0, 54, 2, 12, 32, 1, 32, 1, 65, 12, 106, 16, 2, 54, 2, 8, 32, 1, 65, 8, 106, 16, 2, 33, 0, 32, 1, 65, 16, 106, 36, 0, 32, 0, 65, 127, 115, 65, 1, 113, 11, 77, 1, 1, 127, 32, 0, 32, 0, 40, 2, 0, 65, 237, 156, 153, 142, 4, 108, 65, 185, 224, 0, 106, 34, 1, 54, 2, 0, 32, 1, 65, 11, 118, 32, 1, 115, 34, 0, 65, 7, 116, 65, 128, 173, 177, 233, 121, 113, 32, 0, 115, 34, 0, 65, 15, 116, 65, 128, 128, 152, 254, 126, 113, 32, 0, 115, 34, 0, 65, 18, 118, 32, 0, 115, 65, 1, 118, 11]);
        
        var module = new WebAssembly.Module(wasm);
        var module_instance = new WebAssembly.Instance(module);
        var result = module_instance.exports.f_f92e4801599f4fb494315621cfbfd8b3($0);
        return result;
    }, param);

    win_lose = (win_lose * 10) + n;

    if(!n) {
        lol(win_lose);
        EM_ASM({
            Module.print(UTF8ToString($0));
        }, "JACK POT");
    } else {
        EM_ASM({
            Module.print(UTF8ToString($0))
        }, WIN);
        restart();
    }
}

int main () {
    printf("hello world!");
    return 0;
}