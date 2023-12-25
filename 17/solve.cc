#include <stdio.h>

#include <stdlib.h>
#include <string.h>


#define INFILE "adventofcode.com_2023_day_17_input.txt"
//#define INFILE "test_input.text"
#define MAX_W	144
#define MAX_H	144
#define MAX_SPAN  3

//-----------------------------------------------------------------------------
enum Direction
{
	north,
	east,
	south,
	west,
	dir_max
};
#define opposite(d)	((d+2) & (dir_max-1))

//-----------------------------------------------------------------------------
class Cell
{
public:
	char c;
	int x;
	int y;
	bool visited[dir_max];

	Cell()
	{
		c = 0;
		for (int d=0; d<dir_max; d++)
		{
			visited[d] = false;
		}
	}
};


//-----------------------------------------------------------------------------
class QueueItem
{
public:
	int loss;
	int x;
	int y;
	Direction dir;
	int span;
	QueueItem *next;

	QueueItem(int loss, int x, int y, Direction dir, int span) :
		loss(loss),
		x(x),
		y(y),
		dir(dir),
		span(span)
	{}
};

class Queue
{
private:
	QueueItem *head;
public:
	Queue()
	{
		head = new QueueItem(-1, 0, 0, north, 0);
		head->next = NULL;
	}

	void Add(QueueItem *qi)
	{
		//printf("Add %d (%d, %d) %d : %d\n", qi->loss, qi->x, qi->y, qi->dir, qi->span);
		QueueItem *i = head;
		while (i->next && (qi->loss > i->next->loss))
		{
			i = i->next;
		}
		qi->next = i->next;
		i->next = qi;
	}

	QueueItem *Pop()
	{
		QueueItem *h = head->next;
		if (h != NULL)
		{
			head->next = h->next;
		}
		return h;
	}
};

//-----------------------------------------------------------------------------
class Map
{
public:
	int w;
	int h;
private:
	int x0;
	int y0;
	int x1;
	int y1;
	Cell cells[MAX_H][MAX_W];
	int min_loss;
	Queue q;

public:
	Map()
	{
		w = 0;
		h = 0;
		min_loss = -1;
		x0 = x1 = y0 = y1 = 0;
	}

	void ProcessLine(char *line);

public:
	void Load(const char *filename);
	void Search(QueueItem *qi);
	int Start(int x0, int y0, int x1, int y1);
	void Print();
private:
	int GetLoss(int x, int y);
};


void Map::ProcessLine(char *line)
{
	int len = strlen(line);
	if (line[len - 1] == '\n')
	{
		len--;
	}
	w = len;
	for (int i=0; i<w; i++)
	{
		cells[h][i].c = line[i] - '0';
	}
	h++;
}

void Map::Load(const char *filename)
{
	const int MAX_BUF = 1024;
	char buf[MAX_BUF];
	FILE *fp = fopen(filename, "r");
	while ( fgets(buf, MAX_BUF, fp) != NULL )
	{
		ProcessLine(buf);
	}
	fclose(fp);
}


int Map::GetLoss(int x, int y)
{
	if ((x < 0) || (x >= w) || (y < 0) || (y >= h))
	{
		return -1;
	}

	Cell *cell = &(cells[y][x]);
	return cell->c;
}


void Map::Search(QueueItem *qi)
{
	int loss = qi->loss;
	int x = qi->x;
	int y = qi->y;
	int dir = qi->dir;
	int span = qi->span;

	//printf("Search %d (%d, %d) %d : %d\n", loss, x, y, dir, span);

	if ((x < 0) || (x >= w) || (y < 0) || (y >= h) || (span >= MAX_SPAN))
	{
		return;
	}

	Cell *cell = &(cells[y][x]);
	if (span == 0)
	{
		if (cell->visited[dir])
		{
			return;
		}
		cell->visited[dir] = true;
	}

	if ((min_loss != -1) && (loss > min_loss))
	{
		return;
	}
	if ((x == x1) && (y == y1))
	{
		if ((min_loss == -1) || (loss < min_loss))
		{
			min_loss = loss;
		}
		return;
	}

	for (int d=0; d<dir_max; d++)
	{
		if (d == opposite(dir))
		{
			continue;
		}

		int s = (d == dir) ? span + 1 : 0;
		int xx = x;
		int yy = y;
		switch (d)
		{
		  case north:
			yy--;
			break;
		  case south:
			yy++;
			break;
		  case east:
			xx++;
			break;
		  case west:
			xx--;
			break;
		}
		int dloss;
		dloss = GetLoss(xx, yy);
		if (dloss != -1)
		{
			QueueItem *item = new QueueItem(loss+dloss, xx, yy,
											static_cast<Direction>(d), s);
			q.Add(item);
		}
	}
}

int Map::Start(int x0, int y0, int x1, int y1)
{
	this->x0 = x0;
	this->y0 = y0;
	this->x1 = x1;
	this->y1 = y1;

	QueueItem *qi;
	int loss;

	loss = GetLoss(x0-1, y0);
	if (loss != -1)
	{
		qi = new QueueItem(loss, x0-1, y0, west, 0);
		q.Add(qi);
	}
	loss = GetLoss(x0+1, y0);
	if (loss != -1)
	{
		qi = new QueueItem(loss, x0+1, y0, east, 0);
		q.Add(qi);
	}
	loss = GetLoss(x0, y0-1);
	if (loss != -1)
	{
		qi = new QueueItem(loss, x0, y0-1, north, 0);
		q.Add(qi);
	}
	loss = GetLoss(x0, y0+1);
	if (loss != -1)
	{
		qi = new QueueItem(loss, x0, y0+1, south, 0);
		q.Add(qi);
	}

	qi = q.Pop();
	while (qi != NULL)
	{
		Search(qi);
		delete(qi);
		qi = q.Pop();
	}

	return min_loss;
}


void Map::Print()
{
	printf("---------------\n");
	for (int y=0; y<h; y++)
	{
		for (int x=0; x<w; x++)
		{
			//printf("%c", (cells[y][x].c ? '#' : '.'));
			printf("%c", cells[y][x].c + '0');
		}
		printf("\n");
	}
}


//-----------------------------------------------------------------------------
void part1(Map *map)
{
	int loss = map->Start(0, 0, map->w-1, map->h-1);
	printf("Min loss %d\n", loss);
}

void part2(Map *map)
{
	int max_energy = 0;
	printf("Max energy is %d\n", max_energy);
}


int main(int argc, char **argv)
{
	Map m;
	m.Load(INFILE);
	//m.Print();

	part1(&m);
	part2(&m);
	return 0;
}
