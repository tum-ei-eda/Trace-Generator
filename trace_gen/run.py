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

#!/usr/bin/env python3

import argparse
import sys
import pathlib

import frontends.json.run as frontend
import backends.monitor_gen.run as backend
from common import common as cf

# Read command line arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("description", help="File containing the trace description")
argParser.add_argument("-o", "--outDir", help="Path to the output directory")
args = argParser.parse_args()

# Evaluate output path
outDir = cf.resolveOutDir(args.outDir)

# Call frontend to create traceModel
if args.description.endswith('.json'):
    traceModel = frontend.main(args.description)
else:
    sys.exit("FATAL: Descritption format is not supported. Currently only supporting files of type .json")

# Call backend
backend.main(traceModel, outDir)
