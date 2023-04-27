import warnings
import copy

from FPE.toolchain import utils as tc_utils

from .controls_handling import *
from .connection_handling import *
from .indented_string import IndentedString

from FPE.toolchain.HDL_generation.basic import mux

class DataFlow():
    def __init__(this):
        this.vbuses = {}
        this.endpoints = {}

    def get_all_vbuses(this):
        return this.vbuses

    def get_vbus(this, vbus_name):
        assert type(vbus_name) == str

        try:
            return this.vbuses[vbus_name]
        except KeyError:
            return None

    def add_vbus(this, vbus_name, vbus, overwrite=False):
        assert type(vbus_name) == str
        assert type(vbus) == DriverMap
        assert type(overwrite) == bool

        if (not overwrite) and this.get_vbus(vbus_name) != None:
            raise ValueError("Can't add a vbys using a -pre-exist vbus_name, " + vbus_name)

        this.vbuses[vbus_name] = vbus

    def drive_vbus(this, vbus_name, instr, driving_signal, stage, padding_type, width=None):
        assert type(vbus_name) == str
        assert type(instr) == str
        assert type(driving_signal) == str
        assert type(stage) == str
        assert type(padding_type) == str
        assert type(width) == int

        vbus = this.get_vbus(vbus_name)
        if vbus == None:
            vbus = DriverMap(stage)
            this.add_vbus(vbus_name, vbus)

        vbus.add_driver(instr, driving_signal, stage, padding_type, width)

    def get_all_endpoints(this):
        return this.endpoints

    def get_endpoint(this, endpoint_name):
        assert type(endpoint_name) == str

        try:
            return this.endpoints[endpoint_name]
        except KeyError:
            return None

    def add_endpoint(this, endpoint_name, endpoint, overwrite=False):
        assert type(endpoint_name) == str
        assert type(endpoint) == DriverMap
        assert type(overwrite) == bool

        if (not overwrite) and this.get_endpoint(endpoint_name) != None:
            raise ValueError("Can't add a vbys using a -pre-exist vbus_name, " + endpoint_name)

        this.endpoints[endpoint_name] = endpoint

    def connectEndPoint(this, endpoint_name, instr, vbus_name, stage, padding_type, width=None):
        assert type(endpoint_name) == str
        assert type(instr) == str
        assert type(vbus_name) == str
        assert type(stage) == str
        assert type(padding_type) == str
        assert type(width) == int

        endpoint = this.get_endpoint(endpoint_name)
        if endpoint == None:
            endpoint = DriverMap(stage)
            this.add_endpoint(endpoint_name, endpoint)

        endpoint.add_driver(instr, vbus_name, stage, padding_type, width)

    def merge(A, B):
        assert type(A) == DataFlow
        assert type(B) == DataFlow

        C = copy.deepcopy(A)


        for vbus_name, vbus in B.get_all_vbuses().items():
            bus = C.get_vbus(vbus_name)
            if bus == None:
                C.add_vbus(vbus_name, vbus)
            else:
                C.add_vbus(vbus_name, bus.merge(vbus), overwrite=True)

        for endpoint_name, endpoint in B.get_all_endpoints().items():
            bus = C.get_vbus(endpoint_name)
            if bus == None:
                C.add_endpoint(endpoint_name, endpoint)
            else:
                C.add_endpoint(endpoint_name, bus.merge(endpoint), overwrite=True)

        return C

class DriverMap():
    def __init__(this, stage):
        assert type(stage) == str

        this.stage = stage

        this.drivers = {}

    def get_stage(this):
        return this.stage

    def get_all_drivers(this):
        return this.drivers

    def get_driver(this, instr):
        assert type(instr) == str

        try:
            return this.drivers[instr]
        except KeyError:
            return None

    def add_driver(this, instr, driving_signal, stage, padding_type, width):
        assert type(instr) == str
        assert type(driving_signal) == str
        assert type(stage) == str
        assert type(padding_type) == str
        assert type(width) == int

        if this.get_stage() != stage:
            raise ValueError("vbus' pre-existing stage, " + this.get_stage() + ", and added driver stage, " + stage + ", don'st match")

        if this.get_driver(instr) != None:
            raise ValueError("Can't add a drive for an already driven insttuction, " + instr)

        this.drivers[instr] = DataConnection(driving_signal, padding_type, width)

    def merge(A, B):
        assert type(A) == DriverMap
        assert type(B) == DriverMap


        if A.get_stage() != B.get_stage():
            raise ValueError("can't marge vbuses as stages don't match, " + A.get_stage() + " and " + B.get_stage() )

        C = copy.deepcopy(A)
        stage = B.get_stage()
        for instr, details in B.get_all_drivers().items():
            C.add_driver(instr, details.source, stage, details.padding_type, details.width)

        return C

