#include "task.h"




bool celsius_in_sensor_range(double celsius){
    
    return (celsius < -40.0 || celsius > 125.0 || !isfinite(celsius))? false: true;
}



bool celsius_to_milli(double celsius, int32_t *out_milli_celsius){
    if(out_milli_celsius==NULL || !isfinite(celsius)) return false;
    int64_t result = 0;
    if(celsius < 0){
        result = (celsius*1000) - 0.5;
        if (result < INT32_MIN) return false;
    } else {
        result = (celsius*1000) + 0.5;
        if (result > INT32_MAX) return false;
    }

    *out_milli_celsius = (int32_t)result;
    return true;
}





bool telemetry_prepare(double celsius, bool sensor_fault, int32_t *out_milli_celsius){
    bool temp_in_range = celsius_in_sensor_range(celsius);
    if(sensor_fault || out_milli_celsius==NULL || !temp_in_range) return false;
    return celsius_to_milli(celsius,out_milli_celsius);
}


