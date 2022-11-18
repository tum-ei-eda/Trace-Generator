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

/********************* AUTO GENERATE FILE (create by Trace-Generator) *********************/

#include "${traceModel_.name}_Monitor.h"
#include "${traceModel_.name}_Channel.h"

#include "Components/Channel.h"

#include <sstream>
#include <string>
#include <stdbool.h>

extern "C"
{
  int *${builder_.getInstrCntName()};
  int *${builder_.getBufferName("typeId")};
  % for trVal_i in traceModel_.getAllTraceValues():
  % if trVal_i.dataType == "int":
  int *${builder_.getBufferName(trVal_i.name)};
  % elif trVal_i.dataType == "string":
  char (*${builder_.getBufferName(trVal_i.name)})[${builder_.getStringSize(trVal_i)}];
  % endif
  % endfor
}

extern InstructionMonitorSet* ${traceModel_.name}_InstrMonitorSet;

${traceModel_.name}_Monitor::${traceModel_.name}_Monitor(): Monitor("${traceModel_.name}_Monitor", ${traceModel_.name}_InstrMonitorSet)
{}

void ${traceModel_.name}_Monitor::connectChannel(Channel* channel_)
{
  Monitor::channel = channel_;

  ${traceModel_.name}_Channel* ch = static_cast<${traceModel_.name}_Channel*>(channel_);

  ${traceModel_.name}_Monitor_instrCnt = &(ch->instrCnt);
  ${traceModel_.name}_Monitor_typeId_buffer = ch->typeId;

  % for trVal_i in traceModel_.getAllTraceValues():
  ${traceModel_.name}_Monitor_${trVal_i.name}_buffer = ch->${trVal_i.name};
  % endfor
}

<%
hasString = False
for trVal_i in traceModel_.getAllTraceValues():
    if trVal_i.dataType == "string":
       hasString = True
%>
std::string ${traceModel_.name}_Monitor::getBlockDeclarations(void) const
{
  std::stringstream ret_strs;
  % if hasString:
  ret_strs << "#include <string.h>\n";
  % endif
 
  ret_strs << "extern int *${builder_.getInstrCntName()};\n";
  ret_strs << "extern int *${builder_.getBufferName("typeId")};\n";

  % for trVal_i in traceModel_.getAllTraceValues():
  % if trVal_i.dataType == "int":
  ret_strs << "extern int *${builder_.getBufferName(trVal_i.name)};\n";
  % elif trVal_i.dataType == "string":
  ret_strs << "extern char (*${builder_.getBufferName(trVal_i.name)})[${builder_.getStringSize(trVal_i)}];\n";
  % endif
  % endfor

  return ret_strs.str();
}
