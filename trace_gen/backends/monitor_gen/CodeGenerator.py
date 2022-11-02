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

from mako.template import Template

from .MonitorBuilder import MonitorBuilder as Builder

class CodeGenerator:

    def __init__(self, templateDir_, outDir_):
        self.templateDir_monitor = templateDir_ / "monitor"
        self.templateDir_printer = templateDir_ / "printer"
        self.outDirBase_monitor = outDir_ / "monitor"
        self.outDirBase_printer = outDir_ / "printer"
        
    def generateMonitor(self, traceModel_):

        self.__generateTraceChannel(traceModel_)
        self.__generateMonitor(traceModel_)
        self.__generateInstructionMonitors(traceModel_)

    def generatePrinter(self, traceModel_):

        self.__generatePrinter(traceModel_)
        self.__generateInstructionPrinters(traceModel_)
        
    def __generateTraceChannel(self, traceModel_):

        template = Template(filename = str(self.templateDir_monitor) + "/include/channel.mako")
        code = template.render(**{"traceModel_" : traceModel_, "builder_" : Builder(traceModel_.name)})

        outFile = self.outDirBase_monitor / "include" / (traceModel_.name + "_Channel.h")
        with outFile.open('w') as f:
            f.write(code)

    def __generateMonitor(self, traceModel_):

        template_header = Template(filename = str(self.templateDir_monitor) + "/include/monitor.mako")
        code_header = template_header.render(**{"traceModel_" : traceModel_})

        outFile_header = self.outDirBase_monitor / "include" / (traceModel_.name + "_Monitor.h")
        with outFile_header.open('w') as f:
            f.write(code_header)

        template_src = Template(filename = str(self.templateDir_monitor) + "/src/monitor.mako")
        code_src = template_src.render(**{"traceModel_" : traceModel_, "builder_" : Builder(traceModel_.name)})

        outFile_src = self.outDirBase_monitor / "src" / (traceModel_.name + "_Monitor.cpp")
        with outFile_src.open('w') as f:
            f.write(code_src)

    def __generateInstructionMonitors(self, traceModel_):

        template = Template(filename = str(self.templateDir_monitor) + "/src/instructionMonitors.mako")
        code = template.render(**{"traceModel_" : traceModel_, "builder_" : Builder(traceModel_.name)})

        outFile = self.outDirBase_monitor / "src" / (traceModel_.name + "_InstructionMonitors.cpp")
        with outFile.open('w') as f:
            f.write(code)

    def __generatePrinter(self, traceModel_):

        template_header = Template(filename = str(self.templateDir_printer) + "/include/printer.mako")
        code_header = template_header.render(**{"traceModel_" : traceModel_})

        outFile_header = self.outDirBase_printer / "include" / (traceModel_.name + "_Printer.h")
        with outFile_header.open('w') as f:
            f.write(code_header)

        template_src = Template(filename = str(self.templateDir_printer) + "/src/printer.mako")
        code_src = template_src.render(**{"traceModel_" : traceModel_})

        outFile_src = self.outDirBase_printer / "src" / (traceModel_.name + "_Printer.cpp")
        with outFile_src.open('w') as f:
            f.write(code_src)

    def __generateInstructionPrinters(self, traceModel_):

        template = Template(filename = str(self.templateDir_printer) + "/src/instructionPrinters.mako")
        code = template.render(**{"traceModel_" : traceModel_})
        
        outFile = self.outDirBase_printer / "src" / (traceModel_.name + "_InstructionPrinters.cpp")
        with outFile.open('w') as f:
            f.write(code)
