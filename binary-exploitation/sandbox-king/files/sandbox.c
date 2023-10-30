

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h> 
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <sys/syscall.h>

void run_program(const char* program)	{
	ptrace(PTRACE_TRACEME, 0, NULL, 0);
	if(execl(program, program, NULL) == -1)	{
		fprintf(stderr, "%s\n", "[Error] Exec error");
		exit(-1);		
	}
}

void run_sandbox(int child_pid)	{
	struct user_regs_struct regs;
	siginfo_t *sif = malloc(sizeof(siginfo_t));
	int status;
	int wait_res;
	int num_read = 0;
	waitpid(child_pid, &status, 0);
	ptrace(PTRACE_SETOPTIONS, child_pid, NULL, PTRACE_O_TRACESYSGOOD);

	// Get the starting syscalls, those are fine.
	do{
		ptrace(PTRACE_SYSCALL, child_pid, NULL, NULL);
	    wait_res = waitpid(child_pid, &status, 0);
	    ptrace(PTRACE_GETREGS, child_pid, NULL, &regs);
	    if(regs.orig_rax == 0)
	    	num_read++;
	} while(num_read != 3);

	// Other then that, be very strict!
	while(1)	{
		status = 0;
		ptrace(PTRACE_SYSCALL, child_pid, NULL, NULL);
    	wait_res = waitpid(child_pid, &status, 0);
    	if(wait_res == -1)	{
    		fprintf(stderr, "%s\n", "[Error] Waitpid Error");
    		exit(-1);
    	}

    	ptrace(PTRACE_GETSIGINFO, child_pid, NULL, sif);
    	switch(sif->si_signo)	{
    		case SIGSEGV:
    			fprintf(stderr, "%s\n", "[Error] Segmentation Fault");
    			kill(child_pid, SIGKILL);
    			exit(-1);
    			break;
    		case SIGILL:
    			fprintf(stderr, "%s\n", "[Error] Illegal Instruction");
    			kill(child_pid, SIGKILL);
    			exit(-1);
    			break;
    		default:
    			break;
    	}

    	ptrace(PTRACE_GETREGS, child_pid, NULL, &regs);
    	if(regs.orig_rax > 8)	{
    		fprintf(stderr, "%s\n", "[Error] Illegal Syscall");
    		kill(child_pid, SIGKILL);
    		exit(0);
    	}
	}

}

int main(int argc, char const *argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);

	if(argc < 2)	{
		fprintf(stderr, "%s\n", "Usage ./sandbox <executable file>");
		exit(-1);
	}

	int child_pid = fork();

	if(child_pid == -1)	{
		fprintf(stderr, "%s\n", "[Error] Fork error");
		exit(-1);
	}
	else if(child_pid == 0)	{
		run_program(argv[1]);
	}
	else	{
		run_sandbox(child_pid);
	}

	return 0;
}