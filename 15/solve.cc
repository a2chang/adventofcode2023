#include <stdio.h>


#define INFILE "adventofcode.com_2023_day_15_input.txt"
#define TEXT "HASH,HASH"
#define BUFSIZE 23000


char *get_hash(char *str, int *hash)
{
	unsigned char curr = 0;
	if ((*str == 0) || (*str == '\n'))
	{
		*hash = -1;
		return NULL;
	}

	if (*str == ',')
	{
		str = str + 1;
	}

	while (*str && (*str != ',') && (*str != '\n'))
	{
		curr += *str;
		curr *= 17;
		str = str + 1;
	}
	*hash = curr;
	return str;
}


void part1(char *input)
{
	int sum = 0;
	while (input != NULL)
	{
		int hash = 0;
		input = get_hash(input, &hash);
		if (hash < 0)
		{
			break;
		}
		sum = sum + hash;
		//printf("Hash is %d\n", hash);
	}
	printf("sum is %d\n", sum);
}


void read(char *buf, int bufsize, char *file)
{
	FILE *fp = fopen(file, "r");

	//if (!fp)

	fgets(buf, bufsize, fp);
	fclose(fp);
}


int main(int argc, char **argv)
{
	//char *input = TEXT;
	char input[BUFSIZE+1];
	read(input, BUFSIZE, INFILE);
	//printf("Read %s\n", input);
	part1(input);
	return 0;
}
