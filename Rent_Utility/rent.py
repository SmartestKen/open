import os
try:
	os.remove('/home/ken/open/Rent_Utility/rent.txt')
except Exception:
	pass
	
with open('/home/ken/open/Rent_Utility/rent.txt', 'a') as file:
	file.write("rent for current month, utility for previous month\n")
	file.write('        Kyra             Udai          Keren        Sejal\n')

	rent = 2568.76
	file.write('Jul     %7.3f       %7.3f       %7.3f       %7.3f\n'%(
				rent*0.3, rent*0.5, rent*0.2, 0))


	rent = 2503.53
	utility = 204.48
	file.write('Aug     %7.3f       %7.3f       %7.3f       %7.3f\n'%(
				rent*0.3+utility*0.334, rent*0.5+utility*0.334, rent*0.2+utility*0.334, 0))


	rent = 2565.27
	utility = 82.13
	file.write('Sep     %7.3f       %7.3f       %7.3f       %7.3f\n'%(
				rent*0.3+utility*0.334, rent*0.5+utility*0.334, rent*0.2+utility*0.334, 0))


	rent = 2523.04
	utility = 81.47
	extra = 2565.27*0.5+82.13*0.334-1200
	file.write('Oct     %7.3f        %7.3f       %7.3f         %7.3f\n'%(
				rent*0.3+utility*0.3, rent*0.25+utility*0.3+extra, rent*0.2+utility*0.3, rent*0.25+utility*0.1))
	# print(rent*0.3+utility*0.3+rent*0.25+utility*0.3+rent*0.2+utility*0.3+rent*0.25+utility*0.1-rent-utility)

	cleaner = 65.38
	file.write('Cleaner %7.3f       %7.3f       %7.3f         %7.3f\n'%(
				cleaner*0.25, cleaner*0.25, cleaner*0.25, cleaner*0.25))
	rent = 2527.59
	utility = 77.10
	file.write('Nov     %7.3f        %7.3f       %7.3f         %7.3f\n'%(
				rent*0.3+utility*0.25, rent*0.25+utility*0.25, rent*0.2+utility*0.25, rent*0.25+utility*0.25))

	rent = 2589.42
	utility = 113.14
	file.write('Dec     %7.3f        %7.3f       %7.3f         %7.3f\n'%(
				rent*0.3+utility*0.25, rent*0.25+utility*0.25, rent*0.2+utility*0.25, rent*0.25+utility*0.25))



	rent = 2509.05+5
	utility = 95.96

	file.write('Jan_pre %7.3f     %7.3f       %7.3f         %7.3f\n'%(
				750, 600, 0, 600))
	file.write('Jan_post %7.3f    %7.3f       %7.3f         %7.3f\n'%(
				rent*0.3+utility*0.25-750, rent*0.25+utility*0.25-600, rent*0.2+utility*0.25, rent*0.25+utility*0.25-600))



	rent = 2494.57
	utility = 120.65
	file.write('Feb    %7.3f        %7.3f       %7.3f         %7.3f\n'%(
				rent*0.3 + utility*0.25, rent*0.25 + utility*0.25, rent*0.2 + utility*0.25, rent*0.25 + utility*0.25))


	# +31.75 due to reverse late fee (i.e. get back my payment and re-distribute)
	# +10 for (+5+5) Feb and Mar insurance fee
	rent = 2437.45 + 31.75 + 10
	utility = 97.72
	file.write('Mar    %7.3f        %7.3f       %7.3f         %7.3f\n'%(
				rent*0.3 + utility*0.25, rent*0.25 + utility*0.25, rent*0.2 + utility*0.25, rent*0.25 + utility*0.25))


	rent = 2505.92 + 5
	utility = 89.83
	file.write('April    %7.3f        %7.3f       %7.3f         %7.3f\n' % (
				rent * 0.3 + utility * 0.25, rent * 0.25 + utility * 0.25, rent * 0.2 + utility * 0.25, rent * 0.25 + utility * 0.25))


	rent = 2501.73 + 5
	utility = 56.47
	file.write('May    %7.3f        %7.3f       %7.3f         %7.3f\n' % (
				rent * 0.3 + utility * 0.5, rent * 0.25 + utility * 0, rent * 0.2 + utility * 0.5, rent * 0.25 + utility * 0))


	rent = 2504.21*22/30 + 5
	utility = 60.45*22/30
	file.write('June_p1   %7.3f        %7.3f       %7.3f         %7.3f\n' % (
				rent * 0.3 + utility * 0.5, rent * 0.25 + utility * 0, rent * 0.2 + utility * 0.5, rent * 0.25 + utility * 0))

	rent = 2504.21*8/30
	utility = 60.45*8/30
	file.write('June_p2    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
				rent * 0.35 + utility * 0.5, rent * 0 + utility * 0, rent * 0.25 + utility * 0.5, rent * 0.4 + utility * 0))

	file.write("--------------------------------------------------------------\n")
	file.write("rent for current month, utility for previous month -> \nsimply treat everything current month to avoid errors\n")

	rent = 2504.21*8/30
	utility = 60.45*8/30
	file.write('        Kyra           Spencer          Keren        Sejal\n')
	file.write('June_p2 %7.3f      %7.3f       %7.3f         %7.3f\n' % (
				0, rent*0.25 + utility*0.5, 0, 0))

	rent = 2500.31
	utility = 73.05
	file.write('July    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
				rent*0.3+utility*0.25, rent*0.25+ utility*0.5, rent*0.2+utility*0.25, rent*0.25+utility*0))

	# -5 for key +10 for insurance
	rent = 2564.68 - 5 + 10
	utility = 138.59
	key = 5
	file.write('Aug    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
				rent*0.3+utility*0.25, rent*0.25+ utility*0.5+key, rent*0.2+utility*0.25, rent*0.25+utility*0))    

	rent = 2564.72 + 10
	utility = 76.36

	file.write('Sep_p1    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
				rent*(5/30)*0.3+utility*(5/30)*0.33, rent*(5/30)*0.25+ utility*(5/30)*0.33, rent*(5/30)*0.2+utility*(5/30)*0.33, rent*(5/30)*0.25+utility*(5/30)*0))
	file.write("\n")
	file.write('        Kyra         Brendan         Keren        Sejal\n')
	file.write('Sep_p2    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
				rent*(25/30)*0.35+utility*(25/30)*0.5, 0, rent*(25/30)*0.25+utility*(25/30)*0.5, rent*(25/30)*0.4+utility*(25/30)*0))


	rent = 2510.12 + 5
	utility = 65.08
	file.write('Oct    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
		rent * 0.3 + utility * 0.33, rent * 0.25 + utility * 0.33, rent * 0.2 + utility * 0.33,
		rent * 0.25 + utility * 0))

	rent = 2560.95 + 5
	utility = 73.44
	file.write('Nov    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
		rent * 0.3 + utility * 0.3, rent * 0.25 + utility * 0.2, rent * 0.2 + utility * 0.3,
		rent * 0.25 + utility * 0.2))

	rent = 2510.81 + 5
	utility = 73.97
	file.write('Dec    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
		rent * 0.3 + utility * 0.4, rent * 0.25 + utility * 0.2, rent * 0.2 + utility * 0.4,
		rent * 0.25 + utility * 0))

	rent = 2516.91 + 5
	utility = 70.46
	file.write('Jan    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
		rent * 0.3 + utility * 0.4, rent * 0.25 + utility * 0.2, rent * 0.2 + utility * 0.4,
		rent * 0.25 + utility * 0))

	rent = 2520.97 + 5
	utility = 72.72
	file.write('Feb    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
		rent * 0.3 + utility * 0.4, rent * 0.25 + utility * 0.2, rent * 0.2 + utility * 0.4,
		rent * 0.25 + utility * 0))

	rent = 2545.24 + 5
	utility = 81.32
	file.write('        Kyra         Keren        Sejal\n')
	file.write('Mar  %7.3f       %7.3f         %7.3f\n' % (
		rent * (0.3+0.25/3) + utility * 0.33, rent * (0.2+0.25/3) + utility * 0.33,
		rent * (0.25+0.25/3) + utility * 0.33))


	file.write('Mar_Aj   %7.3f       %7.3f         %7.3f\n' % (
		rent * (0.3+0.25/3) + utility * 0.33 - 871.60, 0,
		rent * (0.25+0.25/3) + utility * 0.33 - 796.95))

	rent = 2508.22 + 5
	utility = 74.72
	file.write('        Kyra         Keren        Sejal\n')
	file.write('Apr  %7.3f       %7.3f         %7.3f\n' % (
		rent * (0.3+0.25/3) + utility * 0.33, rent * (0.2+0.25/3) + utility * 0.33,
		rent * (0.25+0.25/3) + utility * 0.33))



	rent = 2530.39 + 5
	utility = 103.15
	file.write('        Kyra         Keren        Sejal\n')
	file.write('May  %7.3f       %7.3f         %7.3f\n' % (
		rent * (0.3+0.25/3) + utility * 0.33, rent * (0.2+0.25/3) + utility * 0.33,
		rent * (0.25+0.25/3) + utility * 0.33))


	rent = 2499.56 + 5
	utility = 98.31
	file.write('        Kyra         Keren        Sejal        Sajan        Uday\n')
	file.write('Jun(OK)  %7.3f       %7.3f         %7.3f         %7.3f         %7.3f\n' % (
		rent * 0.36*12/30 + utility * 0.38, rent * 0.25 + utility * 0.24,
		rent * 0.39*18/30 + utility * 0.38, rent * 0.36*6/30 + rent * 0.39*12/30, rent * 0.36*12/30))

	rent = 2240.00 + 106.26 + 5
	utility = 98.39
	file.write('        Keren       Sajan        Uday\n')
	file.write('Jul(OK)  %7.3f       %7.3f       %7.3f\n' % (
		rent * (500/2250) + utility * 0.333, rent * (1000/2250) + utility * 0.333,
		rent * (750/2250) + utility * 0.333))

	security=200
	file.write('Security(OK) %7.3f       %7.3f       %7.3f\n' % (
		security * 0.333, security * 0.333,
		security * 0.333))
		
	rent = 2240 + 5
	utility = 179.81+100.84
	file.write('Aug(OK) %7.3f       %7.3f       %7.3f\n' % (
		rent * (500/2250) + utility * 0.333, rent * (1000/2250) + utility * 0.333,
		rent * (750/2250) + utility * 0.333))

	rent = 2240 + 5
	utility = 161.74 + 71.62
	file.write('Sep(S,U) %7.3f       %7.3f       %7.3f\n' % (
		rent * (500/2250) + utility * 0.5, rent * (1000/2250) + utility * 0.5,
		rent * (750/2250)))
		
	blue_0906_ke = 2.5+3.49+6.99*8
	blue_0906_sj = 1.14+1
	blue_0831_ke = 3.49+2.5+6.99*12
	blue_0831_sj = 3.99+3.99+3.34+12.28
	blue_0909_ke = 8*6.99
	blue_0909_sj = 3.99 +2+3.34+5.99
	blue_0914_ke = 6.99*5+0.1
	blue_0914_sj = 1.5
	file.write('Berry %7.3f       %7.3f       %7.3f\n' % (
		blue_0906_ke+blue_0831_ke+blue_0909_ke+blue_0914_ke, 0, 0))
	# print(blue_0906_ke+blue_0906_sj, blue_0831_ke+blue_0831_sj, blue_0909_ke+blue_0909_sj, blue_0914_ke+blue_0914_sj)
		



	rent = 2240*2+10
	utility = 101.13 + 96.93 + 74.35 + 93.86	

	file.write('Oct/Nov(S,U) %7.3f       %7.3f       %7.3f\n' % (
		rent * (500/2250) + utility * 0.33, rent * (1000/2250) + utility * 0.33,
		rent * (750/2250) + utility * 0.33))


	rent = 2240 + 5
	utility = 109.73 + (2320.94 - 2240)
	file.write('Dec(S,U) %7.3f       %7.3f       %7.3f\n' % (
		rent * (500/2250) + utility * 0.33, rent * (1000/2250) + utility * 0.33,
		rent * (750/2250) + utility * 0.33))

	rent = 2322.68 + 5
	utility = 129.5
	file.write('Jan(S,U) %7.3f       %7.3f       %7.3f\n' % (
		rent * (500/2250) + utility * 0.33, rent * (1000/2250) + utility * 0.33,
		rent * (750/2250) + utility * 0.33))
	
	rent = 2324.84 + 5
	utility = 130.81
	file.write('Feb(S,U) %7.3f       %7.3f       %7.3f\n' % (
		rent * (500/2250) + utility * 0.33, rent * (1000/2250) + utility * 0.33,
		rent * (750/2250) + utility * 0.33))
