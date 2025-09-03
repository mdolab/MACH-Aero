#
# Copyright 2014 (c) Pointwise, Inc.
# All rights reserved.
#
# This sample Pointwise script is not supported by Pointwise, Inc.
# It is provided freely for demonstration purposes only.
# SEE THE WARRANTY DISCLAIMER AT THE BOTTOM OF THIS FILE.
#

#############################################################################
##
## SemiCircle.glf
##
## CREATE STRUCTURED TOPOLOGY FROM TWO SELECTED CONNECTORS
## 
## This script automates the creation of six structured domains from two 
## user-specified connectors. In addition to creating the new topology when 
## possible (edge dimensions must both be odd), the elliptic solver is run
## for 10 iterations, allowing the newly generated domains to relax to an
## optimal configuration. Note that an initial dimension can be even and used,
## but the dimension will be changed when input(AutoDim) is set to 1 before
## proceeding.
## 
## For maximum productivity, a GUI is included, but can easily be disabled. 
## Set input(GUI) to 1 on line 39 to enable control over internal dimension.
## Otherwise, simply select three connectors and run the script. The internal
## dimension will be automatically set to an optimal value.
## 
#############################################################################

package require PWI_Glyph 2.3

## Set global parameters
## Default solve resulting grids or not
set input(Solve) 1
## Automatically increment even-dimensioned connectors
set input(AutoDim) 1
## Enable (1)/Disable (0) GUI
set input(GUI) 0

## Switch that interpolates gridline angles on outer edges, should remain 
## set to 1 for most applications.
set interpAngles 1

## Check that connectors form singly-connected loop
proc isLoop { conList } {
  set e [pw::Edge createFromConnectors -single $conList]
  if { [llength $e] != 1 } {
    foreach edge $e {
      $edge delete
    }
    return 0
  }
  
  set chkVal [$e isClosed]
  $e delete

  return $chkVal
}

## Return connectors adjacent to specified node that are also in the list $cons
proc getAdjCons { node cons } {
    set list1 [$node getConnectors]
    set list2 $cons
    
    set relCons [list]
    foreach ll $list1 {
        if {[lsearch -exact $list2 $ll]!=-1} {
            lappend relCons [list $ll]
        }
    }
    
    return $relCons
}

## Create two point connector given two points with dimension $dim
proc createTwoPt { pt1 pt2 dim } {
    set creator [pw::Application begin Create]
        set con [pw::Connector create]
        set seg [pw::SegmentSpline create]
        $seg addPoint $pt1
        $seg addPoint $pt2
        $con addSegment $seg
    $creator end
    $con setDimension $dim
    return $con
}

## Calculate split locations for three connectors to create TriQuad domain
proc splitTri { conList } {
    set c1 [lindex $conList 0]
    set c2 [lindex $conList 1]
    set c3 [lindex $conList 2]
    
    set L1 [expr [$c1 getDimension] - 1 ]
    set L2 [expr [$c2 getDimension] - 1 ]
    set L3 [expr [$c3 getDimension] - 1 ]
    
    if { $L1 < [expr $L2 + $L3] } {
        set cond1 1
    } else { set cond1 0 }
    if { $L2 < [expr $L1 + $L3] } {
        set cond2 1
    } else { set cond2 0 }
    if { $L3 < [expr $L1 + $L2] } {
        set cond3 1
    } else { set cond3 0 }
    
    
    if { $cond1 && $cond2 && $cond3 } {
        set a [expr {($L1+$L3-$L2)/2. + 1}]
        set b [expr {($L1+$L2-$L3)/2. + 1}]
        set c [expr {($L2+$L3-$L1)/2. + 1}]
    
        if { $a == [expr int($a)] } {
            set cc1 1
            set a [expr int($a)]
        } else { set cc1 0 }
        if { $b == [expr int($b)] } {
            set cc2 1
            set b [expr int($b)]
        } else { set cc2 0 }
        if { $c == [expr int($c)] } {
            set cc3 1
            set c [expr int($c)]
        } else { set cc3 0 }
        
        if { $cc1 && $cc2 && $cc3 } {
            set pt1 [$c1 getXYZ -grid $b]
            set pt2 [$c2 getXYZ -grid $c]
            set pt3 [$c3 getXYZ -grid $a]
            
            lappend splCon [$c1 split -I $b]
            lappend splCon [$c2 split -I $c]
            lappend splCon [$c3 split -I $a]
            
            return [list [list $a $b $c] [list $pt1 $pt2 $pt3] $splCon]
        } else { 
            ## dimensions not even
            return -1
        }
    } else {
        ## One dimension is too large
        return -2
    }
}

