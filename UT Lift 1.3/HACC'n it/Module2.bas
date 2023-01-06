Attribute VB_Name = "Module2"

Public Function GirderTx(X, Radius, ThetaBar, NumXFrame, Spacing, XFrameWeight(), LLift1, LLift2, RLift1, RLift2, e_SC(), e_Yo(), SectionLength(), Weight(), LengthtoXFrame(), Alpha()) As Double
Dim LengthUnitConstant, ForceUnitConstant As Double
Dim ThetaX, Theta0, ThetaXBar, Wx, Dx, temp, temp1, temp2, temp3 As Double
Dim Sections, XFrameSections, HLD As Integer
Dim c, ThetaPiLX, ThetaPiL1, ThetaPiL2, ThetaStarLX, ThetaStarL1, ThetaStarL2, TLift1, TLift2 As Double
Dim pi As Double

' If the program is to be changed to metric this will be changed with an if statement
LengthUnitConstant = 12     ' Convert feet to inches
ForceUnitConstant = 1000    ' Convert lbs to kips
pi = 3.14159265358979       ' 4*Atn(1)

If (X < 0) Then
 X = 0.01
End If
If (X > Sheets("C.G. & Ideal Lift").Range("D4") * LengthUnitConstant) Then
 X = Sheets("C.G. & Ideal Lift").Range("D4") * LengthUnitConstant - 0.01
End If

If (X > 1499.7) Then
X = X
End If
' This function will find the Torsion applied by the Girder Self Weight to any given Girder Location X
' See Theory Document for the Exact Formulation
' T(x) = Wx(R/Cos(Theta0) - Dx) Cos(Theta0)

' Determine Number of Girder Cross Sections to Location X
Sections = 1
temp = SectionLength(Sections)
If (X > temp) Then
  Do While (X > temp)
    Sections = Sections + 1
    temp = temp + SectionLength(Sections)
  Loop
End If

' Determine Number of Cross Frames to Location X
If (NumXFrame > 0) Then
  XFrameSections = 0
  If (X > LengthtoXFrame(1)) Then
    If (X > LengthtoXFrame(NumXFrame)) Then
      XFrameSections = NumXFrame
    Else
      Do While (X > LengthtoXFrame(XFrameSections + 1))
        XFrameSections = XFrameSections + 1
      Loop
    End If
  End If
End If

' Include Torsion of Girder Self weight
temp1 = 0
temp3 = 0
For i = 1 To Sections
  If (i < Sections) Then
    Wx = Weight(i) * SectionLength(i)       ' Determine the Weight of Section
    temp1 = temp1 + SectionLength(i)
    temp3 = temp3 + SectionLength(i - 1)    ' Holds the Length to Last Cross-Section Change
    Dx = Radius * (2 * Radius * Sin(SectionLength(i) / 2 / Radius)) / SectionLength(i)  ' Locate Radial Distance of C.G.
    ThetaXBar = (temp1 + temp3) / 2 / Radius                  ' Locate Theta Distance of C.G.

    temp = (LLift1 / Radius + LLift2 / Radius) / 2
    ThetaPiLX = pi - (temp - ThetaXBar)
    If (e_Yo(Sections, i) > 0) Then
      temp2 = pi - (temp - ThetaXBar)
    Else
      temp2 = (temp - ThetaXBar)
    End If
    c = Sqr(Dx ^ 2 + e_Yo(Sections, i) ^ 2 - 2 * Radius * Abs(e_Yo(Sections, i)) * Cos(temp2))
    c = c * Radius / Abs(Radius)
    ThetaStarLX = X / Radius + (Arcsin(Dx * Sin(ThetaPiLX) / c) - temp)
    ' Torque Applied to Cross Section X by the Girder from the beginning to X
    GirderTx = GirderTx + Wx * (Radius / Cos(ThetaStarLX) - c) * Cos(ThetaStarLX)
  Else
    Wx = Weight(i) * (X - temp1)
    Dx = Radius * (2 * Radius * Sin((X - temp1) / 2 / Radius)) / (X - temp1)
    ThetaXBar = (X + temp1) / 2 / Radius

    temp = (LLift1 / Radius + LLift2 / Radius) / 2
    ThetaPiLX = pi - (temp - ThetaXBar)
    If (e_Yo(Sections, i) > 0) Then
      temp2 = pi - (temp - ThetaXBar)
    Else
      temp2 = (temp - ThetaXBar)
    End If
    c = Sqr(Dx ^ 2 + e_Yo(Sections, i) ^ 2 - 2 * Radius * Abs(e_Yo(Sections, i)) * Cos(temp2))
    c = c * Radius / Abs(Radius)
    ThetaStarLX = X / Radius + (Arcsin(Dx * Sin(ThetaPiLX) / c) - temp)
    ' Torque Applied to Cross Section X by the Girder from the beginning to X
    GirderTx = GirderTx + Wx * (Radius / Cos(ThetaStarLX) - c) * Cos(ThetaStarLX)
  End If
