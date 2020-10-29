#!/usr/bin/python
###################################################
# Response surface interpolator from ALAMO
# How to run this program : 
#    python <this program> <infile> <outfile> <aux>
# where <infile> has the following format : 
# line 1 : <npts> <nInputs> 
# line 2 : 1 <test point 1 inputs> 
# line 3 : 2 <test point 2 inputs> 
# .... 
# where <outfile> will be in the following format : 
# line 1 : 1 <interpolated value for test point 1>
# line 2 : 2 <interpolated value for test point 2>
# .... 
# where <aux> is an optional index (1-based) argument
#    to specify which output to evaluate
#==================================================
import sys
import string
import math
import json
###################################################
# Function to get input data for interpolation
#==================================================
def getInputData(inFileName):
   with open(inFileName, "r") as inFile:
      lineIn  = inFile.readline()
      nCols   = lineIn.split()
      nSamp   = int(float(nCols[0]))
      nInputs = int(float(nCols[1]))
      inData  = (nSamp * nInputs) * [0]
      for cnt in range(nSamp):
         lineIn = inFile.readline()
         nCols  = lineIn.split()
         for ind in range(nInputs):
            inData[cnt*nInputs+ind] = float(nCols[ind+1])
   return nSamp, inData, nInputs
###################################################
# Function to generate output file
#==================================================
def genOutputFile(outFileName, outData):
   nLeng = len(outData)
   outfile = open(outFileName, 'w')
   for ind in range(nLeng):
      outfile.write("%d " % (ind+1))
      outfile.write("%e\n" % outData[ind])
   outfile.close()
   return None
