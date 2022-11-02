# 
# Copyright 2022 Chair of EDA, Technical University of Munich
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json

from metamodel import MetaTraceModel

class Parser():

    def parse(self, file_):

        # Read data from json-file
        data = json.load(open(file_))

        # Create "top" trace model
        trace_json = data['trace']
        trace_model = MetaTraceModel.Trace(trace_json['name'])

        # Create trace values (NOTE: Must do that before adding instructions / creating mappings!)
        for trVal_i in trace_json['traceValues']:
            try:
                test = trace_model.createAndAddTraceValue(trVal_i['name'], trVal_i["type"])
            except KeyError:
                test = trace_model.createAndAddTraceValue(trVal_i['name'])
                
        # Create instruction-types for all instruction groups
        for instrGr_i in data['trace']['instructionGroups']:
            instrType_model = trace_model.createAndAddInstructionType(instrGr_i['name'])
            for instr_i in instrGr_i['instructions']:
                instrType_model.createAndAddInstruction(instr_i['name'])

            # Add mappings to instruction-type
            for mapping_i in instrGr_i['mappings']:
                instrType_model.createAndAddMapping(mapping_i['traceValue'], mapping_i['description'])
                
        # Create instruction-types for all singel instructions
        for instr_i in data['trace']['instructions']:
            instrType_model = trace_model.createAndAddInstructionType(instr_i['name'])
            instrType_model.createAndAddInstruction(instr_i['name'])
            
            # Add mappings to instruction-type
            for mapping_i in instr_i['mappings']:
                instrType_model.createAndAddMapping(mapping_i['traceValue'], mapping_i['description'])

        return trace_model
