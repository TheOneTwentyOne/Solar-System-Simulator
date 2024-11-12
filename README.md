### Step 1: Compile
```bash
gfortran -Jbin -Ofast -o bin/main celestial_body.f90 local_solar_system.f90 SolarSystemSim.f90
```

### Step 2: Run
```bash
time ./bin/main
```
