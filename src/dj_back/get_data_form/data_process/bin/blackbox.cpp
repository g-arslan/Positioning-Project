#include <fstream>
#include <iostream>
#include <string>
#include <unistd.h>

const std::string CONFIG_FILE = "config.ini";
const std::string PATH_TO_FILE_KEY = "path";

int main() {
    std::ifstream iniFile(CONFIG_FILE);

    if (!iniFile.good()) {
        std::cerr << "There is no \"" + CONFIG_FILE + "\" found\n";
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

        if (key == PATH_TO_FILE_KEY) {
            found = true;
            path = value;
        }
    }

    if (!found) {
        std::cerr << "There is no \"" + PATH_TO_FILE_KEY + "\" key in \"" + CONFIG_FILE + "\"\n";
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

    std::ofstream resFile("result.txt");
    resFile << "Something happened\n";

    return 0;
}
