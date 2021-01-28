---
title: "LIF Ensemble Analysis using Processor V2"
date: 2021-01-28
description: Analysis of FPEA programs executing ensembles of varying sizes of LIF neurons
slug: ensemble-lif-analysis-processor-v2
categories:
    - FPEA
    - Vivado
    - LIF
    - Branch neurons
    - PYNQ Z2
tags:
    - LIF
    - Processor V2
draft: false
---

## The Goal

The LIF FPEA program was rewritten to use instructions found on the new version of the processor. This includes the use of bit shifting operations to truncate the results of the fixed-point multiplications.
The ALU data width specified in the parameters was also corrected to 32 bits to support the multiplication of 16 bit fixed-point values.

## Git Commit

[2c52cf394eb54c0a09914df724a1e96d161174e7](https://gitlab.com/eStreams/sfpe/-/commit/2c52cf394eb54c0a09914df724a1e96d161174e7)

## FPEA Program Analysis

| Instruction | Used | Percentage (%) | Cycles Used | Cycles Used (%) |
| :-- | :--: | :--: | :--: | :--: |
| Total Number of Instructions | 43 |  | 154 |  |
| ALU Instructions | 18 | 41.860 | 90 | 58.442 |
| NOPs | 12 | 27.907 | 12 | 7.792 |
| Jumps | 5 | 11.628 | 20 | 12.987 |
| BAM Management | 8 | 18.605 | 32 | 20.779 |

![A bar plot comparing the number of cycles used (as a percentage) of the previous and current LIF FPEA programs for each category of instruction. The previous iteration of the LIF ensemble FPEA program was created for the first version of the soft processor whereas this more recent version was created for use with the second version of the processor](lif_fpea_program_percentage_cycles_used_stats.png)

![A bar plot comparing the number of instructions used (as a percentage) of the previous and current LIF FPEA programs for each category of instruction](lif_fpea_program_percentage_instructions_used_stats.png)

As can be seen in the graphs above a 18% and 20% of instructions and cycles respectively are used to manage to position of the BAM pointer. This along with jump instructions and NOPs are severely hampering the program efficiency of the LIF neuron FPEA activation program.

![A bar plot showing the total number of cycles needed to execute the the LIF FPEA program for each version](lif_fpea_program_cycles_used_stats.png)

![A bar plot showing the total number of instructions used to execute the the LIF FPEA program for each version](lif_fpea_program_instructions_used_stats.png)

## Comparison of Slice Logic Used by Each Ensemble

|          Site Type         | 2 Neurons | 5 Neurons | 10 Neurons | 100 Neurons | 1000 Neurons |
| :-- | :--: | :--: | :--: | :--: | :--: |
| Slice LUTs                 |  206 |  214 |  218 |  374 | 1582 |
|   LUT as Logic             |  193 |  201 |  205 |  260 |  516 |
|   LUT as Memory            |   13 |   13 |   13 |  114 | 1066 |
|     LUT as Distributed RAM |   12 |   12 |   12 |  110 | 1034 |
|     LUT as Shift Register  |    1 |    1 |    1 |    4 |   32 |
| Slice Registers            |  241 |  245 |  249 |  265 |  299 |
|   Register as Flip Flop    |  203 |  207 |  211 |  227 |  261 |
|   Register as Latch        |   38 |   38 |   38 |   38 |   38 |
| F7 Muxes                   |    1 |    1 |    0 |    3 |   99 |
| F8 Muxes                   |    0 |    0 |    0 |    0 |   48 |

## Comparison of Memory Used by Each Ensemble

|    Site Type   | 2 Neurons | 5 Neurons | 10 Neurons | 100 Neurons | 1000 Neurons |
| :-- | :--: | :--: | :--: | :--: | :--: |
| Block RAM Tile |    0 |    0 |    0 |    0 |    0 |
|   RAMB36/FIFO* |    0 |    0 |    0 |    0 |    0 |
|   RAMB18       |    0 |    0 |    0 |    0 |    0 |

## Comparison of DSPs Used by Each Ensemble

|    Site Type   | 2 Neurons | 5 Neurons | 10 Neurons | 100 Neurons | 1000 Neurons |
| :-- | :--: | :--: | :--: | :--: | :--: |
| DSPs           |    1 |    1 |    1 |    1 |    1 |
|   DSP48E1 only |    1 |    1 |    1 |    1 |    1 |

## FPGA Resource Utilization

![The line graph shows how the percentage of available slice resources on the FPGA changes as the number of neurons in the ensemble increases.](lif_ensemble_program_resource_allocation.png)

## Future Work

Another way to further improve program efficiency would be to interleave the operations of other LIF into the loop thus replacing NOP and BAM management instructions with ALU instructions using data of other neurons in the ensemble. At this point it is not clear what this would impact in terms of resource usage or in the addition of BAM management instructions (which would reduce the program efficiency).
