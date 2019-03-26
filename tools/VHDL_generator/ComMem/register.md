# Documentation for register

## Parameters
* has_reset, *boolean*,
	- controls if the register has an asynchronize reset
* has_preset, *boolean*,
	- controls if the register has an asynchronize preset
* write_mode, *string*, ["high", "sync", "edge"]
	- "high": write_enable is active high
	- "sync": write_enable is synchronized to the clock raising edge
	- "edge": write_enable is raising edge triggered
* read_mode, *string*, ["high", "sync", "always"]
	- "high": read_enable is active high
	- "sync": read_enable is synchronized to the clock raising edge
	- "always": read_enable isn't used, data_out is always enabled

## Generics
* data_width, *integer*, [0<]
	- the data width of the register

## Ports
##### General Ports
* clock, *in std_logic*,
	- present if write_mode = 1 or read_mode = 1
	- the clock signal used for synchronized actions
* reset, *in std_logic*,
	- present iff has_reset = true
	- resets the registered_value to all 0s
	- supercedes write_enable if both are trying to change the registered_value
	- if high at the same time as preset: registered_value the undefined
* preset, *in std_logic*,
	- present iff has_preset = true
	- presets the registered_value to all 1s
	- supercedes write_enable if both are trying to change the registered_value
	- if high at the same time as reset: registered_value the undefined
##### Data ports
* data_in, *in std_logic_vector(data_width)*,
	- triggered by write_enable
	- when triggered; registered_value is set to the current value of this port
* write_enable, *in std_logic*,
	- behavour depends on write_mode:
		+ 0: triggers data_in for as long as it is held high
		+ 1: triggers data_in once if high on the raising edge of this clock port
		+ 2: triggers data_in once on the raising edge of this port
* data_out, *out std_logic_vector(data_width)*,
	- read_enable present:
		+ true	: triggered by read_enable
		+ false	: always triggered
	- when triggered: outputs the currently registered_value
	- when not triggered: outputs Z
* read_enable, *in std_logic*,
	- present iff read_mode != 2
	- behavour depends on read_mode:
		+ 0: triggers data_out for as long as it is held high
		+ 1: triggers data_out for 1 clock cylce if high on the raising edge of this clock port
		+ 2: no present, data_out is always triggered
