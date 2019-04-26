// By: Alex Ayala
// 12/10/16
// terrain.h
// Prototype of Terrain class

class Terrain
{
	public:
		Terrain();
		~Terrain();
		float midpoint(float, float);
		void generate(int, int, float,  int);
		void draw();
		void points();
		vector<int> getXPoints();
		vector<int> getYPoints();
		void multiplierPlace();
		int multiplierCheck(int);
	private:
		vector<float> x;
		vector<float> y;
		// Vectors of draw point x and y positions.
		// These contain the points used for gfx_line rather than every point itself

		vector<float> xm;
		vector<float> ym;
		// Vectors of midpoint positions

		vector<float> xp;
		vector<float> yp;
		// Vectors of previous draw point x and y positions

		vector<int> multipliersValues;
		// Vector holding multipliers for multiplier spots (i.e. 2, 3, 4, 5)

		vector<int> multipliersLengths;
		// Vector holding lengths of multiplier spots

		vector<int> multipliersIndexes;
		// Vector holding indices of x and y vectors where multiplier spots are

		vector<int> xPoints;
		vector<int> yPoints;
		// Vectors of x and y points of the terrain
		// These are different from the vectors x and y because these contain the actual points for the terrain
};
