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

class CodeBuilder:
# The idea of this class is to contain output code specific
# information (e.g. channel sizes, naming conventions, etc)

    __MAX_STRING_SIZE = 20
    __MAX_INT_SIZE = 8
    __CHANNEL_SIZE = 100
    
    def __init__(self, modelName_):
        self.modelName = modelName_

    def getMaxStringSize(self):
        return self.__MAX_STRING_SIZE

    def getChannelSize(self):
        return self.__CHANNEL_SIZE

    def getBufferName(self, trVal_):
        return (self.__getMonitorPrefix() + trVal_ + "_buffer")

    def getInstrCntName(self):
        return (self.__getMonitorPrefix() + "instrCnt")

    def getStreamSetup(self, type_):
        if(type_ == "int"):
            return self.__getStreamSetupInt()
        elif(type_ == "string"):
            return self.__getStreamSetupString()
        else:
            raise TypeError("Cannot call CodeBuilder::getStreamSetup with type %s" %type_)

    def getEmptyStream(self, type_):
        if(type_ == "int"):
            return self.__getEmptyStreamWithSize(self.__MAX_INT_SIZE + 2)
        elif(type_ == "string"):
            return self.__getEmptyStreamWithSize(self.__MAX_STRING_SIZE)
        else:
            raise TypeError("Cannot call CodeBuilder::getStreamSetup with type %s" %type_)

    def getEoL(self):
        return "\" \""
        
    ## HELPER FUNCTIONS
    
    def __getMonitorPrefix(self):
        return (self.modelName + "_Monitor_")

    def __getStreamSetupInt(self):
        return ("\"0x\" << std::setfill(\'0\') << std::setw(" + str(self.__MAX_INT_SIZE) + ") << std::right << std::hex")

    def __getStreamSetupString(self):
        return ("std::setfill(\' \') << std::setw(" + str(self.__MAX_STRING_SIZE) + ") << std::left")
    
    def __getEmptyStreamWithSize(self, size_):
        return ("std::setfill(\'-\') << std::setw(" + str(size_) + ") << \"\"")
