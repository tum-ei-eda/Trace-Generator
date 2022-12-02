<%page args="map_=None, builder_=None" />
    % for bf_i in map_.getAllBitfields():
    int ${bf_i.name} = 0;
    % for br_i in bf_i.getAllBitRanges():
    static etiss::instr::BitArrayRange R_${bf_i.name}_${br_i.offset}(${br_i.msb},${br_i.lsb});
    ${bf_i.name} += R_${bf_i.name}_${br_i.offset}.read(ba) << ${br_i.offset};
    % endfor
    % endfor
    % if map_.getTraceValue().dataType == "int":
    ret_strs << "${builder_.getBufferName(map_.getTraceValue().name)}[*${builder_.getInstrCntName()}] = " << ${builder_.getDescriptionString(map_.getDescription())} << ";\n";
    % elif map_.getTraceValue().dataType == "string":
    ret_strs << "strcpy(${builder_.getBufferName(map_.getTraceValue().name)}[*${builder_.getInstrCntName()}],\"" << ${builder_.getDescriptionString(map_.getDescription())} << "\");\n";
    % endif