Next i

' Include Torsion of Cross Frames
If (XFrameSections > 0) Then
  Eccentricity = Sheets("Calculated Behavior").Range("D27")
  For i = 1 To XFrameSections
    Wx = XFrameWeight(i)    ' Add Cross Frame Weight
    ThetaXBar = (LengthtoXFrame(i) / Radius)
    Dx = (Radius + Alpha(i) * Spacing / 2)

    temp = (LLift1 / Radius + LLift2 / Radius) / 2
    ThetaPiLX = pi - (temp - ThetaXBar)
    c = Sqr(Dx ^ 2 + e_Yo(1, 1) ^ 2 - 2 * Radius * e_Yo(1, 1) * Cos(ThetaPiLX))
    c = c * Radius / Abs(Radius)
    ThetaStarLX = X / Radius + (Arcsin(Dx * Sin(ThetaPiLX) / c) - temp)
    ' Torque Applied to Cross Section X by the Girder from the beginning to X
    GirderTx = GirderTx + Wx * (Radius / Cos(ThetaStarLX) - c) * Cos(ThetaStarLX)
  Next i
End If

If (X >= LLift1) Then               ' Include Torque from Lifting Reactions
  ThetaPiL1 = pi - (temp - LLift1 / Radius)
  c = Sqr(Radius ^ 2 + e_SC(Sections) ^ 2 - 2 * Radius * e_SC(Sections) * Cos(ThetaPiL1))
  c = c * Radius / Abs(Radius)
  ThetaStarL1 = X / Radius + (Arcsin(Radius * Sin(ThetaPiL1) / c) - temp)
  TLift1 = RLift1 * (Radius / Cos(ThetaStarL1) - c) * Cos(ThetaStarL1)
  GirderTx = GirderTx - TLift1
End If
If (X >= LLift2) Then
  ThetaPiL2 = pi - (temp - LLift2 / Radius)
  c = Sqr(Radius ^ 2 + e_SC(Sections) ^ 2 - 2 * Radius * e_SC(Sections) * Cos(ThetaPiL2))
  c = c * Radius / Abs(Radius)
  ThetaStarL2 = X / Radius + (Arcsin(Radius * Sin(ThetaPiL2) / c) - temp)
  TLift2 = RLift2 * (Radius / Cos(ThetaStarL2) - c) * Cos(ThetaStarL2)
  GirderTx = GirderTx - TLift2
End If

' Output the Torsion Diagram ***************************************************************************
' ******************************************************************************************************
HLD = 0
If (NumXFrame > 0) Then
  For i = 1 To NumXFrame
    If (X >= LengthtoXFrame(i) - 0.01 And X <= LengthtoXFrame(i) + 0.01) Then
      HLD = 1
    End If
  Next
End If

If (X >= LLift1 - 0.01 And X <= LLift1 + 0.01) Then
  HLD = 1
End If
If (X >= LLift2 - 0.01 And X <= LLift2 + 0.01) Then
  HLD = 1
End If

If (HLD = 0) Then
  temp = Sheets("Graphs").Range("P4") + 1
  Sheets("Graphs").Range("P6").Offset(temp, 0) = X
  Sheets("Graphs").Range("P6").Offset(temp, 1) = GirderTx
  Sheets("Graphs").Range("P4") = temp
End If
' ******************************************************************************************************
' ******************************************************************************************************

End Function

Public Function Arcsin(arg1)
  Arcsin = Atn(arg1 / Sqr(1 - arg1 * arg1))
End Function

