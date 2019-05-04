// By: Alex Ayala
// 12/10/16
// terrain.cpp
// Terrain class implementation

#define PI 3.1415926

using namespace std;
#include <ctime>
#include <cmath>
#include <cstdlib>
#include <string>
#include <vector>
#include "gfxnew.h"
#include "terrain.h"

Terrain::Terrain()
{
	
}

// Default constructor

Terrain::~Terrain()
{

}
// Deconstructor

float Terrain::midpoint(float p1, float p2)
{
	float mid;
	mid = (p2+p1)/2.;

	return mid;
}
// Given two values, this calculates the average. This is used to find mid point values for x values and y values

void Terrain::generate(int width, int height, float displacement, int iteration)
{
	float midx, midy;
	if(iteration > 7)
	{
		multiplierPlace();
		points();
		return;
	}
	// Base case. This also calls the functions which generate the actual x and y points and the multipliers

	if(iteration == 1)
	{
		x.clear();
		y.clear();
		// Empties x and y vectors

		srand(time(NULL));
		// Initialize random seed

		x.push_back(0);
		x.push_back(width);
		y.push_back(4./5.*height);
		y.push_back(4./5.*height);
		// Initially creates end points at same height
	}
	else
	{
		for(int i = 1; i < (int) x.size(); i++)
		{
			midx = midpoint(x[i], x[i-1]);
			midy = midpoint(y[i], y[i-1]);
			// Calculates the x and y midpoints

			midy += ((float)rand()/RAND_MAX) * displacement - displacement/2.;
			// Varies the midpoint height by changing it by a random number between -displacement and displacement.

			if(midy > height - 25)
			{
				midy = height-25;
			}
			// Makes it so the terrain can't be lower than 25 pixels from the bottom of the height

			xm.push_back(midx);
			ym.push_back(midy);
			// Stores midpoints in the midpoint vectors
		}
		xp = x;
		yp = y;
		// Stores the current x and y vectors in the xp and yp vectors

		x.clear();
		y.clear();
		// Empties the x and y vectors

		for(int i = 0; i < (int)xp.size(); i++)
		{
			x.push_back(xp[i]);
			y.push_back(yp[i]);
			// Add the previous x and y points back into the vector

			if(i < (int)xp.size()-1)
			{
				x.push_back(xm[i]);
				y.push_back(ym[i]);
			}
			// Add the midpoints from the midpoint vector into the x and y vectors
		}
		// This effectively stores the previous x and y points with the new midpoints in the same vector and in the correct order from smallest
		// to largest x value

		xm.clear();
		ym.clear();
		// Empties midpoint vector
	}
	generate(width, height, displacement*2./3., iteration + 1);
	// Recursively call with a smaller displacement and an iteration incremented by 1
}
// Randomly generates a terrain

void Terrain::draw()
{
	string multi;
	for(int i = 1; i < (int)x.size(); i++)
	{
		gfx_line(x[i-1], y[i-1], x[i], y[i]);
	}
	// Draws lines connecting the draw points stored in the x and y vectors

	for(int i = 0; i < (int)multipliersIndexes.size(); i++)
	{
		multi = to_string(multipliersValues[i]) + "x";
		gfx_line(x[multipliersIndexes[i]], y[multipliersIndexes[i]]-1,
		         x[multipliersIndexes[i] + multipliersLengths[i] - 1], y[multipliersIndexes[i] + multipliersLengths[i]-1]-1);
		gfx_line(x[multipliersIndexes[i]], y[multipliersIndexes[i]]-2,
			 x[multipliersIndexes[i] + multipliersLengths[i] - 1], y[multipliersIndexes[i] + multipliersLengths[i]-1]-2);
		// Puts extra lines above multiplier spots to more clearly show where they are

		gfx_text((x[multipliersIndexes[i]] + x[multipliersIndexes[i] + multipliersLengths[i] - 1])/2., y[multipliersIndexes[i]] + 20, multi.c_str());
		// Shows the multiplier text below multiplier spots

		// Note the -1 in the index for the end. This is because lengths are stored as 2-5 so it pushes the endpoint index 1 farther than the actual end point
	}
}
// Draws the terrain

void Terrain::points()
{
	float slope;
	float yNew;
	float yPrev;
	xPoints.clear();
	yPoints.clear();
	for(int i = 1; i < (int)x.size(); i++)
	{
		slope = (y[i] - y[i-1])/(x[i]-x[i-1]);
		// Calculates the slope
		yPrev = y[i-1];
		for(float j = x[i-1]; j < x[i]; j++)
		{
			yNew = slope + yPrev;
			// Calculates the next y point

			xPoints.push_back((int)roundf(j));
			yPoints.push_back((int)roundf(yNew));
			// Rounds the floats j and yNew and stores them in xPoints and yPoints

			yPrev = yNew;
		}
	}
}
// Generates the actual points for the terrain and stores them in xPoints and yPoints

vector<int> Terrain::getXPoints()
{
	return xPoints;
}

vector<int> Terrain::getYPoints()
{
	return yPoints;
}
// Get functions for the xPoints and yPoints vectors

void Terrain::multiplierPlace()
{
	int length;
	int place;
	bool overlapped;
	multipliersLengths.clear();
	multipliersIndexes.clear();
	multipliersValues.clear();
	// Empties the vectors containing info on the multipliers

	for(int i = 0; i < 4; i++)
	{
		length = rand() % 4 + 2;
		// Calculates length as a random number between 2 and 5

		place = rand() % (x.size()-4);
		// Calculates place as random index between 0 and 5th to last index of x
		// This ensures that the multipliers stay within the terrain previously generated

		do
		{
			overlapped = false;
			for(int k = 0; k < (int)multipliersIndexes.size(); k++)
			{
				for(int l = 0; l < multipliersLengths[k]; l++)
				{
					for(int m = 0; m < length; m++)
					{
						if((x[place + m]) == (x[multipliersIndexes[k] + l]))
						{
							overlapped = true;
							length = rand() % 4 + 2;
							place = rand() % (x.size()-5);
							break;
						}
					}
					if(overlapped)
					{
						break;
					}
				}
				if(overlapped)
				{
					break;
				}
			}
		}while(overlapped);
		// This checks if the multiplier was placed on top of an already existing multiplier

		switch (length)
		{
			case 2:
				multipliersValues.push_back(5);
				break;
			case 3:
				multipliersValues.push_back(4);
				break;
			case 4:
				multipliersValues.push_back(3);
				break;
			case 5:
				multipliersValues.push_back(2);
				break;
			default:
				break;
		}
		// Switch case for adding the values of each multiplier to multipliersValues.
		// The smaller length is, the larger the value of the multiplier

		multipliersLengths.push_back(length);
		multipliersIndexes.push_back(place);
		// Adds length and place to multipliersLengths and multipliersIndexes vectors respectively

		for(int j = 0; j < length; j++)
		{
			y[place + j] = y[place];
		}
		// Makes the multiplier spot flat
	}
}

int Terrain::multiplierCheck(int xpos)
{
	for(int i = 0; i < (int) multipliersIndexes.size(); i++)
	{
		if(xpos >= x[multipliersIndexes[i]] && xpos <= x[multipliersIndexes[i] + multipliersLengths[i] - 1])
		{
			return multipliersValues[i];
		}
	}
	return 1;
}
// Checks where the ship is when it landed and returns a multiplier accordingly
// If the ship landed within the x range of a multiplier spot, that multiplier is returned.
// Otherwise, 1 is returned.
