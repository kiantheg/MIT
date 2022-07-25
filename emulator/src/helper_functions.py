#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Helper functions for UAS-SAR."""

__author__ = "Mason Mitchell, Ramamurthy Bhagavatula, Winston Liu"
__version__ = "1.1"
__maintainer__ = "Ramamurthy Bhagavatula"
__email__ = "ramamurthy.bhagavatula@ll.mit.edu"

# Import required modules and methods
from constants import SPEED_OF_LIGHT
from copy import deepcopy
import logging
import logging.config
import numpy as np
import os
from pathlib import Path
import sys
from warnings import warn

# Default settings
DEFAULT_THETA = np.linspace(-1 * np.pi / 2, np.pi / 2, 10000) # Default beam pattern angle sampling


def setup_logger(name, config):
    """Set up logger.
    
    Args:
        name (str)
            Name of logger to configure. Should be consistent w/ config.
            
        config (dict)
            Logger configuration (https://docs.python.org/3.6/library/logging.config.html). If None 
            then no logging is done.
            
    Returns:
        logger (logging.Logger)
            Configured logger.
            
    Raises:
        KeyError if no logger called matching name is present in config.
    """
    if config is None:
        logger = logging.getLogger()
        logger.propagate = False
    else:
        if name not in config['loggers']:
            raise KeyError(('Logger configuration does have entry matching provided name of + '
                            '\'{0}\'').format(name))
        
        for handler in config['handlers']:
            if config['handlers'][handler]['class'] == 'logging.FileHandler':
                filename = Path(config['handlers'][handler]['filename'])
                if filename.suffix.lower() != '.log':
                    config['handlers'][handler]['filename'] = \
                        filename.with_suffix('.log').as_posix()
        
        logging.captureWarnings(True)
        logging.config.dictConfig(config)
        logger = logging.getLogger(name)
    return logger

def close_logger(logger):
    """Close logger.
    
    Args:
        logger (logging.Logger)
            Logger to close.
    """
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)


def progress_bar(step, total, display_fraction=0.05, increment_name='Step', msg='', done=False, 
                 total_len=25, elapsed_time=None):
    """Prints/updates console text progress bar.
    
    Args:
        step (int)
            Current step number out of total.
            
        total (int)
            Total number of steps.
            
        display_fraction (float)
            Fraction of total number of steps which at integer multiples the progress bar will be 
            updated. Defaults to 0.05.
            
        increment_name (str)
            Name of a step. Should stay constant over a given progress bar's lifetime. Defaults to 
            'Step'.
            
        msg (str)
            Message to print after progress bar. Defaults to ''.
        
        done (bool)
            Indicates whether or not to end progress bar on this update.
            
        total_len (int)
            The number of characters to use to show actual progress bar excluding any text. Defaults
            to 25.
            
        elapsed_time (float)
            The amount of time elapsed since the inception of the progress bar. If None then no time
            information will be printed. Defaults to None.
    """
    # Determine how display fraction maps to step and only update progress bar if it is integer 
    # multiple of the display fraction
    display_step = round(display_fraction * total)
    if step % display_step == 0:
        
        # Display constants
        complete_symbol = '='
        current_symbol = '>'
        incomplete_symbol = '.'
        
        # Set fixed maximum width step progress string
        width = len(str(total))
        percent = 100 * step / total
        step_str = '{0} {1:>{2}}/{3}, {4:>5.1f}%'.format(increment_name, step, width, total, 
                    percent)
        
        # Compute current completion
        complete_len = int(round(total_len * step / float(total)))
        incomplete_len = total_len - complete_len
        progress_bar = complete_symbol * complete_len
        progress_bar += (current_symbol * (incomplete_len >= 1) + 
                         incomplete_symbol * (incomplete_len - 1))
        
        # Update message w/ elapsed time if provided
        if elapsed_time is not None:
            msg = '{0}, {1:.1f} seconds elapsed'.format(msg, elapsed_time)
        
        # Print progress bar
        if not done:
            sys.stdout.write('{0} [{1}] {2}\r'.format(step_str, progress_bar, msg))
        else:
            sys.stdout.write('{0} [{1}] {2}\n'.format(step_str, progress_bar, msg))
        sys.stdout.flush()


