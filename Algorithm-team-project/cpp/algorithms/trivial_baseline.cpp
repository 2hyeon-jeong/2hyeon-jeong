#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int hamming_distance(const string& a, const string& b, int start) {
    int distance = 0;
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
        if (a[i] != b[start + i]) {
            ++distance;
        }
    }
    return distance;
}

int best_position(const string& read, const string& reference) {
    int best_start = 0;
    int best_distance = static_cast<int>(read.size()) + 1;

    for (int start = 0; start <= static_cast<int>(reference.size() - read.size()); ++start) {
        int distance = hamming_distance(read, reference, start);
        if (distance < best_distance) {
            best_distance = distance;
            best_start = start;
            if (distance == 0) {
                break;
            }
        }
    }

    return best_start;
}

int base_index(char base) {
    if (base == 'A') return 0;
    if (base == 'T') return 1;
    if (base == 'C') return 2;
    return 3;
}

char index_base(int index) {
    static const string bases = "ATCG";
    return bases[index];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string reference;
    int read_count;
    if (!(cin >> reference)) {
        return 0;
    }
    cin >> read_count;

    vector<string> reads(read_count);
    for (int i = 0; i < read_count; ++i) {
        cin >> reads[i];
    }

    vector<vector<int>> votes(reference.size(), vector<int>(4, 0));
    for (int i = 0; i < static_cast<int>(reference.size()); ++i) {
        votes[i][base_index(reference[i])] = 1;
    }

    for (const string& read : reads) {
        if (read.empty() || read.size() > reference.size()) {
            continue;
        }
        int start = best_position(read, reference);
        for (int offset = 0; offset < static_cast<int>(read.size()); ++offset) {
            votes[start + offset][base_index(read[offset])] += 1;
        }
    }

    string reconstructed;
    reconstructed.reserve(reference.size());
    for (const auto& counter : votes) {
        int best = static_cast<int>(max_element(counter.begin(), counter.end()) - counter.begin());
        reconstructed.push_back(index_base(best));
    }

    cout << reconstructed << '\n';
    return 0;
}

