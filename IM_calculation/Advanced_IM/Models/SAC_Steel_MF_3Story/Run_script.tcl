
if { $argc != 2 } {
    puts "The add.tcl script requires arguments."
    puts "For example, tclsh add.tcl event_name".
    puts "Please try again."
} else {
    set GM_path [lindex $argv 0]
     puts "GM_path = $GM_path"
    
    set Output_path [lindex $argv 1]	
    puts "Output_path = $Output_path" 			
     			
    }

puts "Start Analyzing..."
set FEMs Sac_Steel_MF_3Story 

puts "FEMs=$FEMs"
puts " "
puts "-------------------------------"
puts " "  	
source [file join [file dirname [info script]] ../general/GMs.tcl]
puts " "
puts [file join [file dirname [info script]]]
puts "-------------------------------"

source [file join [file dirname [info script]] Original/constants_units_kip_in.tcl]	
source [file join [file dirname [info script]] Original/create_steel_mf_model.tcl]
source [file join [file dirname [info script]] Original/models/frame_data.tcl]	
CreateSteelMFModel [file join [file dirname [info script]] Original/models/frame_data.tcl] $FEMs $Output_path

source [file join [file dirname [info script]] ../general/Period.tcl]

source [file join [file dirname [info script]] Recorders.tcl]
source [file join [file dirname [info script]] ../general/Rha.tcl]

puts " "
puts "---------------------------------------------------------------------------"
puts " "

wipe