def deconflict_file(filename):
    """
    Deconflict w/ specified file, if necessary, by extending the name.
    
    Args:
        filename (str)
            File to deconflict with.
        
    Returns:
        new_file (str)
            Path and name of deconflicted file.
    """
    filename = Path(filename)
    if not filename.exists():
        filename.touch()
        return filename.resolve().as_posix()
    else:
        ii = 0
        while filename.with_name('{0}_{1}{2}'.format(filename.stem, ii, filename.suffix)).exists():
            ii += 1
        filename = filename.with_name('{0}_{1}{2}'.format(filename.stem, ii, filename.suffix))
        filename.touch()
        return filename.resolve().as_posix()

    
def yes_or_no(question):
    """Prompts user to answer a "Yes or No" question through keyboard input.
    
    Args:
        question (str)
            Question to ask.
            
    Returns:
        answer (bool)
            True for "Yes" and False for "No".
    """
    # Set of acceptable answer formats
    yes = set(['yes', 'y'])
    no = set(['no', 'n'])
    
    # Iterate till valid answer is given
    while True:
        answer = input(question + " (y/n): ").lower().strip()
        if answer in yes:
            return True
        elif answer in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'")


def is_valid_file(parser, filename, mode):
    """Check if specified argument is a valid file for read or write; meant to be used in the 
    context of argparse.ArgumentParser.
    
    Args:
        parser (argparse.ArgumentParser)
            Instance.
            
        filename (str)
            File to check.
            
        mode (str)
            The read/write mode to check the file for; options are ['r', 'w'].
            
    Raises:
        parser.error if file is not valid for specified mode.
        parser.error if unrecognized mode is specified.
    """
    if filename:
        if mode == 'r':
            try:
                f = open(filename, 'r')
                f.close()
            except:
                parser.error("{0} does not exist or cannot be read!".format(filename))
        elif mode == 'w':
            try:
                f = open(filename, 'w')
                f.close()
                os.remove(filename)
            except:
                parser.error("{0} does not exist or cannot be written to!".format(filename))
        else:
            parser.error("Unrecognized file mode specified!")


def replace_nan(coords, vals):
    """Replace NaN coordinates and values in data using 1-D interpolation. 
    
    Args:
        coords (ndarray) 
            Length M vector containing data coordinates; may have NaNs in it. Assumes that 
            coordinates are uniformly spaced.
            
        vals (ndarray)
            M x N matrix representing data values; may have NaNs in it.
            
    Returns:
        coords_out (ndarray)
            Length M vector of data coordinates with NaNs replaced; should match coords 
            dimensionality.
        
        vals_out (ndarray)
            Matrix representing data values with NaNs replaced.
    """
    # Initialize outputs; make a deep copy to ensure that inputs are not directly modified
    coords_out = np.copy(coords)
    vals_out = np.copy(vals)
    
    # Store inputs original shapes
    coords_shape = coords_out.shape
    vals_shape = vals_out.shape
    
    # Remove singleton dimensions from coordinates
    coords_out = np.squeeze(coords_out)
    
    # Check inputs
    if coords_out.ndim != 1:
        raise ValueError('Coordinates are not 1-D!')
        
    if vals_out.ndim > 2:
        raise ValueError('Data must be a 2-D matrix!')
    elif vals_out.ndim == 1:
        vals_out = np.reshape(vals_out, (-1, 1))
        
    dim_match = coords_out.size == np.asarray(vals_shape)
    transpose_flag = False
    if not np.any(dim_match):
        raise IndexError('No apparent dimension agreement between coordinates and data!')
    elif np.all(dim_match):
        warn(('Ambiguous dimensionalities; assuming columns of data are to be interpolated'), 
             Warning)
    elif dim_match[0] != 1:
        vals_out = vals_out.transpose()
        transpose_flag = True
        
    # Determine where NaN coordinates are replace them using linear interpolation assuming uniform 
    # spacing
    uniform_spacing = np.arange(0, coords_out.size)
    coords_nan = np.isnan(coords_out)
    coords_out[coords_nan] = np.interp(uniform_spacing[coords_nan], uniform_spacing[~coords_nan], 
              coords_out[~coords_nan])
    
    # Iterate over each dimension of data
    for ii in range(0, vals_shape[1]):
        
        # Determine where the NaN data and replace them using linear interpolation
        vals_nan = np.isnan(vals_out[:, ii])
        vals_out[vals_nan, ii] = np.interp(coords_out[vals_nan], coords_out[~vals_nan], 
                vals_out[~vals_nan, ii])
        
    # Reshape results to match inputs
    coords_out = np.reshape(coords_out, coords_shape)
    if transpose_flag:
        vals_out = np.transpose(vals_out)
    vals_out = np.reshape(vals_out, vals_shape)
    return coords_out, vals_out


