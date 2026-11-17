#include "plugin_study/motion_control_interface.hpp"
#include "pluginlib/class_loader.hpp"
int main(int argc,char **argv)
{
    (void)argc;
    (void)argv;

    pluginlib::ClassLoader<motion_control::Motioncontrol> loader("plugin_study","motion_control::Motioncontrol");
    // motion_control::Motioncontrol* controller = loader.createClassInstance("motion_control::Spincontrol");
    motion_control::Motioncontrol* controller = loader.createClassInstance("Spincontrol");

    controller->start();
    controller->end();
    return 0;
}