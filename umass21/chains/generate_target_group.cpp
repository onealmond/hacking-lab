#include <stdio.h>
#include <unordered_map>
#include <vector>

using namespace std;

unordered_map<unsigned int, vector<unsigned int>> target_group = {
 {211,vector<unsigned int>()},
 {136,vector<unsigned int>()},
 {160,vector<unsigned int>()},
 {181,vector<unsigned int>()},
 {352,vector<unsigned int>()},
 {266,vector<unsigned int>()},
 {105,vector<unsigned int>()},
 {271,vector<unsigned int>()},
 {199,vector<unsigned int>()},
 {273,vector<unsigned int>()},
 {247,vector<unsigned int>()},
 {113,vector<unsigned int>()},
 {341,vector<unsigned int>()},
 {110,vector<unsigned int>()},
 {303,vector<unsigned int>()},
 {318,vector<unsigned int>()},
 {116,vector<unsigned int>()},
 {202,vector<unsigned int>()},
 {185,vector<unsigned int>()}
};

unsigned int FUN_001007cc(unsigned int num) {
  unsigned int cur;
  unsigned int ret;
  
  ret = 0;
  cur = num;

  while (cur != 1 && ret < 353) {
    if ((cur & 1) == 0) {
      cur = cur >> 1;
    } else {
      cur = cur * 3 + 1;
    }
    ret++;
  }
  return (unsigned long)ret;
}

int precalculate() {
  unsigned int res, N;

  for (N = 1; N < 900000000; ++N) {
    res = FUN_001007cc(N);
    if (target_group.find(res) != target_group.end()){
      target_group[res].push_back(N);
    }
  }

  for (auto& t : target_group) {
    printf("%u:", t.first);
    for (auto& n : t.second) {
      printf("%u,", n);
    }
    printf("\n");
  }
  
  return 0;
}

int main() {
  precalculate();
  return 0;
}
