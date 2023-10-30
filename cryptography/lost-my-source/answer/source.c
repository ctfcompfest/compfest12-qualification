#include<stdio.h>
int main(){
	freopen("flag_plus_key.txt","r",stdin);
	char flag_plus_key[64];
	scanf("%s",&flag_plus_key);
	char encrypted[32];
	int i;

	for(i=31;i>=0;i--){
		encrypted[31-i]=(char)(i^flag_plus_key[i]^flag_plus_key[63-i]);
	}

	freopen("encrypted.txt","w",stdout);
	for(i=0;i<32;i++){
		printf("%c",encrypted[i]);
	}
}