def parse_mission(mission, sample_interval, min_pos_change_mag=0.1):
    """Compute platform path through specified waypoints. 
    
    Args:
        mission (dict)
            Specifies mission as combination of platform path waypoints, velocities, radar 
            orientation, and regions-of-interest.

        sample_interval (float)
            Time interval (s) between consecutive generated samples of the platform path.
            
        min_pos_change_mag (float)
            Minimum magnitude change in (X, Y) position (m) between consecutive path samples that 
            could be considered a heading change as it pertains to radar orientation.
            Default to 0.1.
            
    Returns:
        platform_pos (ndarray)
            M x 3 array of platform (X, Y, Z) coordinates at specified sampling interval.
            
        radar_heading (ndarray)
            M x 3 array of radar (X, Y, Z) heading at specified sampling interval.
    """
    # Convenience methods
    def h00(t):
        return (1+(2 * t)) * ((1 - t)**2)
    def h10(t):
        return t * ((1 - t)**2)
    def h01(t):
        return (t**2) * (3 - (2 * t))
    def h11(t):
        return (t**2) * (t - 1)
    def h00_dot(t):
        return ( - 6 * t) * (1 - t)
    def h10_dot(t):
        return (3 * (t**2)) - (4 * t) + 1
    def h01_dot(t):
        return ( - 6) * (t - 1) * t
    def h11_dot(t):
        return t * ((3 * t) - 2)
    
    waypoints_pos_vel = np.array(mission['waypoints_pos_vel'])
    pos = waypoints_pos_vel[:, :3]
    vel = waypoints_pos_vel[:, 3:]
    
    x, y, z = [], [], []
    x_dot, y_dot, z_dot = [], [], []
    
    # Calculates cubic hermite spline
    for i in range(len(pos) - 1):
        for j in range(0, 101):
            t = j / 100
            
            h00_t = h00(t)
            h10_t = h10(t)
            h01_t = h01(t)
            h11_t = h11(t)
            
            h00_dot_t = h00_dot(t)
            h10_dot_t = h10_dot(t)
            h01_dot_t = h01_dot(t)
            h11_dot_t = h11_dot(t)
            
            x.append(h00_t * pos[i][0] + 
                     h10_t * vel[i][0] + 
                     h01_t * pos[i + 1][0] + 
                     h11_t * vel[i + 1][0])
            y.append(h00_t * pos[i][1] + 
                     h10_t * vel[i][1] + 
                     h01_t * pos[i + 1][1] + 
                     h11_t * vel[i + 1][1])
            z.append(h00_t * pos[i][2] + 
                     h10_t * vel[i][2] + 
                     h01_t * pos[i + 1][2] +
                     h11_t * vel[i + 1][2])
            
            x_dot.append(h00_dot_t * pos[i][0] + 
                         h10_dot_t * vel[i][0] + 
                         h01_dot_t * pos[i + 1][0] + 
                         h11_dot_t * vel[i + 1][0])
            y_dot.append(h00_dot_t * pos[i][1] + 
                         h10_dot_t * vel[i][1] + 
                         h01_dot_t * pos[i + 1][1] + 
                         h11_dot_t * vel[i + 1][1])
            z_dot.append(h00_dot_t * pos[i][2] + 
                         h10_dot_t * vel[i][2] + 
                         h01_dot_t * pos[i + 1][2] + 
                         h11_dot_t * vel[i + 1][2])
            
    # Get position and velocity waypoints
    positions = np.transpose([x, y, z])
    velocities = np.transpose([x_dot, y_dot, z_dot])
    
    # Length of path segments
    path_segment_lengths = np.abs(np.linalg.norm(positions[:-1] - positions[1:], axis=1))
    # Velocity magnitudes, i.e., speeds
    speeds = np.abs(np.linalg.norm(velocities[1:], axis=1))
    # Scale all speeds to maximum speed
    speeds = speeds / max(speeds) * mission['max_speed']
    
    # Calculate total time for path
    times = path_segment_lengths / speeds
    cumulative_times = np.insert(np.cumsum(times), 0, 0)
    
    # Interp list generation
    interp_vals = np.arange(0, cumulative_times[-1] + sample_interval, sample_interval)
    
    # Interpolate platform path samples
    x_interp = np.interp(interp_vals, cumulative_times, x)
    y_interp = np.interp(interp_vals, cumulative_times, y)
    z_interp = np.interp(interp_vals, cumulative_times, z)
    platform_pos = np.transpose([x_interp, y_interp, z_interp])
    
    # Compute radar heading as fixed yaw relative to platform (X, Y) heading
    num_samples = platform_pos.shape[0]
    platform_heading_xy = np.diff(platform_pos[:, :2], axis=0)
    heading_change = np.linalg.norm(platform_heading_xy, axis=1) >= min_pos_change_mag
    platform_heading_xy = np.insert(platform_heading_xy, 0, mission['init_xy_heading'], axis=0)
    # Radar orientation rotation matrix under standard aircraft principal axes
    radar_yaw = np.radians(mission['radar_yaw'])
    radar_rot_matrix = np.array([[     np.cos(radar_yaw), np.sin(radar_yaw)], 
                                 [-1 * np.sin(radar_yaw), np.cos(radar_yaw)]])
    radar_heading = np.zeros((num_samples, 2))
    radar_heading[0, :] = np.squeeze(radar_rot_matrix @ mission['init_xy_heading'][:, np.newaxis])
    # Iterate over each path sample except for first and last
    for sample_idx in range(1, num_samples - 1):
        if heading_change[sample_idx - 1]:
            mean_heading_xy = (platform_heading_xy[sample_idx, :] + platform_heading_xy[sample_idx - 1, :]) / 2
            radar_heading[sample_idx, :] = np.squeeze(radar_rot_matrix @ mean_heading_xy[:, np.newaxis])
        else:
            radar_heading[sample_idx, :] = radar_heading[sample_idx - 1, :]
    radar_heading[-1, :] = radar_heading[-2, :]
    radar_heading = np.append(radar_heading, np.zeros((num_samples, 1)), axis=1)
    radar_heading = radar_heading / np.linalg.norm(radar_heading, axis=1)[:, np.newaxis]
    
    return platform_pos, radar_heading