## Create domains
proc createTopo { pts dims outerCons } {
    global input

    set pt0 [lindex $pts 0]
    set pt1 [lindex $pts 1]
    set pt2 [lindex $pts 2]
    
    set temp1 [pwu::Vector3 add $pt0 $pt1]
    set temp2 [pwu::Vector3 add $temp1 $pt2]
    set cntr [pwu::Vector3 divide $temp2 3.0]
    
    set nc1 [createTwoPt $pt0 $cntr [lindex $dims 2]]
    set nc2 [createTwoPt $pt1 $cntr [lindex $dims 0]]
    set nc3 [createTwoPt $pt2 $cntr [lindex $dims 1]]
    
    set conList [list $nc1 $nc2 $nc3]
    foreach oc $outerCons {
        foreach c $oc {
            lappend conList $c
        }
    }
    
    set doms [pw::DomainStructured createFromConnectors $conList]
    
    if $input(Solve) {
        solve_Grid $cntr $doms 10
    } else {
        solve_Grid $cntr $doms 0
    }
    
    return $doms
}

## Run elliptic solver for 10 interations with floating BC on interior lines to 
## smooth grid
proc solve_Grid { cntr doms num } {
    global interpAngles
    
    set solver_mode [pw::Application begin EllipticSolver $doms]
        if {$interpAngles == 1} {
            foreach ent $doms {
                foreach bc [list 1 2 3 4] {
                    $ent setEllipticSolverAttribute -edge $bc \
                        EdgeAngleCalculation Interpolate
                }
            }
        }
        
        for {set ii 0} {$ii<3} {incr ii} {
            set tempDom [lindex $doms $ii]
            set inds [list]
            for {set jj 1 } {$jj <= 4 } {incr jj} {
                set tmpEdge [$tempDom getEdge $jj]
                set n1 [$tmpEdge getNode Begin]
                set n2 [$tmpEdge getNode End]
                set c1 [pwu::Vector3 equal -tolerance 1e-6 [$n1 getXYZ] $cntr]
                set c2 [pwu::Vector3 equal -tolerance 1e-6 [$n2 getXYZ] $cntr]
                if { $c1 || $c2 } {
                    lappend inds [list $jj]
                }
            }
            set temp_list [list]
            for {set jj 0} {$jj < [llength $inds] } {incr jj} {
                lappend temp_list [list $tempDom]
            }
            foreach ent $temp_list bc $inds {
                $ent setEllipticSolverAttribute -edge $bc \
                    EdgeConstraint Floating
                $ent setEllipticSolverAttribute -edge $bc \
                    EdgeAngleCalculation Orthogonal
            }
        }
        
        $solver_mode run $num
    $solver_mode end
    
    return
}

## Since final grid is actually two TriQuad grids, can run smoother on all 
## domains at very end.
proc solve_All { doms num } {
    set solver_mode [pw::Application begin EllipticSolver $doms]
    
        foreach ent $doms {
            foreach bc [list 1 2 3 4] {
                $ent setEllipticSolverAttribute -edge $bc \
                    EdgeConstraint Floating
            }
        }
        
        $solver_mode run $num
    $solver_mode end
    
    return
}

