#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sort MRM_SCAN_INFO messages [1] from PulsON 440 taking into account dropped and out-of-order 
messages/packets.
"""

__author__ = 'Ramamurthy Bhagavatula Mason Mitchell, Winston Liu'
__version__ = '1.0'
__maintainer__ = 'Ramamurthy Bhagavatula'
__email__ = 'ramamurthy.bhagavatula@ll.mit.edu'

"""References
[1] Monostatic Radar Application Programming Interface (API) Specification
    PulsON (R) 400 Series
    Version: 1.2.2
    Date: January 2015
    https://timedomain.com/wp-content/uploads/2015/12/320-0298E-MRM-API-Specification.pdf
    
[2] https://numpy.org/doc/stable/reference/generated/numpy.argsort.html
"""


# Import required modules and methods
import numpy as np

# Constants
MAX_MESSAGE_ID = 2**16 - 1


def sort_scan_msgs(msg_ids, timestamps, msg_idxs, num_msgs_total):
    """Sort MRM_SCAN_INFO messages, taking into account dropped messages and message ID wrapping.
    
    Args:
        msg_ids (array-like)
            In order received (i.e., not sorted), message IDs parsed from MRM_SCAN_INFO messages; 
            field #1 of MRM_SCAN_INFO packet definition [1].
            
        timestamps (array-like)
            In order received (i.e., not sorted), timestamps parsed from MRM_SCAN_INFO messages;
            field 3 of MRM_SCAN_INFO packet definition [1].
            
        msg_idxs (array-like)
            In order received (i.e., not sorted), message indices parsed from MRM_SCAN_INFO 
            messages; field 17 (note typo, repeat 11, in API numbering) of MRM_SCAN_INFO packet 
            definition [1].
            
        num_msgs_total (int)
            Total number of MRM_SCAN_INFO messages used to provide an (singular) scan; should be the 
            same for all MRM_SCAN_INFO messages generated from MRM_CONTROL_REQUEST and can thus be
            parsed from a single MRM_SCAN_INFO belonging to said request; field 19 of MRM_SCAN_INFO
            packet definition [1].
            
    Returns:
        msg_sort_idxs (ndarray)
            The index array that sort the MRM_SCAN_INFO messages into intended order; format/use is 
            the same as index array returned by numpy.argsort [2].
            
        unwrap_msg_ids (ndarray)
            Message IDs, in order received, unwrapped such that no longer overflow when they exceed 
            2**16 - 1. Useful for disambiguating multiple messages sharing the same wrapped message 
            ID. In order to go back to wrapped (i.e., as transmitted) message IDs, take the modulo 
            of each unwrapped message ID by 2**16 - 1.
            
        unwrap_missing_msg_ids (ndarray)
            Message IDs, in order expected, of messages that are missing. In combination with 
            'unwrap_msg_ids', useful for disambiguating multiple messages sharing the same wrapped 
            message ID of which one or more have been dropped. In order to go back to wrapped (i.e., 
            as transmitted) message IDs, take the modulo of each unwrapped message ID by 2**16 - 1.
    """
    # Convert all input array-likes to ndarrays
    msg_ids = np.asarray(msg_ids)
    timestamps = np.asarray(timestamps)
    msg_idxs = np.asarray(msg_idxs)
    
    # Sort messages by timestamp and then per-scan message index 
    msg_sort_idx = np.lexsort((msg_idxs, timestamps))
    msg_reverse_sort_idx = np.argsort(msg_sort_idx)
    sorted_msg_ids = np.take_along_axis(msg_ids, msg_sort_idx, axis=None)
    
    # Account for message ID wrapping
    msg_ids_diff = np.diff(sorted_msg_ids)
    msg_ids_diff[np.nonzero(msg_ids_diff > 0)] = 0
    msg_ids_diff[np.nonzero(msg_ids_diff < 0)] = 1
    msg_ids_diff = np.insert(msg_ids_diff, 0, 0)
    msg_ids_wrap_offset = np.cumsum(msg_ids_diff) * (MAX_MESSAGE_ID + 1)
    sorted_unwrap_msg_ids = sorted_msg_ids + msg_ids_wrap_offset
    unwrap_msg_ids = np.take_along_axis(sorted_unwrap_msg_ids, msg_reverse_sort_idx, axis=None)
    
    # Compute expected first and last unwrapped message IDs and the expected overall number of 
    # messages assuming no missing/dropped messages
    exp_first_unwrap_msg_id = sorted_unwrap_msg_ids[0] - msg_idxs[msg_sort_idx[0]]
    exp_last_unwrap_msg_id = \
        num_msgs_total - 1 - msg_idxs[msg_sort_idx[-1]] + sorted_unwrap_msg_ids[-1]
    exp_num_msgs = exp_last_unwrap_msg_id - exp_first_unwrap_msg_id + 1
    
    # Determine unwrapped message IDs of missing/dropped messages
    exp_unwrap_msg_ids = np.arange(exp_num_msgs) + exp_first_unwrap_msg_id
    unwrap_missing_msg_ids = np.setdiff1d(exp_unwrap_msg_ids, sorted_unwrap_msg_ids)
    
    return msg_sort_idx, unwrap_msg_ids, unwrap_missing_msg_ids