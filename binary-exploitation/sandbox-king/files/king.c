

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

int main()
{
	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Enter your shellcode, king: ");
	void* buf = mmap(0, 50, PROT_EXEC|PROT_READ|PROT_WRITE, MAP_ANON|MAP_PRIVATE, -1, 0);
	if(fgets(buf, 50, stdin) == NULL)
		exit(0);
	void (*code)() = (void(*)())buf;
	code();
	exit(0);
}