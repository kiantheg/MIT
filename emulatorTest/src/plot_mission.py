#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Plotting Code for 3-D Cubic Hermine Splines"

__author__ = "Mason Mitchell, Winston Liu"
__version__ = "1.1"
__maintainer__ = "Ramamurthy Bhagavatula"
__email__ = "ramamurthy.bhagavatula@ll.mit.edu"


# Import required modules and methods
import argparse
from helper_functions import parse_mission
from math import ceil
from matplotlib.patches import Polygon, Wedge
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np
from pathlib import Path
import sys
import yaml


# Default settings
DEFAULT_INTERVAL = .5 # Time interval (s) between consecutive path markers
DEFAULT_MARKER_SIZE = 50 # Size of path markers
DEFAULT_BEAM_SPACING = 0.25 # Fraction of overall path at multiples of which radar beam will be drawn
DEFAULT_TIME_SPACING = 0.2 # Fraction of the overall path at multiples of which the elapsed time will be labeled

# Default directories and file
INPUT_DIR = Path(__file__).resolve().parents[1] / 'input'
DEFAULT_MISSION = 'mission.yml'

# Visualization settings
START_COLOR = '#b3de69'
WAYPOINT_COLOR = '#fdb462'
PATH_COLOR = '#80b1d3'
END_COLOR = '#fb8072'
ORIENTATION_COLOR = '#373640'
ROI_ALPHA = 0.5
ROI_FACECOLOR = '#8dd3c7'
ROI_EDGECOLOR = '#558078'
ROI_LINESTYLE = '--'
ROI_LINEWIDTH = 3
BEAM_RADIUS = 10 # (m)
BEAM_ALPHA = 0.5
BEAM_FACECOLOR = '#bebada'
BEAM_EDGECOLOR = '#858299'
BEAM_LINESTYLE = '-'
BEAM_LINEWIDTH = 3
TIME_COLOR = '#ad2424'
AXES_LIMIT_DILATION = 1.1
MIN_AXES_SIZE = 2 * BEAM_RADIUS # (m)

def parse_args(args):
    """Input argument parser.
    Args:
        args (list)
            Input arguments as taken from command line execution via sys.argv[1:].
            
    Returns:
        parsed_args (namespace)
            Parsed arguments.
            
    Raises:
        FileNotFoundError if 'mission' cannot be found.
    """
    # Parse input arguments
    parser = argparse.ArgumentParser(
        description="Plots platform path as a function of mission specified in file provided.",
        epilog=("Plotting is done using mplot3d's scatter method "
                "(https://matplotlib.org/stable/tutorials/toolkits/mplot3d.html#scatter-plots). "
                "Any arguments/settings controlling the actual visualization (e.g., --marker_size) "
                "is in the context of the scatter method."))
    parser.add_argument('-m', '--mission', nargs='?', type=str, 
                        default=DEFAULT_MISSION, const=DEFAULT_MISSION,
                        help=("YML file specifying mission. If not at the path specified, will "
                              f"also look in '{INPUT_DIR}''. Defaults to '{DEFAULT_MISSION}''."))
    parser.add_argument('-i', '--interval', type=float, default=DEFAULT_INTERVAL,
                        help=("Time interval (s) between consecutive path markers. Larger values "
                              f"will space them out more. Defaults to {DEFAULT_INTERVAL}."))
    parser.add_argument('-s', '--marker_size', type=float, default=DEFAULT_MARKER_SIZE,
                        help=f"Size of path markers. Defaults to {DEFAULT_MARKER_SIZE}.")
    parser.add_argument('-nr', '--no_roi', action='store_true', 
                        help="Visualize region-of-interest (ROI) specified in 'mission' file.")
    parser.add_argument('-nb', '--no_beam', action='store_true',
                        help=("Visualize radar azimuthal beamwidth and heading specified in "
                              "'mission' file."))
    parser.add_argument('-bs', '--beam_spacing', type=float, default=DEFAULT_BEAM_SPACING,
                        help=("Fraction of overall path at multiples of which radar beam will be "
                              "drawn. Must be in [0, 1] range inclusive; values outside this range "
                              "will be clipped. Too high a fraction may slow down rendering. "
                              f"Defaults to {DEFAULT_BEAM_SPACING}."))
    parser.add_argument('-ts', '--time_spacing', type=float, default=DEFAULT_TIME_SPACING,
                        help=("Fraction of overall path at multiples of which the elapsed time of "
                              "the platform path will be labeled. Must be in [0, 1] range inclusive; "
                              "values outside this range will be clipped. Too high a fraction may "
                              f"slow down rendering. Defaults to {DEFAULT_TIME_SPACING}."))
    parsed_args = parser.parse_args(args)
    
    # Additional parsing
    mission = Path(parsed_args.mission).resolve()
    # Check if mission exists at specified path
    if not mission.exists():
        # Check if mission exists in INPUT_DIR
        mission = INPUT_DIR.joinpath(mission.name).resolve()
        if not mission.exists():
            raise FileNotFoundError(f"'{mission.name}'' cannot be found at path specified or in "
                                    f"input directory '{INPUT_DIR}'!")
    parsed_args.mission = mission.as_posix()
    # Make sure beam and time spacing is in [0, 1] range inclusive
    parsed_args.beam_spacing = np.clip(parsed_args.beam_spacing, 0, 1)
    parsed_args.time_spacing = np.clip(parsed_args.time_spacing, 0, 1)
    return parsed_args


