#pragma rtGlobals=3		// Use modern global access method and strict wave access.

Menu "Stuff"
	"SNR combine", SNRcombine(snrL1, snrH1)
	"NumBeforeEachFAP" , NumPointsBeforeFAP(FAP)
	"sampling Of GPS timess",  samplingOfGPStimes(realGPS, lnL, far, snr)
	"Matching the coherent GPS times with the Likelihoods", matchingData(realGPS_sampled, far_sampled, snr_sampled)//, lnL_sampled, )
	"test",  PromptTest()
End


Function PromptTest()
	String BCRstring
	Prompt BCRstring, "Example:", popup Wavelist("BCR*", ";", "")
	DoPrompt "Select waves", BCRstring
	If (v_flag)
		return -1
	endif
	 
	Wave BayesCoherentRatio = $BCRstring
	print BCRstring
	print BayesCoherentRatio
End

		
		
		
		
	
Function matchingData(realGPS_sampled, far_sampled, snr_sampled) // , lnL_sampled)

Wave realGPS_sampled, far_sampled, snr_sampled //,  lnL_sampled



//Duplicate/O  Htime realGPS_sampled
//Duplicate/O  FAR far_sampled
//Duplicate/O   SNR snr_sampled



	String GPStimeBayesString
	Prompt GPStimeBayesString, "GPS Bayes:", popup Wavelist("*GPS*", ";", "")
	DoPrompt "Select waves", GPStimeBayesString
	If (v_flag)
		return -1
	endif
	Wave GPStimeBayes = $GPStimeBayesString


	String BCRstring
	Prompt BCRstring, "Example:", popup Wavelist("*", ";", "")
	DoPrompt "Select waves", BCRstring
	If (v_flag)
		return -1
	endif
	Wave BayesCoherentRatio = $BCRstring
	
	
	


	// ROUNDING of real GPS to match the BPStimeBayes
	string realGPSroundedName = "realGPS_rounded"
	duplicate/O realGPS_sampled $realGPSroundedName
	Wave realGPSrounded=$realGPSroundedName
	Variable targetDP
	targetDP = round(2) // the DP that my number will be 
	realGPSrounded = round( realGPSrounded * (10^targetDP)) / (10^targetDP)

	//Store the name of the wave plus the string "_OneThird" into newWaveName
	string GPSName=NameOfWave(GPStimeBayes)+"_srt"
	//string lnLName="lnL_srt"
	string farName="far_srt"
	string snrName="snr_srt"
	string coherentBayesName =  NameOfWave(BayesCoherentRatio)+"_srt"

	
	//Duplicate fluorescence as a wave named fluorescence_OneThird
	duplicate/O  GPStimeBayes $GPSName
	//duplicate/O GPStimeBayes $lnLName
	duplicate/O GPStimeBayes $farName
	duplicate/O GPStimeBayes $snrName
	duplicate/O GPStimeBayes $coherentBayesName
	//Reference fluorescence_OneThird so that you can use it
	Wave GPSsort=$GPSName
	//Wave lnLsort=$lnLName
	Wave farsort=$farName
	Wave SNRsort=$snrName
	Wave bayesSort = $coherentBayesName
	
	variable i
	variable  x
		
	for( i = 0; i < numpnts(GPStimeBayes); i += 1)
		//GPSsort[i] = 0
		//lnLsort[i] = 0
		farsort[i] = 0
		bayesSort[i] = 0
		SNRsort[i]= 0
	endFor
		
	i = 0
	 
	 variable numMatches =0
	 
	for( i = 0; i < numpnts(GPStimeBayes); i += 1)
		for (x = 0; x < numpnts(realGPSrounded); x += 1)
			if  (GPStimeBayes[i] == realGPSrounded[x])
				numMatches +=1
				GPSsort[i] = GPStimeBayes[i]
				//lnLsort[i] = lnL_sampled[x]
				farsort[i] = far_sampled[x]
				bayesSort[i] =  BayesCoherentRatio[i]
				SNRsort[i]= snr_sampled[x]
			endif
		endFor
	endFor  
	
	string outputStatment = "Number of Matches = "  + num2str(numMatches)
	print(outputStatment)
	
	
End



Function SNRcombine(snrL1, snrH1)
	
	Wave snrL1, snrH1

	//Create wave of size SNR L1
	string snrName="snr"
	duplicate/O snrL1 $snrName
	Wave SNR=$snrName
	variable i =0
	for( i = 0; i < numpnts(SNR); i += 1)
		SNR[i]= 0
	endFor
	for( i = 0; i < numpnts(snrL1); i += 1)
		SNR[i]= sqrt((snrL1[i]*snrL1[i])+(snrH1[i]*snrH1[i]))
	endFor

end
	
	 


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
	
	
Function samplingOfGPStimes(realGPS, lnL, far, snr)

Wave realGPS, lnL, far, snr

	//Store the name of the wave plus the string "_OneThird" into newWaveName
	string GPSName=NameOfWave(realGPS)+"_sampled"
	string lnLName=NameOfWave(lnL)+"_sampled"
	string farName=NameOfWave(far)+"_sampled"
	string snrName=NameOfWave(snr)+"_sampled"
	//Duplicate fluorescence as a wave named fluorescence_OneThird
	duplicate/O realGPS $GPSName
	duplicate/O lnL $lnLName
	duplicate/O far $farName
	duplicate/O snr $snrName
	
	//Reference fluorescence_OneThird so that you can use it
	Wave GPSsamp=$GPSName
	Wave lnLsamp=$lnLName
	Wave farsamp=$farName
	Wave SNRsamp=$snrName
	 
	variable numOriginal = numpnts(realGPS)
	variable  numToDelete =  numOriginal - 1000
	
	// delete the points after the 1st 1000 points
	deletepoints 0, numToDelete, GPSsamp
	deletepoints 0, numToDelete, lnLsamp
	deletepoints 0, numToDelete, farsamp
	deletepoints 0, numToDelete, SNRsamp
	
	
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
			deletepoints x, 1, SNRsamp
		endif
	
	endFor  
	
	
End

	
	
	
	

	
	
	
	
	end