## Main procedure to split two connectors into half-OH topology
proc splitSemiCircle { cons } {
    global input newDoms lowerBound upperBound

    set con(1) [lindex $cons 0]
    set con(2) [lindex $cons 1]
    
    set L1 [$con(1) getLength -arc 1.0]
    set L2 [$con(2) getLength -arc 1.0]

    if {$L2 > $L1} { 
        set sE 1
        set lE 2
    } else { 
        set sE 2 
        set lE 1
    }
    
    set N1 [$con($sE) getDimension]
    set N2 [$con($lE) getDimension]
    
    ## Check parity. If both are odd, no problem, otherwise, connectors must 
    ## be split. Even-dimensioned connectors pose problems. Either re-dimension
    ## or exclude. input(AutoDim) will automatically increase their dimension.
    if {[expr $N1%2]==0 || [expr $N2%2] == 0 } {
        puts "Inconsistent Dimension."
        if { !$input(AutoDim) } { exit }
        
        set dimMode [pw::Application begin Dimension]
        if {[expr $N1%2] == 0} {
            incr N1
            $con($sE) resetGeneralDistributions
            $con($sE) setDimension $N1
            $dimMode balance -resetGeneralDistributions
            puts "Re-dimensioned [$con($sE) getName]."
        }
        
        if {[expr $N2%2] == 0} {
            incr N2
            $con($lE) resetGeneralDistributions
            $con($lE) setDimension $N2
            $dimMode balance -resetGeneralDistributions
            puts "Re-dimensioned [$con($lE) getName]."
        }
        $dimMode end
    }
    
    ## Exit if dimensions are too small to support split operations
    if { $N1 < 5 || $N2 < 5 } { 
        puts "Dimension too small."
        exit 
    }
    
    set N1_split [expr ($N1-1)/2+1]
    set N2_split [expr ($N2-1)/2+1]
  
    set lowerBound [expr abs($N2_split-$N1_split)+2]
    set upperBound [expr $N1_split+$N2_split-3]
    set w(Message) [list $lowerBound $upperBound]
    
    set N3 [expr $lowerBound+$upperBound]
    if { [expr $N3%2] != 0 } { incr N3 }
    set input(sDim) [expr $N3/2]
    
    set node1 [$con($sE) getNode Begin]
    set node2 [$con($sE) getNode End]
    
    set param1 [$con($sE) getParameter -closest [pw::Application getXYZ [$con($sE) getXYZ -arc 0.5]]]
    set tmp_cons1 [$con($sE) split $param1]
    
    set param2 [$con($lE) getParameter -closest [pw::Application getXYZ [$con($lE) getXYZ -arc 0.5]]]
    set tmp_cons2 [$con($lE) split $param2]
    
    set pt1 [[lindex $tmp_cons2 0] getXYZ -arc 1.0]
    set pt2 [[lindex $tmp_cons1 0] getXYZ -arc 1.0]
    
    ## Enable GUI if desired
    if $input(GUI) {
        makeWindow
        tkwait window .top
    }
    
    ## Retrieve calculated/specified value for the splitting connector dimension
    set midDim $input(sDim)
    
    if {[expr (($N1+1)/2+($N2+1)/2+$midDim)%2]==0} {incr midDim}
    set midCon1 [createTwoPt $pt1 $pt2 $midDim]
    
    set list1 [getAdjCons $node1 [concat $tmp_cons1 $tmp_cons2]]
    $midCon1 alignOrientation $list1
    lappend list1 [list $midCon1]
    
    ## Attempt splitting operation
    set temp [splitTri $list1]

    ## Check results of split
    if {$temp != -1 && $temp != -2} {
        set dims [lindex $temp 0]
        set pts [lindex $temp 1]
        set splCons [lindex $temp 2]
        
        set doms1 [createTopo $pts $dims $splCons]
    } elseif {$temp == -1} { 
        puts "Unable to match dimensions, check edge dimensions."
        puts "Sum of three connector dimensions must be odd."
        exit 
    } else {
        puts "Unable to match dimensions, check edge dimensions."
        puts "No edge may have a dimension longer than the sum of the other two."
    }
    
    set midCon2 [createTwoPt $pt1 $pt2 $midDim]
    
    set list2 [getAdjCons $node2  [concat $tmp_cons1 $tmp_cons2]]
    $midCon2 alignOrientation $list2
    lappend list2 [list $midCon2]
    
    ## Attempt splitting operation
    set temp2 [splitTri $list2]

    ## Check results of split
    if {$temp2 != -1 && $temp2 != -2} {
        set dims [lindex $temp2 0]
        set pts [lindex $temp2 1]
        set splCons [lindex $temp2 2]
        
        set doms2 [createTopo $pts $dims $splCons]
    } elseif {$temp2 == -1} { 
        puts "Unable to match dimensions, check edge dimensions."
        puts "Sum of three connector dimensions must be odd."
        exit 
    } else {
        puts "Unable to match dimensions, check edge dimensions."
        puts "No edge may have a dimension longer than the sum of the other two."
    }
    
    set newDoms [concat $doms1 $doms2]
    
    if $input(Solve) { 
        solve_All $newDoms 5 
    } else { 
        solve_All $newDoms 0 
    }
    
    return
}

