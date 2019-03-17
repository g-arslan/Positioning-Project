#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <unistd.h>

const std::string PATH_TO_FILE_KEY = "RoverFile";

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cerr << "No config file provided\n";
        return 1;
    }

    std::string config_path = argv[1];

    std::ifstream iniFile(config_path);

    if (!iniFile.good()) {
        std::cerr << "There is no \"" + config_path + "\" found\n";
        return 1;
    }

    std::string line, path;
    bool found = false;

    while (getline(iniFile, line)) {
        int equal = -1;
        for (size_t i = 0; i < line.size(); ++i) {
            if (line[i] == '=') {
                equal = i;
                break;
            }
        }

        if (equal == -1) continue;

        std::string key = line.substr(0, equal), value = line.substr(equal + 1, (int)line.size() - equal - 1);

        while (key.back() == ' ') key.pop_back();
        reverse(value.begin(), value.end());
        while (value.back() == ' ') value.pop_back();
        reverse(value.begin(), value.end());

        if (key == PATH_TO_FILE_KEY) {
            found = true;
            path = value;
        }
    }

    if (!found) {
        std::cerr << "There is no \"" + PATH_TO_FILE_KEY + "\" key in \"" + config_path + "\"\n";
        return 1;
    }

    std::ifstream dataFile(path);

    if (!dataFile.good()) {
        std::cerr << "There is no data file \"" + path + "\" found\n";
        return 1;
    }

    // Pretend like something happening
    srand(time(NULL));
    int sec = rand() % 7 + 1;
    sleep(sec);

    std::ofstream resSolFile("result.csv");
    resSolFile << "Some result.sol\n";

    std::ofstream statsFile("result.pdf");
    statsFile << "Some stats\n";

    return 0;
}
