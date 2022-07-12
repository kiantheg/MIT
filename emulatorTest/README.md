# 1. Table of Contents
- [1. Table of Contents](#1-table-of-contents)
- [2. Description](#2-description)
  - [2.1. Host-MRM Interaction Model](#21-host-mrm-interaction-model)
  - [2.2. Radar Signal Model](#22-radar-signal-model)
  - [2.3. UAS Motion Model](#23-uas-motion-model)
  - [2.4. Error Models](#24-error-models)
  - [2.5. Notes/Cautions](#25-notescautions)
  - [2.6. Disclaimers](#26-disclaimers)
- [3. Directory Tree](#3-directory-tree)
  - [3.1. Files of Note](#31-files-of-note)
- [4. Prerequisites](#4-prerequisites)
  - [4.1. Python/Modules](#41-pythonmodules)
    - [4.1.1. conda](#411-conda)
    - [4.1.2. pip](#412-pip)
  - [4.2. Local/Internal Network](#42-localinternal-network)
  - [4.3. Host Software](#43-host-software)
- [5. Usage and Behavior](#5-usage-and-behavior)
  - [5.1 Basic Usage](#51-basic-usage)
    - [5.1.1 Arguments](#511-arguments)
  - [5.2. Input/Parameter Files](#52-inputparameter-files)
    - [5.2.1 Scatterers](#521-scatterers)
    - [5.2.2 Mission](#522-mission)
  - [5.3. Examples](#53-examples)
    - [5.3.1. No Host Interaction](#531-no-host-interaction)
    - [5.3.2. Commanding a Finite Number of Scans](#532-commanding-a-finite-number-of-scans)
    - [5.3.3. Error Models Active](#533-error-models-active)
  - [5.4. Logging](#54-logging)
    - [5.4.1. Logging Levels](#541-logging-levels)
- [6. Credits](#6-credits)

# 2. Description
This software, hereafter referred to as the emulator, emulates the behavior of the Time Domain PulsON 440 Monostatic Radar Module (MRM). The primary purpose of this software is to enable the development of Host software for command and control of the MRM. Specifically, modeling of the following is done to a reasonable degree:
- The [Application Programming Interface (API)](docs/320-0298E-MRM-API-Specification.pdf) between a Host and a MRM.
- The UDP-based communication model typically used to communicate between a Host and a MRM.

Assuming that Host software has been developed, the emulator can interact with said Host software to
- Test the validity of the Host software's implementation/usage of the [API](docs/320-0298E-MRM-API-Specification.pdf),
- Prototype the interaction pattern/sequence diagram between the Host software and a MRM, and
- Explore the relationship between MRM settings and the structure and "tempo" of the data produced by a MRM.

The emulator also has a simple model of integration of the MRM onto an Unmanned Aerial System (UAS) in that the motion or path of the UAS can be specified and will be reflected (to a degree) in the data the emulator produces. All of these models are subject to various, appropriate, and parameterized sources of error.

## 2.1. Host-MRM Interaction Model
The interaction between Host software and a MRM is nearly identical to that of a [client-server](https://en.wikipedia.org/wiki/Client%E2%80%93server_model) wherein the Host software is a client making requests of the MRM as a server. One important distinction is that unlike typical, modern client-server applications (e.g., websites) where many clients may interact with a server, this application typically limits itself to one client making it [peer-to-peer](https://en.wikipedia.org/wiki/Peer-to-peer) in terms of interaction. For most developers, this distinction is not important but worth noting for those whose target applications involve either multiple Host software instances and/or multiple MRMs.

The basic interaction pattern is a request-confirm or send-receive one whereby the Host software makes requests of the MRM to which the MRM responds appropriately. This is reflected in the [API](docs/320-0298E-MRM-API-Specification.pdf) where the majority of messages come in pairs in which one message originates from the Host software (request) and its paired message originates from the MRM (confirm). The emulator models this Host-MRM interaction as a synchronous exchange in order to reduce complexity and transparency though the [actual MRM may not be so limited](#25-notescautions). 

## 2.2. Radar Signal Model
The radar model implemented in the emulator is an extremely simple one only modeling power received as a function of platform position, scatterer positions, and a very coarse Radar Cross Section (RCS) scaling. This approach was taken to promote emulator stability and speed with the assumption that exploration of detailed radar phenomenology would be done with an actual MRM. The following system and phenomenology aspects are addressed at a minimal level; anything not described here (e.g., typical components of the radar [range equation](https://www.ll.mit.edu/media/6946)) should be assumed to not be accounted for by the emulator. This does not preclude inclusion of such factors when generating data offline for use by the emulator.
- [Free space path loss](https://en.wikipedia.org/wiki/Free-space_path_loss)) (also referred to as propagation loss);
- [Main lobe](https://en.wikipedia.org/wiki/Main_lobe) (equivalently main beam) rolloff;
- Receive noise as [Additive White Gaussian Noise (AWGN)](https://en.wikipedia.org/wiki/Additive_white_Gaussian_noise).

## 2.3. UAS Motion Model
The UAS motion, specifically its path, is modeled as a [cubic hermite spline interpolation](https://en.wikipedia.org/wiki/Cubic_Hermite_spline) between provided position-velocity waypoints in order to promote "smoothness" of flight. Specifically, the implementation of said model is in [parse_mission](https://github.com/bwsiuassar/emulator/blob/02dea6616db5fd1b48ae27d02f016c14f4d79632/src/helper_functions.py#L304) method of [src/help_functions.py](src/helper_functions.py). There is no guarantee that for any given set of specified waypoints that the computed path will satisfy them to any degree of accuracy. Consequently, a visualization utility has been provided via [src/plot_mission.py](src/plot_mission.py) to help users define and validate desired UAS motion. Refer to the explanation of the [mission](#522-mission) input file for how the UAS motion is parameterized and visualized. 

## 2.4. Error Models
The following sources of real error/non-ideal behavior are modeled, parameterized, and activated depending on developer specified [arguments](#511-arguments).
- [Built-in-Test (BIT) Failures](https://en.wikipedia.org/wiki/Built-in_self-test) - The MRM as a monolithic device may encounter some manner of fault during its operation preventing it from producing accurate and trustworthy data. Simply modeled as a [Bernoulli trial](https://en.wikipedia.org/wiki/Bernoulli_trial). Refer to the MRM [data sheet](docs/320-0317E-P440-Data-Sheet-User-Guide.pdf) and [API](docs/320-0298E-MRM-API-Specification.pdf) for more details on actual failure mechanisms.
- [UDP Packet Loss](https://en.wikipedia.org/wiki/Packet_loss) - By the nature of UDP-based communication, packets/messages sent from the MRM to the Host may be lost by any number of mechanisms. Simply modeled as a [Bernoulli trial](https://en.wikipedia.org/wiki/Bernoulli_trial) on a packet-by-packet basis.
- [No Guarantee of UDP Packet Order](https://en.wikipedia.org/wiki/User_Datagram_Protocol#Attributes): By the nature of UDP-based communication, packets/messages sent from the MRM to the Host are not guaranteed to arrive in the order in which they were sent. Modeled as a two-step stochastic process beginning with a [Bernoulli trial](https://en.wikipedia.org/wiki/Bernoulli_trial) as to whether or not the packet's order will be maintained or not. If a packet's order is not maintained, then a fair draw from a predefined number of consecutive packets determines which packet will be swapped with the one under consideration. This does not model any real UDP/network stack but rather just the randomness of UDP packet arrival order.

## 2.5. Notes/Cautions
- **Limited API Implementation**
  
  Only a minimum of the [API](docs/320-0298E-MRM-API-Specification.pdf) is implemented in the emulator as much of it is not relevant or realistic in the emulator's expected use cases. Refer to [src/formats.py](src/formats.py) for the implemented subset.

- **No Correspondence With Actual Time**
  
  The emulator makes no attempt to execute in a time that is reflective of the actual MRM operation as this is entirely infeasible. Correspondence with "real" timings (e.g., the timing/spacing of scans) is modeled through the metadata (e.g., timestamps) that the MRM generates. This being the case, none of the timing advertised outside of the [API](docs/320-0298E-MRM-API-Specification.pdf) messages (e.g., log message timestamps) is representative of anything beyond program time of execution.

- **Emulator Memory Usage**
  
  In certain configurations, the emulator can ingest large amounts of data and produce correspondingly large(r) amounts of data. Both of these cases may require substantial memory. Developers should take note of their resource utilization to avoid Host unresponsiveness.

- **Synchronous Interaction/Model**
  
  The request-confirm model inherently promotes a [synchronous](https://www.youtube.com/watch?v=N5Ky-mz6n-8) event sequence and the emulator's behavior reflects this. It is important to note that the actual MRM has only been observed to use synchronous interaction in all cases but when errors occur. Therefore, it is strongly recommended that developers assume a synchronous model and implement appropriate checks to avoid unknown behavior. This in turn promotes successful integration of any developed Host software with the actual MRM and avoid potentially harmful interactions with the MRM.

- **YAML Usage/Familiarity**
  
  This codebase uses [YAML](https://yaml.org/) for all configuration and parameterization needs. It is recommended that users have at least a basic familiarity with YAML in order to understand and utilize these aspects of the codebase.

## 2.6. Disclaimers
While proper execution/compatibility of any developed Host software with the emulator is expected to translate into compatibility with the actual MRM, no such guarantees are made. Developers should test their Host software with the real MRM prior to needing it for actual operation.

All information provided here assumes that Host software is being developed in [Python](https://www.python.org/). Development in other languages and compatibility with this emulator software is at the developer's risk.

[**Go to Top**](#1-table-of-contents)

# 3. Directory Tree
```console
.
├── config
│   ├── logger_config.yml
|   └── radar_config.yml
├── docs
│   ├── 320-0298E-MRM-API-Specification.pdf
│   ├── 320-0317E-P440-Data-Sheet-User-Guide.pdf
│   ├── COMM_CHECK API.pdf
│   └── COMM_CHECK API.pptx
├── input
│   ├── mission.yml
│   ├── multi_roi_mission.yml
│   ├── multi_roi_scatterers.yml
│   └── scatterers.yml
├── src
│   ├── constants.py
│   ├── emulator.py
│   ├── formats.py
│   ├── helper_functions.py
│   ├── plot_mission.py
│   └── sort_scan_msgs.yml
├── .gitignore
├── conda_environment.yml
├── LICENSE
├── pip_requirements.txt
└── README.md
```

## 3.1. Files of Note
- Configuration
  - [config/logger_config.yml](config/logger_config.yml) - Emulator [logging](#54-logging) configuration including logging level.
- Documentation
  - [docs/320-0298E-MRM-API-Specification.pdf](docs/320-0298E-MRM-API-Specification.pdf) - PulsON 440 MRM API.
  - [docs/COMM_CHECK API.pdf](docs/COMM_CHECK%20API.pdf) - API for custom message **ONLY** available with the emulator; **NOT** available with actual MRM.
- Input/Parameter
  - [input/mission.yml](input/mission.yml) - Example mission specification.
  - [input/mission.yml](input/mission.yml) - Example scatterers specification.
- Source
  - [src/emulator.py](src/emulator.py) - Emulator implementation.
  - [src/plot_mission.py](src/plot_mission.py) - Mission visualization.

[**Go to Top**](#1-table-of-contents)

# 4. Prerequisites
## 4.1. Python/Modules
The following lists the required Python modules to run the emulator.

| Required Module                       | Minimum Tested Version |
| :------------------------------------ | :--------------------- |
| [Python](https://www.python.org/)     | 3.8.5                  |
| [matplotlib](https://matplotlib.org/) | 3.3.2                  |
| [NumPy](https://numpy.org/)           | 1.19.2                 |
| [PyYAML](https://pyyaml.org/)         | 5.3.1                  |
| [SciPy](https://www.scipy.org/)       | 1.5.2                  |

Provided in this software package are configuration files that will allow you to meet these requirements using either the [conda](https://docs.conda.io/en/latest/) or [pip](https://pip.pypa.io/en/stable/) package managers. Listed below are the steps to meet and use the requirements for each package manager. Please use only one of these options to avoid creating package/environment conflicts

### 4.1.1. [conda](https://docs.conda.io/en/latest/)
In addition to installing requested modules and necessary dependencies, conda can install these items in a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) that is useful for minimizing the complexity of your development and execution environment. The following steps do exactly this.
  1. [Create 'emulator' environment from environment file](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) - `conda env create -f conda_environment.yml`
  2. [Activate 'emulator' environment]((https://docs.conda.io/en/latest/)) - `conda activate emulator`

### 4.1.2. [pip](https://pip.pypa.io/en/stable/)
  1. [Install from requirements file](https://pip.pypa.io/en/stable/user_guide/#requirements-files) - `pip install -r pip_requirements.txt`

## 4.2. Local/Internal Network
Unlike the actual MRM, the emulator runs on the same machine as the Host software. As a result, the emulator resides on the Host's local network (e.g., an IP address of *localhost* or 127.0.0.1) and communicates to any Host software over local, socket-based connections. Whether or not your Host machine is capable of and/or allows this sort of communication is for developers to address.

That said, here are some potentially useful resources to a) validate local network accessibility and b) understand how to interface with the emulator through UDP socket-based communication.
- Official Python resources
  - [socket](https://docs.python.org/3/library/socket.html) module
  - [Socket HOWTO](https://docs.python.org/3/library/socket.html)
  - [UDP communication](https://wiki.python.org/moin/UdpCommunication)
- Tutorials/Examples
  - [UDP client/server template](https://pymotw.com/2/socket/udp.html)
  - [Socket programming](https://realpython.com/python-sockets/) (uses TCP as opposed to UDP; concepts/structures still apply to UDP)

## 4.3. Host Software
This software package does not contain any code to directly interact with the emulator. Developers must create their own Host software if they want to induce any meaningful behavior from the emulator. Until this is done, the emulator will merely boot up, idle, and then shut down.

[**Go to Top**](#1-table-of-contents)

# 5. Usage and Behavior
The emulator is typically executed through command line invocation of [emulator.py](src/emulator.py) (e.g., `python emulator.py`) whose [arguments](#511-arguments) control the manner in which it runs.

The emulator should be invoked before any Host software in the same way an actual MRM should power on and boot successfully before attempting to interface with it. **To that end, it is very important that developers wait for the emulator to advertise its readiness with the message** `READY to respond to requests`. Any attempted interaction with the emulator prior to this readiness will be ignored at best and, at worst, create unpredictable behavior within the emulator.

## 5.1 Basic Usage
The emulator is designed to be used in conjunction with Host software which will direct the emulator to various behaviors. The following is the basic, ordered sequence of broad event categories that are expected to occur.
1. Command line invocation of [emulator.py](src/emulator.py) with appropriate [arguments](#511-arguments), e.g., `python emulator.py`.
2. Invocation and execution of Host software.
3. C2 and data exchange between emulator and Host.
4. Completion of Host software behavior.
5. Emulator shutdown.

### 5.1.1 Arguments
`--op_mode`
- **Description/Purpose:** Emulator operation mode.
- **Type**: string
- **Choices/Requirements:** 
  - `develop` - Run the emulator under ideal assumptions without any of the [error models](#24-error-models).
  - `test` - Run the emulator with the [error models](#24-error-models); packet related error models are applied only to [MRM_SCAN_INFO](docs/320-0298E-MRM-API-Specification.pdf) messages.
  - `real` - Run the emulator with the [error models](#24-error-models); packet related errors are applied to all messages.
- **Default:** `develop`

`data_mode`
- **Description/Purpose:** Radar data generation mode.
- **Type**: string
- **Choices/Requirements:** 
  - `constant` - Generates data that linearly increases on a scan-by-scan basis.
  - `ramp` - Generates data that linearly increases on a [MRM_SCAN_INFO](docs/320-0298E-MRM-API-Specification.pdf) message-by-message basis.
  - `offline` - Generates data based on data specified by the `--offline_data` argument.
  - `realtime` - Generates data based on real-time calculation of signals generated from point scatterers specified by the `--scatterers` argument.
- **Default:** `ramp`

`--offline_data`
- **Description/Purpose:** Path (relative or absolute) to offline data file..
- **Type**: string
- **Choices/Requirements:** 
  - Must be specified if `offline` is specified for `--data_mode` argument.
  - If path cannot be immediately resolved, will look in default location for file; this behavior can be used to centralize input files.
  - File must be a [pickle](https://docs.python.org/3/library/pickle.html) containing data in the format produced by [simulate_sar_data.py](https://github.com/bwsiuassar/gold_standard_code/blob/master/backprojection/simulate_sar_data.py)

`--scatterers`
- **Description/Purpose:** Path (relative or absolute) to file specifying scatterers.
- **Type**: string
- **Choices/Requirements:**
  - Must be specified if `realtime` is specified for `--data_mode` argument.
  - If path cannot be immediately resolved, will look in default location for file; this behavior can be used to centralize input files.
  - File must be a YAML whose contents are formatted in accordance to the README. 
- **Default**: See/run [src/emulator.py](src/emulator.py) help.

`--mission`
- **Description/Purpose:** Path (relative or absolute) to file specifying mission, i.e., platform path waypoints, velocities, radar orientation, and regions-of-interest.
- **Type**: string
- **Choices/Requirements:**
  - Must be specified if `realtime` is specified for `--data_mode` argument.
  - If path cannot be immediately resolved, will look in default location for file; this behavior can be used to centralize input files.
  - File must be a YAML whose contents are formatted in accordance to the README.
- **Default**: See/run [src/emulator.py](src/emulator.py) help.

`--timeout`
- **Description/Purpose:** Amount of time (s) for emulator to idle (i.e., receiving no messages from host) before shutting down.
- **Type**: numeric
- **Choices/Requirements:** 
  - Strictly greater than 0.
- **Default:** See/run [src/emulator.py](src/emulator.py) help.

`--ip`
- **Description/Purpose:** IP address to use for emulator.
- **Type**: string
- **Choices/Requirements:** 
  - Only `localhost` or equivalently `127.0.0.1` are known to reliably work.
- **Default:** See/run [src/emulator.py](src/emulator.py) help.

`--port`
- **Description/Purpose:** Port to use for emulator.
- **Type**: numeric
- **Choices/Requirements:** 
  - Specified port must not conflict with any other network activity.
  - Ports above 10000 are generally considered safe/available but developer should confirm before using.
- **Default:** See/run [src/emulator.py](src/emulator.py) help.

`--add_noise`
- **Description/Purpose:** Include [AWGN](https://en.wikipedia.org/wiki/Additive_white_Gaussian_noise) noise to radar data generated with either `offline` or `realtime` specified for `--data_mode` argument.
- **Type**: flag

`--noise_mag`
- **Description/Purpose:** Magnitude of AWGN noise.
- **Type**: numeric
- **Default:** See/run [src/emulator.py](src/emulator.py) help.

`--prop_loss`
- **Description/Purpose:** Include range propagation loss.
- **Type**: flag

`--beam_rolloff`
- **Description/Purpose:** Include beam rolloff.
- **Type**: flag

`--bit_prob`
- **Description/Purpose:** BIT failure probability.
- **Type**: numeric
- **Choices/Requirements:** 
  - Must be in range [0, 1] inclusive.
- **Default:** See/run [src/emulator.py](src/emulator.py) help.

`--drop_prob`
- **Description/Purpose:** Dropped message/packet probability.
- **Type**: numeric
- **Choices/Requirements:** 
  - Must be in range [0, 1] inclusive.
- **Default:** See/run [src/emulator.py](src/emulator.py) help.

`--order_prob`
- **Description/Purpose:** Out-of-order message/packet arrival probability.
- **Type**: numeric
- **Choices/Requirements:** 
  - Must be in range [0, 1] inclusive.
- **Default:** See/run [src/emulator.py](src/emulator.py) help.

## 5.2. Input/Parameter Files
In coordination with the specific emulator's command line [arguments](#511-arguments), there are input/parameter files that determine the radar scan data generated by the emulator. Specifically, coordinated specification of [scatterers](#521-scatterers) and [mission](#522-mission) whose further explanations are provided in the subsequent sections. It is important to note that while the logic, format, and intended use of these files is described here, the potential complexity of these inputs combined with the complexity of the emulator means that it is the user's responsibility to understand and validate these files for correct behavior.

Common to all these considerations is the following:
- Units of meters, seconds, Hz, and degrees are used.
- All coordinates are specified relative to (0, 0, 0) origin of common (X, Y, Z) Cartesian coordinate system.
- UAS attitude, radar orientation, radar beamwidth, and any other angular quantities are in [standard aircraft axes](https://www.grc.nasa.gov/www/k-12/airplane/rotations.html).
- [RCS](https://en.wikipedia.org/wiki/Radar_cross-section) is specified in square meters.

Provided in this repository are two pairings of scatterer and mission files as examples for users.
- Single Region-of-Interest (ROI) example
  - [input/mission.yml](input/mission.yml)
  - [input/scatterers.yml](input/scatterers.yml)
- Multiple ROI example
  - [input/multi_roi_mission.yml](input/multi_roi_mission.yml)
  - [input/multi_roi_scatterers.yml](input/multi_roi_scatterers.yml)  

### 5.2.1 Scatterers
In the emulator's `realtime` data mode (as specified by the `--datamode` argument), radar scan data is generated as a result of reflection of the transmitted radar energy off of point scatterers. Point scatterers are also referred to as isotropic scatterers in that they reflect incident energy equally in all directions regardless of incident angle, i.e., with no directivity. To specify a point scatterer, all that is needed is its spatial coordinates and [RCS](https://en.wikipedia.org/wiki/Radar_cross-section). This simplicity is why they are often a useful object/target model when first exploring and validating almost any aspect of a [radar model](#22-radar-signal-model). 

The YAML file pointed to by the `--scatterers` argument is used to specify the point scatterer(s) used by the emulator in the `realtime` data mode. The format of the file's content are as follow:
- **pos_rcs** - Sequence whose entry 4-element sequences each specify a separate scatterer.
  - Elements 1 through 3 specify (X, Y, Z) position.
  - Element 4 specified RCS.
- **bandwidth** - Crude approximation of the range resolution, support, of spread of the scattering model.
  - Strongly advised that users use this specific value as long as they are using the PulsON 440 MRM as the radar of interest.

Shown below is the contents of the [input/scatterers.yml](input/scatterers.yml) template/example provided with this repository.
```yaml
# Fixed/known scatterer (X, Y, Z) position (m) and RCS (m^2); one scatterer per row
pos_rcs:
  - [ 7.5, 12.5, 0, 500]
  - [   6,   11, 0, 400]
  - [   6,   14, 0, 300]
  - [   9,   14, 0, 200]
  - [   9,   11, 0, 100]

# Signal and propagation variables
bandwidth: 2437500000 # (Hz)
```

### 5.2.2 Mission
In the emulator's `realtime` data mode (as specified by the `--datamode` argument), the position of the UAS, and thus the radar, is a primarily a function of user specified parameters applied to a [predefined motion model](#23-uas-motion-model). In addition to its position, the orientation of the radar relative to the UAS is also user specified and maintained in accordance with the generated motion. This aspect is of particular importance given that, in conjunction with the scatterers defined by the `--scatterers` argument, the radars visibility of any given scatterer at any given time will be a function of its orientation and position at said time.

In order to help properly configure missions, analyze results, and resolve issues, users are also able to visualize the specified mission with fiducials for reference. Specifically, the functionality of [src/plot_mission.py](src/plot_mission.py) will plot the position of the UAS (and radar), the orientation of the radar, and specified ROIs for reference. The most immediate value of this tool is to confirm that the specified mission will allow the radar to have visibility of the desired ROIs and thus scatterers within them.

The YAML file pointed to by the `--mission` argument is used to specify all of these mission aspects. The format of the file's content are as follow:
- **max_speed** - Maximum platform speed constraint.
- **waypoints_pos_vel** - Sequence whose entry 6-element sequences each specify a separate waypoint which platform will traverse in order.
  - Elements 1 through 3 specify (X, Y, Z) position.
  - Elements 4 through 6 specify (X, Y, Z) velocity.
- **init_xy_heading** - Entry 2-element sequence specifies initial platform (X, Y) heading
  - Used in conjunction with **radar_yaw** to initialize and generate radar orientation.
- **radar_yaw** - Radar orientation yaw relative to platform.
  - Used in conjunction with **init_xy_heading** to initialize and generate radar orientation.
- **beamwidth** - Radar beamwidth used to determine radar azimuthal field-of-view.
- **roi** - Sequence whose entries each specify a separate X-Y plane ROI to visualize.
  - Each entry is a sequence specifying the ordered (X, Y) vertices of a ROI's bounding polygon.

Shown below is the contents of [input/multi_roi_mission.yml](input/multi_roi_mission.yml) example provided with this repository. 
```yaml
# Platform parameters
max_speed: 4 # Maximum platform speed (m/s) constraint
waypoints_pos_vel: # Waypoint (X, Y, Z) coordinates (m) and (V_X, V_Y, V_Z) velocities (m/s); one waypoint per row
  - [ 0,  0,  0, 0, 0,  1] 
  - [ 0,  0, 15, 1, 0,  0]
  - [20,  0, 15, 1, 0,  0]
  - [20, 20, 15, 0, 1,  0]
  - [40, 20, 10, 1, 0,  0]
  - [40,  0, 10, 0, 1,  0]
  - [40,  0,  0, 0, 0, -1]
init_xy_heading: [1, 0] # Initial (X, Y) heading (vector) of the platform; once it motion it will snap to velocity

# Radar parameters 
radar_yaw: -90 # Fixed radar orientation as yaw (degrees) from platform (V_X, V_Y) heading in standard aircraft axes (https://www.grc.nasa.gov/www/k-12/airplane/rotations.html)
beamwidth: 60 # Radar azimuthal beamwidth (degrees)

# Regions-of-interest (ROIs) vertices' (X, Y) coordinates to be visualized with plot_mission.py
roi: 
  one:
    - [ 5, 10]
    - [ 5, 20]
    - [15, 20]
    - [15, 10]
  two:
    - [25, 30]
    - [25, 35]
    - [35, 35]
    - [35, 30]
  three:
    - [50, 15]
    - [50,  5]
    - [70,  5]
    - [70, 15]
```

As mentioned above, a mission can be visualized in order using [src/plot_mission.py](src/plot_mission.py). Specifically, the above example can be visualized by running `python src/plot_mission.py -m multi_roi_mission.yml` which will yield the following plot barring differences in a users display settings.

![Visualization of mission specified by input/multi_roi_mission.yml.](/docs/plot_multi_roi_mission.png "Visualization of mission specified by input/multi_roi_mission.yml.")

## 5.3. Examples
Shown next are a few examples of canonical use cases/invocations of the emulator for reference. The console output produced by emulator is provided to illustrate the overall Host-MRM event sequence from the emulator's perspective. **These assume/can only be realized if the appropriate Host code is implemented and executed in coordination with the emulator meaning that invoking the emulator alone via the provided command line arguments will not recreate these results.**

### 5.3.1. No Host Interaction
In this case, the emulator runs without any interaction from Host software. This leads to the following emulator event sequence:
1. Boot up.
2. Ready for messages from Host software.
3. Shuts down after idling too long.
 
Assuming valid arguments, these three (3) basic steps always occur regardless of emulator arguments. This specific example utilizes the emulators default [arguments](#511-arguments), i.e., `python emulator.py`.

```console
$ python src\emulator.py
2021-07-24 16:37:27,409   STATE       STARTING emulator...
2021-07-24 16:37:27,409   STATE       WAIT for readiness confirmation...
2021-07-24 16:37:27,411   STATE       BOOTING...
2021-07-24 16:37:27,412   STATE       BOOTED in 'develop' operational mode.
2021-07-24 16:37:27,412   STATE       OPENING connection for host...
2021-07-24 16:37:27,415   STATE       OPENED connection for host.
2021-07-24 16:37:27,415   STATE       READY to respond to requests.
2021-07-24 16:37:37,429   STATE       TIMED OUT; emulator idle timeout of 10 seconds exceeded; emulator will shut down.
2021-07-24 16:37:37,430   REFERENCE   Messages, as identified by message ID, were sent in following order --> []
2021-07-24 16:37:37,435   REFERENCE   Following messages, as identified by message ID, were dropped --> []
2021-07-24 16:37:37,435   STATE       SHUTTING DOWN emulator...
2021-07-24 16:37:37,436   STATE       CLOSING connection to host...
2021-07-24 16:37:37,436   STATE       CLOSED connection to host.
2021-07-24 16:37:37,437   STATE       SHUT DOWN complete.
```

### 5.3.2. Commanding a Finite Number of Scans
In this example, the Host software makes the following sequential requests of the emulator:
1. Communication check
2. Status check
3. Configuration set
4. Configuration get
5. Request for four (4) scans

As can be seen from the emulator's console output, this is a more complicated sequence involving significantly increased amount of messaging between the Host software and the emulator. This specific example is realized using the emulator's default [arguments](#511-arguments), i.e., `python emulator.py`, and the appropriate Host code invocation.

```console
2021-07-24 23:24:15,687   STATE       STARTING emulator...
2021-07-24 23:24:15,687   STATE       WAIT for readiness confirmation...
2021-07-24 23:24:15,688   STATE       BOOTING...
2021-07-24 23:24:15,688   STATE       BOOTED in 'develop' operational mode.
2021-07-24 23:24:15,689   STATE       OPENING connection for host...
2021-07-24 23:24:15,691   STATE       OPENED connection for host.
2021-07-24 23:24:15,692   STATE       READY to respond to requests.
2021-07-24 23:24:19,656   INFO        RECEIVE MESSAGE #1 --> MRM_COMM_CHECK_REQUEST.
2021-07-24 23:24:19,656   STATE       COMMUNICATION CHECK request received...
2021-07-24 23:24:19,657   STATE       COMMUNICATION CHECK completed.
2021-07-24 23:24:19,657   INFO        SEND MESSAGE #1 --> MRM_COMM_CHECK_CONFIRM.
2021-07-24 23:24:19,658   INFO        RECEIVE MESSAGE #2 --> MRM_GET_STATUSINFO_REQUEST.
2021-07-24 23:24:19,658   STATE       STATUS GET request received...
2021-07-24 23:24:19,658   STATE       STATUS SENT.
2021-07-24 23:24:19,658   INFO        SEND MESSAGE #2 --> MRM_GET_STATUSINFO_CONFIRM.
2021-07-24 23:24:19,660   INFO        RECEIVE MESSAGE #3 --> MRM_SET_CONFIG_REQUEST.
2021-07-24 23:24:19,660   STATE       CONFIGURATION SET request received...
2021-07-24 23:24:19,660   STATE       CONFIGURATION SET.
2021-07-24 23:24:19,660   INFO        SEND MESSAGE #3 --> MRM_SET_CONFIG_CONFIRM.
2021-07-24 23:24:19,661   INFO        RECEIVE MESSAGE #4 --> MRM_GET_CONFIG_REQUEST.
2021-07-24 23:24:19,661   STATE       CONFIGURATION GET request received...
2021-07-24 23:24:19,661   STATE       CONFIGURATION SENT.
2021-07-24 23:24:19,661   INFO        SEND MESSAGE #4 --> MRM_GET_CONFIG_CONFIRM.
2021-07-24 23:24:19,662   INFO        RECEIVE MESSAGE #5 --> MRM_CONTROL_REQUEST.
2021-07-24 23:24:19,663   STATE       COLLECTION REQUEST received...
2021-07-24 23:24:19,663   STATE       COLLECTING...
2021-07-24 23:24:19,675   INFO        SEND MESSAGE #5 --> MRM_CONTROL_CONFIRM.
2021-07-24 23:24:19,676   INFO        SEND MESSAGE #6 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,676   INFO        SEND MESSAGE #7 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,676   INFO        SEND MESSAGE #8 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,676   INFO        SEND MESSAGE #9 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,676   INFO        SEND MESSAGE #10 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,676   INFO        SEND MESSAGE #11 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,677   INFO        SEND MESSAGE #12 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,677   INFO        SEND MESSAGE #13 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,677   INFO        SEND MESSAGE #14 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,678   INFO        SEND MESSAGE #15 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,678   INFO        SEND MESSAGE #16 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,678   INFO        SEND MESSAGE #17 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,678   INFO        SEND MESSAGE #18 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,679   INFO        SEND MESSAGE #19 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,679   INFO        SEND MESSAGE #20 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,679   INFO        SEND MESSAGE #21 --> MRM_SCAN_INFO.
2021-07-24 23:24:19,680   STATE       COLLECTION DONE.
2021-07-24 23:24:29,694   STATE       TIMED OUT; emulator idle timeout of 10 seconds exceeded; emulator will shut down.
2021-07-24 23:24:29,695   REFERENCE   Messages, as identified by message ID, were sent in following order --> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
2021-07-24 23:24:29,700   REFERENCE   Following messages, as identified by message ID, were dropped --> []
2021-07-24 23:24:29,702   STATE       SHUTTING DOWN emulator...
2021-07-24 23:24:29,703   STATE       CLOSING connection to host...
2021-07-24 23:24:29,705   STATE       CLOSED connection to host.
2021-07-24 23:24:29,705   STATE       SHUT DOWN complete.
```

### 5.3.3. Error Models Active

This example is a repeat of the [previous one](#532-commanding-a-finite-number-of-scans) but with the [error models](#24-error-models) active and their associated probabilities inflated. The overall Host-MRM event sequence remains the same but with the presence of errors, the exact sequence and content of the messages changes. Specifically, towards the end of the output as `REFERENCE` statements, the emulator states that a number of messages have arrived/been sent out of order and some have been dropped.

This specific example is realized by invoking the emulator with `python emulator.py --op_mode test --drop_prob 0.25 --order_prob 0.25`, and the appropriate Host code invocation.

```console
2021-07-24 23:36:08,776   STATE       STARTING emulator...
2021-07-24 23:36:08,777   STATE       WAIT for readiness confirmation...
2021-07-24 23:36:08,777   STATE       BOOTING...
2021-07-24 23:36:08,777   STATE       BOOTED in 'test' operational mode.
2021-07-24 23:36:08,778   STATE       OPENING connection for host...
2021-07-24 23:36:08,780   STATE       OPENED connection for host.
2021-07-24 23:36:08,781   STATE       READY to respond to requests.
2021-07-24 23:36:10,059   INFO        RECEIVE MESSAGE #1 --> MRM_COMM_CHECK_REQUEST.
2021-07-24 23:36:10,059   STATE       COMMUNICATION CHECK request received...
2021-07-24 23:36:10,059   STATE       COMMUNICATION CHECK completed.
2021-07-24 23:36:10,060   INFO        SEND MESSAGE #1 --> MRM_COMM_CHECK_CONFIRM.
2021-07-24 23:36:10,061   INFO        RECEIVE MESSAGE #2 --> MRM_GET_STATUSINFO_REQUEST.
2021-07-24 23:36:10,061   STATE       STATUS GET request received...
2021-07-24 23:36:10,061   STATE       STATUS SENT.
2021-07-24 23:36:10,061   INFO        SEND MESSAGE #2 --> MRM_GET_STATUSINFO_CONFIRM.
2021-07-24 23:36:10,062   INFO        RECEIVE MESSAGE #3 --> MRM_SET_CONFIG_REQUEST.
2021-07-24 23:36:10,063   STATE       CONFIGURATION SET request received...
2021-07-24 23:36:10,063   STATE       CONFIGURATION SET.
2021-07-24 23:36:10,063   INFO        SEND MESSAGE #3 --> MRM_SET_CONFIG_CONFIRM.
2021-07-24 23:36:10,064   INFO        RECEIVE MESSAGE #4 --> MRM_GET_CONFIG_REQUEST.
2021-07-24 23:36:10,064   STATE       CONFIGURATION GET request received...
2021-07-24 23:36:10,064   STATE       CONFIGURATION SENT.
2021-07-24 23:36:10,065   INFO        SEND MESSAGE #4 --> MRM_GET_CONFIG_CONFIRM.
2021-07-24 23:36:10,068   INFO        RECEIVE MESSAGE #5 --> MRM_CONTROL_REQUEST.
2021-07-24 23:36:10,068   STATE       COLLECTION REQUEST received...
2021-07-24 23:36:10,068   STATE       COLLECTING...
2021-07-24 23:36:10,080   INFO        SEND MESSAGE #5 --> MRM_CONTROL_CONFIRM.
2021-07-24 23:36:10,080   INFO        SEND MESSAGE #6 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,081   INFO        SEND MESSAGE #7 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,086   INFO        SEND MESSAGE #8 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,087   INFO        SEND MESSAGE #9 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,087   INFO        SEND MESSAGE #10 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,087   INFO        SEND MESSAGE #11 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,087   INFO        SEND MESSAGE #12 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,087   INFO        SEND MESSAGE #13 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,088   INFO        SEND MESSAGE #14 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,088   INFO        SEND MESSAGE #15 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,088   INFO        SEND MESSAGE #16 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,088   INFO        SEND MESSAGE #17 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,088   INFO        SEND MESSAGE #18 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,089   INFO        SEND MESSAGE #19 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,089   INFO        SEND MESSAGE #20 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,089   INFO        SEND MESSAGE #21 --> MRM_SCAN_INFO.
2021-07-24 23:36:10,090   STATE       COLLECTION DONE.
2021-07-24 23:36:20,099   STATE       TIMED OUT; emulator idle timeout of 10 seconds exceeded; emulator will shut down.
2021-07-24 23:36:20,100   REFERENCE   Messages, as identified by message ID, were sent in following order --> [0, 1, 2, 3, 4, 10, 6, 7, 5, 9, 8, 11, 18, 13, 14, 15, 19, 17, 12, 16, 20]
2021-07-24 23:36:20,101   REFERENCE   Following messages, as identified by message ID, were dropped --> [6, 11, 15, 19]
2021-07-24 23:36:20,101   STATE       SHUTTING DOWN emulator...
2021-07-24 23:36:20,104   STATE       CLOSING connection to host...
2021-07-24 23:36:20,106   STATE       CLOSED connection to host.
2021-07-24 23:36:20,108   STATE       SHUT DOWN complete.
```

## 5.4. Logging
The emulator's logging is implemented using the standard Python [logging](https://docs.python.org/3/howto/logging.html) functionality. Configuration of the logger is done via [logging_config.yml](config/logger_config.yml) which specifies a dictionary that follows a specific [schema](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema). In its default configuration, logs are output both to console via `ext://sys.stdout` and to the file "emulator.log". 

### 5.4.1. Logging Levels
In addition to the [standard logging levels](https://docs.python.org/3/library/logging.html#logging-levels), two (2) new levels are created by the emulator to strike a reasonable balance between verbosity and utility of the logs. The intended purpose of each logging level is described in the table below. For all standard logging levels, "Intended Purpose" is taken from this [HOWTO](https://docs.python.org/3/howto/logging.html).

| Level       | Numeric Value | Intended Purpose                                                                                                                                                                                                     |
| :---------- | :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CRITICAL`  | 50            | A serious error, indicating that the program itself may be unable to continue running.                                                                                                                               |
| `ERROR`     | 40            | Due to a more serious problem, the software has not been able to perform some function.                                                                                                                              |
| `WARNING`   | 30            | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.                                               |
| `STATE`     | 28            | Reports the current state (e.g., "CONFIGURATION SET") of the emulator. Most concise indicator of emulator activity.                                                                                                  |
| `REFERENCE` | 24            | Provides ground truth of non-deterministic emulator behavior such as impact of [error models](#24-error-models). Two such examples of note are the order in which packets/messages were sent and which were dropped. |
| `INFO`      | 20            | Confirmation that things are working as expected.                                                                                                                                                                    |
| `DEBUG`     | 10            | Detailed information, typically of interest only when diagnosing problems.                                                                                                                                           |

[**Go to Top**](#1-table-of-contents)

# 6. Credits
Credit for this codebase goes to the following persons (in alphabetical order):
- Ramamurthy Bhagavatula
- Winston Liu
- Mason Mitchell

[**Go to Top**](#1-table-of-contents)
