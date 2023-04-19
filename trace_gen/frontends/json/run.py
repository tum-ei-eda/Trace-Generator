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
import pathlib
import pickle

from .Parser import Parser, M2isarmodel

def main(inFile_, model_path, core_name:str, outdir_=None):
    
    # Find pathes for json-description and output-directory
    inFile = pathlib.Path(inFile_).resolve()
    if outdir_ is not None:
        outdir = pathlib.Path(outdir_).resolve()
    else:
        outdir = None
    m2isar_model = pathlib.Path(model_path).resolve()

    # Parse json-description to trace-model
    print("")
    print("-- Generation TraceModel from JSON-file --")
    model = Parser().parse(inFile)

    # Load a specific core model from m2isarmodel file into this FE
    print("")
    print("-- Reading from m2isarmodel-file --")
    models = M2isarmodel().load_models(m2isar_model)
    instr = M2isarmodel().resolve_instruction(models, core_name) # ISA for the sepcific core name

    # Resolve descriptions in trace-model and parse bitfield and bitrange from m2isar-model to trace-model
    print("")
    print("-- Generating TraceModel: BifField and BitRange, from m2isarmodel --")
    Parser().resolveDescriptions(model, instr)
    
    if outdir is not None:
        print("")
        print("-- Storing model --")
        print("Out-directory: %s" %outdir)

        # Creating out-directory
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        # Make path for out-file
        outfile_name = 'trace.model'
        outfile = outdir / outfile_name
        print("File: %s" % outfile_name)
        if outfile.is_file():
            print("\tFile exists and will be replaced!")
            # TODO: Add possibility for user to aboard overwrite?
            
        # Dump model to file
        with outfile.open('wb') as f:
            pickle.dump(model, f)

    return model
            
# Run this if called stand-alone (i.e. this file is directly called)
if __name__ == '__main__':

    argParser = argparse.ArgumentParser()
    argParser.add_argument("input_file", help="Path to file containing the json description of the trace.")
    argParser.add_argument("-o", "--output_dir", help="Directory to store generated trace-model.")
    argParser.add_argument("m2isar_model", help="Path to m2isarmodel-file.")
    argParser.add_argument("core_name", help="A specific core name in the m2isarmodel.")
    args = argParser.parse_args()
    
    main(args.input_file, args.m2isar_model, args.core_name, args.output_dir)
