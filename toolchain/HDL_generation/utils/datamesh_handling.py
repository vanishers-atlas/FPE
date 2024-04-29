# Make sure is FPE discoverable
if __name__ == "__main__":
    import sys
    path = __file__.split("\\")
    levels_below_FPE = path[::-1].index("FPE") + 1
    sys.path.append("\\".join(path[:-levels_below_FPE]))

import copy

from FPE.toolchain import utils as tc_utils

from FPE.toolchain.HDL_generation.utils.controls_handling import *
from FPE.toolchain.HDL_generation.utils.connection_handling import *
from FPE.toolchain.HDL_generation.utils.indented_string import IndentedString

from FPE.toolchain.HDL_generation.basic import mux

# The DataMesh Class is meant to absertact away the details of inter-component bus networks
# To do thise the bus(es) are abserted into 3 parts: drivers, channels. and sinks,
# drivers and sinks can be though of as the input and outputs of the mesh,
# a channels as bridges between drivers and sinks.
# when adding a driver/sink, one most also provide which instruction, and stage it using pipelining,
# this connection exist for; For any instruction only one driver by be connected to each channel,
# and only one channel be connect to each sink.
# Note when using a pipelined DataMesh that stage of all connected drivers, channels, and sinks most match


class DataMesh():
    def __init__(this, pipelined=True):
        this._pipelined = pipelined
        this._channel_stages = {}
        this._channel_drivers = {}
        this._channel_sinks = {}

    def _dump(this, preface):
        print(preface, "pipelined : ", this._pipelined)
        for channel in this.get_all_channels():
            print()
            print(preface, "channel : ", channel)
            print(preface, "Stage : ", this._channel_stages[channel])
            print(preface, "Drivers")
            this._channel_drivers[channel]._dump(preface + ">")
            print(preface, "Sinks")
            this._channel_sinks[channel]._dump(preface + ">")


    def compute_datapaths(this):
        data_paths = {}

        for channel in this.get_all_channels():
            channel_stage = this.get_channel_stage(channel)
            for condition, sink in this.get_all_sinks(channel).get_connections():
                # Connect sink and driver details
                sink_name = sink.end()
                sink_padding = sink.padding_type()
                sink_width = sink.width()

                driver = this.get_driver_connection(channel, condition)
                if driver == None:
                    raise ValueError("Incomplete Datamesh, missing a driver for channel, %s, under condition, %s"%(channel, condition, ) )
                driver_name = driver.end()
                driver_padding = driver.padding_type()
                driver_width = driver.width()

                if driver_padding != sink_padding:
                    raise ValueError("Trying to connect driver and sink with different padding_types, %s & %s"%(driver_padding, sink_padding) )

                if sink_name not in data_paths.keys():
                    data_paths[sink_name] = SwitchedConnection(sink_name, stage=channel_stage, fixed_width=sink_width)
                data_paths[sink_name].add_connection(driver_name, condition, driver_width, driver_padding)
                assert data_paths[sink_name]._fixed_width == sink_width

        return data_paths


    def merge(this, that):
        merged =  copy.deepcopy(this)
        try:
            for channel in that.get_all_channels():
                channal_stage = that.get_channel_stage(channel)

                # copy across channel drivers
                drivers = that.get_all_drivers(channel)
                merged.merge_drivers(drivers, channel, stage=channal_stage, inplace_channel=True)

                # copy across channel sinks
                sinks = that.get_all_sinks(channel)
                merged.merge_sinks(sinks, channel, stage=channal_stage, inplace_channel=True)
        except Exception as e:
            print()
            print("THIS")
            this._dump("")

            print()
            print("THAT")
            that._dump("")
            print()

            raise e

        return merged


    # Channel handling, note a channel must be declared before being driven or sunk
    def get_all_channels(this):
        return this._channel_stages.keys()

    def get_channel_stage(this, channel_name):
        return this._channel_stages[channel_name]


    def declare_channel(this, channel_name, stage=None):
        assert this._pipelined and type(stage) == str, "In a pipelined DataMesh stage must be a str"
        assert this._pipelined or stage == None, "In a non=pipelined DataMesh stage must be left as None"

        assert type(channel_name) == str

        if channel_name in this.get_all_channels():
            raise KeyError("Trying to declare an already existing channel")
        else:
            this._channel_stages [channel_name] = stage
            this._channel_drivers[channel_name] = SwitchedConnection(channel_name, stage=stage)
            this._channel_sinks  [channel_name] = SwitchedConnection(channel_name, stage=stage)


    # Driver handling
    def get_driver(this, channel, condition):
        assert type(channel) == str
        assert type(condition) == str

        try:
            return this._channel_drivers[channel].get_connection(condition).end()
        except AttributeError:
            return None
        except KeyError:
            raise KeyError("Trying to get a driver for an undeclaced channel, " + channel)

    def get_driver_connection(this, channel, condition):
        assert type(channel) == str
        assert type(condition) == str

        try:
            return this._channel_drivers[channel].get_connection(condition)
        except KeyError:
            raise KeyError("Trying to get a driver connection for an undeclaced channel, " + channel)

    def get_all_drivers(this, channel):
        assert type(channel) == str

        try:
            return this._channel_drivers[channel]
        except KeyError:
            raise KeyError("Trying to get all drivers for an undeclaced channel, " + channel)


    def connect_driver(this, driver, channel, condition, stage=None, padding_type=None, width=None, inplace_channel=False):
        assert this._pipelined and type(stage) == str, "In a pipelined DataMesh stage must be a str"
        assert this._pipelined or stage == None, "In a non=pipelined DataMesh stage must be left as None"

        assert type(driver) == str
        assert type(channel) == str
        assert type(condition) == str

        # Channel checks
        try:
            if this.get_channel_stage(channel) != stage:
                raise ValueError("Channel's declared stage, %s, does not match driver's given stage, %s"%(this.channels[channel], stage) )
        except KeyError:
            if inplace_channel:
                this.declare_channel(channel, stage)
            else:
                raise ValueError("trying to connect driver to an undeclared channel, %s"%(channel, ) )

        # Condition checks
        if this.get_driver(channel, condition) != None:
            raise ValueError("trying to connect driver to to a channel, %s, that's already driven for that condition, %s"%(channel, condition, ) )

        # Update internal data structure
        this._channel_drivers[channel].add_connection(driver, condition, width, padding_type)

    def merge_drivers(this, drivers, channel, stage=None, inplace_channel=False):
        assert this._pipelined and type(stage) == str, "In a pipelined DataMesh stage must be a str"
        assert this._pipelined or stage == None, "In a non=pipelined DataMesh stage must be left as None"

        assert type(drivers) == SwitchedConnection
        assert type(channel) == str

        # Channel checks
        try:
            if this.get_channel_stage(channel) != stage:
                raise ValueError("Error with channel, %s: declared stage, %s, does not match drivers' given stage, %s"%(channel, this.get_channel_stage(channel), stage) )
        except KeyError:
            if inplace_channel:
                this.declare_channel(channel, stage)
            else:
                raise ValueError("Error with channel, %s: trying to merge drivers to an undeclared channel"%(channel, ) )

        # Update internal data structure
        this._channel_drivers[channel] = this._channel_drivers[channel].merge(drivers)


    # Sink handling
    def get_sink(this, channel, condition):
        assert type(channel) == str
        assert type(condition) == str

        try:
            return this._channel_sinks[channel].get_connection(condition).end()
        except AttributeError:
            return None
        except KeyError:
            raise KeyError("Trying to get a sink for an undeclaced channel, " + channel)

    def get_sink_connection(this, channel, condition):
        assert type(channel) == str
        assert type(condition) == str

        try:
            return this._channel_sinks[channel].get_connection(condition)
        except KeyError:
            raise KeyError("Trying to get a driver connection for an undeclaced channel, " + channel)


    def get_all_sinks(this, channel):
        assert type(channel) == str

        try:
            return this._channel_sinks[channel]
        except  KeyError:
            raise KeyError("Trying to get all sinks for an undeclaced channel, " + channel)


    def connect_sink(this, sink, channel, condition, stage=None, padding_type=None, width=None, inplace_channel=False):
        assert this._pipelined and type(stage) == str, "In a pipelined DataMesh stage must be a str"
        assert this._pipelined or stage == None, "In a non=pipelined DataMesh stage must be left as None"

        assert type(sink) == str
        assert type(channel) == str
        assert type(condition) == str

        try:
            if this.get_channel_stage(channel) != stage:
                raise ValueError("Channel's declared stage, %s, does not match sink's given stage, %s"%(this.channels[channel], stage) )
        except KeyError:
            if inplace_channel:
                this.declare_channel(channel, stage)
            else:
                raise ValueError("trying to connect sink to an undeclared channel, %s"%(channel, ) )

        # Condition checks
        if this.get_sink(channel, condition) != None:
            raise ValueError("trying to connect driver to to a channel, %s, that's already driven for that condition, %s"%(channel, condition, ) )

        # Update internal data structure
        this._channel_sinks[channel].add_connection(sink, condition, width, padding_type)

    def merge_sinks(this, sinks, channel, stage=None, inplace_channel=False):
        assert this._pipelined and type(stage) == str, "In a pipelined DataMesh stage must be a str"
        assert this._pipelined or stage == None, "In a non=pipelined DataMesh stage must be left as None"

        assert type(sinks) == SwitchedConnection
        assert type(channel) == str

        # Channel checks
        try:
            if this.get_channel_stage(channel) != stage:
                raise ValueError("Channel's declared stage, %s, does not match sinks' given stage, %s"%(this.channels[channel], stage) )
        except KeyError:
            if inplace_channel:
                this.declare_channel(channel, stage)
            else:
                raise ValueError("trying to merge sinks to an undeclared channel, %s"%(channel, ) )

        # Update internal data structure
        this._channel_sinks[channel] = this._channel_sinks[channel].merge(sinks)