class DataConnection():
    def __init__(this, source, padding_type, width):
        assert type(source) == str
        assert type(padding_type) == str
        assert type(width) == int

        this.source = source
        this.padding_type = padding_type
        this.width = width

    def __str__(this):
        return this.source + " " + this.padding_type + " " + str(this.width)


def convert_dataflow_to_muxes(dataflow, output_path, force_generation, arch_head, arch_body):
    assert type(dataflow) == DataFlow
    assert type(output_path) == str
    assert type(force_generation) == bool
    assert type(arch_head) == IndentedString
    assert type(arch_body) == IndentedString

    # Create a dereferenced map of inputs for each endpoint
    direct_connections = []
    precheck_muxed_connections = []
    for endpoint_name, endpoint in dataflow.get_all_endpoints().items():
        endpoint_stage = endpoint.get_stage()
        signal_map = MuxMap(endpoint_name, endpoint_stage)

        for instr, endpoint_connection in endpoint.get_all_drivers().items():
            vbus = dataflow.get_vbus(endpoint_connection.source)
            vbus_connection = vbus.get_driver(instr)
            vbus_stage = vbus.get_stage()

            signal_map.add_connection(instr, vbus_connection, vbus_stage, endpoint_connection, endpoint_stage)


        NUM_SOURCES = len(signal_map.get_all_sources())
        if   NUM_SOURCES == 0:
            raise ValueError("endpoint with no inputs, "%(endpoint_name, ) )
        elif NUM_SOURCES == 1:
            direct_connections.append(signal_map)
        else:
            precheck_muxed_connections.append(signal_map)

    # Handle direct connections
    arch_body += "-- Direct Connected Datapaths\n"
    for connection in direct_connections:
        src_signal = connection.get_all_sources()[0]
        connection_details = connection.get_connection_detail(src_signal)
        for dst_signal in connection.get_dests():
            arch_body += "%s <= %s;\n\n"%(dst_signal, connect_signals(src_signal, connection_details["vbus_width"], connection_details["endpoint_width"], connection_details["padding_type"]), )

    # Add mux sharing checks here
    muxed_connections = []
    for candidate in precheck_muxed_connections:
        match_not_found = True
        for referance in muxed_connections:
            if candidate.equivalent(referance):
                referance.add_dests(candidate.get_dests())
                match_not_found = False
                break
        if match_not_found:
            muxed_connections.append(candidate)


    # Handle muxed connections
    controls = init_controls()
    arch_body += "-- Muxed Datapaths\n"
    for connection in muxed_connections:
        # Generate mux component
        mux_interface, mux_name = mux.generate_HDL(
            {
                "inputs"  : len(connection.get_all_sources()),
            },
            output_path,
            module_name=None,
            concat_naming=False,
            force_generation=force_generation
        )

        # Instaniate Mux, while generating control sel_signal
        dst_signal = connection.get_dests()[0]
        dst_width = connection.get_connection_detail(connection.get_all_sources()[0])["endpoint_width"]

        control_signal = dst_signal + "_mux_sel"
        control_width = mux_interface["sel_width"]

        control_values = {}

        arch_head += "signal %s : std_logic_vector(%i downto 0);\n"%(control_signal, control_width - 1, )
        arch_head += "signal %s_mux_out : std_logic_vector(%i downto 0);\n"%(dst_signal, dst_width - 1, )

        arch_body += "%s_mux : entity work.%s(arch)\>\n"%(dst_signal, mux_name, )

        arch_body += "generic map (data_width => %i)\n"%(dst_width, )

        arch_body += "port map (\n\>"
        arch_body += "sel =>  %s,\n"%(control_signal, )

        for sel_value, src_signal in enumerate(connection.get_all_sources()):
            connection_details = connection.get_connection_detail(src_signal)

            control_value = tc_utils.unsigned.encode(sel_value, control_width)
            control_values[control_value] = connection_details["instrs"]

            arch_body += "data_in_%i => %s,\n"%(
                sel_value,
                connect_signals(src_signal, connection_details["vbus_width"], connection_details["endpoint_width"], connection_details["padding_type"]),
            )

        for sel_value in range(len(connection.get_all_sources()), mux_interface["number_inputs"]):
            arch_body += "data_in_%i => (others => '0'),\n"%(sel_value, )

        arch_body += "data_out => %s_mux_out\n"%(dst_signal)

        arch_body += "\<);\n\<\n"

        source_signal = connection.get_dests()[0]
        for dst_signal in connection.get_dests():
             arch_body += "%s <= %s_mux_out;\n"%(dst_signal, source_signal, )
        arch_body += "\n"

        # Default any inused instrs to all 0
        add_control(controls, connection.get_stage(), control_signal, control_values, "std_logic_vector", control_width)

    return controls, arch_head, arch_body

