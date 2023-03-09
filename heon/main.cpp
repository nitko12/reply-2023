#include <bits/stdc++.h>

using namespace std;

int const di[] = {-1, 0, 0, 1};
int const dj[] = {0, -1, 1, 0};
string const MOVE = "ULRD";

mt19937 rng(chrono::high_resolution_clock::now().time_since_epoch().count());

int rand(int x, int y) {
  uniform_int_distribution<int> gen(x, y);
  return gen(rng);
}

pair<int, int> fix_coord(int i, int j, int R, int C) {
  return {(i + R) % R, (j + C) % C};
}

struct Instance {
  int C, R, S;
  vector<vector<int>> V, wormhole;
  vector<int> L;

  Instance(int _C, int _R, int _S) {
    C = _C;
    R = _R;
    S = _S;
    V.resize(R, vector<int>(C));
    wormhole.resize(R, vector<int>(C));
    L.resize(S);
  }
};

struct Solution {
  vector<vector<string>> snakes;
  vector<vector<int>> used;
  Instance const *ins;
  bool current_snake_found_path = false;

  Solution(Instance const &_ins) {
    ins = &_ins;
    used.resize(ins->R, vector<int>(ins->C));
  }

  void dfs(int i, int j, int len) {
    used[i][j] = 1;

    if (len == 0) {
      current_snake_found_path = true;
      return;
    }

    for (int dir = 0; dir < 4; dir++) {
      if (current_snake_found_path)
        break;

      auto [ni, nj] = fix_coord(i + di[dir], j + dj[dir], ins->R, ins->C);
      if (used[ni][nj])
        continue;
      if (ins->wormhole[ni][nj]) {
        // TODO: implement wormholes
        continue;
      }

      snakes.back().push_back(string(1, MOVE[dir]));
      dfs(ni, nj, len - 1);
      if (!current_snake_found_path)
        snakes.back().pop_back();
    } 
  }

  void add_snake_at(int i, int j, int snake_len) {
    snakes.back().push_back(to_string(j));
    snakes.back().push_back(to_string(i));

    // TODO: make smarter dfs, mby greedy? idk
    dfs(i, j, snake_len - 1);
    if (current_snake_found_path)
      current_snake_found_path = false;
    else {
      // path not found
      snakes.back().pop_back();
      snakes.back().pop_back();
    }
  }
};


Solution generate_random_sol(Instance &ins) {
  Solution sol{ins};

  for (int it = 0; it < ins.S; it++) {
    // initialize new snake
    sol.snakes.emplace_back();

    if (!ins.L[it])
      continue;

    for (int tries = 0; tries < 10; tries++) {
      int i = rand(0, ins.R - 1);
      int j = rand(0, ins.C - 1);
      if (ins.wormhole[i][j] || sol.used[i][j])
        continue;

      sol.add_snake_at(i, j, ins.L[it]);
      
      // if path found
      if (!sol.snakes.back().empty())
        break;
    }
  }

  return sol;
}

void input_snake_len(Instance &ins, ifstream &in) {
  for (int i = 0; i < ins.S; i++) 
    in >> ins.L[i];
}

void input_matrix(Instance &ins, ifstream &in) {
  string num;
  for (int i = 0; i < ins.R; i++) {
    for (int j = 0; j < ins.C; j++) {
      in >> num;
      if (num == "*") {
        ins.wormhole[i][j] = 1;
      } else {
        ins.V[i][j] = stoi(num);
      }
    }
  }
}


int main() {
  // string const file_path = "../in/00-example.txt";
  // string const file_path = "../in/01-chilling-cat.txt";
  // string const file_path = "../in/02-swarming-ant.txt";
  // string const file_path = "../in/03-input-anti-greedy.txt";
  // string const file_path = "../in/04-input-low-points.txt";
  string const file_path = "../in/05-input-opposite-points-holes.txt";
  
  ifstream in(file_path);
  
  int C, R, S;
  in >> C >> R >> S;

  Instance ins{C, R, S};
  input_snake_len(ins, in);
  input_matrix(ins, in);

  Solution sol = generate_random_sol(ins);
  int it = 0;
  for (auto &snake_path : sol.snakes) {
    for (auto &move : snake_path)
      cout << move << " ";

    if (++it != S)
      cout << "\n";
  }
  
  in.close();
}
