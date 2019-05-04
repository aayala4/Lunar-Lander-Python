// By: Alex Ayala
// 12/9/16
// ship.h
// Ship class prototype


class Ship
{
	public:
		Ship();
		~Ship();
		Ship(double, double, double, double);
		double getXpos();
		double getYpos();
		void setPos(double, double);
		double getXvel();
		double getYvel();
		void setVel(double, double);
		double getGas();
		void setGas(double);
		void rotate(double);
		void setAng(double);
		double getAng();
		void setAccMode(int);
		int getAccMode();
		void accelerate(double&, double&);
		void accelerateChange(int);
		void draw();
		int collision(vector<int>, vector<int>);
		void hitbox();
	private:
		double xpos;
		double ypos;
		// Used for position

		double xVel;
		double yVel;
		// Used for velocities

		double ang;
		// Used for orientation of ship

		int accMode;
		// Represents the strength of the thrusters. Higher is stronger and lower is weaker.

		double gas;	
		// Stores amount of fuel left

		vector<int> foot1XPoints;
		vector<int> foot1YPoints;
		vector<int> foot2XPoints;
		vector<int> foot2YPoints;
		// Stores x and y coordinates of the foot points

		vector<int> leg1XPoints;
		vector<int> leg1YPoints;
		vector<int> leg2XPoints;
		vector<int> leg2YPoints;
		// Stores x and y coordinates of the leg points

		vector<int> bodyXPoints;
		vector<int> bodyYPoints;
		// Stores x and y coordinates of the body points
};
