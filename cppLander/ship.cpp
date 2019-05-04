// By: Alex Ayala
// 12/9/16
// ship.cpp
// Implementation of Ship class

#define PI 3.1415926
#include <cmath>
#include <vector>
using namespace std;
#include "ship.h"
#include "gfxnew.h"

Ship::Ship()
{
	xpos = 0;
	ypos = 0;
	gas = 750;
	ang = 0;
	xVel = 0;
	yVel = 0;	
	accMode = 0;
}
// Default Constructor

Ship::~Ship()
{
}
// Deconstructor

Ship::Ship(double x, double y, double xv, double yv)
{
	xpos = x;
	ypos = y;
	gas = 750;
	ang = 0;
	accMode = 0;
	xVel = xv;
	yVel = yv;
}
// Overloaded Constructor

double Ship::getXpos()
{
	return xpos;
}

double Ship::getYpos()
{
	return ypos;
}

void Ship::setPos(double x, double y)
{
	xpos = x;
	ypos = y;
}
// Get and set methods for xpos and ypos

double Ship::getXvel()
{
	return xVel;
}

double Ship::getYvel()
{
	return yVel;
}

void Ship::setVel(double xv, double yv)
{
	xVel = xv;
	yVel = yv;
}
// Get and set methods for xVel and yVel

double Ship::getGas()
{
	return gas;
}

void Ship::setGas(double g)
{
	if(g > 0)
	{
		gas = g;
	}
	else
	{
		gas = 0;
	}
	// Ensures that gas does not go below 0
}
// Get and set methods for gas

void Ship::rotate(double newAng)
{
	if(newAng > 0)
	{
		ang = 0;
	}
	else if(newAng < -PI)
	{
		ang = -PI;
	}
	else
	{
		ang = newAng;
	}
}
// Changes angle based on newAng. Also makes sure that angle stays between -PI and 0 inclusive

void Ship::setAng(double angle)
{
	ang = angle;
}

double Ship::getAng()
{
	return ang;
}
// Get and set methods for angle

void Ship::setAccMode(int mode)
{
	accMode = mode;
}

int Ship::getAccMode()
{
	return accMode;
}
// Get and set methods for accMode

void Ship::accelerate(double &xv, double &yv)
{
	xv = xv + .025*accMode*cos(ang);
	yv = yv + .035*accMode*sin(ang);
	gas = gas - .015*accMode;
	if(gas < 0)
	{
		 gas = 0;
	}
}
// Changes the passed x and y velocities based on their current values, the ship's angle, and accMode
// If gas gets below 0 it's also set to 0

void Ship::accelerateChange(int modifier)
{
	accMode += modifier;
	if(accMode < 0 || accMode > 8)
	{
		accMode -= modifier;
	}
	// Ensures that accMode stays within the range 0 and 8 inclusive
	if(gas <= 0)
	{
		accMode = 0;
	}
	// If out of gas then accMode is 0
}
// changes accMode depending on the modifier

void Ship::draw()
{
	gfx_line(xpos - 6.*cos(ang + PI/6.), ypos - 6.*sin(ang + PI/6.),
		 xpos - 12.*cos(ang + PI/6.), ypos - 12.*sin(ang + PI/6.));

	gfx_line(xpos - 6.*cos(ang - PI/6.), ypos - 6.*sin(ang - PI/6.),
		 xpos - 12.*cos(ang - PI/6.), ypos -  12.*sin(ang - PI/6.));
	// Draw landing gear

	if(accMode > 0)
	{
		gfx_line(xpos - 6.*cos(ang + PI/6.), ypos - 6.*sin(ang + PI/6.),
			 xpos - 6.*cos(ang) - ((double)accMode)*2.*cos(ang), ypos - 6.*sin(ang) - ((double)accMode)*2.*sin(ang));
	
		gfx_line(xpos - 6.*cos(ang - PI/6.), ypos - 6.*sin(ang - PI/6.),
			 xpos - 6.*cos(ang) - ((double)accMode)*2.*cos(ang), ypos - 6.*sin(ang) - ((double)accMode)*2.*sin(ang));
		// Draw fire
	}
	gfx_circle(xpos, ypos, 6);
	// Draw body
}
// Draws the ship