def main(args):
    """Displays platform path as a function of specified mission.
    
    Args:
        args (list)
            Input arguments as taken from command line execution via sys.argv[1:].
    """
    # Parse input arguments
    parsed_args = parse_args(args)
    
    # Read mission file
    with open(parsed_args.mission, 'r') as f:
        mission = yaml.load(f, Loader=yaml.FullLoader)
    mission['waypoints_pos_vel'] = np.asarray(mission['waypoints_pos_vel'])
    mission['init_xy_heading'] = np.asarray(mission['init_xy_heading'])
    if 'roi' in mission.keys() and not parsed_args.no_roi:
        roi_min_x = 1e10
        roi_max_x = -1e10
        roi_min_y = 1e10
        roi_max_y = -1e10
        for roi_name, roi_coords in mission['roi'].items():
            mission['roi'][roi_name] = np.asarray(roi_coords)
            roi_min_x = min((roi_min_x, np.amin(mission['roi'][roi_name][:, 0])))
            roi_max_x = max((roi_max_x, np.amax(mission['roi'][roi_name][:, 0])))
            roi_min_y = min((roi_min_y, np.amin(mission['roi'][roi_name][:, 1])))
            roi_max_y = max((roi_max_y, np.amax(mission['roi'][roi_name][:, 1])))
    # Calculate platform path and radar heading
    platform_pos, radar_heading = parse_mission(mission, parsed_args.interval)
    
    # Due to limitations in matplotlib's 3D functionality, have to play some tricks to get axes' 
    # limits and aspect ratio where we want
    x_lim = [np.amin(platform_pos[:, 0]), np.amax(platform_pos[:, 0])]
    y_lim = [np.amin(platform_pos[:, 1]), np.amax(platform_pos[:, 1])]
    z_lim = [0, AXES_LIMIT_DILATION * np.amax(platform_pos[:, 2])]
    if 'roi' in mission.keys() and not parsed_args.no_roi:
        x_lim[0] = min([x_lim[0], roi_min_x])
        x_lim[1] = max([x_lim[1], roi_max_x])
        y_lim[0] = min([y_lim[0], roi_min_y])
        y_lim[1] = max([y_lim[1], roi_max_y])
    x_mid = (x_lim[0] + x_lim[1]) / 2
    y_mid = (y_lim[0] + y_lim[1]) / 2
    x_span = AXES_LIMIT_DILATION * (x_lim[1] - x_lim[0])
    y_span = AXES_LIMIT_DILATION * (y_lim[1] - y_lim[0])
    if x_span == 0:
        x_lim[0] = x_mid - MIN_AXES_SIZE / 2
        x_lim[1] = x_mid + MIN_AXES_SIZE / 2
        x_span = MIN_AXES_SIZE
    else:
        x_lim = [x_mid - x_span / 2, x_mid + x_span / 2]
    if y_span == 0:
        y_lim[0] = y_mid - MIN_AXES_SIZE / 2
        y_lim[1] = y_mid + MIN_AXES_SIZE / 2
        y_span = MIN_AXES_SIZE
    else:
        y_lim = [y_mid - y_span / 2, y_mid + y_span / 2]
    aspect_ratio = np.array([x_span, y_span, z_lim[1]])
    aspect_ratio = aspect_ratio / np.amin(aspect_ratio)
    
    # Plot platform path and waypoints
    fig = plt.figure()
    plt.style.use("seaborn-paper")
    ax = fig.add_subplot(projection='3d')
    ax.scatter(platform_pos[0, 0], platform_pos[0, 1], platform_pos[0, 2], depthshade=False, 
               c=START_COLOR, marker='D', s=parsed_args.marker_size, label="Start Position")
    ax.scatter(mission['waypoints_pos_vel'][1:-1, 0], mission['waypoints_pos_vel'][1:-1, 1], 
               mission['waypoints_pos_vel'][1:-1, 2], depthshade=False, c=WAYPOINT_COLOR, 
               s=parsed_args.marker_size, label=f"Waypoints")
    ax.scatter(platform_pos[-1, 0], platform_pos[-1, 1], platform_pos[-1, 2], depthshade=False, 
               c=END_COLOR, marker='s', s=parsed_args.marker_size, label="End Position",)
    ax.scatter(platform_pos[1:-1, 0], platform_pos[1:-1, 1], platform_pos[1:-1, 2], 
               depthshade=False, c=PATH_COLOR, s=(parsed_args.marker_size / 2),
               label=f"Platform Path; Interval = {parsed_args.interval} s")
    
    # Plot ROI if specified
    if 'roi' in mission.keys() and not parsed_args.no_roi:
        for idx, roi_coords in enumerate(mission['roi'].values()):
            label = "Regions of Interest" if idx == 0 else ''
            roi_patch = Polygon(roi_coords, alpha=ROI_ALPHA, facecolor=ROI_FACECOLOR, 
                                edgecolor=ROI_EDGECOLOR, linestyle=ROI_LINESTYLE, 
                                linewidth=ROI_LINEWIDTH, label=label)
            ax.add_patch(roi_patch)
            art3d.pathpatch_2d_to_3d(roi_patch)
            
    # Plot radar azimuthal beam and heading if specified
    if not parsed_args.no_beam:
        # Radar orientation at each platform path sample
        ax.quiver(platform_pos[:, 0], platform_pos[:, 1], platform_pos[:, 2],
                  radar_heading[:, 0], radar_heading[:, 1], radar_heading[:, 2], 
                  colors=ORIENTATION_COLOR, label="Radar Orientation")
        # Radar beam at spaced at specified fraction of overall platform path
        beam_span = mission['beamwidth'] / 2
        beam_idx = np.arange(0, platform_pos.shape[0], 
                             ceil(parsed_args.beam_spacing * platform_pos.shape[0]))
        if beam_idx[-1] == platform_pos.shape[0]:
            beam_idx = beam_idx[:-1]
        beam_idx = beam_idx[1:]
        beam_angles = np.degrees(np.arctan2(radar_heading[beam_idx, 1], radar_heading[beam_idx, 0]))
        beam_pos = platform_pos[beam_idx, :]
        for idx in range(beam_idx.size):
            label = 'Radar Beam' if idx == 0 else ''
            beam_patch = Wedge(beam_pos[idx, :2], BEAM_RADIUS, beam_angles[idx] - beam_span, 
                               beam_angles[idx] + beam_span, alpha=BEAM_ALPHA,
                               facecolor=BEAM_FACECOLOR, edgecolor=BEAM_EDGECOLOR, 
                               linestyle=BEAM_LINESTYLE, linewidth=BEAM_LINEWIDTH, label=label)
            ax.add_patch(beam_patch)
            art3d.pathpatch_2d_to_3d(beam_patch, beam_pos[idx, 2])
            
    # Time elapsed labels
    time_idx = np.arange(0, platform_pos.shape[0], 
                         ceil(parsed_args.time_spacing * platform_pos.shape[0]))
    if time_idx[-1] == platform_pos.shape[0]:
        time_idx = time_idx[:-1]
    time_idx = time_idx[1:]
    time_pos = platform_pos[time_idx, :]
    time_elapsed = time_idx * parsed_args.interval
    for idx in range(time_idx.size):
        ax.text(time_pos[idx, 0], time_pos[idx, 1], time_pos[idx, 2], 
                f"{time_elapsed[idx]} s", zdir=(1, 1, 1), color=TIME_COLOR)
        
    # Limits, aspect ratio, and labels
    ax.set_xlim(x_lim[0], x_lim[1])
    ax.set_ylim(y_lim[0], y_lim[1])
    ax.set_zlim(z_lim[0], z_lim[1])
    ax.set_box_aspect(aspect_ratio)
    x_ticks = ax.get_xticks()
    y_ticks = ax.get_yticks()
    min_tick_spacing = min([x_ticks[1] - x_ticks[0], y_ticks[1] - y_ticks[0]])
    x_mid = round(x_mid)
    y_mid = round(y_mid)
    x_ticks = np.concatenate((np.flip(np.arange(x_mid, x_lim[0] - min_tick_spacing, -1 * min_tick_spacing)),
                              np.arange(x_mid + min_tick_spacing, x_lim[1] + min_tick_spacing, min_tick_spacing)))
    y_ticks = np.concatenate((np.flip(np.arange(y_mid, y_lim[0] - min_tick_spacing, -1 * min_tick_spacing)),
                              np.arange(y_mid + min_tick_spacing, y_lim[1] + min_tick_spacing, min_tick_spacing)))
    z_ticks = np.arange(0, z_lim[1] + min_tick_spacing, min_tick_spacing)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_zticks(z_ticks)
    ax.set_title(f"Platform Path; Approximate Mission Time = {parsed_args.interval * platform_pos.shape[0]} s")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.legend()
    plt.show()


if __name__ == '__main__':
    """Standard Python alias for command line execution."""
    main(sys.argv[1:])
