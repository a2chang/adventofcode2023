// Need to link with stdc++ library:
//	gcc -lstdc++ solve.cc


#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define INFILE "adventofcode.com_2023_day_15_input.txt"
//#define INFILE "test_input.text"
#define TEXT "HASH,HASH"
#define BUFSIZE 23000


typedef struct _list_item
{
	char *label;
	int value;
	struct _list_item *next;
} list_item;


void ll_add(list_item *head, char *label, int value)
{
	// assert(head != NULL)
	while (head->next != NULL)
	{
		head = head->next;
		if (strcmp(head->label, label) == 0)
		{
			head->value = value;
			return;
		}
	}

	list_item *item = new(list_item);
	item->label = label;
	item->value = value;
	item->next = NULL;
	head->next = item;
}

void ll_remove(list_item *head, char *label)
{
	// assert(head != NULL)
	while (head->next != NULL)
	{
		if (strcmp(head->next->label, label) == 0)
		{
			list_item *snowman = head->next;
			head->next = head->next->next;
			delete(snowman);
			return;
		}
		head = head->next;
	}
}


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

void part2(char *input)
{
	int num_bins = 256;
	list_item bins[num_bins];
	for (int i=0; i<num_bins; i++)
	{
		bins[i].next = NULL;
	}

	// Process string
	char chars_label[] = "qwertyuiopasdfghjklzxcvbnm";
	char chars_value[] = "1234567890";
	int hash;
	while (input != NULL)
	{
		if (*input == ',')
		{
			input++;
		}

		int n = strspn(input, chars_label);
		if (n == 0)
		{
			break;
		}

		int cmd = input[n];
		input[n] = NULL;
		if (cmd == '-')
		{
			//printf("Label %s (%c)\n", input, cmd);
			get_hash(input, &hash);
			ll_remove(&(bins[hash]), input);
			input += n + 1;
		}
		else if (cmd == '=')
		{
			int value = atoi(input + n + 1);
			//printf("Label %s (%c) %d\n", input, cmd, value);
			get_hash(input, &hash);
			ll_add(&(bins[hash]), input, value);
			input += n + 1;
			n = strspn(input, chars_value);
			input += n;
		}
	}

	// Compute focusing power
	long power = 0;
	for (int i=0; i<num_bins; i++)
	{
		list_item *vixen = &(bins[i]);
		int slot = 1;
		while (vixen->next != NULL)
		{
			vixen = vixen->next;
			//printf("=> Bin %d  Slot %d = %d\n", (i + 1), slot, vixen->value);
			power += (i + 1) * slot * vixen->value;
			slot++;
		}
	}
	printf("Focusing power is %ld\n", power);
}


void read(char *buf, int bufsize, const char *file)
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
	part2(input);
	return 0;
}
