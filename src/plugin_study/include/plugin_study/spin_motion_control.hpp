#pragma once
#include "plugin_study/motion_control_interface.hpp"
namespace motion_control{
    class Spincontrol:public Motioncontrol
    {
        public:
            void start();
            void end();
    };
}