###################################################
# Model parameters
#==================================================
in_labels = ['MEA_UPD.GASABSIN', 'MEA_UPD.GASINCO2FRXN', 'MEA_UPD.SOLVENTABSIN', 'MEA_UPD.STRIP_PRES', 'X_SOLVENT_CALC.AMINECONC', 'X_SOLVENT_CALC.CO2LOADING']
labels = ['CO2CAPTURE', 'REB_DUTY', 'SRD']
in_indexes = [3, 4, 14, 15, 16, 17]
indexes = [5, 6, 1]
nInputs = 6
nOutputs = 3
###################################################
# Interpolate function for ALAMO
#==================================================
def interpolate(npts, XX, oid):
   if oid == 0:
      g = lambda X: - 2483.8943904062111869280 * math.log(X[3]) + 14260.947087527023541043 * math.log(X[4]) - 7783.4823666874435730278 * math.log(X[14]) - 83.391958961905658043179 * math.log(X[15]) - 12108.794407377039533458 * math.log(X[16]) - 1303.5841777749087668781 * math.log(X[17]) - 46145.822550298500573263 * math.exp(X[4]) + 110182.30356839382147882 * math.exp(X[16]) + 8899.1933371932573209051 * math.exp(X[17]) - 0.25827158933365812172947E-004 * X[3]**2 + 75331.362983971106586978 * X[4]**2 + 0.56883210396592609971633E-005 * X[14]**2 - 222785.92549600076745264 * X[16]**2 - 31064.233879442796023795 * X[17]**2 + 99051.924041676655178890 * X[16]**3 + 15696.201592656330831232 * X[17]**3 + 2.0649439504454920601972 * X[3]*X[4] - 0.17397183969193021692594E-004 * X[3]*X[14] + 0.95802695755843131570142E-004 * X[3]*X[15] + 2.6989044425226302870158 * X[3]*X[16] - 0.40353890521029117666174 * X[3]*X[17] + 0.96863725875091055694810 * X[4]*X[14] + 0.93970093093345241630487 * X[4]*X[15] - 12727.735696466483204858 * X[4]*X[16] + 14552.999837704192032106 * X[4]*X[17] - 0.32888563548957289173202 * X[14]*X[16] - 0.20690902050524739852477 * X[14]*X[17] - 15646.603379964913983713 * X[16]*X[17] - 0.17926916162754098923136E-003 * (X[3]*X[4])**2 - 0.19326816308236362783324E-002 * (X[3]*X[16])**2 + 0.10180411857765516055185E-002 * (X[3]*X[17])**2 - 0.54903584248480134105685E-004 * (X[4]*X[14])**2 - 0.24998179876098608248516E-004 * (X[14]*X[16])**2 + 0.10289475992230754286452E-003 * (X[14]*X[17])**2 + 44373.713963556561793666 * (X[16]*X[17])**2 + 0.52112123229917353851311E-006 * (X[3]*X[16])**3 - 0.37810963184066450402555E-006 * (X[3]*X[17])**3 + 223964.15208054005051963 * (X[4]*X[17])**3 - 0.10235361925566872144758E-007 * (X[14]*X[17])**3 - 0.13740732834628343835871E-003 * X[3]*X[4]*X[14] + 1.2618647442203889674772 * X[3]*X[4]*X[17] + 0.12933649266562262250893E-003 * X[3]*X[14]*X[16] - 0.10688347528103567826794E-003 * X[3]*X[14]*X[17] - 1.2137988978906699699678 * X[3]*X[16]*X[17] - 1.5270023658935898414057 * X[4]*X[14]*X[17] + 40405.364011022124032024 * X[4]*X[16]*X[17] + 0.82721045657494318703584 * X[14]*X[16]*X[17] - 549232.18664306646678597 * (X[4]*X[16]*X[17])**2 + 0.65429879487995376563525E-001 * X[3]/X[4] - 4180296.3558935965411365 * X[4]/X[3] - 74549683.192036151885986 * X[4]/X[14] - 1039.1319633230866656959 * X[4]/X[16] + 32.956358234392155281967 * X[4]/X[17] - 161.18069084576018212829 * X[14]/X[3] + 0.29585606146989545939263 * X[14]/X[4] - 0.56175495402511800568934E-002 * X[14]/X[17] - 137.39314606417511299696 * X[16]/X[17] + 546.23010740583526967384 * X[17]/X[4] + 376.55118103583424726821 * X[17]/X[16] - 0.17358403029889368482023E-005 * (X[14]/X[4])**2
   if oid == 1:
      g = lambda X: - 244844.94236610399093479 * math.log(X[3]) - 5082240.8800576860085130 * math.log(X[4]) + 115579.12611916544847190 * math.log(X[14]) + 27113766.041596472263336 * math.log(X[15]) + 11677633.080908503383398 * math.log(X[16]) - 31133042.267704952508211 * math.log(X[17]) + 46569396.226958245038986 * math.exp(X[4]) - 68939115.292506009340286 * math.exp(X[16]) - 124619172.50849500298500 * math.exp(X[17]) + 0.39163199312990089676068E-002 * X[3]**2 - 52779873.121387250721455 * X[4]**2 - 0.20946381510954136667690E-001 * X[14]**2 + 100058622.77340166270733 * X[16]**2 + 360810669.42879289388657 * X[17]**2 - 268138530.28195494413376 * X[17]**3 - 529.45723759490988413745 * X[3]*X[4] + 0.10665371701518348498960E-001 * X[3]*X[14] - 2414.3992089256726103486 * X[3]*X[17] - 88.064260518687532908189 * X[4]*X[14] - 61774.111140143453667406 * X[4]*X[15] - 88272415.705305576324463 * X[4]*X[17] + 0.57426198199581099390620E-001 * X[14]*X[15] + 294.19891491742845346380 * X[14]*X[17] + 615254.75130981474649161 * X[15]*X[17] - 94083479.926182657480240 * X[16]*X[17] + 1.9181421606003430380127 * (X[3]*X[17])**2 - 98.593667072805601492291 * (X[4]*X[15])**2 - 7892.1656420395929671940 * (X[15]*X[17])**2 + 686554045.74238049983978 * (X[16]*X[17])**2 - 0.89837143532948786611020E-003 * (X[3]*X[17])**3 - 0.10181602712323515499125E-004 * (X[14]*X[17])**3 + 39.495358817116816396720 * (X[15]*X[17])**3 - 2076884007.6687822341919 * (X[16]*X[17])**3 + 7502.1537426231416247902 * X[3]*X[4]*X[16] + 3696.5032410832727691741 * X[3]*X[4]*X[17] - 0.22217924988330497310107E-002 * X[3]*X[14]*X[17] + 3766.4980024772548858891 * X[4]*X[14]*X[16] - 2580.4879473405835597077 * X[4]*X[14]*X[17] - 50653.130119624634971842 * X[4]*X[15]*X[16] + 382543.34711127314949408 * X[4]*X[15]*X[17] + 5.7171142055364283507402 * X[14]*X[15]*X[17] - 1485.4613999433547633089 * X[14]*X[16]*X[17] - 12.790124347800379212003 * (X[3]*X[4]*X[16])**2 - 1.1560173495723562453463 * (X[4]*X[14]*X[16])**2 - 6.1225066571073938348491 * X[14]/X[17] - 47177.526045553771837149 * X[15]/X[17] - 816484.17750111478380859 * X[17]/X[4] + 10763124290.063362121582 * X[17]/X[14] + 9680870726.6221542358398 * X[17]/X[15] + 0.10569110291019222387914E-003 * (X[14]/X[17])**2 + 14.022311803820791453745 * (X[15]/X[17])**2 + 5.0897540284869524640499 * (X[14]/X[15])**3 - 0.19563463427727020155222E-002 * (X[15]/X[17])**3
   if oid == 2:
      g = lambda X: - 9855.0037611449188261759 * math.log(X[3]) - 36577.460315435382653959 * math.log(X[4]) + 3374.4925526480428743525 * math.log(X[14]) - 4813.3184529778827709379 * math.log(X[15]) + 53260.914451919023122173 * math.log(X[16]) + 236.47268587830163255603 * math.log(X[17]) + 569507.15219983912538737 * math.exp(X[4]) - 491785.03681741439504549 * math.exp(X[16]) + 27354.744248302245978266 * math.exp(X[17]) - 0.23205817093045366959541E-004 * X[3]**2 - 949417.60681380925234407 * X[4]**2 + 0.38471828010564047305229E-005 * X[14]**2 + 0.73466533618488050194628 * X[15]**2 + 1191893.5564414013642818 * X[16]**2 - 68402.274714482686249539 * X[17]**2 + 349473.66772730776574463 * X[4]**3 - 0.95551460055435296497839E-003 * X[15]**3 - 591250.44584891502745450 * X[16]**3 + 32548.253431841138080927 * X[17]**3 + 14.033361480140014165841 * X[3]*X[4] + 0.14320192941187455588394E-003 * X[3]*X[14] + 0.18970664505803455906346E-002 * X[3]*X[15] + 25.047416502788450998196 * X[3]*X[16] + 18.030642708642158567045 * X[3]*X[17] + 4.7295003537738988796946 * X[4]*X[14] - 671.20538457110103536252 * X[4]*X[15] - 1131045.1915436764247715 * X[4]*X[16] - 345334.84527979703852907 * X[4]*X[17] - 0.31013757682747992126815E-003 * X[14]*X[15] - 2.5448458343452049490452 * X[14]*X[16] - 4.7292741484322551315245 * X[14]*X[17] - 141.77496103764636359301 * X[15]*X[16] - 310.58153016168364501937 * X[15]*X[17] + 67234.327104274707380682 * X[16]*X[17] - 0.14055377340077666523110E-001 * (X[3]*X[4])**2 - 0.91480944459197861828859E-002 * (X[3]*X[16])**2 - 0.80530410663268228721456E-002 * (X[3]*X[17])**2 - 0.64322227478017120726184E-003 * (X[4]*X[14])**2 - 12.536786191507191645655 * (X[4]*X[15])**2 + 4218529.7912311227992177 * (X[4]*X[16])**2 + 2557602.4569214861840010 * (X[4]*X[17])**2 + 0.22292777725162410754067E-003 * (X[14]*X[16])**2 + 0.82995313120442517317021E-003 * (X[14]*X[17])**2 - 4.7313811025468446302966 * (X[15]*X[16])**2 + 2.6003296170745273663272 * (X[15]*X[17])**2 - 273641.51011098216986284 * (X[16]*X[17])**2 + 0.62882108155492180120777E-005 * (X[3]*X[4])**3 + 0.19830968646044564449374E-005 * (X[3]*X[16])**3 + 0.20933142966551466475432E-005 * (X[3]*X[17])**3 + 0.11714246318798107208572E-006 * (X[4]*X[14])**3 + 0.12239568407763873336691 * (X[4]*X[15])**3 - 9608444.5513682793825865 * (X[4]*X[16])**3 - 10287518.801493234932423 * (X[4]*X[17])**3 - 0.73060098262322588464029E-007 * (X[14]*X[17])**3 + 0.23709081330868856524186E-001 * (X[15]*X[16])**3 - 0.10628832802169979263041E-001 * (X[15]*X[17])**3 + 715395.61828530288767070 * (X[16]*X[17])**3 + 0.25698781816485952560485E-005 * X[3]*X[4]*X[14] + 0.22597728672134925927140E-002 * X[3]*X[4]*X[15] - 37.291857277202019815832 * X[3]*X[4]*X[16] - 11.824988441775341030393 * X[3]*X[4]*X[17] - 0.40414593525632016413453E-006 * X[3]*X[14]*X[15] - 0.26230689043309950636215E-003 * X[3]*X[14]*X[16] + 0.93079529207249542927752E-005 * X[3]*X[14]*X[17] + 0.22476356358225768779235E-002 * X[3]*X[15]*X[16] - 0.23772298831510668346012E-002 * X[3]*X[15]*X[17] - 45.831624415733479338542 * X[3]*X[16]*X[17] - 0.66905002372897931159357E-002 * X[4]*X[14]*X[15] + 1.9046216522232606305209 * X[4]*X[14]*X[16] + 8.2242224190604709121999 * X[4]*X[14]*X[17] + 4922.4394803371160378447 * X[4]*X[15]*X[16] + 1798.9427991877923886932 * X[4]*X[15]*X[17] - 27192.053332072155171772 * X[4]*X[16]*X[17] + 0.20685438704789956866625E-002 * X[14]*X[15]*X[16] - 0.27601015495658585800764E-002 * X[14]*X[15]*X[17] + 13.039459157709059056174 * X[14]*X[16]*X[17] + 0.83799013180742387696398 * X[15]*X[16]*X[17] + 0.30766550372253984729776E-001 * (X[3]*X[4]*X[16])**2 + 0.19131693028951100160606E-001 * (X[3]*X[4]*X[17])**2 + 0.64163194509234661166985E-001 * (X[3]*X[16]*X[17])**2 - 0.19497971990473891065049E-002 * (X[4]*X[14]*X[16])**2 - 0.38283047011508984473760E-002 * (X[4]*X[14]*X[17])**2 - 51.549520665003178976349 * (X[4]*X[15]*X[16])**2 - 68.562754925355392288111 * (X[4]*X[15]*X[17])**2 - 0.84709862962513773898543E-002 * (X[14]*X[16]*X[17])**2 - 0.52797029455446168829703E-004 * (X[3]*X[16]*X[17])**3 + 1.4395778272980326306651 * (X[4]*X[15]*X[17])**3 + 0.31246966531795315481215E-005 * (X[14]*X[16]*X[17])**3 - 0.12422926446452703386214 * X[3]/X[4] - 0.64140216983586587073951E-001 * X[3]/X[16] - 16976362.320892490446568 * X[4]/X[3] + 42547789.340307913720608 * X[4]/X[14] - 93.962028932405360137636 * X[14]/X[3] + 0.46470760192678817190881E-001 * X[14]/X[4] - 89.671836458023321370092 * X[14]/X[15] - 0.47286260549310295264736E-001 * X[14]/X[16] + 0.18645324131708609308872E-002 * X[14]/X[17] - 6.1966917591503563045308 * X[15]/X[4] - 0.10848555015626062947298 * X[15]/X[17] + 71.750680098626801850514 * X[16]/X[17] + 413.58736811395073118547 * X[17]/X[4] + 742405.40779638488311321 * X[17]/X[15]
   Ys = npts * [0.0]
   for ss in range(npts):
      Xt = nInputs * [0.0]
      for ii in range(nInputs):
         Xt[ii] = XX[ss*nInputs+ii]
      Ys[ss] = g(Xt)
   return Ys
###################################################
# Main program
#==================================================
infileName  = sys.argv[1]
if infileName=="__labels__":
   sys.exit(0)
outfileName = sys.argv[2]
index = 0
if len(sys.argv) > 3:
   y = sys.argv[3]
   if y.isdigit():
      y = int(y)
      if y in range(1, nOutputs+1):
         index = y - 1
   else:
      if y in labels:
         index = labels.index(y)
(nSamples, inputVectors, nInputs) = getInputData(infileName)
result = interpolate(nSamples, inputVectors, index)
genOutputFile(outfileName, result)
