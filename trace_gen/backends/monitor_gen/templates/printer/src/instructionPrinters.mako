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

#include "Components/Printer.h"
#include "Components/Channel.h"

#include "${traceModel_.name}_Channel.h"

#include <sstream>
#include <string>

InstructionPrinterSet *${traceModel_.name}_InstrPrinterSet = new InstructionPrinterSet("${traceModel_.name}_InstrPrinterSet");

% for type_i in traceModel_.getAllInstructionTypes():
static InstructionPrinter *instrPrinter_${type_i.name} = new InstructionPrinter(
  ${traceModel_.name}_InstrPrinterSet,
  "${type_i.name}",
  ${type_i.identifier},
  [](Channel* channel_, int instr_){
    std::stringstream ret_strs;
    ${traceModel_.name}_Channel* channel = static_cast<${traceModel_.name}_Channel*>(channel_);
    % for trVal_i in traceModel_.getAllTraceValues():
    % if type_i.getMapping(trVal_i) is not None:
    ret_strs << channel->${trVal_i.name}[instr_] << "  ";
    % else:
    ret_strs << "----------  ";
    % endif
    % endfor
    return ret_strs.str();
  }
);
% endfor
