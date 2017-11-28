from Population import *
from Predictions import Interpolation_BAU_1972 
from Predictions import Interpolation_BAU_2012 

T = np.linspace( 1890, 2100, 211)
Time_Ran, Population_Ran = Load_Calibration( "Randers_2052.csv", "Year", "Population")

P0 = Population()
UN_Med = P0.UN_Medium.GetVector( T)

BAU_1972 = Interpolation_BAU_1972()
BAU_1972.Solve(T)
BAU_2012 = Interpolation_BAU_2012()
BAU_2012.Solve(T)
Difference = UN_Med - BAU_2012.Population 

for i in range( len( BAU_2012.Time)):
    print( BAU_2012.Time[i], BAU_2012.Population[i])

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))

plt.plot( BAU_1972.Time, BAU_1972.Population, "--", lw=1, color="b", label="Население (BAU-1972) [млн]")
plt.plot( BAU_2012.Time, BAU_2012.Population, "-", lw=3, color="b", label="Население (Рандерс-2012) [млн]")
plt.plot( T[125:], UN_Med[125:], "-", lw=2, color="g", label="Население (ООН-2010) [млн]")
plt.plot( T[100:], Difference[100:], "--", lw=3, color="r", label="Разница ООН-Рандерс [млн]")

#plt.errorbar( Time_Ran, Population_Ran, yerr=Population_Ran*0.03, fmt='.', color="r", label="Население (Рандерс-2012) [млн]")
plt.errorbar( P0.Calibration_Year, P0.Calibration_Total, yerr=P0.Calibration_Delta, fmt='.', color="k", label="Население (статистика ООН)")

plt.xlabel("Годы")
plt.xlim( 1900, 2100)
plt.ylabel("миллионов")
plt.ylim( 0, 12000)
plt.title( 'Аппроксимация NewWorld 2012 г: Население')
plt.grid(True)
plt.legend(loc=0)
plt.savefig( ".\\Graphs\\figure_07_03.png")
fig.show()