class SwitchedConnection():
    def __init__(this, fixed_end, stage=None, fixed_width=None):
        assert type(fixed_end) == str
        this._fixed = fixed_end

        assert stage == None or type(stage) == str
        this._stage = stage

        assert fixed_width == None or type(fixed_width) == int and fixed_width > 0
        this._fixed_width = fixed_width

        this._switched = {}


    def _dump(this, preface=""):
        print(preface, this._fixed, this._stage)
        for k, v in this._switched.items():
            print(preface, k)
            v._dump(preface+">")


    def get_stage(this):
        return this._stage


    def get_fixed_end(this):
        return this._fixed

    def get_fixed_width(this):
        return this._fixed_width


    def get_connection(this, condition):
        try:
            return this._switched[condition]
        except KeyError:
            return None

    def get_connections(this):
        return this._switched.items()


    def add_connection(this, switched_end, condition, width=None, padding_type=None):
        assert width == None or type(width) == int and width > 0, "width must be either None, for simple singals, or a natural number, for data signals"
        assert width == None or type(padding_type) == str, "When width exists, padding_type must be a str naming how to handle padding"

        assert (width == None and padding_type == None) or (width != None and padding_type != None), "When width is none, a simple signal, padding_type should also be None"

        assert type(switched_end) == str
        assert type(condition) == str

        connection = this.get_connection(condition)
        if connection == None:
            # No driver so safe to drive
            this._switched[condition] = ConnectionDetails(switched_end, width=width, padding_type=padding_type)
        elif connection.same(ConnectionDetails(switched_end, width=width, padding_type=padding_type)):
            # Existing driver is the same as the one be connected as left existing one
            pass
        else:
            print()
            print(this._fixed, condition, switched_end, width, padding_type)
            connection._dump("")
            exit()
            
            # Existing driver and the one be connected don't mathc, therefore raise error
            raise ValueError("Can't add a connection for an already connected condition, " + condition)


    def merge(this, that):
        if this.get_stage() != that.get_stage():
            raise ValueError("Can't merge SwitchedConnections with different stages: %s & %s given"%(this.get_stage(), that.get_stage(), ) )
        if this.get_fixed_end() != that.get_fixed_end():
            raise ValueError("Can't merge SwitchedConnections with different fixed ends: %s & %s given"%(this.get_fixed_end(), that.get_fixed_end(), ) )

        merged = copy.deepcopy(this)
        for condition, details in that.get_connections():
            merged.add_connection(details.end(), condition, width= details.width(), padding_type=details.padding_type())

        return merged

class ConnectionDetails():
    def __init__(this, end, width=None, padding_type=None):
        assert type(end) == str

        assert width == None or type(width) == int
        assert padding_type == None or type(padding_type) == str
        assert (padding_type == None) == (width == None)

        this._end = end
        this._width = width
        this._padding_type = padding_type

    def _dump(this, preface=""):
        print(preface, this._end,  str(this._width), this._padding_type )


    def end(this):
        return this._end

    def width(this):
        return this._width

    def padding_type(this):
        return this._padding_type


    def same(this, that):
        if this._end != that._end:
            return False
        if this._padding_type != that._padding_type:
            return False
        if this._width != that._width:
            return False

        return True
