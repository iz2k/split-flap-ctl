/*
 * hall-sensor.c
 *
 *  Created on: 12 ago. 2020
 *      Author: Ibon Zalbide
 */
#include <msp430.h>
#include <typedefs.h>
#include <constants.h>
#include <global_variables.h>
#include <drivers/hall-sensor.h>
#include <drivers/filter.h>

float hall_filter=0;
float max_val=0;
bool detection_done = true;

// Returns true when detection is positive
bool hall_sense()
{
    // Add new value to filter
    hall_filter = filter(hall_filter, hall_val, 0.1);

    // Reset detection when far from magnet
    if(hall_filter==0)
    {
        max_val = 0;
        detection_done=false;
    }

    // Find max value
    if (hall_filter > max_val)
    {
        max_val = hall_filter;
    }

    // Check if detection is not done
    if(detection_done == false)
    {
        // Check value falling below max
        if (hall_filter < max_val - reg_hall_threshold)
        {
            // Current detection ends
            detection_done=true;
            return true;
        }
    }

    return false;
}
