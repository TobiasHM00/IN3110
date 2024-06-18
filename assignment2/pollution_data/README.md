# Pollution data - metadata

The `pollution_data` directory contains data on amounts of air pollution in Norway, measured in " $1000$ tonne $\mathrm{CO_2}$ equivalents" as function of year for the period $1990 - 2022$, from different sources: air traffic, farming, industry, oil and gas production and road_traffic. The air pollution data is divided into different types of greenhouse gasses. The data retrieved and adapted from SSB (https://www.ssb.no/statbank/sq/10084054).

The possible greenhouse gasses that could be documented are ${\mathrm{CO_2}, \mathrm{CH_4}, \mathrm{N_2O}, \mathrm{SF_6}, \mathrm{H_2}}$. These are some of the gasses monitored by _World meteorological organization_, but not all of them might be present in this directory.

## Note

To prevent long folder names, only a shortened version of the complete pollution source was used as folder names under `by_src`

Here is a mapping from our folder names to the complete source name referred to by SSB:

- `src_airtraffic` - Aviation, navigation, fishing, motor equipment etc.
- `src_agriculture` - Agriculture
- `src_industry` - Manufacturing industries and mining
- `src_oil_and_gas` - Oil and gas extraction
- `src_road_traffic` - Road traffic
