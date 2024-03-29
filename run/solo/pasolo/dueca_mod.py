## -*-python-*-
## this is an example dueca_mod.py file, for you to start out with and adapt
## according to your needs. Note that you need a dueca_mod.py file only for the
## node with number 0

## in general, it is a good idea to clearly document your set up
## this is an excellent place.

## node set-up
ecs_node = 0   # dutmms1, send order 3
#aux_node = 1   # dutmms3, send order 1
#pfd_node = 2   # dutmms5, send order 2
#cl_node = 3    # dutmms4, send order 0

## priority set-up
# normal nodes: 0 administration
#               1 simulation, unpackers
#               2 communication
#               3 ticker

# administration priority. Run the interface and logging here
admin_priority = dueca.PrioritySpec(0, 0)

# priority of simulation, just above adiminstration
sim_priority = dueca.PrioritySpec(1, 0)

# nodes with a different priority scheme
# control loading node has 0, 1 and 2 as above and furthermore
#               3 stick priority
#               4 ticker priority
# priority of the stick. Higher than prio of communication
# stick_priority = dueca.PrioritySpec(3, 0)

# timing set-up
# timing of the stick calculations. Assuming 100 usec ticks, this gives 2500 Hz
# stick_timing = dueca.TimeSpec(0, 4)

# this is normally 100, giving 100 Hz timing
sim_timing = dueca.TimeSpec(0, 100)

## for now, display on 50 Hz
display_timing = dueca.TimeSpec(0, 200)

## log a bit more economical, 25 Hz
log_timing = dueca.TimeSpec(0, 400)

## ---------------------------------------------------------------------
### the modules needed for dueca itself
if this_node_id == ecs_node:

    # create a list of modules:
    DUECA_mods = []
    DUECA_mods.append(dueca.Module("dusime", "", admin_priority))
    DUECA_mods.append(dueca.Module("dueca-view", "", admin_priority))
    DUECA_mods.append(dueca.Module("activity-view", "", admin_priority))
    DUECA_mods.append(dueca.Module("timing-view", "", admin_priority))
    DUECA_mods.append(dueca.Module("log-view", "", admin_priority))
    DUECA_mods.append(dueca.Module("channel-view", "", admin_priority))

    # create the entity with that list
    DUECA_entity = dueca.Entity("dueca", DUECA_mods)

## ---------------------------------------------------------------------
# modules for your project (example)
mymods = []

if this_node_id == ecs_node:
    mymods.append(dueca.Module(
        "motion-control", "", admin_priority).param(
            ('set_timing', display_timing),
            ('check_timing', (10000, 20000)),
            #('add-fixed-sound', "rpm1left"),
            #('add-fixed-sound', "rpm1right"),
            #('add-fixed-sound', "gearup"),
            #('event-interval', 500),
            #('add-fixed-sound', "geardown"),
            #('event-interval', 530),
        ))

    mymods.append(dueca.Module(
        'world-listener', "", sim_priority).param(
            ('set-timing', display_timing),
            ('check-timing', (10000, 20000)),
            ('control-logger', "HDFLogConfig://ph-sound"),
            ('set-listener',
             dueca.PortAudioListener().param(
                 ('set-devicename',
                  "Logitech Stereo H650e: USB Audio (hw:3,0)"),

                 # old style hacks, link to the label
                 # ('add-controlled-static-sound', (
                 #     "rpm1left", "PA34_rpm1_left.wav")),
                 # ( 'set-coordinates', ( 0, 1.0 )),

                 # ('add-controlled-static-sound', (
                 #     "rpm1right", "PA34_rpm1_right.wav")),
                 # ('set-coordinates', ( 1, 1.0)),

                 # new style, use factory, and let type+label be key
                 ('add-object-class-data', (
                     "AudioObjectFixed:gearup", "", "PortAudioObjectFixed",
                     "PA34_gear_up.wav")),
                 ('add-object-class-coordinates', (0, 0.07)),
                 ('add-object-class-data', (
                     "AudioObjectFixed:geardown", "", "PortAudioObjectFixed",
                     "PA34_gear_down.wav")),
                 ('add-object-class-coordinates', (1, 0.07)),
                 ('add-object-class-data', (
                     "AudioObjectFixed:gearmulti", "", "PortAudioMultiObject",
                     "PA34_gear_down.wav",
                     "AudioFileSelection://ph-sound")),
                 ('add-object-class-coordinates', (0.1, 0.1)),

             ).complete()),
            ('keep-running', False),
        ))

    mymods.append(dueca.Module(
        "audio-test-gui", "", admin_priority).param(
            ("add-control",
             ("left-channel", "AnyAudioClass://audio", "gearup")),
            ("add-control",
             ("right-channel", "AnyAudioClass://audio", "geardown")),
            ("add-control",
             ("both-channel", "AnyAudioClass://audio", "gearmulti",
              "AudioFileSelection://ph-sound"))
            ))

# etc, each node can have modules in its mymods list

# then combine in an entity (one "copy" per node)
if mymods:
    myentity = dueca.Entity("ph-sound", mymods)