int Ship::collision(vector<int> xt, vector<int> yt)
{
	bool foot1Touch = false;
	bool foot2Touch = false;

	for(int i = 0; i < (int)xt.size(); i++)
	{
		for(int j = 0; j < (int)bodyXPoints.size(); j++)
		{
			if(bodyXPoints[j] > xt[i] - 2 && bodyXPoints[j] < xt[i] + 2)
			{
				if(bodyYPoints[j] > yt[i])
				{
					return 1;
					// Indicates the ship crashed
				}
			}
		}
	}
	// Checks if any part of the body touches (or goes below) the points of the terrain they're lined up with

	for(int i = 0; i < (int)xt.size(); i++)
	{
		for(int k = 0; k < (int)foot1XPoints.size(); k++)
		{
			if(foot1XPoints[k] > xt[i] - 2 && foot1XPoints[k] < xt[i] + 2)
			{
				if(foot1YPoints[k] >= yt[i])
				{
					foot1Touch = true;
				}
			}
			if(foot2XPoints[k] > xt[i] - 2 && foot2XPoints[k] < xt[i] + 2)
			{
				if(foot2YPoints[k] >= yt[i])
				{
					foot2Touch = true;
				}
			}
			if(foot1Touch && foot2Touch)
			{
				return 2;
				// Indicates the ship potentially landed
			}
		}

	}
	// Checks if both feet touch (or go below) the points of the terrain they're lined up with

	for(int i = 0; i < (int)xt.size(); i++)
	{
		for(int k = 0; k < (int)leg1XPoints.size(); k++)
		{
			if(leg1XPoints[k] > xt[i] - 2 && leg1XPoints[k] < xt[i] + 2)
			{
				if(leg1YPoints[k] >= yt[i])
				{
					return 1;
				}
				// Ship crashed
			}
			if(leg2XPoints[k] > xt[i] - 2 && leg2XPoints[k] < xt[i] + 2)
			{
				if(leg2YPoints[k] >= yt[i])
				{
					return 1;
				}
				// Ship crashed
			}
		}

	}
	// Checks if any part of either leg touches (or goes below) the points of the terrain they're lined up with

	return 0;	
}

void Ship::hitbox()
{
	bodyXPoints.clear();
	bodyYPoints.clear();
	leg1XPoints.clear();
	leg1YPoints.clear();
	leg2XPoints.clear();
	leg2YPoints.clear();
	foot1XPoints.clear();
	foot1YPoints.clear();
	foot2XPoints.clear();
	foot2YPoints.clear();
	// Empties the point vectors

	for(float i = 0; i < 2.*PI; i += .25)
	{
		bodyXPoints.push_back((int)roundf(xpos - 6.*cos(i)));
		bodyYPoints.push_back((int)roundf(ypos - 6.*sin(i)));			
	}
	// Fill body point vectors with locations of body points

	for(float i = 6.; i < 11.; i += 1)
	{
		leg1XPoints.push_back((int)roundf(xpos - i*cos(ang + PI/6.)));
		leg1YPoints.push_back((int)roundf(ypos - i*sin(ang + PI/6.)));
		leg2XPoints.push_back((int)roundf(xpos - i*cos(ang - PI/6.)));
		leg2YPoints.push_back((int)roundf(ypos - i*sin(ang - PI/6.)));
	}
	// Fill leg point vectors with locations of leg points

	for(float i = 11.; i <= 12.; i += 1)
	{
		foot1XPoints.push_back((int)roundf(xpos - i*cos(ang + PI/6.)));
		foot1YPoints.push_back((int)roundf(ypos - i*sin(ang + PI/6.)));
		foot2XPoints.push_back((int)roundf(xpos - i*cos(ang - PI/6.)));
		foot2YPoints.push_back((int)roundf(ypos - i*sin(ang - PI/6.)));	
	}
	// Fill foot point vectors with locations of foot points. The feet extend the legs
}
// Calculates and stores the positions of the points of the hitbox
