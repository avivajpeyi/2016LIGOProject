#pragma rtGlobals=3		// Use modern global access method and strict wave access.

Menu "Stuff"
	"NumBeforeEachFAP" , NumPointsBeforeFAP(FAP)
	"sampling Of GPS timess",  samplingOfGPStimes(realGPS, lnL, far)
End



Function NumPointsBeforeFAP(FAP)
	Wave FAP
	
	//Store the name of the wave plus the string "_OneThird" into newWaveName
	string newFAPListName=NameOfWave(FAP)+"_uniqueList"
	//Duplicate fluorescence as a wave named fluorescence_OneThird
	duplicate/O FAP $newFAPListName
	//Reference fluorescence_OneThird so that you can use it
	Wave uniqueFAPlist=$newFAPListName
	
	variable x
	for (x =0; x <numpnts(FAP); x+=1)
		uniqueFAPlist[x] = 0
	endFor

	string newFAPCountName = NameOfWave(FAP)+"_count"
	//Duplicate fluorescence as a wave named fluorescence_OneThird
	duplicate/O uniqueFAPlist $newFAPCountName
	//Reference fluorescence_OneThird so that you can use it
	Wave Count=$newFAPCountName
	
	variable n = numpnts(FAP)
	variable i
	variable numFAPpoints = 0
	
	variable currentFAP = FAP[n-1]
	uniqueFAPlist[0] = currentFAP
	variable prevCount = 0
	
	for (i =n-1; i>0; i-=1)
		if  (currentFAP == FAP[i])
			//Count[numFAPpoints] =1 + Count[numFAPpoints]
		else
			prevCount = Count[numFAPpoints]
			currentFAP =  FAP[i]
			numFAPpoints +=1
			uniqueFAPlist[numFAPpoints] = currentFAP
			Count[numFAPpoints] = prevCount +1
		endif
	endfor
End
	
	
Function samplingOfGPStimes(realGPS, lnL, far)

Wave realGPS, lnL, far



	//Store the name of the wave plus the string "_OneThird" into newWaveName
	string GPSName=NameOfWave(realGPS)+"_sampled"
	string lnLName=NameOfWave(lnL)+"_sampled"
	string farName=NameOfWave(far)+"_sampled"
	//Duplicate fluorescence as a wave named fluorescence_OneThird
	duplicate/O realGPS $GPSName
	duplicate/O lnL $lnLName
	duplicate/O far $farName
	//Reference fluorescence_OneThird so that you can use it
	Wave GPSsamp=$GPSName
	Wave lnLsamp=$lnLName
	Wave farsamp=$farName
	
	 
	variable numOriginal = numpnts(realGPS)
	variable  numToDelete =  numOriginal - 1000
	
	// delete the points after the 1st 1000 points
	deletepoints 0, numToDelete, GPSsamp
	deletepoints 0, numToDelete, lnLsamp
	deletepoints 0, numToDelete, farsamp
	
	
	// delete every third data point 
	variable x
	variable check = 3
	
	for (x = numpnts(GPSsamp); x > 0; x -= 1)
		if  (check == 3)
			check = 1
		else 
			check +=1
			deletepoints x, 1, GPSsamp
			deletepoints x, 1, lnLsamp
			deletepoints x, 1, farsamp
		endif
	
	endFor  
	
	
End

	
	
	

	
	
	
	
	end