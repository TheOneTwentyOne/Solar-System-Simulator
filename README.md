### Step 1: Compile
gfortran Linux:
```bash
gfortran -Jbin -Ofast -o bin/main celestial_body.f90 local_solar_system.f90 SolarSystemSim.f90
```
or, ifort Windows:
```bash
ifort /module:bin /Ofast /exe:bin\main.exe celestial_body.f90 local_solar_system.f90 SolarSystemSim.f90
```
or, ifx Windows
```bash
ifx /module:bin /Ofast /exe:bin\main.exe celestial_body.f90 local_solar_system.f90 SolarSystemSim.f90
```

### Step 2: Run
```bash
time ./bin/main
```
