from Utilities import *

def GetFile( data_name, sum_data_EIA, sum_well_HP, sum_well_HA, sum_well_P, sum_well_A, proj_name="Hughes2014"):
    bft2bmy = 0.3048**3 * 365
    Y,AEO2016 = Load_Calibration( data_name, "Year", "AEO2016") 
    Hughes,Actual = Load_Calibration( data_name, proj_name, "Actual")
    AEO2016 *= bft2bmy 
    Hughes *= bft2bmy
    Actual *= bft2bmy
    sp = int( Y[0] - 1994)
    for i in range( sp, len(sum_data_EIA)):
        sum_data_EIA[i] += AEO2016[i-sp]
        sum_well_HP[i] += Hughes[i-sp]
        sum_well_HA[i] += Actual[i-sp]
    WP,WA = Load_Calibration( data_name, "Wells_Plan", "Wells_Actual")
    if len(WP) < 1: return np.array( sum_well_HP)
    for i in range( sp, len(sum_data_EIA)):
        sum_well_P[i] += WP[i-sp]
        sum_well_A[i] += WA[i-sp]
    return np.array( sum_well_HP)

Year = np.linspace( 1994, 2040, 47)
sum_EIA = np.zeros( len( Year))
sum_HP = np.zeros( len( Year))
sum_HA = np.zeros( len( Year))
sum_WP = np.ones( len( Year)) * 20000
sum_WA = np.ones( len( Year)) * 20000
f1_Barnett = GetFile( "./Data/US01_Barnett_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f2_Marcellus = GetFile( "./Data/US02_Marcellus_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f3_Haynesville = GetFile( "./Data/US03_Haynesville_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f4_EagleFord = GetFile( "./Data/US04_EagleFord_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f5_Fayetteville = GetFile( "./Data/US05_Fayetteville_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f6_Woodford = GetFile( "./Data/US06_Woodford_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f7_Bakken = GetFile( "./Data/US07_Bakken_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f8_Haynesville = GetFile( "./Data/US08_Utica_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA, proj_name="Yakimov2017")
f9_Others = GetFile( "./Data/US09_Others_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
for i in range( 6):
    sum_HP[i] += 19.6
    sum_HA[i] += 19.6

Prediction_T = np.linspace( 2017, 2100, 84)
Prediction_Conventional = Hubbert( 1998, 1, .085, 600, 100).GetVector( Prediction_T)
Prediction_TG_Huges = Hubbert( 2016, 1, .07, 428).GetVector( Prediction_T)
Prediction_TG_EIA = Hubbert( 2042, .07, .107, 820).GetVector( Prediction_T)
Prediction_Total_Huges = Prediction_Conventional/1.1 + Prediction_TG_Huges 
Prediction_Total_EIA = Prediction_Conventional/1.1 + Prediction_TG_EIA

EIA_Year, EIA_Withdrawals = Load_Calibration( "./Data/US11_US_Gas_EIA.csv", "year", "gross")
EIA_Repress, EIA_VnF = Load_Calibration( "./Data/US11_US_Gas_EIA.csv", "repress", "vnf")
EIA_GW, EIA_OW = Load_Calibration( "./Data/US11_US_Gas_EIA.csv", "gas_wells", "oil_wells")
EIA_TG, EIA_CBM = Load_Calibration( "./Data/US11_US_Gas_EIA.csv", "TG_wells", "CBM_wells")
EIA_Repress, EIA_VnF = Load_Calibration( "./Data/US11_US_Gas_EIA.csv", "repress", "vnf")
EIA_dry, EIA_Marketed = Load_Calibration( "./Data/US11_US_Gas_EIA.csv", "dry", "marketed")
mfty2bmy = 0.3048**3/1000
EIA_Withdrawals *= mfty2bmy
EIA_Repress *= mfty2bmy
EIA_VnF *= mfty2bmy
EIA_GW *= mfty2bmy
EIA_OW *= mfty2bmy
EIA_TG *= mfty2bmy
EIA_CBM *= mfty2bmy
EIA_dry *= mfty2bmy
EIA_Marketed *= mfty2bmy
EIA_Extracted = EIA_Withdrawals - EIA_Repress
EIA_Production = EIA_Extracted - EIA_VnF 

for i in range( len(EIA_CBM)):
    if EIA_GW[i] < 0: EIA_GW[i] = 0
    if EIA_OW[i] < 0: EIA_OW[i] = 0
    if EIA_TG[i] < 0: EIA_TG[i] = 0
    if EIA_CBM[i] < 0: EIA_CBM[i] = 0
for i in range( 36):
    EIA_Production[i] = EIA_Marketed[i]    
    EIA_dry[i] = EIA_Marketed[i]    
    EIA_Extracted[i] = EIA_Marketed[i] * 1.1
    EIA_Withdrawals[i] = EIA_Marketed[i] * 1.1 
    
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Добыча природного газа в США', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( EIA_Year, EIA_Withdrawals, "-", lw=1, color='r', label="Добыча всего")
ax1.plot( EIA_Year, EIA_Extracted, "-", lw=3, color='r', label="Минус закачка ({:.1f}·10¹² м³)".format(np.sum(EIA_Extracted)/1000))
ax1.plot( Year[:-24], sum_HP[:-24], "-", lw=3, color='m', label="Коммерческий сланцевый газ")
ax1.plot( Prediction_T, Prediction_Total_Huges, "--", lw=3, color='b', label="Hughes-2016 ({:.1f}·10¹² м³)".format(np.sum(Prediction_Total_Huges)/1000))
ax1.plot( Prediction_T, Prediction_Total_EIA, "-", lw=3, color='b', label="AEO-2016 ({:.1f}·10¹² м³)".format(np.sum(Prediction_TG_EIA)/1000))
ax1.plot( Prediction_T, Prediction_TG_Huges, "--", lw=3, color='m')
##ax1.plot( Prediction_T, Prediction_Total_EIA, "-.", lw=2, color='r')
ax1.set_xlim( 1900, 2100)
ax1.set_ylim( 0, 1100)
ax1.set_ylabel("Млрд м³ в год")
ax1.grid(True)
ax1.set_title( "Добыча газа")
ax1.legend(loc=0)
ax1.annotate("Несуществующие перспективные запасы 8·10¹² м³", xy=(2043, 793), xytext=(1995, 1000), arrowprops=dict(facecolor='black', shrink=0.05))

ax2.plot( EIA_Year[67:], EIA_OW[67:]+EIA_GW[67:]+EIA_CBM[67:], "-", lw=3, color='k', label='Рудничный газ')
ax2.plot( EIA_Year[67:], EIA_GW[67:]+EIA_OW[67:], "-", lw=3, color='r', label='"Классический" газ')
ax2.plot( EIA_Year[67:], EIA_OW[67:], "-", lw=2, color='g', label='Попутный газ')
ax2.plot( Prediction_T, Prediction_Conventional, "--", lw=3, color='k', label='Экстраполяция')
ax2.set_xlim( 1900, 2100)
ax2.set_ylim( 0, 800)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Млрд м³ в год")
ax2.grid(True)
ax2.set_title( "Добыча по типу местрождения")
ax2.legend(loc=2)

plt.savefig( ".\\Graphs\\figure_11_12.png")
fig.show()
