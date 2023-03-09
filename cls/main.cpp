#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>

#define POP_SIZE 1000

using namespace std;

struct Specimen {
	vector<vector<string>> snakes;
	vector<vector<bool>> map;
};

int C;
int R;
int S;
int* Slens;
vector<pair<int, int>> wormholeLocations;
string** matrix;

bool wormhole(vector<vector<bool>>& map, int* i, int* j) {
	for(int t = 0; t < wormholeLocations.size(); ++t){
		int newLocation = rand() % wormholeLocations.size();
		int new_i = wormholeLocations[newLocation].first;
		int new_j = wormholeLocations[newLocation].second;
		if(new_i != *i || new_j != *j) {
			*i = new_i;
			*j = new_j;
			return true;
		}
	}
	return false;
}

bool recursiveGenerate(vector<string>& snake_string, vector<vector<bool>>& map, int i, int j, int length) {
	if(map[i][j]) {
		return false;
	}

	bool onWormhole = matrix[i][j] == "*";

	if(onWormhole) {
		if(length == 1) {
			return false;
		}
		if(!wormhole(map, &i, &j)) {
			return false;
		}
		snake_string.push_back(to_string(i));
		snake_string.push_back(to_string(j));
		--length;
	}
	--length;
	map[i][j] = 1;
	if(length == 0) {
		return true;
	}

	int direction = rand() % 4;
	bool success = false;
	int new_i = i, new_j = j;
	for(int k = 0; k < 4; ++k, direction = (direction + 1) % 4){
		switch(direction) {
			case 0:
				if(--new_i < 0) {
					new_i = R - 1;
				}
				snake_string.push_back("L");
			break;
			case 1:
				if(++new_i >= R) {
					new_i = 0;
				}
				snake_string.push_back("R");
			break;
			case 2:
				if(--new_j < 0) {
					new_j = C - 1;
				}
				snake_string.push_back("U");
			break;
			case 3:
				if(++new_j >= C) {
					new_j = 0;
				}
				snake_string.push_back("D");
			break;
		}
		success = recursiveGenerate(snake_string, map, new_i, new_j, length);
		if(!success) {
			snake_string.pop_back();
		}
	}
	if(!success) {
		map[i][j] = 0;
		/*if(onWormhole) {
			snake_string.pop_back();
			snake_string.pop_back();
		}*/
	}
	return success;
}

bool generateSpecimen(Specimen& specimen) {
	for(int snake = 0; snake < S; ++snake) {
		bool success = false;
		for(int t = 0; t < 100; ++t) {
			int i = rand() % R;
			int j = rand() % C;
			vector<string> snake_string;
			snake_string.push_back(to_string(i));
			snake_string.push_back(to_string(j));
			success = recursiveGenerate(snake_string, specimen.map, i, j, Slens[snake]);
			if(success) {
				specimen.snakes.push_back(snake_string);
				break;
			}
		}
		if(!success) {
			return false;
		}
	}
	return true;
}

void initPopulation(Specimen* population) {
	for(int i = 0; i < POP_SIZE; ++i) {
		Specimen newSpecimen = {vector<vector<string>>(S, vector<string>()),
								vector<vector<bool>>(R, vector<bool>(C, 0))};
		generateSpecimen(newSpecimen);
		population[i] = newSpecimen;
	}
}

vector<vector<string>> immunological() {
	
	// inicijaliziraj populaciju
	Specimen population[POP_SIZE];
	initPopulation(population);
	// ponavljaj do zaustavljanja:
		// evaluiraj populaciju
		// odaberi neke ili sve za kloniranje
		// kloniraj odabrane
		// hipermutiraj klonove
		// evaluiraj klonove
		// populacija = najbolji klonovi
		// stvori skroz nove jedinke
		// zamijeni najgore u populaciji s novim jedinkama
	
	// vrati najbolju jedinku
}

int main() {
	srand(time(NULL));
	cin >> C;
	cin >> R;
	cin >> S;
	

	Slens = (int*) malloc(S * sizeof(int));
	matrix = new string*[R];
	for(int i = 0; i < R; ++i) {
		matrix[i] = new string[C];
	}
	
	/* READ FROM FILE */
	for(int i = 0; i < S; ++i) {
		cin >> Slens[i];
	}

	for(int i = 0; i < R; ++i) {
		for(int j = 0; j < C; ++j) {
			cin >> matrix[i][j];
		}
	}

	Specimen newSpecimen = {vector<vector<string>>(S, vector<string>()),
								vector<vector<bool>>(R, vector<bool>(C, 0))};
	bool what = generateSpecimen(newSpecimen);
	cout << what << "\n";
	for(int i = 0; i < newSpecimen.snakes.size(); ++i) {
		for(int j = 0; j < newSpecimen.snakes[i].size(); ++j) {
			cout << newSpecimen.snakes[i][j] << " ";
		}
		cout << "\n";
	}

	/*vector<vector<string>> best = immunological(C, R, S, Slens, matrix);
	
	for(int i = 0; i < best.size(); ++i) {
		cout << best[i][0];
		for(int j = 1; j < best[i].size(); ++j) {
			cout << " " << best[i][j];
		}
		cout << "\n";
	}*/
	
}