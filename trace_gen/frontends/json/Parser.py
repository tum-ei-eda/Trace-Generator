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
import re
import sys
import pickle
# import dill

sys.path.append('/usr/local/research/projects/SystemDesign/work/performance-evaluation/qin/M2-ISA-R')
sys.path.append('/usr/local/research/projects/SystemDesign/work/performance-evaluation/qin/Trace-Generator/trace_gen')
from metamodel import MetaTraceModel
from m2isar.metamodel import arch
from m2isar.metamodel.arch import CoreDef

class M2isarmodel():

    def load_model(self, file):
        """ Load .m2isarmodel file """
        
        # load model
        with open(file, 'rb') as f:
            model: "dict[str, CoreDef]" = pickle.load(f)
        return model

    def resolve_instruction(self, model, core_name):
        """ Return a list of instr_objs in a specific core_obj """

        # A core object with the specific name
        core_obj = model[core_name]
        instr_list = core_obj.instructions.values()
        return instr_list
    
    def resolve_namelists(self, instr_list):
        """ Return a dict, instr_name as keys and bf_name lists as values """

        # Dict of name lists
        name_lists = {}

        for instr_i in instr_list:
            bf_name = []
            for enc in reversed(instr_i.encoding):
                if isinstance(enc, arch.BitField):
                    bf_name.append(enc.name)
            name_lists[instr_i.name] = bf_name
        return name_lists

    def resolve_bitrange(self, instr_name, bf_name, instr_list):
        """ Return bitrange components of a bitfield """

        # For the track of bit position
        enc_idx = 0

        # Bitrange components of a bitfield
        offset = []
        msb = []
        lsb = []

        for instr_i in instr_list:

            # Find the instr_i with the instr_name
            if instr_name.lower() == instr_i.name.lower():
                for enc in reversed(instr_i.encoding):
                    if isinstance(enc, arch.BitField):
                        length = enc.range.length

                        # Find the enc with the bf_name
                        if (bf_name == enc.name):
                            offset.append(enc.range.lower)
                            msb.append(enc_idx + length - 1)
                            lsb.append(enc_idx)
                        enc_idx += length
                    else:
                        enc_idx += enc.length
        return (offset, msb, lsb)

