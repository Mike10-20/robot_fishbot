#include "plugin_study/spin_motion_control.hpp"
#include <iostream>
using namespace std;
namespace motion_control{
    void Spincontrol::start()
    {
        cout<<"spin_start"<<endl;
    }
    void Spincontrol::end()
    {
        cout<<"spin_end"<<endl;
    }
}
#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(motion_control::Spincontrol,motion_control::Motioncontrol)