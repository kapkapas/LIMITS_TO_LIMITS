from Predictions import *

class Markov_Chain:
    def __init__( self, taus, Years, Year0, time_shift=0):
        self.Years = Years
        self.Year0 = Year0
        self.Filter = self.GetRho(taus[0])
        offset = int( self.Year0 - self.Years[0]) 
        for i in range( 1, len(taus)):
            self.Filter = np.convolve( self.Filter, self.GetRho(taus[i]))[offset:offset+len(self.Years)]
        self.Filter = np.roll( self.Filter, time_shift)
        return        
    def GetRho(self, tau):
        Time = self.Years - self.Year0
        tmp = np.exp( -Time/tau)
        for i in range( len(self.Years)):
            if self.Years[i]>=self.Year0: break
            tmp[i] = 0.0
        norm = np.sum( tmp)
        #print( tau, norm, 1/norm)
        return tmp/norm

Years = np.linspace( 1800,2200,401)
mc = Markov_Chain([3, 8, 5, 10], Years, Years[0])
Discovery = np.zeros( len(Years))

dYear, Discovery_Actual = Load_Calibration( "./Data/Backdated_Discovery_Laherrere_2014.csv", "Year", "Discovery")
for i in range(len(Years)):
    if Years[i] < dYear[0]: continue
    if dYear[-1] < Years[i]: break
    Discovery[i] = Discovery_Actual[ int(Years[i]-dYear[0])]
for i in range(99,-1,-1):
    Discovery[i] = Discovery[i+1] * 0.92

Discovery_Projected = np.array( Discovery)
for i in range(215,len(Years)):
    Discovery_Projected[i] = Discovery_Projected[i-1] * 0.965

Developed_Resource = np.convolve( mc.Filter, Discovery_Projected)[0:len(Years)]

Cumulative_Discovery = np.array( Discovery_Projected)
Cumulative_Developed = np.array( Developed_Resource)
for i in range( 1, len(Years)):
    Cumulative_Discovery[i] += Cumulative_Discovery[i-1]
    Cumulative_Developed[i] += Cumulative_Developed[i-1]

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Aлгоритм "Нефтяной шок" (П.Пукайт)', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1.5, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Обнаружение и подготовка месторождений нефти")
ax1.plot( Years[50:], mc.Filter[0:-50]*10000, "--", lw=2, color="k", label="Фильтр х 10'000")
ax1.plot( Years, Discovery, "-", lw=2, color="b", label="Открытия (Лагеррер, 2014), URR={:.0f} млрд т".format( np.sum(Discovery)/1000))
ax1.plot( Years, Discovery_Projected, "--", lw=2, color="b", label="Будущие открытия, URR={:.0f} млрд т".format( np.sum(Discovery_Projected)/1000))
ax1.plot( Years, Developed_Resource, "-", lw=2, color="g", label="Освоенные ресурсы, URR={:.0f} млрд т".format( np.sum(Developed_Resource)/1000))
ax1.set_xlim( 1850, 2150)
ax1.set_ylim( 0, 6000)
ax1.set_ylabel("млн тонн")
ax1.grid(True)
ax1.legend(loc=0)

ax2.set_title("Запасы")
ax2.plot( Years, Cumulative_Discovery/1000, "-", lw=2, color="b", label="Всего открыто (Лагеррер, 2014)")
ax2.plot( Years, Cumulative_Developed/1000, "-", lw=2, color="g", label="Всего освоено (модель)")
ax2.set_xlim( 1850, 2150)
ax2.set_ylim( 0, 320)
ax2.set_xlabel("Год")
ax2.set_ylabel("млрд тонн")
ax2.grid(True)
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_16_04.png")
fig.show()
