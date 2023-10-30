#include <stdio.h> // basic lib
#include <ctype.h>
#include <stdlib.h> // srand, rand, system()
#include <time.h> // time
#include <string.h>
#include <unistd.h>

int seed;
uint money = 0;

void setSeed(){
	seed = time(NULL);
	srand(seed);
}

int randomizer(int n){
	int numberBucket;
	for(int i=0; i<n; i++)
		numberBucket = rand() + 1;
	return numberBucket;
}

uint read_uint()	{
	char buf[5];
	fgets(buf, 5, stdin);
	return atoi(buf);
}

int betParser(char* input){

	int length = strlen(input);
	for(int i=0; i<length; i++){
		if (!(isdigit(input[i])) && input[i] != '\n') {
			printf("Hey, Invalid input :");
			printf(input);
			return 0;
		}
	}
	return 1;
}

void gameTime(){
	money = randomizer(1) % 100000;

	int limit = 15;
	int betNumber, status, random, guess, win;

	char buf[100];

	printf("We're kind, so here's your starting money, it's on the house :)\n");

	while(limit-- && money > 0){
		win = 0;
		printf("Money : %u\n\n", money);

		char play[100];
		printf("Continue playing (1 = yes/0 = no): ");
		fgets(play, 100, stdin);

		int valPlay = atoi(play);

		if (valPlay == 1) {
			printf("Place your bet : ");
			fgets(buf, 100, stdin);
			
			printf(buf);
			betNumber = atoi(buf);

			printf("\nGuess (Number 1-100): ");
			guess = read_uint();

			printf("Rolling Dice ... \n");
			sleep(1);
			random = randomizer(10) % 100;
			printf("THE NUMBER IS %d\n\n", random);
			sleep(1);

			if (random == guess){
				printf("Nice!\n");
				win = betNumber * 5;

			} else {
				printf("WRONG LOL!\n");
				win = betNumber * -5;

				if ((int) win > (int) money) {
					sleep(1);
					system("clear");

					money = 0;

					break;
				}
			}

			money += win;
			sleep(2);
			system("clear");
		}
		else	{
			break;
		}
		
	}

	printf("Enough playing, GET OUT!\n");
}

void shopTime(){

	char flag[1000];
	char c[500];

	FILE *fptr;
	if ((fptr = fopen("flag.txt", "r")) == NULL) {
		printf("Error! opening file");
		exit(1);
	}

	fscanf(fptr, "%[^\n]", flag);
	fclose(fptr);

	uint flagPrice = 0xDEADBEEF, buy;

	printf("%s%u\n", "Current money : ", money);
	printf("%s\n", "Welcome to our shop");
	printf("%s\n", "Unfortunately, the only available thing right now is a random string :/");
	printf("%s\n", "You can buy it for a dead beef (boss idea, not mine idk why)");
	printf("%s\n\n", "So, buy it or not? (0 for No / 1 for YES PLS)");

	printf("0/1 : ");
	buy = read_uint();

	if (buy == 1) {
		if (money < flagPrice) {
			printf("%s\n", "No POORZ allowed here, scram!");
		} else {
			printf("%s\n%s\n", "idk what is this but here you go : ", flag);
		}
	} else {
		printf("%s\n", "What ru doing here then, get out.");
	}

	sleep(1);
	system("clear");
}

int main(int argc, char const *argv[]){
	setvbuf(stdout, NULL, _IONBF, 0);
	setSeed();
	int choice;
	
	while(1){
		printf("%s\n", "Welcome to the most illegal gambling site, win a flag prize!");
		printf("%s\n", "What do you want to do today?");

		printf("1. Guess the Number\n2. Shop\n3. Exit\n");
		
		printf("Choice : ");
		choice = read_uint();

		sleep(1);
		system("clear");

		if (choice == 1)
			gameTime();
		else if (choice == 2)
			shopTime();
		else if (choice == 3)
			break;
		else{
			printf("Not possible, try again!\n");
			sleep(1);
			system("clear");
		}
	}

	return 0;
}