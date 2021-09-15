# ----Units&Constants.tcl---------------------------------------------------------
# Use constants from http://www.wsdot.wa.gov/Metrics/factors.htm
# define basic units  
set m 1.;			
set sec 1.;
set kN 1.;  
set rad 1.;
# what is my mass unit? 
# Must be such that we must have [force unit] = [mass unit] * [record accel unit]
# Using the factors here, the acceleration will always become m/s^2 (even if in "g"), so
# 1kN= [mass unit] * 1 m/s^2  <=> [mass unit] =  1 kN *s^2 / 1 m
#                                             =  [1000 kg * m/s^2] *s^2/ m
#                                             =  1000 kg
# so the mass unit is the ton or the Mg. Of course I could have set directly
# set ton 
set ton  1. ;
set Mg  $ton;

# define derivative metric units
set kg [expr $ton/1000.];
set kPa [expr $kN/pow($m,2)];
set cm  [expr $m/100.];		
set mm [expr $m/1000.];
set Pa  [expr $kPa/1000.];
set MPa [expr 1000.*$kPa];
set GPa [expr 1000.*$MPa];
set N [expr $kN/1000.];
set MN [expr $kN*1000.];
set kgf [expr 9.81*$N] ;   # kilogram of force
set tnf [expr 1000.*$kgf] ;   # ton of force
set cm2 [expr $cm*$cm];
set cm4 [expr $cm2*$cm2];
set m2  [expr $m*$m];
set m3  [expr $m2*$m];
set m4  [expr $m2*$m2];
set mm2 [expr $mm*$mm];
set mm4 [expr $mm2*$mm2];
# define Imperial dependent units
set in   [expr 2.54*$cm];
set in2   [expr $in*$in];
set in3   [expr $in2*$in];
set in4   [expr $in2*$in2];
set ft [expr 12.*$in];
set lbm [expr $kg*0.4536];   # 1 pound of mass
set lbf [expr $N*4.448222];  # 1 pound of force
set kipf [expr $lbf*1000];    # classic force unit for struct. engineering
set kipm [expr $lbm*1000];    # classic mass unit
set kipsec2_ft [expr $kipf*$sec*$sec/$ft]; # classic mass unit in struct engineering 
set Ksi  [expr 6894.757*$kPa];
set psi  [expr 6.894757*$kPa];
set psfm  [expr 4.8824*$kg/$m2]; # pound of mass per sq.foot
set psff  [expr 47.88*$Pa]; # pound of force per sq.foot

#puts "$kipsec2_ft"
#puts "$ft"

# define constants
set pi [expr 2.*asin(1.0)];		
set g [expr 9.81*$m/pow($sec,2)];
set U 	1.e10;		# a really large number
set u 	[expr 1./$U];	# a really small number