def compute_az_beam_pattern(antenna_config, theta=DEFAULT_THETA):
    """Generates antenna azimuthal beam pattern based on provided configuration.
    
    Args:
        antenna_config (dict)
            Antenna configuration. Required keys are 'type' which specifies the type of antenna to 
            model, and 'params' which specifies the parameters specific to the antenna type and thus 
            vary from type to type.
            
        theta (ndarray)
            Azimuth angles (radians), relative to broadside (i.e., theta = 0), at which beam pattern 
            should be computed. Defaults to DEFAULT_THETA.
            
    Returns:
        beam_pattern (ndarray)
            Linear-valued, normalized, azimuthal beam pattern. To convert to dB, only apply 
            10 * log10 as conversion from voltage to power has already been done.
            
        theta (ndarray)
            Azimuth angles (radians), relative to broadside (i.e., theta = 0), at which beam pattern 
            was computed.
            
        updated_antenna_config (dict)
            Antenna configuration as updated by any internal logic for reference.
            
    Raises:
        KeyError if unknown antenna type is specified.
    """
    # Uniform linear array
    if antenna_config['type'] == 'uniform_linear_array':
        # Parse antenna parameters
        center_lambda = SPEED_OF_LIGHT / antenna_config['params']['center_freq']
        elem_spacing = antenna_config['params']['elem_spacing'] * center_lambda
        # Compute knowing number of elements or desired beamwidth
        if 'num_elem' in antenna_config['params'].keys():
            num_elem = antenna_config['params']['num_elem']
        elif 'beamwidth' in antenna_config['params'].keys():
            beamwidth = np.radians(antenna_config['params']['beamwidth'])
            num_elem = 0.886 * center_lambda / (elem_spacing * beamwidth)
        # Compute beam pattern
        beam_pattern = (np.sin(num_elem * np.pi * elem_spacing / center_lambda * np.sin(theta)) / 
                        (num_elem * np.sin(np.pi * elem_spacing / center_lambda * np.sin(theta))))
        beam_pattern = np.abs(beam_pattern)**2
        # Update antenna configuration
        updated_antenna_config = deepcopy(antenna_config)
        beamwidth = 2 * np.abs(np.degrees(theta[np.argmin(np.abs(beam_pattern - 0.5))]))
        updated_antenna_config['params']['beamwidth'] = beamwidth
        updated_antenna_config['params']['num_elem'] = num_elem
        
    else:
        raise KeyError(f"Unknown antenna type of {antenna_config['type']} specified!")
    
    return beam_pattern, theta, updated_antenna_config