###########################################################################
## GUI 
###########################################################################
## Load TK
if {$input(GUI)} {
    pw::Script loadTk

    # Initialize globals
    set infoMessage ""

    set color(Valid)   SystemWindow
    set color(Invalid) MistyRose

    set w(Window)           [tk::toplevel .top]
    set w(LabelTitle)           .top.title
    set w(FrameMain)          .top.main
      set w(LabelDimension)     $w(FrameMain).ldim
      set w(EntryDimension)     $w(FrameMain).edim
      set w(LabelSolve)            $w(FrameMain).lslv
      set w(EntrySolve)            $w(FrameMain).eslv
      set w(ButtoncOH)            $w(FrameMain).doit
    set w(FrameButtons)      .top.fbuttons
      set w(Logo)                   $w(FrameButtons).pwlogo
      set w(ButtonCancel)        $w(FrameButtons).bcancel
    set w(Message)             .top.msg

    # dimension field validation
    proc validateDim { dim widget } {
      global w color input lowerBound upperBound
      
      if { [string is integer -strict $dim] && $dim >= $lowerBound && $dim <= $upperBound } {
        $w($widget) configure -background $color(Valid)
      } else {
        $w($widget) configure -background $color(Invalid)
      }
      updateButtons
      return 1
    }

    # return true if none of the entry fields are marked invalid
    proc canCreate { } {
      global w color
      return [expr \
        [string equal -nocase [$w(EntryDimension) cget -background] $color(Valid)]]
    }

    # enable/disable action buttons based on current settings
    proc updateButtons { } {
      global w infoMessage lowerBound upperBound

      if { [canCreate] } {
        $w(ButtoncOH) configure -state normal
        set infoMessage "Press Create OH"
      } else {
        $w(ButtoncOH) configure -state disabled
        set infoMessage "Enter integer between $lowerBound and $upperBound"
      }
      update
    }

    # set the font for the input widget to be bold and 1.5 times larger than
    # the default font
    proc setTitleFont { l } {
      global titleFont
      if { ! [info exists titleFont] } {
        set fontSize [font actual TkCaptionFont -size]
        set titleFont [font create -family [font actual TkCaptionFont -family] \
            -weight bold -size [expr {int(1.5 * $fontSize)}]]
      }
      $l configure -font $titleFont
    }

    ###############################################################################
    # pwLogo: Define pointwise logo
    ###############################################################################
    proc pwLogo {} {
      set logoData {
    R0lGODlheAAYAIcAAAAAAAICAgUFBQkJCQwMDBERERUVFRkZGRwcHCEhISYmJisrKy0tLTIyMjQ0
    NDk5OT09PUFBQUVFRUpKSk1NTVFRUVRUVFpaWlxcXGBgYGVlZWlpaW1tbXFxcXR0dHp6en5+fgBi
    qQNkqQVkqQdnrApmpgpnqgpprA5prBFrrRNtrhZvsBhwrxdxsBlxsSJ2syJ3tCR2siZ5tSh6tix8
    ti5+uTF+ujCAuDODvjaDvDuGujiFvT6Fuj2HvTyIvkGKvkWJu0yUv2mQrEOKwEWNwkaPxEiNwUqR
    xk6Sw06SxU6Uxk+RyVKTxlCUwFKVxVWUwlWWxlKXyFOVzFWWyFaYyFmYx16bwlmZyVicyF2ayFyb
    zF2cyV2cz2GaxGSex2GdymGezGOgzGSgyGWgzmihzWmkz22iymyizGmj0Gqk0m2l0HWqz3asznqn
    ynuszXKp0XKq1nWp0Xaq1Hes0Xat1Hmt1Xyt0Huw1Xux2IGBgYWFhYqKio6Ojo6Xn5CQkJWVlZiY
    mJycnKCgoKCioqKioqSkpKampqmpqaurq62trbGxsbKysrW1tbi4uLq6ur29vYCu0YixzYOw14G0
    1oaz14e114K124O03YWz2Ie12oW13Im10o621Ii22oi23Iy32oq52Y252Y+73ZS51Ze81JC625G7
    3JG825K83Je72pW93Zq92Zi/35G+4aC90qG+15bA3ZnA3Z7A2pjA4Z/E4qLA2KDF3qTA2qTE3avF
    36zG3rLM3aPF4qfJ5KzJ4LPL5LLM5LTO4rbN5bLR6LTR6LXQ6r3T5L3V6cLCwsTExMbGxsvLy8/P
    z9HR0dXV1dbW1tjY2Nra2tzc3N7e3sDW5sHV6cTY6MnZ79De7dTg6dTh69Xi7dbj7tni793m7tXj
    8Nbk9tjl9N3m9N/p9eHh4eTk5Obm5ujo6Orq6u3t7e7u7uDp8efs8uXs+Ozv8+3z9vDw8PLy8vL0
    9/b29vb5+/f6+/j4+Pn6+/r6+vr6/Pn8/fr8/Pv9/vz8/P7+/gAAACH5BAMAAP8ALAAAAAB4ABgA
    AAj/AP8JHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNqZCioo0dC0Q7Sy2btlitisrjpK4io4yF/
    yjzKRIZPIDSZOAUVmubxGUF88Aj2K+TxnKKOhfoJdOSxXEF1OXHCi5fnTx5oBgFo3QogwAalAv1V
    yyUqFCtVZ2DZceOOIAKtB/pp4Mo1waN/gOjSJXBugFYJBBflIYhsq4F5DLQSmCcwwVZlBZvppQtt
    D6M8gUBknQxA879+kXixwtauXbhheFph6dSmnsC3AOLO5TygWV7OAAj8u6A1QEiBEg4PnA2gw7/E
    uRn3M7C1WWTcWqHlScahkJ7NkwnE80dqFiVw/Pz5/xMn7MsZLzUsvXoNVy50C7c56y6s1YPNAAAC
    CYxXoLdP5IsJtMBWjDwHHTSJ/AENIHsYJMCDD+K31SPymEFLKNeM880xxXxCxhxoUKFJDNv8A5ts
    W0EowFYFBFLAizDGmMA//iAnXAdaLaCUIVtFIBCAjP2Do1YNBCnQMwgkqeSSCEjzzyJ/BFJTQfNU
    WSU6/Wk1yChjlJKJLcfEgsoaY0ARigxjgKEFJPec6J5WzFQJDwS9xdPQH1sR4k8DWzXijwRbHfKj
    YkFO45dWFoCVUTqMMgrNoQD08ckPsaixBRxPKFEDEbEMAYYTSGQRxzpuEueTQBlshc5A6pjj6pQD
    wf9DgFYP+MPHVhKQs2Js9gya3EB7cMWBPwL1A8+xyCYLD7EKQSfEF1uMEcsXTiThQhmszBCGC7G0
    QAUT1JS61an/pKrVqsBttYxBxDGjzqxd8abVBwMBOZA/xHUmUDQB9OvvvwGYsxBuCNRSxidOwFCH
    J5dMgcYJUKjQCwlahDHEL+JqRa65AKD7D6BarVsQM1tpgK9eAjjpa4D3esBVgdFAB4DAzXImiDY5
    vCFHESko4cMKSJwAxhgzFLFDHEUYkzEAG6s6EMgAiFzQA4rBIxldExBkr1AcJzBPzNDRnFCKBpTd
    gCD/cKKKDFuYQoQVNhhBBSY9TBHCFVW4UMkuSzf/fe7T6h4kyFZ/+BMBXYpoTahB8yiwlSFgdzXA
    5JQPIDZCW1FgkDVxgGKCFCywEUQaKNitRA5UXHGFHN30PRDHHkMtNUHzMAcAA/4gwhUCsB63uEF+
    bMVB5BVMtFXWBfljBhhgbCFCEyI4EcIRL4ChRgh36LBJPq6j6nS6ISPkslY0wQbAYIr/ahCeWg2f
    ufFaIV8QNpeMMAkVlSyRiRNb0DFCFlu4wSlWYaL2mOp13/tY4A7CL63cRQ9aEYBT0seyfsQjHedg
    xAG24ofITaBRIGTW2OJ3EH7o4gtfCIETRBAFEYRgC06YAw3CkIqVdK9cCZRdQgCVAKWYwy/FK4i9
    3TYQIboE4BmR6wrABBCUmgFAfgXZRxfs4ARPPCEOZJjCHVxABFAA4R3sic2bmIbAv4EvaglJBACu
    IxAMAKARBrFXvrhiAX8kEWVNHOETE+IPbzyBCD8oQRZwwIVOyAAXrgkjijRWxo4BLnwIwUcCJvgP
    ZShAUfVa3Bz/EpQ70oWJC2mAKDmwEHYAIxhikAQPeOCLdRTEAhGIQKL0IMoGTGMgIBClA9QxkA3U
    0hkKgcy9HHEQDcRyAr0ChAWWucwNMIJZ5KilNGvpADtt5JrYzKY2t8nNbnrzm+B8SEAAADs=}

      return [image create photo -format GIF -data $logoData]
    }

    # Build the user interface
    proc makeWindow { } {
      global w input cons
      
      wm withdraw .

      # Ceate the widgets
      label $w(LabelTitle) -text "Semi-Circle Parameters"
      setTitleFont $w(LabelTitle)

      frame $w(FrameMain)

      label $w(LabelDimension) -text "Cross dimension:" -anchor e
      entry $w(EntryDimension) -width 6 -bd 2 -textvariable input(sDim)
      $w(EntryDimension) configure -state disabled

      label $w(LabelSolve) -text "Run solver?" -padx 2 -anchor e
      checkbutton $w(EntrySolve) -variable input(Solve)
      $w(EntrySolve) configure -state disabled
      
      button $w(ButtoncOH) -text "Create Topo" -command { destroy .top }
      $w(ButtoncOH) configure -state disabled

      message $w(Message) -textvariable infoMessage -background beige \
                          -bd 2 -relief sunken -padx 5 -pady 5 -anchor w \
                          -justify left -width 300

      frame $w(FrameButtons) -relief sunken

      button $w(ButtonCancel) -text "Cancel" -command { destroy . }
      label $w(Logo) -image [pwLogo] -bd 0 -relief flat

      # set up validation after all widgets are created so that they all exist when
      # validation fires the first time; if they don't all exist, updateButtons
      # will fail
      $w(EntryDimension) configure -validate key \
        -vcmd { validateDim %P EntryDimension }

      # lay out the form
      pack $w(LabelTitle) -side top
      pack [frame .sp -bd 1 -height 2 -relief sunken] -pady 4 -side top -fill x
      pack $w(FrameMain) -side top -fill both -expand 1

      # lay out the form in a grid
      grid $w(LabelDimension) $w(EntryDimension) -sticky ew -pady 3 -padx 3
      grid $w(LabelSolve) $w(EntrySolve) -sticky ew -pady 3 -padx 3
      grid $w(ButtoncOH) -columnspan 2 -pady 3

      # give all extra space to the second (last) column
      grid columnconfigure $w(FrameMain) 1 -weight 1

      pack $w(Message) -side bottom -fill x -anchor s
      pack $w(FrameButtons) -fill x -side bottom -padx 2 -pady 4 -anchor s
      pack $w(ButtonCancel) -side right -padx 2
      pack $w(Logo) -side left -padx 5

      bind .top <Key-Escape> { $w(ButtonCancel) invoke }
      bind .top <Control-Key-Return> { $w(ButtoncOH) invoke }
      bind .top <Control-Key-f> { $w(ButtoncOH) invoke }
      bind $w(EntryDimension) <Key-Return> { $w(ButtoncOH) invoke }

      # move keyboard focus to the first entry
      focus $w(ButtoncOH)
      raise .top
      
      $w(EntryDimension) configure -state normal
      $w(EntrySolve) configure -state normal
      updateButtons
      
    }
}

