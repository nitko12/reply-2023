#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>

#define POP_SIZE 1000
#define CLONE_FACTOR 100

using namespace std;

struct Specimen {
	vector<vector<string>> snakes;
	vector<vector<bool>> map;
	int fitness;
};

struct custom_less_than {
	inline bool operator() (const Specimen& specimen1, const Specimen& specimen2) {
		return (specimen1.fitness < specimen2.fitness);
	}
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
		int wnew_i = wormholeLocations[newLocation].first;
		int wnew_j = wormholeLocations[newLocation].second;
		if(wnew_i != *i || wnew_j != *j) {
			int new_i = wnew_i;
			int new_j = wnew_j;
			int direction = rand() % 4;
			for(int k = 0; k < 4; ++k, direction = (direction + 1) % 4){
				switch(direction) {
					case 0:
						if(--new_i < 0) {
							new_i = R - 1;
						}
					break;
					case 1:
						if(++new_i >= R) {
							new_i = 0;
						}
					break;
					case 2:
						if(--new_j < 0) {
							new_j = C - 1;
						}
					break;
					case 3:
						if(++new_j >= C) {
							new_j = 0;
						}
					break;
				}
				if(map[new_i][new_j] == 0) {
					*i = new_i;
					*j = new_j;
					return true;
				}
			}
		}
	}
	return false;
}

bool recursiveGenerate(vector<string>& snake_string, vector<vector<bool>>& map, int i, int j, int length) {
	/*cout << "LENGHT=" << length << "\n";
	for(int i = 0; i < snake_string.size(); ++i) {
		cout << snake_string[i] << " ";
	}
	
	cout << "\n";
	*/
	if(map[i][j]) {
		return false;
	}
	
	--length;

	if(matrix[i][j] == "*") {
		if(length == 0) {
			return false;
		}
		if(!wormhole(map, &i, &j)) {
			return false;
		}
		snake_string.push_back(to_string(i));
		snake_string.push_back(to_string(j));
		bool success = recursiveGenerate(snake_string, map, i, j, length);
		if(!success) {
			snake_string.pop_back();
			snake_string.pop_back();
		}
		return success;
	}
	map[i][j] = 1;
	if(length == 0) {
		return true;
	}

	int direction = rand() % 4;
	bool success = false;
	for(int k = 0; k < 4; ++k, direction = (direction + 1) % 4){
		int new_i = i, new_j = j;
		switch(direction) {
			case 0:
				if(--new_i < 0) {
					new_i = R - 1;
				}
				snake_string.push_back("U");
			break;
			case 1:
				if(++new_i >= R) {
					new_i = 0;
				}
				snake_string.push_back("D");
			break;
			case 2:
				if(--new_j < 0) {
					new_j = C - 1;
				}
				snake_string.push_back("L");
			break;
			case 3:
				if(++new_j >= C) {
					new_j = 0;
				}
				snake_string.push_back("R");
			break;
		}
		success = recursiveGenerate(snake_string, map, new_i, new_j, length);
		if(!success) {
			snake_string.pop_back();
		} else {
			break;
		}
	}
	if(!success) {
		map[i][j] = 0;
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
		Specimen newSpecimen = {vector<vector<string>>(),
								vector<vector<bool>>(R, vector<bool>(C, 0)),
								0};
		generateSpecimen(newSpecimen);
		population[i] = newSpecimen;
	}
}

void evaluate(Specimen* population, int popSize) {
	for(int p = 0; p < popSize; ++p) {
		population[p].fitness = 0;
		for(int i = 0; i < R; ++i) {
			for(int j = 0; j < C; ++j) {
				if(population[p].map[i][j]) {
					population[p].fitness += stoi(matrix[i][j]);
				}
			}
		}
	}
}

/*vector<vector<string>>*/ void immunological() {
	
	// inicijaliziraj populaciju
	Specimen population[POP_SIZE];
	Specimen clones[POP_SIZE*CLONE_FACTOR];
	initPopulation(population);

	// ponavljaj do zaustavljanja:
	for(int iter = 0; iter < 1; ++iter) {
		// evaluiraj populaciju
		evaluate(population, POP_SIZE);
		// odaberi neke ili sve za kloniranje
		// kloniraj odabrane
		// hipermutiraj klonove
		// evaluiraj klonove
		// populacija = najbolji klonovi
		// stvori skroz nove jedinke
		// zamijeni najgore u populaciji s novim jedinkama
	}

	for(int k = 0; k < POP_SIZE; ++k) {
		cout << "SPECIMEN " << k << "\tFitness=" << population[k].fitness << "\n";
		for(int i = 0; i < population[k].snakes.size(); ++i) {
			for(int j = 0; j < population[k].snakes[i].size(); ++j) {
				cout << population[k].snakes[i][j] << " ";
			}
			cout << "\n";
		}
	}
		
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
			if(matrix[i][j] == "*") {
				wormholeLocations.push_back(make_pair(i, j));
			}
		}
	}

	immunological();

	/*vector<vector<string>> best = immunological();
	
	for(int i = 0; i < best.size(); ++i) {
		cout << best[i][0];
		for(int j = 1; j < best[i].size(); ++j) {
			cout << " " << best[i][j];
		}
		cout << "\n";
	}*/
	
}