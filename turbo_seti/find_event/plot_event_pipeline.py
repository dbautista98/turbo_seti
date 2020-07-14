#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:31:11 2020

Part of the Breakthrough Listen software package turboSETI

Front-facing script to plot drifting, narrowband events in a set of generalized 
cadences of ON-OFF radio SETI observations.

The main function contained in this file is *plot_event_pipeline*
    Plot_event_pipeline calls plot_candidate_events from plot_events.py to 
    plot the events in an output .csv file generated by find_event_pipeline.py
    
Usage (beta):
    import plot_event_pipeline;
    plot_event_pipeline.plot_event_pipeline(event_csv_string, 
                                            fils_list_string,
                                            user_validation=False
                                            offset=0)
    
    event_csv_string   The string name of a .csv file that contains the  
                        list of events at a given filter level, created as 
                        output from find_event_pipeline.py. The 
                        .csv should have a filename containing information
                        about its parameters, for example
                        "kepler1093b_0015_f2_snr10.csv"
                        Remember that the file was created with some cadence
                        (ex. ABACAD) and ensure that the cadence matches the
                        order of the files in fils_list_string
                        
    fils_list_string    The string name of a plaintext file ending in .lst 
                        that contains the filenames of .fil files, each on a 
                        new line, that corresponds to the cadence used to
                        create the .csv file used for event_csv_string.
                   
                        
    user_validation     A True/False flag that, when set to True, asks if the
                        user wishes to continue with their input parameters
                        (and requires a 'y' or 'n' typed as confirmation)
                        before beginning to run the program. Recommended when
                        first learning the program, not recommended for 
                        automated scripts.
    
    offset              The amount that the overdrawn "best guess" line from
                        the event parameters in the csv should be shifted from
                        its original position to enhance readability. Can be
                        set to 0 (default; draws line on top of estimated
                        event) or 'auto' (shifts line to the left by an auto-
                        calculated amount, with addition lines showing original
                        position).

author: 
    Version 2.0 - Sofia Sheikh (ssheikhmsa@gmail.com), 
    Version 1.0 - Emilio Enriquez (jeenriquez@gmail.com)
    
Last updated: 05/24/2020

"""

from . import plot_event
import pandas


def plot_event_pipeline(event_csv_string, 
                        fils_list_string,  
                        user_validation=False,
                        offset=0):
    
    # reading in the .csv containing the events
    candidate_event_dataframe = pandas.read_csv(event_csv_string)
    
    # reading in the list of .fil files
    fil_file_list = []
    for file in pandas.read_csv(fils_list_string, encoding='utf-8', header=None, chunksize=1):
        fil_file_list.append(file.iloc[0,0])  
        
    # obtaining source names
    source_name_list = []
    for fil in fil_file_list:
        source_name = fil.split('_')[5] 
        source_name_list.append(source_name)
     
    # get rid of bytestring "B'"s if they're there (early versions of
    # seti_event.py added "B'"s to all of the source names)
    on_source_name_original = candidate_event_dataframe.Source[0]
    if on_source_name_original[0] == 'B' and on_source_name_original[-1] == '\'':
        on_source_name = on_source_name_original[2:-2]   
    else:
        on_source_name = on_source_name_original
    candidate_event_dataframe = candidate_event_dataframe.replace(to_replace=on_source_name_original,
                                           value=on_source_name)
        
    # take filter-level information from the .csv filename
    filter_level = event_csv_string.split('_')[2] 

    # begin user validation
    print("Plotting some events for: ", on_source_name)
    print("There are " + str(len(candidate_event_dataframe.Source)) + " total events in the csv file " + event_csv_string)
    print("therefore, you are about to make " + str(len(candidate_event_dataframe.Source)) + " .png files.")
    
    if user_validation == True:
        question = "Do you wish to proceed with these settings?"
        while "the answer is invalid":
            reply = str(input(question+' (y/n): ')).lower().strip()
            if reply == '':
                return
            if reply[0] == 'y':
                break
            if reply[0] == 'n':
                return

    # move to plot_event.py for the actual plotting
    plot_event.plot_candidate_events(candidate_event_dataframe, 
                                     fil_file_list,
                                     filter_level,
                                     source_name_list,
                                     offset=offset)
    return