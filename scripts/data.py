import csv

class Henakart:
    """Start the class Henakart where I can open and set up the CSV files sent by email."""
    def __init__(self, csv_name):
        self.csv_name = csv_name

    @property
    def cleaning_data(self):
        data = self.csv_name
        data = [r.split(";") for r in data]
        data[0].insert(0, "Vuelta")
        data[0].pop(-1)

        valor_reemplazo = "0"
        for fila in data:
            for i, datos in enumerate(fila):
                fila[i] = fila[i].strip()
                if datos == '' or datos == "\n": 
                    fila[i]= valor_reemplazo
        return data    
    @property
    def swap_rows(self): #list: [driver [lap_time]]
        new_data = self.cleaning_data[0:]
        data_swap = []
        n = len(new_data[0])
        for r in range(0, n):    
            data_swap.append([v[r] for v in new_data])  
        return data_swap
    
    """VARIABLES for the CHARTS"""
    
    @property
    def race(self): #ALL driver times lap by lap --> Dict race = {piloto: tiempos: FLOAT} 
        swap_rows = self.swap_rows[1:]
        carrera = {}
        for carreras in swap_rows:
            carrera [carreras[0]] = carreras[1:]
        for tiempos in carrera.values():
            for i, t in enumerate(tiempos):
                tiempos[i] = float(t)
        return carrera
    
    
    @property #LIST with the laps [1,2,3,4,5...]
    def laps_base(self):
        for d, t in self.race.items():
            l = [x + 1 for x in range(len(t[:]))]
        return l      
            
        
    @property #LIST with the DRIVER NAMES
    def drivers(self):
        driver = [d for d in self.race.keys()]
        return driver

    def race_driver(self, driver = False): #{Driver: time}
        race_d = {}
        for d, t in self.race.items():
            if d == driver:
                race_d[d] = t
        return race_d
    

    @property
    def absolute_mean(self): #ABSOLUTE MEAN
        mean_list =[]
        for laps in self.race.values():
            for t in laps:
                if t == 0.0:
                    continue
                mean_list.append(t)
        mean = round(sum(mean_list)/len(mean_list), 3)
        m = []
        l = len(self.laps_base)
        for x in range(1, l + 1):
            m.append(mean)

        return m
    
    def mean_per_driver(self, driver = None): #MEAN BY DRIVER
        
        mean_driver = {}
        pilot = {}
        for d, t in self.race.items():
            for tt in t:
                if tt == 0.0:
                    continue
                elif d not in mean_driver:
                    mean_driver[d]= []
                mean_driver[d].append(tt)
        for d, time in mean_driver.items():
            mean_driver[d]=[round(sum(time)/len(time), 3)]
        if driver is not None:
            for d, time in mean_driver.items():
                if d == driver:
                    pilot[d] = time
            return pilot             
        else:
            return mean_driver


    @property #MEAN LAP BY LAP
    def mean_per_lap(self):
        mean_pl = {}
        mean = self.race.copy()
        mean_perlap = []
        
        for t in mean.values():
            for i, tt in enumerate(t):
                if tt == 0.0 or tt >= 100.00:
                    continue
                if i not in mean_pl:
                    mean_pl[i]=[]
                mean_pl[i].append(tt)
        
        for v, t in mean_pl.items():
            mean_perlap.append(round(sum(t)/len(t), 3))
        return mean_perlap
    
    @property #ABSOLUTE BEST LAP OF THE RACE
    def best_lap_absolute(self):
        best_la = []
        best_abs = self.race.copy()
        best_lap = 10000E50
        for tiempos in best_abs.values():
            for t in tiempos:
                if t == 0.0:
                    continue
                if t <= best_lap:
                    best_lap = t
            best_la = best_lap
        m = []
        l = len(self.laps_base)
        for x in range(1, l + 1):
            m.append(best_la)
        return  m
        
    @property # BEST LAP BY LAP
    def best_lap_lap(self):
        best_pl = {}
        bestpl = self.race.copy()
        best_lap = 10000E50
        best_lpl = []
        for t in bestpl.values():
            for i, tt in enumerate(t):
                if tt == 0.0 or tt >= 100.00:
                    continue
                if i not in best_pl:
                    best_pl[i]=[]
                best_pl[i].append(tt)
        for x, y in best_pl.items():
            best_lpl.append(min(y))
        return best_lpl
                
    def best_lap_driver(self, driver = None): #BEST LAP BY DRIVER
        bestpd = self.race.copy()
        best_pd = {}
        for d, t in bestpd.items():
            for tt in t:
                if tt == 0.0:
                    continue
                if d not in best_pd:
                    best_pd[d] = []
                best_pd[d].append(tt)  
        for d, t in best_pd.items():
            best_pd[d]= [min(t)]
        if driver is not None:
            for d, t in best_pd.items():
                if d == driver:
                    return f"{driver}: {best_pd[d]}"
        else:
            return best_pd
    @property
    def all_vars(self): #Dict with driver´s lap by lap times, and adding four of the above variables
        race_all_variable  = self.race.copy()
        race_all_variable["ABSOLUTE MEAN OF THE RACE"] = self.absolute_mean
        race_all_variable["ABSOLUTE BEST LAP OF THE RACE"] = self.best_lap_absolute
        race_all_variable["MEAN PER LAP"] = self.mean_per_lap
        race_all_variable["BEST LAP PER LAP"] = self.best_lap_lap
        
        return race_all_variable
    @property
    def variables(self):
        variab = []
        for v, t in self.all_vars.items():
            variab.append(v)

        return variab

    
        
if __name__ == "__main__":
    pass