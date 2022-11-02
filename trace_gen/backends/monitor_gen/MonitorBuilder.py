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

class MonitorBuilder:

    __MAX_STRING_SIZE = 100
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

    def __getMonitorPrefix(self):
        return (self.modelName + "_Monitor_")
        
    