class MuxMap():
    def __init__(this, dest, stage):
        assert type(dest) == str
        assert type(stage) == str

        this.dests = [dest, ]
        this.stage = stage

        this.connections = {}

    def get_stage(this):
        return this.stage

    def add_dests(this, dests):
        assert type(dests) == list
        if __debug__:
            for dest in dests:
                assert type(dest) == str

        this.dests = this.dests + dests


    def get_dests(this):
        return this.dests

    def get_all_sources(this):
        return list(this.connections.keys())

    def get_connection_detail(this, source):
        try:
            return this.connections[source]
        except KeyError:
            return None

    def add_connection(this, instr, vbus_connection, vbus_stage, endpoint_connection, endpoint_stage):
        assert type(instr) == str
        assert type(vbus_connection) == DataConnection
        assert type(endpoint_connection) == DataConnection

        if vbus_connection.padding_type != endpoint_connection.padding_type:
            raise ValueError("vbus and endpoint's padding_types don't match, " + vbus_connection.padding_type + " and " + endpoint_connection.padding_type)

        if vbus_stage != this.get_stage():
            raise ValueError("vbus stage don't match MuxMap's stage, " + vbus_stage + " and " + this.get_stage())
        if endpoint_stage != this.get_stage():
            raise ValueError("endpoint stage don't match MuxMap's stage, " + endpoint_stage + " and " + this.get_stage())

        try:
            this.connections[vbus_connection.source]["instrs"].append(instr)
        except KeyError:
            this.connections[vbus_connection.source] = {
                "vbus_width" : vbus_connection.width,
                "endpoint_width" : endpoint_connection.width,
                "padding_type" : vbus_connection.padding_type,
                "instrs" : [instr, ],
            }

    def equivalent(A, B):
        # Check stages
        if A.get_stage() != B.get_stage():
            return False

        # Check sources
        if sorted(A.get_all_sources()) != sorted(B.get_all_sources()):
            return False

        # Check source details
        for source in A.get_all_sources():
            A_details = A.get_connection_detail(source)
            B_details = B.get_connection_detail(source)

            if A_details["vbus_width"] != B_details["vbus_width"]:
                return False

            if A_details["endpoint_width"] != B_details["endpoint_width"]:
                return False

            if A_details["padding_type"] != B_details["padding_type"]:
                return False

            if sorted(A_details["instrs"]) != sorted(B_details["instrs"]):
                return False

        return True


    def __str__(this):
        string = " ".join(this.dests) + "\n"
        for instr, connection in this.connections.items():
            string += instr + " " + str(connection["vbus_width"]) + " " + str(connection["endpoint_width"]) + " " + connection["padding_type"] + " " + str(connection["instrs"]) + "\n"
        return string

########################################################################################################
#                                         Deprecated Functions                                         #
########################################################################################################

def init_datapaths():
    warnings.warn("Use of stand alone functions is deprecated, instead please DataFlow, DriverMap, and DataConnection classes")

    return DataFlow()


def add_datapath_source(datapath, meta_signal, stage, instr, signal, padding_type, width=None):
    warnings.warn("Use of stand alone functions is deprecated, instead please DataFlow, DriverMap, and DataConnection classes")

    assert type(datapath) == DataFlow
    assert type(meta_signal) == str
    assert type(stage) == str
    assert type(instr) == str
    assert type(signal) == str
    assert type(padding_type) == str
    assert type(width) == int

    datapath.drive_vbus(vbus_name=meta_signal, instr=instr, driving_signal=signal, stage=stage, padding_type=padding_type, width=width)

def add_datapath_dest(datapath, meta_signal, stage, instr, signal, padding_type, width=None):
    warnings.warn("Use of stand alone functions is deprecated, instead please DataFlow, DriverMap, and DataConnection classes")

    assert type(datapath) == DataFlow
    assert type(meta_signal) == str
    assert type(stage) == str
    assert type(instr) == str
    assert type(signal) == str
    assert type(padding_type) == str
    assert type(width) == int

    datapath.connectEndPoint(endpoint_name=signal, instr=instr, vbus_name=meta_signal, stage=stage, padding_type=padding_type, width=width)

def add_datapath(datapath, meta_signal, stage, src_dst, instr, signal, padding_type, width=None):
    warnings.warn("Use of add_datapath is deprecated, instead please use add_datapath_source and add_datapath_dest")

    assert type(src_dst) == bool

    if src_dst:
        add_datapath_source(datapath, meta_signal, stage, instr, signal, padding_type, width)
    else:
        add_datapath_dest(datapath, meta_signal, stage, instr, signal, padding_type, width)


def merge_datapaths(A, B):
    warnings.warn("Use of stand alone functions is deprecated, instead please DataFlow, DriverMap, and DataConnection classes")

    return A.merge(B)


def gen_datapath_muxes(datapath, output_path, force_generation, arch_head, arch_body):
    warnings.warn("Use of stand alone functions is deprecated, instead please DataFlow, DriverMap, and DataConnection classes")

    return convert_dataflow_to_muxes(datapath, output_path, force_generation, arch_head, arch_body)
