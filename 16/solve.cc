#include <stdio.h>

#include <stdlib.h>
#include <string.h>


#define INFILE "adventofcode.com_2023_day_16_input.txt"
//#define INFILE "test_input.text"
#define MAX_W	128
#define MAX_H	128

//-----------------------------------------------------------------------------
typedef int Direction;
#define north	1
#define east	2
#define south	4
#define west	8

#define ns	(north | south)
#define ew	(east | west)
#define ne	(north | east)
#define sw	(south | west)
#define nw	(north | west)
#define se	(south | east)
#define opposite(d)	( ((d<<2) & 15) | (d>>2) )

//-----------------------------------------------------------------------------
class Cell
{
public:
	char c;
	int seen;

	Cell()
	{
		c = '.';
		seen = 0;
	}

	bool enter(Direction dir, Direction *exits)
	{
		int tmp = seen;
		seen |= dir;
		switch (c)
		{
		  case '\\':
			if (dir & ne)	{ *exits = dir^ne; }
			if (dir & sw)	{ *exits = dir^sw; }
			break;
		  case '/':
			if (dir & nw)	{ *exits = dir^nw; }
			if (dir & se)	{ *exits = dir^se; }
			break;
		  case '|':
			if (dir & ew)	{ *exits = ns; }
			else			{ *exits = opposite(dir); }
			break;
		  case '-':
			if (dir & ns)	{ *exits = ew; }
			else			{ *exits = opposite(dir); }
			break;
		  default:
			{ *exits = opposite(dir); }
		}
		return tmp & dir;
	}
};


//-----------------------------------------------------------------------------
class Map
{
public:
	int w;
	int h;
private:
	Cell cells[MAX_H][MAX_W];

public:
	Map()
	{
		w = 0;
		h = 0;
	}

	void process_line(char *line);

public:
	void load(const char *filename);
	void light(int x, int y, Direction dir);
	int get_energy_and_reset();
	void print();
};


void Map::process_line(char *line)
{
	int len = strlen(line);
	if (line[len - 1] == '\n')
	{
		len--;
	}
	w = len;
	for (int i=0; i<w; i++)
	{
		cells[h][i].c = line[i];
	}
	h++;
}

void Map::load(const char *filename)
{
	const int MAX_BUF = 1024;
	char buf[MAX_BUF];
	FILE *fp = fopen(filename, "r");
	while ( fgets(buf, MAX_BUF, fp) != NULL )
	{
		process_line(buf);
	}
	fclose(fp);
}

void Map::light(int x, int y, Direction dir)
{
	if ((x < 0) || (x >= w) || (y < 0) || (y >= h))
	{
		return;
	}

	Direction exits;
	bool seen = cells[y][x].enter(dir, &exits);
	if (seen)
	{
		return;
	}

	if (exits & north)		{ light(x, y-1, south); }
	if (exits & south)		{ light(x, y+1, north); }
	if (exits & east)		{ light(x+1, y, west); }
	if (exits & west)		{ light(x-1, y, east); }
	//print();
}

int Map::get_energy_and_reset()
{
	int sum = 0;
	for (int y=0; y<h; y++)
	{
		for (int x=0; x<w; x++)
		{
			if (cells[y][x].seen)
			{
				cells[y][x].seen = 0;
				sum++;
			}
		}
	}
	return sum;
}

void Map::print()
{
	printf("---------------\n");
	for (int y=0; y<h; y++)
	{
		for (int x=0; x<w; x++)
		{
			printf("%c", (cells[y][x].seen ? '#' : '.'));
		}
		printf("\n");
	}
}


//-----------------------------------------------------------------------------
void part1(Map *map)
{
	map->light(0, 0, west);
	int energy = map->get_energy_and_reset();
	printf("Energy is %d\n", energy);
}

void part2(Map *map)
{
	int max_energy = 0;
	int energy;
	for (int x=0; x<map->w; x++)
	{
		map->light(x, 0, north);
		energy = map->get_energy_and_reset();
		if (energy > max_energy)
		{
			max_energy = energy;
		}
		map->light(x, map->h - 1, south);
		energy = map->get_energy_and_reset();
		if (energy > max_energy)
		{
			max_energy = energy;
		}
	}
	for (int y=0; y<map->w; y++)
	{
		map->light(0, y, west);
		energy = map->get_energy_and_reset();
		if (energy > max_energy)
		{
			max_energy = energy;
		}
		map->light(map->w - 1, y, east);
		energy = map->get_energy_and_reset();
		if (energy > max_energy)
		{
			max_energy = energy;
		}
	}
	printf("Max energy is %d\n", max_energy);
}


int main(int argc, char **argv)
{
	Map m;
	m.load(INFILE);
	//m.print();

	part1(&m);
	part2(&m);
	return 0;
}
