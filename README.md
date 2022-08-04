# UAS-SAR: team5

### rishita dhalbisoi, kian chen, g simmons, ziqian xiao :)

## Getting Emulator ready:
* If you don't already have the emulator repo, download it here --> [emulator](https://github.com/bwsiuassar/emulator.gite)
* **Please ensure that the emulator is in the same folder as the team 5 directory!**
* Recommended emulator settings:
    * Logger state = `STATUS`
* Look at the emulator readme for running emulator commands --> [emulator commands] (https://github.com/bwsiuassar/emulator#511-arguments)
   > Our code runs with all op_modes (develop, test, real) 
* Open up a terminal window to run the emulator

## Running Our Program
* Open up another new terminal window while the emulator is running. This terminal window is where you will run our code.
* Run `client.py` and follow the prompted messages to execute the program

## Configurations
* We currently have set configurations in `configurations.py`. Feel free to change the paramaters such as `scan_count` and `range_resolution` here.
   * Change COORDINATES to adjust where you want your image to be.
   * Change RANGE_RESOLUTION and CROSS_RANGE_RESOLUTION to make the pixels the size you want.
   * Change SCAN_END to adjust the range you want to scan (we don't recommand to adjust the SCAN_START time)
   * Change SCAN_RES and BII to adjust the resolution (read P440 API for more details [P440 API] (https://github.com/bwsiuassar/emulator/blob/main/docs/320-0298E-MRM-API-Specification.pdf)

## Enjoy :D

<!-- MARKDOWN LINKS & IMAGES -->
[Contributions] (https://github.com/bwsiuassar/team5/graphs/contributors)
