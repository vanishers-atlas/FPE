# Import ParseTreeListener to extend
from antlr4 import ParseTreeListener

# Import utils libraries
from FPE.toolchain import utils  as tc_utils
from FPE.toolchain import FPE_assembly as asm_utils
from FPE.toolchain.HDL_generation import utils  as gen_utils

####################################################################

class handler(ParseTreeListener):

    def __init__(this, program_context, overwrites_encoding, pc_value_encoding, loop_id_encoding):
        this.program_context = program_context
        this.overwrites_encoding = overwrites_encoding
        this.pc_value_encoding = pc_value_encoding
        this.loop_id_encoding = loop_id_encoding

        this.PC = 0

        this.loop_id = 0
        this.loop_nesting = []

        this.loops_finished = {}
        this.loops_unfinished = []

        this.FSM_loop_exit_order= []
        this.FSM_on_overwrite = {}
        this.FSM_loop_starts = {}
        this.FSM_loop_ends = {}

    def get_loop_details(this):
        assert(len(this.loops_unfinished) == 0)

        return this.loops_finished

    def get_FSM_details(this):
        assert len(this.FSM_on_overwrite) == this.loop_id
        assert len(this.FSM_loop_exit_order) == this.loop_id

        this.FSM_first_loop = this.FSM_loop_exit_order[0]
        FSM_on_fallthrough = { this.FSM_loop_exit_order[-1] : this.FSM_first_loop}
        for i, k in enumerate(this.FSM_loop_exit_order[:-1]):
            FSM_on_fallthrough[k] = this.FSM_loop_exit_order[i+1]

        try:
            return this.FSM_first_loop, this.edges
        except AttributeError:

            this.edges = {}
            for curr_id in this.FSM_on_overwrite.keys():
                # Handle next_id for overwrite values
                next_id = this.FSM_on_overwrite[curr_id]
                next_id_overwrite = tc_utils.unsigned.encode(next_id, this.loop_id_encoding["width"])
                update_window = this.FSM_loop_ends[next_id] - this.FSM_loop_starts[curr_id]
                if 0 <= update_window and update_window < 2 and curr_id != next_id:
                    stall_overwrtie = "1"
                else:
                    stall_overwrtie = "0"
                #print(curr_id, next_id, this.FSM_loop_ends[next_id], this.FSM_loop_starts[curr_id], update_window, stall_overwrtie)
                #print()

                # Handle next_id for fallthrough values
                next_id = FSM_on_fallthrough[curr_id]
                next_id_fallthrough = tc_utils.unsigned.encode(next_id, this.loop_id_encoding["width"])
                update_window = this.FSM_loop_ends[next_id] - this.FSM_loop_ends[curr_id]
                if 0 <= update_window and update_window < 2 and curr_id != next_id:
                    stall_fallthrough = "1"
                else:
                    stall_fallthrough = "0"
                #print(curr_id, next_id, this.FSM_loop_ends[next_id], this.FSM_loop_ends[curr_id], update_window, stall_fallthrough)
                #print()

                this.edges[curr_id] = (next_id_overwrite, stall_overwrtie, next_id_fallthrough, stall_fallthrough)

            return this.FSM_first_loop, this.edges


    def enterState_rep(this, ctx):
        this.loop_nesting.append(this.loop_id)

        this.enterState_rep_loops(ctx)
        this.enterState_rep_FSM(ctx)

        this.loop_id += 1

    def enterState_rep_loops(this, ctx):
        loop_name = "rep_bank_loop_%i"%(this.loop_id, )
        overwrites = asm_utils.evaluate_expr(ctx.expr(), this.program_context) - 1

        # Handle overwrites
        overwrites_encoded = tc_utils.unsigned.encode(overwrites, this.overwrites_encoding["width"])

        # Setting the PC overwrite value to current PC, ie the PC of the first instruction of the loop
        this.loops_unfinished.append((
            loop_name,
            {
                "start_value" : tc_utils.unsigned.encode(this.PC, this.pc_value_encoding["width"]),
                "end_value"   : None,
                "overwrites" : overwrites_encoded,
            },
        ))

    def enterState_rep_FSM(this, ctx):
        # Handle FSM_on_overwrite
        this.FSM_on_overwrite[this.loop_id] = None

        # Handle FSM_on_fallthrough
        pass

        # Record loop starts for stall computing
        this.FSM_loop_starts[this.loop_id] = this.PC

    def exitState_rep(this, ctx):
        this.exitState_rep_loops(ctx)
        this.exitState_rep_FSM(ctx)
        this.loop_nesting.pop()

    def exitState_rep_loops(this, ctx):
        loop_name, loop_details = this.loops_unfinished.pop()

        # Set the end value to the loop, to PC - 1, ie the last instruction in the loop
        # - 1 as this.PC is incremented on entering an operation
        loop_details["end_value"] = tc_utils.unsigned.encode(this.PC - 1, this.pc_value_encoding["width"])

        this.loops_finished[loop_name] = loop_details

    def exitState_rep_FSM(this, ctx):
        ending_loop_id = this.loop_nesting[-1]

        # Handle FSM_on_overwrite
        for loop_id in reversed(this.loop_nesting):
            if this.FSM_on_overwrite[loop_id] == None:
                this.FSM_on_overwrite[loop_id] = ending_loop_id
            else:
                break

        # Handle FSM_on_fallthrough
        this.FSM_loop_exit_order.append(ending_loop_id)

        # Record loop ends for stall computing
        # - 1 as this.PC is incremented on entering an operation
        this.FSM_loop_ends[ending_loop_id] = this.PC - 1


    def enterOperation(this, ctx):
        this.PC += 1
