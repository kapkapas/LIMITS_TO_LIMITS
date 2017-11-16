from Population import *

BP_Year, BP_2008P = Load_Calibration( "10_BP_Renewable.csv", "Year", "2008")
BP_2011P, BP_2012P = Load_Calibration( "10_BP_Renewable.csv", "2011", "2012")
BP_2014P, BP_2015P = Load_Calibration( "10_BP_Renewable.csv", "2014", "2015")
BP_2016P, BP_2017P = Load_Calibration( "10_BP_Renewable.csv", "2016", "2017")

print(BP_Year, BP_2008P)

diff_2011 = BP_2011P * 100 / BP_2017P 
diff_2012 = BP_2012P * 100 / BP_2017P 
diff_2014 = BP_2014P * 100 / BP_2017P 
diff_2015 = BP_2015P * 100 / BP_2017P 
diff_2016 = BP_2016P * 100 / BP_2017P 

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Мировое производство возобновляемой энергии по отчётам "ВР" 2008-2017 гг', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[3, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( BP_Year[26:-6], BP_2011P[26:-6], "--", lw=1, color='m', label="Отчёт 2011 г")
ax1.plot( BP_Year[26:-5], BP_2012P[26:-5], "--", lw=1, color='k', label="Отчёт 2012 г")
ax1.plot( BP_Year[:-3], BP_2014P[:-3], "-", lw=1, color='r', label="Отчёт 2014 г")
ax1.plot( BP_Year[:-2], BP_2015P[:-2], "-", lw=1, color='g', label="Отчёт 2015 г")
ax1.plot( BP_Year[:-1], BP_2016P[:-1], "-", lw=1, color='b', label="Отчёт 2016 г")
ax1.plot( BP_Year, BP_2017P, "-", lw=1, color='k', label="Отчёт 2017 г")
ax1.set_xlim( 1965, 2020)
ax1.set_ylabel("Млн тонн нефтяного эквивалента в год")
ax1.grid(True)
ax1.set_title( "Абсолютные значения (кроме гидро)")
ax1.legend(loc=0)

ax2.plot( BP_Year[26:-6], diff_2011[26:-6], "--", lw=1, color='m')
ax2.plot( BP_Year[26:-5], diff_2012[26:-5], "--", lw=1, color='k')
ax2.plot( BP_Year[:-3], diff_2014[:-3], "-", lw=1, color='r')
ax2.plot( BP_Year[:-2], diff_2015[:-2], "-", lw=1, color='g')
ax2.plot( BP_Year[:-1], diff_2016[:-1], "-", lw=1, color='b')
ax2.set_xlim( 1965, 2020)
ax2.set_ylim( 90, 110)
ax2.set_xlabel("Годы")
ax2.set_ylabel("%%")
ax2.grid(True)
ax2.set_title( "В %% к отчёту 2017 г")

plt.savefig( ".\\Graphs\\figure_09_11.png")
fig.show()
