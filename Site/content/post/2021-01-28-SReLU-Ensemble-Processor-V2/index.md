---
title: "SReLU Ensemble Analysis using Processor V2"
date: 2021-01-28
description: Analysis of FPEA programs executing ensembles of varying sizes of SReLU neurons
slug: ensemble-srelu-analysis-processor-v2
categories:
    - FPEA
    - Vivado
    - SReLU
    - Branch neurons
    - PYNQ Z2
tags:
    - SReLU
    - Processor V2
draft: false
---

## The Goal

The SReLU FPEA program was rewritten to use instructions found on the new version of the processor. This includes the use of bit shifting operations to truncate the results of the fixed-point multiplications.
The ALU data width specified in the parameters was also corrected to 32 bits to support the multiplication of 16 bit fixed-point values.

## Git Commit

[69a6a12663b2cf82e2c0e82a09bfae838c50cc65](https://gitlab.com/eStreams/sfpe/-/commit/69a6a12663b2cf82e2c0e82a09bfae838c50cc65)

## FPEA Program Analysis

| Instruction | Used | Percentage (%) | Cycles Used | Cycles Used (%) |
| :-- | :--: | :--: | :--: | :--: |
| Total Number of Instructions | 35 |  | 127 |  |
| ALU Instructions | 20 | 57.143 | 100 | 78.740 |
| NOPs | 11 | 31.429 | 11 | 8.661 |
| Jumps | 2 | 5.714 | 8 | 6.299 |
| BAM Management | 2 | 5.714 | 8 | 6.299 |

![A bar plot comparing the number of cycles used (as a percentage) of the previous and current SReLU FPEA programs for each category of instruction. The previous iteration of the SReLU ensemble FPEA program was created for the first version of the soft processor whereas this more recent version was created for use with the second version of the processor](srelu_fpea_program_percentage_cycles_used_stats.png)

![A bar plot comparing the number of instructions used (as a percentage) of the previous and current SReLU FPEA programs for each category of instruction](srelu_fpea_program_percentage_instructions_used_stats.png)

![A bar plot showing the total number of cycles needed to execute the the SReLU FPEA program for each version](srelu_fpea_program_cycles_used_stats.png)

![A bar plot showing the total number of instructions used to execute the the SReLU FPEA program for each version](srelu_fpea_program_instructions_used_stats.png)

## Comparison of Slice Logic Used by Each Ensemble

|          Site Type         | 2 Neurons | 5 Neurons | 10 Neurons | 100 Neurons | 1000 Neurons |
| :-- | :--: | :--: | :--: | :--: | :--: |
| Slice LUTs                 |  169 |  170 |  172 |  230 |  665 |
|   LUT as Logic             |  156 |  157 |  159 |  182 |  281 |
|   LUT as Memory            |   13 |   13 |   13 |   48 |  384 |
|     LUT as Distributed RAM |   12 |   12 |   12 |   44 |  352 |
|     LUT as Shift Register  |    1 |    1 |    1 |    4 |   32 |
| Slice Registers            |  206 |  229 |  233 |  246 |  284 |
|   Register as Flip Flop    |  187 |  194 |  198 |  211 |  249 |
|   Register as Latch        |   19 |   35 |   35 |   35 |   35 |
| F7 Muxes                   |    0 |    0 |    0 |    3 |   32 |
| F8 Muxes                   |    0 |    0 |    0 |    0 |   16 |

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

![The line graph shows how the percentage of available slice resources on the FPGA changes as the number of neurons in the ensemble increases.](srelu_ensemble_program_resource_allocation.png)

## Future Work

Another way to further improve program efficiency would be to interleave the operations of other SReLU into the loop thus replacing NOP instructions with ALU instructions using data of other neurons in the ensemble. At this point it is not clear what this would impact in terms of resource usage or in the addition of BAM management instructions (which would reduce the program efficiency).
