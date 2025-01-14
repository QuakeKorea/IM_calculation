##############################################################################################################
# Reagan Chandramohan                                                                                        #
# John A. Blume Earthquake Engineering Center                                                                #
# Stanford University                                                                                        #
# Last edited: 28-Jul-2016                                                                                   #
##############################################################################################################

# Script called from "run_ida_mp_hpc.tcl".
# Define recorders and run one ground motion at one Sa(T1) level.

##############################################################################################################

# Define the recorder directory
set recorderdir $outpath/$indir/$outfilename/SaT1_[format "%.5f" $sat1]
file mkdir $recorderdir

# Define drift recorders for all stories
#set dt_rec 0.01
#recorder Node -file $recorderdir/story1_disp.out -time -dT $dt_rec -node [lindex $ctrl_nodes 1] -dof 1 disp
recorder EnvelopeDrift -file $recorderdir/story1_drift_env.out -iNode [lindex $ctrl_nodes 0] -jNode \
        [lindex $ctrl_nodes 1] -dof 1 -perpDirn 2
for {set story 2} {$story <= $num_stories} {incr story} {
#    recorder Node -file $recorderdir/story${story}_disp.out -dT $dt_rec -node [lindex $ctrl_nodes $story] \
#            -dof 1 disp
    recorder EnvelopeDrift -file $recorderdir/story${story}_drift_env.out -iNode [lindex $ctrl_nodes \
            [expr {$story - 1}]] -jNode [lindex $ctrl_nodes $story] -dof 1 -perpDirn 2
}

# Define the ground motion time series
timeSeries Path [expr {10 + $i}] -dt $dt -filePath $inpath/$indir/$filename -factor [expr {$g*$sat1/$sat1_gm}]
set eq_load_pattern 3
pattern UniformExcitation $eq_load_pattern 1 -accel [expr {10 + $i}]

# Define the time step used to run the analysis using the central difference scheme
#set dt_factor 0.8
#set periods_file [open $modeldir/Model_Info/periods.out]
#while {[gets $periods_file line] >= 0} {set period $line}
#close $periods_file
#set dt_analysis [expr {$dt_factor*$period/$pi}]
set dt_analysis 1.5e-4

# Initialize the analysis parameters and run the analysis. Check whether the structure has collapsed after
# every ground motion second and halt the analysis if it has. Also send and receive a message from the master
# process to check if the analysis is to be deleted and aborted.
constraints Transformation
numberer RCM
system SparseGEN
algorithm Linear
integrator CentralDifference
analysis Transient

set gm_length [expr {($numpts - 1)*$dt}]
set total_steps [expr {int($gm_length/$dt_analysis)}]
set steps_per_batch [expr {int(1.0/$dt_analysis)}]
set collapse_flag false
set abort_flag false

for {set steps_run 0} {$steps_run < $total_steps} {incr steps_run $steps_per_batch} {
    set fail [analyze $steps_per_batch $dt_analysis]

    if {$fail} {
        set max_drift inf
        set collapse_flag true
        break
    } else {
        set max_drift [max_drift_model $ctrl_nodes]
        if {$max_drift >= $col_drift} {
            set collapse_flag true
            break
        }
    }
    
    send -pid 0 "$this_procid $gm $sat1 $stage STATUS"
    recv -pid 0 command
    if {$command == "ABORT"} {
        set abort_flag true
        file delete -force $recorderdir
        break
    }
}

# Compute the peak story drift from the recorder files if the structure hasn't collapsed and the analysis
# wasn't aborted
if {!$collapse_flag && !$abort_flag} {
    set max_drift [max_drift_outfile $recorderdir $num_stories]
}

# Delete the recorded data
file delete -force $recorderdir
