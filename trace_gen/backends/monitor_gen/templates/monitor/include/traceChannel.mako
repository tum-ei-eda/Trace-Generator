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

#ifndef {traceModel_.name.upper()}_CHANNEL_H
#define {traceModel_.name.upper()}_CHANNEL_H

#include "Components/Channel.h"

Class ${traceModel_.name}_Channel: public Channel
{

  ${traceModel_.name}_Channel() {};
  ~${traceModel_.name}_Channel() {};

  % for trVal_i in traceModel_.getAllTraceValues():
  % if trVal_i.dataType == "int":
  int ${trVal_i.name} [${traceModel_.getChannelSize()}];
  % elif trVal_i.dataType == "string":
  char ${trVal_i.name} [${traceModel_.getChannelSize()}] [${traceModel_.getMaxStringSize()}];
  % endif
  % endfor
}

#endif // ${traceModel_.name.upper()}_CHANNEL_H