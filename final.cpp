// By: Alex Ayala
// 12/9/16
// final.cpp
// Final Project

#include <iostream>
#include <string>
#include <cmath>
#include <unistd.h>
#include <vector>
using namespace std;

#include "gfxnew.h"
#include "ship.h"
#include "terrain.h"

#ifndef PI
#define PI 3.1415926
#endif

int main()
{
	string scoreStr = "", gasStr = "", altStr = "", xVelStr = "", yVelStr = "";
	int state = 1;
	// Start at menu

	int score = 0;
	// Number of points

	int width = 1400;
	int height = 800;
	// Initial window dimensions

	int collided = 0;
	// Is used to see if there is no collision (0), a crash (1), or a potential landing (2)

	int multiplier = 1;
	double dt = .01;
	// Time factor

	int event;
	char c = 0;
	bool running = true;
	bool playing = true;

	Ship ship;
	// The spaceship

	Terrain terrain;
	// The current terrain

	double xVel, yVel, x, y, ang, gas;
	// x and y velocities, x and y positions, angle, and fuel

	vector<int> xTerrain, yTerrain;
	// Hold the x and y coordinates of the terrain points

	gfx_open(width, height, "Lunar Lander");
	// Opens graphics window
	while(running)
	{
		switch(state)
		{
			case 1:
			// Menu state
				gfx_text(width/2 - 60, height/2, "LUNAR LANDER");
				gfx_text(width/2 - 60, height/2 + 20, "Press P to play");
				gfx_text(width/2 - 60, height/2 + 100, "Controls:");
				gfx_text(width/2 - 60, height/2 + 120, "Left and Right Arrows: Rotate Ship");
				gfx_text(width/2 - 60, height/2 + 140, "Up and Down Arrows: Strengthen/Weaken Thrusters");
				gfx_text(width/2 - 60, height/2 + 160, "Q: Quit");
				// Displays menu

				while(state == 1)
				{
					event = gfx_event_waiting();
					// Stores the event in event

					if(event != 0)
					{
						c = gfx_wait();
					}
					// Checks if an event actually happened. If it did, stores the value of the event in c.

					if(event == 1)
					// Checks if the event was a key release
					{
						switch(c)
						{
							case 'p':
								state = 2;
								score = 0;
								ship.setGas(750);
								break;
								// If p is pressed, starts the game
							case 'q':
								state = 3;
								// If q is pressed, quits the program
								break;
							default:
								break;
						}
					}
				}
				gfx_clear();
				break;
			case 2:
			// Playing the game state
				ship.setPos(100, 100);
				ship.setVel(50, 0);
				ship.setAng(0);
				ship.setAccMode(0);
				// Initializes ship position, velocity, orientation, and accMode

				playing = true;
				terrain.generate(width, height, 450, 1);
				// Generate new terrain

				collided = 0;
				multiplier = 1;
				// Initialized to not collided and multiplier of 1

				xTerrain = terrain.getXPoints();
				yTerrain = terrain.getYPoints();
				// Gets terrain points

				while(playing)
				{
					c = 0;
					// Reset c to 0

					event = gfx_event_waiting();
					// Stores event in event

					if(event != 0)
					// Checks if an event happened. If it did, then store the value of the event in c
					{
						c = gfx_wait();
					}

					gas = ship.getGas();
					xVel = ship.getXvel();
					yVel = ship.getYvel();
					x = ship.getXpos();
					y = ship.getYpos();
					ang = ship.getAng();
					// Get the fuel, velocities, positions, and angle

					y = y + yVel*dt + .5*30.*dt*dt;
					x = x + xVel*dt;
					if(x > width + 10)
					{
						x = -10;
					}
					else if(x < -10)
					{
						x = width + 10;
					}
					// If ship goes off on the side of the screen, it is moved to the other side.

					if(y < -50)
					{
						x = 100;
						y = 100;
						xVel = 50;
						yVel = 0;
						ship.setAng(0);
						ship.setAccMode(0);					
					}
					// If the ship goes too high, then it is placed back at the initial spawn point

					if(xVel >= 100)
					{
						xVel = 100;
					}
					else if(xVel <= -100)
					{
						xVel = -100;
					}
					// Makes x velocity stay within -100 and 100 inclusive

					yVel = yVel + 10.*dt;
					// Calculate new y velocity

					ship.accelerate(xVel, yVel);
					// Accelerates ship

					ship.setPos(x, y);
					ship.setVel(xVel, yVel);
					// Update ship's new velocities and position	

					if(event == 1)
					// Checks if event is a key release
					{
						switch(c)
						{
							case 'Q':
								ship.rotate(ang - PI/14.);
								break;
							// Left Arrow
							case 'S':
								ship.rotate(ang + PI/14.);
								break;
							// Right Arrow
	
							case 'T':
								ship.accelerateChange(-1);
								break;
							// Down Arrow
							case 'R':
								ship.accelerateChange(1);
								break;
							// Up arrow
							case 'q':
								playing = false;
								state = 3;
							// Effectively quit program
								break;
							default:
								break;
						}
					}

					ship.hitbox();
					// Recalculates ship's hitbox

					collided = ship.collision(xTerrain, yTerrain);
					// Checks if the ship collided with the terrain

					switch(collided)
					{
						case 1:
							playing = false;
							gfx_text(width/2 - 40, height/2 - 20, "YOU CRASHED");
							gfx_text(width/2 - 40, height/2, "YOU LOST 100 FUEL UNITS");
							score += 5;
							ship.setGas(ship.getGas() - 100); 
							gfx_flush();
							usleep(4000000);
							break;
						// Crashed
						case 2:
							multiplier = terrain.multiplierCheck(ship.getXpos());
							// Checks if the ship landed on a multiplier spot

							playing = false;
							if(yVel < 12 && abs(xVel) < 25)
							{
								ship.setGas(ship.getGas() + 50);
								score += multiplier*50;
								gfx_text(width/2 - 40, height/2 - 20, "GOOD LANDING");
								gfx_text(width/2 - 40, height/2, "50 FUEL UNITS ADDED");
							}
							// If the user has a good landing

							else if(yVel < 25 && abs(xVel) < 25)
							{
								score += multiplier*15;
								gfx_text(width/2 - 40, height/2 - 20, "HARD LANDING");
							}
							// If the user has a hard landing

							else
							{
								playing = false;
								gfx_text(width/2 - 40, height/2 - 20, "YOU CRASHED");
								gfx_text(width/2 - 40, height/2, "YOU LOST 100 FUEL UNITS");
								score += 5;
								ship.setGas(ship.getGas() - 100); 
							}
							// If the user was going too fast resulting in a crash

							gfx_flush();
							usleep(4000000);
							break;
						// Potentially landed
						default:
							break;
					
					}

					gfx_clear();
					scoreStr = "SCORE    " + to_string(score);
					gasStr = "FUEL     " + to_string((int)gas);
					altStr = "ALTITUDE               " + to_string((int)(height - 10 - y));
					xVelStr = "HORIZONTAL SPEED       " + to_string((int)(xVel));
					yVelStr = "VERTICAL SPEED         " + to_string((int)(-yVel));
					gfx_text(40, 40, scoreStr.c_str());
					gfx_text(40, 60, gasStr.c_str());
					gfx_text(width - 200, 40, altStr.c_str());
					gfx_text(width - 200, 60, xVelStr.c_str());
					gfx_text(width - 200, 80, yVelStr.c_str());
					// Print score, fuel, height, and velocity info

					terrain.draw();
					ship.draw();
					gfx_flush();
					usleep(10000);
					// Redraw terrain and ship and briefly pauses so movement is slow enough for the user

					if(ship.getGas() <= 0)
					{
						state = 1;
						playing = false;
						gfx_text(width/2, height/2, "YOU RAN OUT OF FUEL");
						gfx_text(width/2, height/2 + 20, "GAME OVER.");
						gfx_flush();
						usleep(5000000);
						break;
					}
					// Checks if the user ran out of fuel. If so, then it's game over
				}
				gfx_clear();
				break;
			case 3:
				running = false;
				break;
			// Effectively quits program
			default:
				break;
		}
	}

	return 0;
}

