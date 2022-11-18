/*
 * Copyright 2022 Chair of EDA, Technical University of Munich
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *	 http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/********************* AUTO GENERATE FILE (create by M2-ISA-R-Perf) *********************/

#include "Components/Monitor.h"

#include "etiss/Instruction.h"

#include <sstream>
#include <string>

InstructionMonitorSet *${traceModel_.name}_InstrMonitorSet = new InstructionMonitorSet("${traceModel_.name}_InstrMonitorSet");

% for instr_i in traceModel_.getAllInstructions():
static InstructionMonitor *${builder_.getInstrMonitorName(instr_i.name)} = new InstructionMonitor(
  ${traceModel_.name}_InstrMonitorSet,
  "${instr_i.name}",
  [](etiss::instr::BitArray &ba, etiss::instr::Instruction &instr, etiss::instr::InstructionContext &ic){
    std::stringstream ret_strs;
    ret_strs << "${builder_.getBufferName("typeId")}[*${builder_.getInstrCntName()}] = " << ${instr_i.getInstructionType().identifier} << ";\n";
    % for map_i in instr_i.getAllMappings():
    % for bf_i in map_i.getAllBitfields():
    int ${bf_i.name} = 0;
    % for br_i in bf_i.getAllBitRanges():
    static etiss::instr::BitArrayRange R_${bf_i.name}_${br_i.offset}(${br_i.msb},${br_i.lsb});
    ${bf_i.name} += R_${bf_i.name}_${br_i.offset}.read(ba) << ${br_i.offset};
    % endfor
    % endfor
    % if map_i.getTraceValue().dataType == "int":
    ret_strs << "${builder_.getBufferName(map_i.getTraceValue().name)}[*${builder_.getInstrCntName()}] = " << ${builder_.getDescriptionString(map_i.getDescription())} << ";\n";
    % elif map_i.getTraceValue().dataType == "string":
    ret_strs << "strcpy(${builder_.getBufferName(map_i.getTraceValue().name)}[*${builder_.getInstrCntName()}],\"" << ${builder_.getDescriptionString(map_i.getDescription())} << "\");\n";
    % endif
    % endfor
    ret_strs << "*${builder_.getInstrCntName()} += 1;\n";
    return ret_strs.str();
  }
);
% endfor
