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

#include "${traceModel_.name}_Printer.h"

#include "Components/Printer.h"

#include <iostream>
#include <iomanip>

extern InstructionPrinterSet* ${traceModel_.name}_InstrPrinterSet;

${traceModel_.name}_Printer::${traceModel_.name}_Printer(): Printer("${traceModel_.name}_Printer", ${traceModel_.name}_InstrPrinterSet)
{}

void ${traceModel_.name}_Printer::initialize(void)
{
  std::stringstream caption_strs;	
  % for trVal_i in traceModel_.getAllTraceValues():
  caption_strs << ${builder_.getStreamSetupCaption(trVal_i)} << "${trVal_i.name}" << ${builder_.getSeparater()};
  % endfor

  streamer.openStream();
  streamer.stream(caption_strs.str() + "\n");
}