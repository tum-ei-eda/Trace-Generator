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

class MetaTraceModel_base:
    __isFrozen = False

    def __setattr__(self, key, value):
        if self.__isFrozen and not hasattr(self, key):
            raise TypeError("Attempting to add new attribute to frozen class %r" %self)
        object.__setattr__(self, key, value)

    def __init__(self):
        self.__isFrozen = True

class Trace(MetaTraceModel_base):

    def __init__(self, name_):
        self.name = name_
        self.instructionTypes = []
        self.instructions = {}
        self.traceValues = {}
        
        super().__init__()

    def createAndAddTraceValue(self, name_, type_="int"):
        trVal = TraceValue(name_, type_)
        self.traceValues[name_] = trVal
        return trVal
        
    def createAndAddInstructionType(self, name_, id_):
        instrType = InstructionType(name_, id_, self)
        self.instructionTypes.append(instrType)
        return instrType

    def getAllTraceValues(self):
        return self.traceValues.values()

    def registerInstruction(self, instr_):
        self.instructions[instr_.name] = instr_
    
    def getInstruction(self, name_):
        try:
            return self.instructions[name_]
        except KeyError:
            return None
    
    def getAllInstructions(self):
        return self.instructions.values()

    def getAllInstructionTypes(self):
        return self.instructionTypes

    def getAllMappings(self):
        mappings = []
        for instrType_i in self.getAllInstructionTypes():
            mappings.extend(instrType_i.getAllMappings())
        return mappings

    def getAllDescriptions(self):
        descriptions = []
        for map_i in self.getAllMappings():
            descriptions.append(map_i.description)
        return descriptions
    
class InstructionType(MetaTraceModel_base):

    def __init__(self, name_, id_, parent_):
        self.name = name_
        self.identifier = id_
        self.instructions = []
        self.mappings = {}
        self.__parent = parent_
        
        super().__init__()

    def createAndAddInstruction(self, name_):
        
        if self.__parent.getInstruction(name_) is not None:
            raise TypeError("Cannot create instruction %s. Instruction has already been created for instruction-type %s" %(name_, self.__parent.getInstruction(name_).getInstructionType().name))
            
        instr = Instruction(name_, self)
        self.__parent.registerInstruction(instr)
        self.instructions.append(instr)
        return instr

    def createAndAddMapping(self, trValName_, description_):

        # Look up trace-value in dict. of parent/trace-model
        try:
            trVal = self.__parent.traceValues[trValName_]
        except KeyError:
            raise TypeError("Mapping for instruction %s: Cannot create mapping for trace-value %s. Trace-value does not exist (Make sure to add all trace-values to the trace-model before creating mappings)" %(self.name, trValName_))

        mapping = Mapping(trVal, Description(description_))
        self.mappings[trValName_] = mapping
        return mapping

    def getAllInstructions(self):
        return self.instructions
    
    def getAllMappings(self):
        return self.mappings.values()

    def getMapping(self, trVal_):

        try:
            return self.mappings[trVal_.name]
        except KeyError:
            return None
    
class Instruction(MetaTraceModel_base):

    def __init__(self, name_, type_):
        self.name = name_
        self.instructionType = type_
        
        super().__init__()

    def getAllMappings(self):
        return self.instructionType.getAllMappings()

    def getInstructionType(self):
        return self.instructionType
    
class TraceValue(MetaTraceModel_base):

    def __init__(self, name_, type_):
        self.name = name_
        self.dataType = type_
        
        super().__init__()

class Mapping(MetaTraceModel_base):

    def __init__(self, trVal_, descr_):
        self.traceValue = trVal_
        self.description = descr_
        
        super().__init__()

    def getTraceValue(self):
        return self.traceValue

    def getDescription(self):
        return self.description.resolved

    def getAllBitfields(self):
        return self.description.bitfields
    
class Description(MetaTraceModel_base):

    def __init__(self, orig_):
        self.original = orig_
        self.resolved = ""
        self.bitfields = []

    def createAndAddBitfield(self, name_):
        bf = Bitfield(name_)
        self.bitfields.append(bf)
        return bf

class Bitfield(MetaTraceModel_base):

    def __init__(self, name_):
        self.name = name_
        self.bitRanges = []

    def createAndAddBitRange(self, offset_, msb_, lsb_):
        br = BitRange(offset_, msb_, lsb_)
        self.bitRanges.append(br)
        return br

    def getAllBitRanges(self):
        return self.bitRanges

class BitRange(MetaTraceModel_base):

    def __init__(self, offset_, msb_, lsb_):
        self.offset = offset_
        self.msb = msb_
        self.lsb = lsb_
