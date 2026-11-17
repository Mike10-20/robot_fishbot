#ifndef MOTION
#define MOTION
namespace motion_control{
    class Motioncontrol
    {
    public:
        virtual void start() = 0;
        virtual void end() = 0;
    };
}
#endif