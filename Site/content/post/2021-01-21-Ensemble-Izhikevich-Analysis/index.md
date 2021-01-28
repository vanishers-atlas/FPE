---
title: "Ensemble Izhikevich Analysis"
date: 2021-01-21
description: Analysis of FPEA programs executing ensembles of varying sizes of Izhikevich neurons
slug: ensemble-izhikevich-analysis
categories:
    - FPEA
    - Vivado
    - Izhikevich
    - Branch neurons
    - PYNQ Z2
tags:
    - Izhikevich
    - Processor V2
draft: false
---

## The Goal

This work establishes how the resources allocated for the Izhikevich FPEA program on the FPGA changes when executing 2, 5, 10, 100 or 1000 neurons in an ensemble.

Between this version of the Izhikevich neuron FPEA program and the last changes were made to improve the overall program efficiency by reordering instructions in the assembly program as well as using the output from slice P on the DSP slice as an operand to instructions allowing the data to be used two cycles earlier in subsequent instructions than if the data was written to memory.

As well as the previously mentioned changes, the Izhikevich FPEA program was rewritten to use instructions found on the new version of the processor. This includes the use of bit shifting operations to truncate the results of the fixed-point multiplications.
The ALU data width specified in the parameters was also corrected to 32 bits to support the multiplication of 16 bit fixed-point values.

## Git Commit

[9890cb78bd0e6f3ae219ce09ef047f0e65909efa](https://gitlab.com/eStreams/sfpe/-/commit/9890cb78bd0e6f3ae219ce09ef047f0e65909efa)

## FPEA Program Analysis

| Instruction | Used | Percentage (%) | Cycles Used | Cycles Used (%) |
| :-- | :--: | :--: | :--: | :--: |
| Total Number of Instructions | 78 |  | 268 |  |
| ALU Instructions | 40 | 51.282 | 200 | 74.627 |
| NOPs | 28 | 35.897 | 29 | 10.448 |
| Jumps | 6 | 7.692 | 24 | 8.955 |
| BAM Management | 4 | 5.128 | 16 | 5.970 |

![A bar plot comparing the number of cycles used (as a percentage) of the previous and current Izhikevich FPEA programs for each category of instruction](izhikevich_fpea_program_percentage_cycles_used_stats.png)

![A bar plot comparing the number of instructions used (as a percentage) of the previous and current Izhikevich FPEA programs for each category of instruction](izhikevich_fpea_program_percentage_instructions_used_stats.png)

As can be seen in the plots above almost 80% of the processor cycles are executing ALU instructions despite 35% of the instructions in the program being NOPs.
It is possible to reduce the number of jumps in the program by 1/3 by including the addition of the after-spike reset recovery to the recovery variable in the same jumps as the resetting of the of the post-spike membrane potential, though how this may affect the size of data being handled has not yet been experimented with in out work.

![A bar plot showing the total number of cycles needed to execute the the Izhikevich FPEA program for each version](izhikevich_fpea_program_cycles_used_stats.png)

![A bar plot showing the total number of instructions used to execute the the Izhikevich FPEA program for each version](izhikevich_fpea_program_instructions_used_stats.png)

By using the output from slice P of the DSP slice as an operand in instructions a number of NOP instructions could be removed from the program however the combination of NOPs and jump instructions in the program still prevent the program efficiency from reaching 90%.

## Comparison of Slice Logic Used by Each Ensemble

|          Site Type         | 2 Neurons | 5 Neurons | 10 Neurons | 100 Neurons | 1000 Neurons |
| :-- | :--: | :--: | :--: | :--: | :--: |
| Slice LUTs                 |  345 |  292 |  304 |  479 | 1317 |
|   LUT as Logic             |  331 |  278 |  290 |  386 |  580 |
|   LUT as Memory            |   14 |   14 |   14 |   93 |  737 |
|     LUT as Distributed RAM |   12 |   12 |   12 |   88 |  704 |
|     LUT as Shift Register  |    2 |    2 |    2 |    5 |   33 |
| Slice Registers            |  300 |  323 |  327 |  340 |  383 |
|   Register as Flip Flop    |  267 |  274 |  278 |  291 |  334 |
|   Register as Latch        |   33 |   49 |   49 |   49 |   49 |
| F7 Muxes                   |    9 |   10 |   10 |   18 |   80 |
| F8 Muxes                   |    0 |    0 |    0 |    0 |    2 |

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

![The line graph shows how the percentage of available slice resources on the FPGA changes as the number of neurons in the ensemble increases.](izhikevich_ensemble_program_resource_allocation.png)

## Future Work

Another way to further improve program efficiency would be to interleave the operations of other Izhikevich into the loop thus replacing NOP instructions with ALU instructions using data of other neurons in the ensemble. At this point it is not clear what this would impact in terms of resource usage or in the addition of BAM management instructions (which would reduce the program efficiency).