class Parser():

    def __init__(self):
        self.currentIdentifier = 0
        self.setIdAuto = True
        
    def parse(self, file_):

        # Read data from json-file
        with open(file_) as f:
            data = json.load(f)

        # Create "top" trace model
        trace_json = data['trace']
        trace_model = MetaTraceModel.Trace(trace_json['name'])

        # Try to read setId attribute
        try:
            setIdAttr = trace_json['setId']
            if setIdAttr == "Automatic":
                self.setIdAuto = True
            elif setIdAttr == "Manual":
                self.setIdAuto = False
            else:
                print("ERROR: setId attribute is set to %s. The only currently supported flags are \"Automatic\" and \"Manual\"" % setIdAttr)
                self.setIdAuto = True
        except KeyError:
            self.setIdAuto = True

        if self.setIdAuto == True:
            self.currentIdentifier = 0

        # Try to read separator attribute
        try:
            trace_model.setSeparator(trace_json['separator'])
        except KeyError:
            pass
        
        # Create trace values (NOTE: Must do that before adding instructions / creating mappings!)
        for trVal_i in trace_json['traceValues']:
            try:
                trace_model.createAndAddTraceValue(trVal_i['name'], trVal_i["type"], trVal_i["size"])
            except KeyError:
                try:
                    trace_model.createAndAddTraceValue(trVal_i['name'], trVal_i["type"])
                except KeyError:
                    trace_model.createAndAddTraceValue(trVal_i['name'])
                
        # Create instruction-types for all instruction groups
        try:
            instructionGroups = data['trace']['instructionGroups']
        except KeyError:
            instructionGroups = []

        for instrGr_i in instructionGroups:
            instrType_model = trace_model.createAndAddInstructionType(instrGr_i['name'], self.__getId(instrGr_i))
            for instr_i in instrGr_i['instructions']:
                instrType_model.createAndAddInstruction(instr_i['name'])

            # Add mappings to instruction-type
            self.__addMapping(instrType_model, instrGr_i)
                
        # Create instruction-types for all singel instructions
        try:
            instructions = data['trace']['instructions']
        except KeyError:
            instructions = []

        for instr_i in instructions:
            instrType_model = trace_model.createAndAddInstructionType(instr_i['name'], self.__getId(instr_i))
            instrType_model.createAndAddInstruction(instr_i['name'])

            # Add mappings to instruction-type
            self.__addMapping(instrType_model, instr_i)
                    
        return trace_model


    # TODO: Initial solution with BITFIELD keyword. Find way to incoperate CoreDSL?
    def resolveDescriptions(self, name_lists, traceModel_, coredsl):
        """ Resolve descriptions and create bitfield and bitrange coperating with CoreDSL """
        
        # Bitrange components of a bitfield
        offset = []
        msb = []
        lsb = []

        for descr_i in traceModel_.getAllDescriptions():

            # For each line in json-file, which has "discription:"
            descr_temp = descr_i.original

            # Resolve BITFIELD keyword
            bitfieldDescriptions = re.findall(
                "\$\{BITFIELD[^\}]*\}", descr_temp)
            
            if bitfieldDescriptions:
                for bfDescr_i in bitfieldDescriptions:

                    # Resolve bf name
                    bfName = re.split("\$\{BITFIELD\s", bfDescr_i)[1]
                    bfName = re.split("\}", bfName)[0]
                    for instr_i in descr_i.getInstructionType().getAllInstructions():  
                        
                        # Raise err
                        if instr_i.name.upper() not in name_lists.keys():
                            print("")
                            print(f'The instr_name \'{instr_i.name}\' in trace did not match the m2isarmodel.')
                        if bfName not in name_lists[instr_i.name.upper()]:
                            print("")
                            print(f'The bf_name \'{bfName}\' of \'{instr_i.name}\' in trace did not match the m2isarmodel.')
                        
                        # For each instruction that has the same descriptions
                        offset, msb, lsb = M2isarmodel().resolve_bitrange(instr_i.name, bfName, coredsl)
                        if not instr_i.bitfieldExists(bfName):
                            bitfield = instr_i.createAndAddBitfield(bfName)
                            for i in range(0, len(offset)): 

                                # For the bitfield that has one or more bitranges
                                bitfield.createAndAddBitRange(offset[i], msb[i], lsb[i])

                    # Replace bitfield notation with name of bitfield
                    descr_temp = re.sub(
                    "\$\{BITFIELD[^\}]*\}", bitfield.name, descr_temp, 1)
                    self.__resolvePreprocessing(descr_i, descr_temp)                      

    ## HELPER FUNCTIONS

    def __resolveBitfields(self, descr_):

        descr_temp = descr_.original
            
        # Resolve BITFIELD keyword
        bitfieldDescriptions = re.findall("\$\{BITFIELD[^\}]*\}", descr_temp)
        
        if bitfieldDescriptions:
            for bfDescr_i in bitfieldDescriptions:
        
                # Isolate bitfield description 
                bitfield_str = re.split("\$\{BITFIELD", bfDescr_i)[1]
                bitfield_str = re.split("\}", bitfield_str)[0]
        
                # Split bitfield description into name and range description
                splitStr = re.split("\[", bitfield_str)
                
                # Find name and create new bitfield model
                bitfieldName = splitStr[0].replace(' ', '')
                for instr_i in descr_.getInstructionType().getAllInstructions():

                    if not instr_i.bitfieldExists(bitfieldName):
                        bitfield = instr_i.createAndAddBitfield(bitfieldName)
                    
                        # Find and add bit ranges
                        rangeStr = splitStr[1].replace(']','')
                        ranges = re.split("\|", rangeStr)
                        for r_i in ranges:
                            r = r_i.replace('(','')
                            r = r.replace(')','')
                            r = r.replace(' ', '')
                            r_split = re.split(":", r)
                            offset = r_split[0]
                            bits = re.split(",", r_split[1])
                            msb = bits[0]
                            lsb = bits[1]
                            bitfield.createAndAddBitRange(offset, msb, lsb)

                # Replace bitfield notation with name of bitfield
                descr_temp = re.sub("\$\{BITFIELD[^\}]*\}", bitfield.name, descr_temp, 1)

        return descr_temp

    def __resolvePreprocessing(self, descrModel_, descrStr_):

        # Break description into preprocessed and not-preprocessed description-snippets
        firstSplit = True
        for split_i in re.split("\${", descrStr_):
        
            # First split only contains of not-preprocessed snippet
            if firstSplit:
                firstSplit = False
                if split_i:
                    descrModel_.createAndAppendDescriptionSnippet(split_i)
        
            else:
        
                # Loop through split_i to find end of preprocessed snippet
                preProcessedSnippet = ""
                numNestedBrackets = 0
                startNotPreProcessedSnippet = 0
                for c in split_i:
        
                    startNotPreProcessedSnippet += 1
                        
                    if c == '}':
                        if numNestedBrackets != 0:
                            numNestedBrackets -= 1
                        else:
                            break
        
                    elif c == '{':
                        numNestedBrackets += 1
        
                    preProcessedSnippet += c
                            
                descrModel_.createAndAppendDescriptionSnippet(preProcessedSnippet, True)
                if (startNotPreProcessedSnippet < len(split_i)):
                    descrModel_.createAndAppendDescriptionSnippet(split_i[startNotPreProcessedSnippet : ])
    
    def __addMapping(self, instrTypeModel_, instrOrGroup_):
        for mapping_i in instrOrGroup_['mappings']:
            try:
                instrTypeModel_.createAndAddMapping(mapping_i['traceValue'], mapping_i['description'], mapping_i['position'])
            except KeyError:
                instrTypeModel_.createAndAddMapping(mapping_i['traceValue'], mapping_i['description'], "pre")


    def __getId(self, instrOrGroup_):
        retId = 0
        if self.setIdAuto == True:
            retId = self.currentIdentifier
            self.currentIdentifier += 1
        else:
            try:
                retId = instrOrGroup_['id']
            except KeyError:
                print("ERROR: SetId attribute set to \"Manual\", but no identifier specidied for instruction or instruction group %s" %instrOrGroup_['name'])
        return retId
            
