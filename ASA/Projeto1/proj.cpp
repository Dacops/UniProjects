/*
Projeto Realizado pelo o Grupo tp012:
    David Pires ist1 103458
    Diogo Miranda ist1 102536
*/

#include <iostream>
#include <vector>
#include <cstring>
#include <unordered_map>
#include <algorithm>
#include <string>
#include <sstream>
#include <iterator>
#include <numeric>
#include <iomanip>


using namespace std;


int lines, columns;                         // number of lines and columns.
bool allZeros = true;                       // check if all entries are 0
vector<int> _linesValues;                   // vector to save free spaces per row.
vector<int> _occupiedColumns;               // vector to save occupied columns per row (offset).
//create a hashmap where the keys are a pair of vectors and the values are the number of combinations
unordered_map<string, long> map;


void readInput() {

    ios::sync_with_stdio(false);            // faster read speeds.
    cin >> lines;
    cin >> columns;                         // columns are not used but still need to be read.
    _linesValues.resize(lines);             // create vector that saves free spaces per row.
    _occupiedColumns.resize(lines);         // create vector that saves occupied columns per row.
    for (int i = 0; i < lines; i++) {
        cin >> _linesValues[i];
        if (_linesValues[i] != 0) { allZeros = false; }
        _occupiedColumns[i] = 0;
    }
}

vector<int> normalize(vector<int> arg) {
    int min = min_element(arg.begin(),arg.end()) - arg.begin();
    vector<int> normalized;
    normalized.resize(lines);
    for(int i = 0; i < (int)arg.size(); i++)    
        normalized[i] = arg[i] - arg[min];
    return normalized;
}

string hashFunc(vector<int> arg, vector<int> arg1) {
    ostringstream aux;
    ostringstream aux2;
    copy(arg.begin(), arg.end(), ostream_iterator<int>(aux, ""));
    copy(arg1.begin(), arg1.end(), ostream_iterator<int>(aux2, ""));
    return aux.str() + aux2.str();
}

bool isOver(vector<int> values) {

    int flag = 0;
    //if there's 2 values more than 1 in 2 consecutive lines than the combinations from the subproblem are >1
    for(int i=0; i<(int)values.size(); i++) {
        if (values[i]>1 ? flag++ : flag=0);
        if (flag==2) return false;
    }
    return true;
}

bool isPossible(int pos, int size, vector<int> values, vector<int> occupied) {

    // square gets out of matrix
    if(pos+size>(int)values.size()) return false;

    // offset in rows below is bigger then current position
    for(int i=pos; i<pos+size; i++) {
        if(occupied[pos]<occupied[i]) return false;
    }

    return true;
}

long getCombinations(vector<int> values, vector<int> occupied) {

    // vectors to be transformed by this iteration.
    vector<int> newValues;
    vector<int> newOccupied; 

    // sizes of inputted vectors.
    int size = (int)values.size();
    newValues.resize(size);
    newOccupied.resize(size);

    // Remove lines with 1 or less free spots (creates new vectors).
    for(int i=0; i<size; i++) {
        if(values[i]>1) {
            newValues[i]=values[i];
            newOccupied[i]=occupied[i];
        }
        else {
            newValues[i]=0;
            newOccupied[i]=columns;
        }
    }


    // if the pair of newValues newOccupied was already calculated, add the number of combinations to the total and return else insert it to map
    if(map.find(hashFunc(newValues,normalize(newOccupied))) != map.end()) { return map[hashFunc(newValues,normalize(newOccupied))]; }

    // If only one line has free spots there's only 1 possible combination (all 1x1).
    if(isOver(newValues)) { map[hashFunc(newValues,normalize(newOccupied))] = 1; return map[hashFunc(newValues,normalize(newOccupied))]; }

    // Implement dynamic coding. Check if inputted vector was already calculated.

    // Get minimum offset position.
    int minOff = newOccupied[0], minPos = 0;
    for(int i=0; i<(int)newOccupied.size(); i++) {
        if(newOccupied[i]<minOff) {
            minOff = newOccupied[i];
            minPos = i;
        }
    }

    // Check if Squares of nxn size can fit in the free spots.
    for(int n=newValues[minPos]; n>0; n--) {

        // is it possible to place a nxn square on this line
        if(isPossible(minPos,n,newValues,newOccupied)) {

            // new vectors need to be created, so they can be edited, newValues and newOccupied are being
            // used by all instances created in this generation.
            vector<int> newerValues;
            vector<int> newerOccupied;
            newerValues.resize((int)newValues.size());
            newerOccupied.resize((int)newOccupied.size());

            // fills new vectors.
            for (int j=0; j<(int)newValues.size(); j++) {
                newerValues[j] = newValues[j];
                newerOccupied[j] = newOccupied[j];
            }

            // updates new vectors.
            for (int j=minPos; j<minPos+n; j++) {
                newerValues[j] -= n;
                newerOccupied[j] += n;
            }
            //add more to the hashmap the number of combinations of the subproblem
            map[hashFunc(newValues,normalize(newOccupied))] += getCombinations(newerValues, newerOccupied);
        }
    }
    return map[hashFunc(newValues,normalize(newOccupied))];
}


int main() {

    readInput();
    if(allZeros) {
        cout << 0 << endl;
        return 0;
    }
    cout << getCombinations(_linesValues, _occupiedColumns) << endl;

    return 0;
}