## Set Info label
set text1 "Please select two connectors or one unstructured domain."
## Pull entities from current selection
set mask [pw::Display createSelectionMask -requireDomain {Unstructured} -requireConnector {}]

###############################################
## This script uses the getSelectedEntities command added in 17.2R2
## Catch statement should check for previous versions
if { [catch {pw::Display getSelectedEntities -selectionmask $mask curSelection}] } {
    set picked [pw::Display selectEntities -description $text1 \
        -selectionmask $mask curSelection]
    
    if {!$picked} {
        puts "Script aborted."
        exit
    }
} elseif { [llength $curSelection(Connectors)] != 2 && \
        [llength $curSelection(Domains)] != 1 } {
    puts $text1
    exit
}
###############################################

## First check for unstructured domain in selection. If so, replace with half-OH
if {[llength $curSelection(Domains)]==1} {
    set tempDom [lindex $curSelection(Domains) 0]
    set edgeCount [$tempDom getEdgeCount]
    if { $edgeCount != 1 } {
        puts "Domain has multiple edges."
        exit
    }
    
    set temp [$tempDom getEdge 1]
    set conCount [$temp getConnectorCount]
    if { $conCount != 2 } {
        puts "Domain edge has more than 2 connectors."
        exit
    }
    
    set cons [list [$temp getConnector 1] [$temp getConnector 2]]
    
    set domStatus [list [$tempDom getRenderAttribute LineMode]\
        [$tempDom getRenderAttribute FillMode]]
    
    set newDoms [splitSemiCircle $cons]
    
    pw::Entity delete $tempDom
    foreach dd $newDoms {
        $dd setRenderAttribute LineMode [lindex $domStatus 0]
        $dd setRenderAttribute FillMode [lindex $domStatus 1]
    }
    
    exit
    
} elseif {[llength $curSelection(Connectors)]==2} {
    set bool [isLoop $curSelection(Connectors)]
    
    if $bool {
        set cons $curSelection(Connectors)
        set newDoms [splitSemiCircle $curSelection(Connectors)]
    } else {
        puts "Connectors do not form closed loop."
    }
    
    exit
} else {
    puts "Please select either one unstructured domain or two connectors."
    exit
}

#
# DISCLAIMER:
# TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, POINTWISE DISCLAIMS
# ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED
# TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE, WITH REGARD TO THIS SCRIPT. TO THE MAXIMUM EXTENT PERMITTED
# BY APPLICABLE LAW, IN NO EVENT SHALL POINTWISE BE LIABLE TO ANY PARTY
# FOR ANY SPECIAL, INCIDENTAL, INDIRECT, OR CONSEQUENTIAL DAMAGES
# WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF
# BUSINESS INFORMATION, OR ANY OTHER PECUNIARY LOSS) ARISING OUT OF THE
# USE OF OR INABILITY TO USE THIS SCRIPT EVEN IF POINTWISE HAS BEEN
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGES AND REGARDLESS OF THE
# FAULT OR NEGLIGENCE OF POINTWISE.
#

