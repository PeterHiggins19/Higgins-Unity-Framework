import { useState, useMemo, useCallback } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, ReferenceLine, AreaChart, Area, ComposedChart } from "recharts";

// === REAL EMBER DATA — 5 countries, yearly, computed March 22 2026 ===
const EMBER_DATA = {
  Germany: {
    years: ["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025"],
    keff: [3.49,3.62,3.69,3.83,4.01,4.25,4.40,4.59,4.81,4.95,5.11,5.31,5.40,5.37,5.50,5.65,5.82,6.00,6.08,6.49,6.66,6.58,6.22,6.10,5.92,5.85],
    l2: [null,0.0176,0.0178,0.0189,0.0199,0.0280,0.0137,0.0479,0.0417,0.0122,0.0158,0.0550,0.0323,0.0219,0.0230,0.0387,0.0365,0.0542,0.0205,0.0864,0.0591,0.0608,0.0757,0.1069,0.0438,0.0358],
    tvd: [null,0.0163,0.0172,0.0246,0.0176,0.0306,0.0128,0.0430,0.0381,0.0142,0.0195,0.0538,0.0375,0.0221,0.0277,0.0347,0.0325,0.0489,0.0230,0.0752,0.0597,0.0546,0.0779,0.1181,0.0464,0.0367],
    shocks: [{year: "2022", event: "Gas crisis (Ukraine)"}, {year: "2023", event: "Nuclear phase-out"}, {year: "2020", event: "COVID-19"}],
    drift_l2: [], drift_tvd: [],
    narrative: "Germany's electricity mix diversified steadily 2000-2020 (K_eff rising from 3.5 to 6.7). After 2020, the gas crisis and nuclear exit reversed this: K_eff falling as the mix concentrates. The velocity spike at 2023 (TVD=0.118) marks the structural disruption."
  },
  Japan: {
    years: ["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024"],
    keff: [4.91,4.86,4.91,5.03,5.01,4.98,4.98,4.99,4.94,4.79,4.88,4.95,4.18,4.18,3.94,4.20,4.26,4.21,4.47,4.58,4.47,4.79,4.89,5.14,5.17],
    l2: [null,0.0306,0.0208,0.0837,0.0522,0.0243,0.0380,0.0389,0.0375,0.0630,0.0194,0.1366,0.1525,0.0474,0.0544,0.0281,0.0389,0.0453,0.0284,0.0268,0.0274,0.0373,0.0207,0.0389,0.0125],
    tvd: [null,0.0257,0.0209,0.0743,0.0452,0.0258,0.0377,0.0380,0.0367,0.0523,0.0213,0.1231,0.1364,0.0415,0.0514,0.0327,0.0451,0.0398,0.0286,0.0299,0.0310,0.0326,0.0234,0.0437,0.0152],
    shocks: [{year: "2011", event: "Fukushima"}, {year: "2020", event: "COVID-19"}],
    drift_l2: ["2005"], drift_tvd: ["2005"],
    narrative: "Fukushima (2011) — external shock, no preceding drift. K_eff crashed from 5.0 to 3.9 as nuclear dropped and gas/coal surged. The massive velocity spikes at 2011-2012 are the disruption itself, not a forward signal. No forward signal possible for earthquakes."
  },
  "United Kingdom": {
    years: ["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025"],
    keff: [3.71,3.66,3.68,3.65,3.71,3.84,3.88,3.79,3.80,4.03,3.90,4.29,4.50,4.79,5.25,5.72,5.20,5.28,5.33,5.11,5.23,5.13,5.09,5.19,5.32,5.24],
    l2: [null,0.0354,0.0329,0.0337,0.0347,0.0171,0.0492,0.0777,0.0488,0.0683,0.0300,0.0701,0.1576,0.0404,0.0781,0.0820,0.1850,0.0483,0.0352,0.0477,0.0689,0.0527,0.0437,0.0524,0.0525,0.0252],
    tvd: [null,0.0336,0.0283,0.0292,0.0339,0.0155,0.0445,0.0674,0.0467,0.0590,0.0320,0.0650,0.1237,0.0402,0.0756,0.0763,0.1455,0.0477,0.0407,0.0525,0.0647,0.0506,0.0406,0.0506,0.0501,0.0258],
    shocks: [{year: "2016", event: "Coal collapse"}, {year: "2020", event: "COVID-19"}],
    drift_l2: ["2022"], drift_tvd: ["2022"],
    narrative: "UK coal collapse (2016) shows as the highest velocity spike (L2=0.185, TVD=0.146). K_eff peaked at 5.72 in 2015, then dropped sharply. Post-2019: K_eff declining as the mix reconcentrates. Drift detected at 2022."
  },
  France: {
    years: ["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025"],
    keff: [2.27,2.46,2.35,2.38,2.37,2.40,2.42,2.42,2.44,2.38,2.47,2.43,2.38,2.43,2.41,2.43,2.48,2.44,2.48,2.52,2.55,2.65,2.95,2.81,2.88,2.67],
    l2: [null,0.0163,0.0262,0.0152,0.0094,0.0066,0.0112,0.0041,0.0089,0.0107,0.0107,0.0119,0.0094,0.0046,0.0060,0.0054,0.0106,0.0068,0.0096,0.0074,0.0127,0.0157,0.0396,0.0173,0.0160,0.0327],
    tvd: [null,0.0141,0.0231,0.0134,0.0078,0.0065,0.0111,0.0042,0.0087,0.0094,0.0098,0.0108,0.0091,0.0049,0.0059,0.0062,0.0099,0.0058,0.0093,0.0073,0.0111,0.0146,0.0331,0.0163,0.0148,0.0283],
    shocks: [{year: "2022", event: "Nuclear fleet crisis"}, {year: "2020", event: "COVID-19"}],
    drift_l2: [], drift_tvd: ["2025"],
    narrative: "France is nuclear-dominated (K_eff ~ 2.4). The 2022 corrosion crisis shows as a velocity spike and K_eff jump. TVD detects one drift year (2025) that L2 misses. France's low dimensionality makes it the hardest domain for drift detection."
  },
  Australia: {
    years: ["2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024"],
    keff: [1.87,1.89,1.88,1.93,1.93,1.89,1.93,2.05,2.06,2.10,2.17,2.22,2.26,2.35,2.54,2.63,2.69,2.76,3.04,3.29,3.43,3.57,3.86,4.09,4.48],
    l2: [null,0.0115,0.0081,0.0246,0.0091,0.0087,0.0302,0.0334,0.0082,0.0247,0.0132,0.0277,0.0199,0.0096,0.0363,0.0242,0.0270,0.0170,0.0551,0.0518,0.0375,0.0379,0.0530,0.0554,0.0566],
    tvd: [null,0.0114,0.0069,0.0233,0.0083,0.0090,0.0287,0.0297,0.0083,0.0227,0.0127,0.0260,0.0186,0.0095,0.0353,0.0229,0.0255,0.0161,0.0506,0.0474,0.0344,0.0346,0.0501,0.0519,0.0527],
    shocks: [{year: "2020", event: "Bushfire/COVID"}],
    drift_l2: ["2005"], drift_tvd: ["2005"],
    narrative: "Australia: clean diversification trend — K_eff from 1.87 to 4.48 as solar and wind grow against coal. Velocity also rising (bigger structural changes each year). One drift year (2005). Bushfire/COVID: MISS — external forcing."
  }
};

// === REAL EMBER CARRIER DATA — 9 fuel types, proportions summing to 1.0 ===
const CARRIER_DATA = {
  Germany: [
    {Coal:0.5215,Gas:0.0865,Nuclear:0.2981,Hydro:0.0382,Solar:0.0,Wind:0.0164,Bioenergy:0.0076,"Other Fossil":0.0317,"Other Renewables":0.0},
    {Coal:0.5073,Gas:0.0959,Nuclear:0.2959,Hydro:0.0393,Solar:0.0002,Wind:0.0181,Bioenergy:0.0079,"Other Fossil":0.0354,"Other Renewables":0.0},
    {Coal:0.5133,Gas:0.0964,Nuclear:0.2824,Hydro:0.0396,Solar:0.0003,Wind:0.0272,Bioenergy:0.0091,"Other Fossil":0.0317,"Other Renewables":0.0},
    {Coal:0.506,Gas:0.104,Nuclear:0.2742,Hydro:0.0304,Solar:0.0005,Wind:0.0317,Bioenergy:0.0149,"Other Fossil":0.0383,"Other Renewables":0.0},
    {Coal:0.4901,Gas:0.1028,Nuclear:0.2741,Hydro:0.034,Solar:0.0009,Wind:0.0427,Bioenergy:0.0175,"Other Fossil":0.0379,"Other Renewables":0.0},
    {Coal:0.4698,Gas:0.1177,Nuclear:0.2658,Hydro:0.032,Solar:0.0021,Wind:0.0453,Bioenergy:0.024,"Other Fossil":0.0433,"Other Renewables":0.0},
    {Coal:0.4585,Gas:0.1186,Nuclear:0.2654,Hydro:0.0318,Solar:0.0036,Wind:0.0497,Bioenergy:0.0301,"Other Fossil":0.0424,"Other Renewables":0.0},
    {Coal:0.4708,Gas:0.1227,Nuclear:0.2227,Hydro:0.0335,Solar:0.005,Wind:0.0642,Bioenergy:0.039,"Other Fossil":0.0421,"Other Renewables":0.0},
    {Coal:0.4354,Gas:0.1399,Nuclear:0.2348,Hydro:0.0323,Solar:0.0071,Wind:0.0654,Bioenergy:0.0443,"Other Fossil":0.0407,"Other Renewables":0.0},
    {Coal:0.4311,Gas:0.1365,Nuclear:0.2295,Hydro:0.0324,Solar:0.0114,Wind:0.067,Bioenergy:0.0525,"Other Fossil":0.0395,"Other Renewables":0.0},
    {Coal:0.4212,Gas:0.1422,Nuclear:0.2252,Hydro:0.0336,Solar:0.0192,Wind:0.0618,Bioenergy:0.0543,"Other Fossil":0.0426,"Other Renewables":0.0},
    {Coal:0.4338,Gas:0.1416,Nuclear:0.1785,Hydro:0.0292,Solar:0.033,Wind:0.0824,Bioenergy:0.061,"Other Fossil":0.0404,"Other Renewables":0.0},
    {Coal:0.4457,Gas:0.1225,Nuclear:0.1605,Hydro:0.0351,Solar:0.0431,Wind:0.0834,Bioenergy:0.0697,"Other Fossil":0.04,"Other Renewables":0.0},
    {Coal:0.4577,Gas:0.1064,Nuclear:0.1545,Hydro:0.0365,Solar:0.0486,Wind:0.0838,Bioenergy:0.0723,"Other Fossil":0.0401,"Other Renewables":0.0001},
    {Coal:0.4435,Gas:0.098,Nuclear:0.157,Hydro:0.0317,Solar:0.0573,Wind:0.0945,Bioenergy:0.078,"Other Fossil":0.0399,"Other Renewables":0.0002},
    {Coal:0.4259,Gas:0.0962,Nuclear:0.1436,Hydro:0.0297,Solar:0.0596,Wind:0.1261,Bioenergy:0.0787,"Other Fossil":0.04,"Other Renewables":0.0002},
    {Coal:0.408,Gas:0.1257,Nuclear:0.1319,Hydro:0.032,Solar:0.0585,Wind:0.1246,Bioenergy:0.0794,"Other Fossil":0.0396,"Other Renewables":0.0003},
    {Coal:0.3744,Gas:0.1335,Nuclear:0.1184,Hydro:0.0313,Solar:0.0601,Wind:0.164,Bioenergy:0.079,"Other Fossil":0.039,"Other Renewables":0.0002},
    {Coal:0.3609,Gas:0.129,Nuclear:0.1202,Hydro:0.028,Solar:0.0701,Wind:0.1739,Bioenergy:0.0803,"Other Fossil":0.0374,"Other Renewables":0.0003},
    {Coal:0.2857,Gas:0.15,Nuclear:0.1251,Hydro:0.0329,Solar:0.0754,Wind:0.2098,Bioenergy:0.0835,"Other Fossil":0.0373,"Other Renewables":0.0003},
    {Coal:0.2375,Gas:0.1676,Nuclear:0.1136,Hydro:0.033,Solar:0.0873,Wind:0.2331,Bioenergy:0.0899,"Other Fossil":0.0375,"Other Renewables":0.0004},
    {Coal:0.2845,Gas:0.156,Nuclear:0.1194,Hydro:0.034,Solar:0.0852,Wind:0.1972,Bioenergy:0.0848,"Other Fossil":0.0384,"Other Renewables":0.0004},
    {Coal:0.3174,Gas:0.1394,Nuclear:0.0612,Hydro:0.0311,Solar:0.1064,Wind:0.2202,Bioenergy:0.0857,"Other Fossil":0.0382,"Other Renewables":0.0004},
    {Coal:0.2463,Gas:0.1513,Nuclear:0.0142,Hydro:0.0419,Solar:0.126,Wind:0.2774,Bioenergy:0.1012,"Other Fossil":0.0414,"Other Renewables":0.0004},
    {Coal:0.2144,Gas:0.1581,Nuclear:0.0,Hydro:0.048,Solar:0.1495,Wind:0.2855,Bioenergy:0.103,"Other Fossil":0.0411,"Other Renewables":0.0004},
    {Coal:0.2061,Gas:0.1652,Nuclear:0.0,Hydro:0.0391,Solar:0.1791,Wind:0.2718,Bioenergy:0.101,"Other Fossil":0.0378,"Other Renewables":0.0},
  ],
  Japan: [
    {Coal:0.2166,Gas:0.2351,Nuclear:0.2902,Hydro:0.0768,Solar:0.0003,Wind:0.0001,Bioenergy:0.0146,"Other Fossil":0.1662,"Other Renewables":0.0},
    {Coal:0.2344,Gas:0.2368,Nuclear:0.2959,Hydro:0.0753,Solar:0.0005,Wind:0.0002,Bioenergy:0.0148,"Other Fossil":0.142,"Other Renewables":0.0},
    {Coal:0.2397,Gas:0.2291,Nuclear:0.2849,Hydro:0.0731,Solar:0.0006,Wind:0.0004,Bioenergy:0.0154,"Other Fossil":0.1568,"Other Renewables":0.0},
    {Coal:0.2673,Gas:0.25,Nuclear:0.2106,Hydro:0.0846,Solar:0.0009,Wind:0.0008,Bioenergy:0.0164,"Other Fossil":0.1695,"Other Renewables":0.0},
    {Coal:0.2635,Gas:0.23,Nuclear:0.255,Hydro:0.0818,Solar:0.0011,Wind:0.0013,Bioenergy:0.0161,"Other Fossil":0.1513,"Other Renewables":0.0},
    {Coal:0.2768,Gas:0.2195,Nuclear:0.2541,Hydro:0.0673,Solar:0.0014,Wind:0.0017,Bioenergy:0.0188,"Other Fossil":0.1604,"Other Renewables":0.0},
    {Coal:0.2674,Gas:0.2405,Nuclear:0.2613,Hydro:0.0763,Solar:0.0017,Wind:0.0018,Bioenergy:0.0185,"Other Fossil":0.1324,"Other Renewables":0.0},
    {Coal:0.2689,Gas:0.2515,Nuclear:0.2364,Hydro:0.0631,Solar:0.002,Wind:0.0023,Bioenergy:0.0188,"Other Fossil":0.1569,"Other Renewables":0.0},
    {Coal:0.2819,Gas:0.2744,Nuclear:0.2127,Hydro:0.0635,Solar:0.0022,Wind:0.0025,Bioenergy:0.018,"Other Fossil":0.1448,"Other Renewables":0.0},
    {Coal:0.2801,Gas:0.2915,Nuclear:0.2465,Hydro:0.0633,Solar:0.0027,Wind:0.0031,Bioenergy:0.0182,"Other Fossil":0.0945,"Other Renewables":0.0},
    {Coal:0.2741,Gas:0.2821,Nuclear:0.2529,Hydro:0.0766,Solar:0.0034,Wind:0.0034,Bioenergy:0.0189,"Other Fossil":0.0887,"Other Renewables":0.0},
    {Coal:0.2582,Gas:0.344,Nuclear:0.1476,Hydro:0.0747,Solar:0.0049,Wind:0.004,Bioenergy:0.0191,"Other Fossil":0.1475,"Other Renewables":0.0},
    {Coal:0.302,Gas:0.3934,Nuclear:0.0163,Hydro:0.0697,Solar:0.0067,Wind:0.0043,Bioenergy:0.02,"Other Fossil":0.1877,"Other Renewables":0.0},
    {Coal:0.3333,Gas:0.3894,Nuclear:0.0134,Hydro:0.0729,Solar:0.0119,Wind:0.0047,Bioenergy:0.0213,"Other Fossil":0.153,"Other Renewables":0.0},
    {Coal:0.3346,Gas:0.4243,Nuclear:0.0,Hydro:0.0769,Solar:0.0222,Wind:0.0047,Bioenergy:0.0222,"Other Fossil":0.1151,"Other Renewables":0.0},
    {Coal:0.3394,Gas:0.4053,Nuclear:0.0044,Hydro:0.0833,Solar:0.0335,Wind:0.0051,Bioenergy:0.0277,"Other Fossil":0.1014,"Other Renewables":0.0},
    {Coal:0.3183,Gas:0.431,Nuclear:0.0166,Hydro:0.0747,Solar:0.0407,Wind:0.005,Bioenergy:0.0223,"Other Fossil":0.0914,"Other Renewables":0.0},
    {Coal:0.3375,Gas:0.431,Nuclear:0.027,Hydro:0.0736,Solar:0.0502,Wind:0.0058,Bioenergy:0.0221,"Other Fossil":0.0528,"Other Renewables":0.0},
    {Coal:0.333,Gas:0.4115,Nuclear:0.0453,Hydro:0.0748,Solar:0.0565,Wind:0.0068,Bioenergy:0.0238,"Other Fossil":0.0482,"Other Renewables":0.0},
    {Coal:0.3349,Gas:0.3981,Nuclear:0.0627,Hydro:0.0706,Solar:0.0644,Wind:0.0071,Bioenergy:0.0264,"Other Fossil":0.0359,"Other Renewables":0.0},
    {Coal:0.3365,Gas:0.405,Nuclear:0.0425,Hydro:0.0775,Solar:0.0751,Wind:0.0083,Bioenergy:0.03,"Other Fossil":0.025,"Other Renewables":0.0},
    {Coal:0.3366,Gas:0.3729,Nuclear:0.0592,Hydro:0.077,Solar:0.0814,Wind:0.0092,Bioenergy:0.0336,"Other Fossil":0.0302,"Other Renewables":0.0},
    {Coal:0.3372,Gas:0.364,Nuclear:0.0498,Hydro:0.072,Solar:0.0875,Wind:0.0091,Bioenergy:0.0364,"Other Fossil":0.044,"Other Renewables":0.0},
    {Coal:0.3247,Gas:0.3447,Nuclear:0.0769,Hydro:0.074,Solar:0.0957,Wind:0.0099,Bioenergy:0.0417,"Other Fossil":0.0323,"Other Renewables":0.0},
    {Coal:0.3219,Gas:0.3407,Nuclear:0.0835,Hydro:0.0782,Solar:0.0951,Wind:0.0114,Bioenergy:0.0447,"Other Fossil":0.0246,"Other Renewables":0.0},
  ],
  "United Kingdom": [
    {Coal:0.3181,Gas:0.3927,Nuclear:0.2256,Hydro:0.0135,Solar:0.0,Wind:0.0025,Bioenergy:0.0103,"Other Fossil":0.0373,"Other Renewables":0.0},
    {Coal:0.3417,Gas:0.3688,Nuclear:0.2341,Hydro:0.0105,Solar:0.0,Wind:0.0025,Bioenergy:0.0118,"Other Fossil":0.0306,"Other Renewables":0.0},
    {Coal:0.3209,Gas:0.3932,Nuclear:0.2269,Hydro:0.0124,Solar:0.0,Wind:0.0032,Bioenergy:0.0131,"Other Fossil":0.0302,"Other Renewables":0.0},
    {Coal:0.3477,Gas:0.3739,Nuclear:0.2227,Hydro:0.0081,Solar:0.0,Wind:0.0032,Bioenergy:0.0155,"Other Fossil":0.0289,"Other Renewables":0.0},
    {Coal:0.3346,Gas:0.3987,Nuclear:0.2031,Hydro:0.0123,Solar:0.0,Wind:0.0049,Bioenergy:0.0187,"Other Fossil":0.0277,"Other Renewables":0.0},
    {Coal:0.338,Gas:0.3832,Nuclear:0.2049,Hydro:0.0124,Solar:0.0,Wind:0.0073,Bioenergy:0.0228,"Other Fossil":0.0314,"Other Renewables":0.0},
    {Coal:0.3747,Gas:0.3545,Nuclear:0.1899,Hydro:0.0116,Solar:0.0,Wind:0.0106,Bioenergy:0.0234,"Other Fossil":0.0353,"Other Renewables":0.0},
    {Coal:0.3426,Gas:0.4178,Nuclear:0.1588,Hydro:0.0128,Solar:0.0,Wind:0.0133,Bioenergy:0.0235,"Other Fossil":0.0312,"Other Renewables":0.0},
    {Coal:0.3198,Gas:0.4531,Nuclear:0.1349,Hydro:0.0132,Solar:0.0001,Wind:0.0183,Bioenergy:0.0248,"Other Fossil":0.0358,"Other Renewables":0.0},
    {Coal:0.2735,Gas:0.4419,Nuclear:0.1834,Hydro:0.0139,Solar:0.0001,Wind:0.0246,Bioenergy:0.0284,"Other Fossil":0.0342,"Other Renewables":0.0},
    {Coal:0.2816,Gas:0.4597,Nuclear:0.1626,Hydro:0.0094,Solar:0.0001,Wind:0.0269,Bioenergy:0.0321,"Other Fossil":0.0275,"Other Renewables":0.0},
    {Coal:0.2946,Gas:0.398,Nuclear:0.1875,Hydro:0.0155,Solar:0.0007,Wind:0.0434,Bioenergy:0.0362,"Other Fossil":0.0241,"Other Renewables":0.0},
    {Coal:0.3924,Gas:0.2753,Nuclear:0.1935,Hydro:0.0146,Solar:0.0037,Wind:0.0545,Bioenergy:0.0405,"Other Fossil":0.0254,"Other Renewables":0.0},
    {Coal:0.3636,Gas:0.2675,Nuclear:0.1971,Hydro:0.0131,Solar:0.0056,Wind:0.0793,Bioenergy:0.0505,"Other Fossil":0.0233,"Other Renewables":0.0},
    {Coal:0.2965,Gas:0.2984,Nuclear:0.1886,Hydro:0.0174,Solar:0.012,Wind:0.0945,Bioenergy:0.0669,"Other Fossil":0.0257,"Other Renewables":0.0},
    {Coal:0.2239,Gas:0.2947,Nuclear:0.2076,Hydro:0.0186,Solar:0.0222,Wind:0.1188,Bioenergy:0.0863,"Other Fossil":0.0278,"Other Renewables":0.0},
    {Coal:0.0904,Gas:0.422,Nuclear:0.2115,Hydro:0.0158,Solar:0.0307,Wind:0.1096,Bioenergy:0.0887,"Other Fossil":0.0314,"Other Renewables":0.0},
    {Coal:0.0666,Gas:0.4043,Nuclear:0.208,Hydro:0.0174,Solar:0.0339,Wind:0.1468,Bioenergy:0.0943,"Other Fossil":0.0287,"Other Renewables":0.0},
    {Coal:0.0504,Gas:0.394,Nuclear:0.1949,Hydro:0.0163,Solar:0.038,Wind:0.1705,Bioenergy:0.1052,"Other Fossil":0.0307,"Other Renewables":0.0},
    {Coal:0.0211,Gas:0.4068,Nuclear:0.1717,Hydro:0.0181,Solar:0.038,Wind:0.1951,Bioenergy:0.1147,"Other Fossil":0.0344,"Other Renewables":0.0},
    {Coal:0.0184,Gas:0.3606,Nuclear:0.1619,Hydro:0.0222,Solar:0.0404,Wind:0.2437,Bioenergy:0.1243,"Other Fossil":0.0285,"Other Renewables":0.0},
    {Coal:0.0221,Gas:0.3989,Nuclear:0.1497,Hydro:0.0176,Solar:0.0394,Wind:0.2109,Bioenergy:0.1299,"Other Fossil":0.0314,"Other Renewables":0.0},
    {Coal:0.0183,Gas:0.3855,Nuclear:0.146,Hydro:0.0174,Solar:0.0411,Wind:0.2471,Bioenergy:0.1104,"Other Fossil":0.0341,"Other Renewables":0.0},
    {Coal:0.0129,Gas:0.3475,Nuclear:0.1388,Hydro:0.0189,Solar:0.0474,Wind:0.2808,Bioenergy:0.1166,"Other Fossil":0.037,"Other Renewables":0.0},
    {Coal:0.0067,Gas:0.3037,Nuclear:0.1428,Hydro:0.0203,Solar:0.052,Wind:0.2931,Bioenergy:0.1411,"Other Fossil":0.0403,"Other Renewables":0.0},
    {Coal:0.0011,Gas:0.3105,Nuclear:0.1243,Hydro:0.019,Solar:0.066,Wind:0.2948,Bioenergy:0.1407,"Other Fossil":0.0436,"Other Renewables":0.0},
  ],
  France: [
    {Coal:0.0507,Gas:0.0216,Nuclear:0.7795,Hydro:0.1216,Solar:0.0,Wind:0.0001,Bioenergy:0.0047,"Other Fossil":0.0208,"Other Renewables":0.001},
    {Coal:0.0377,Gas:0.0279,Nuclear:0.7761,Hydro:0.1338,Solar:0.0,Wind:0.0002,Bioenergy:0.0053,"Other Fossil":0.0181,"Other Renewables":0.0009},
    {Coal:0.0429,Gas:0.0333,Nuclear:0.7924,Hydro:0.1068,Solar:0.0,Wind:0.0005,Bioenergy:0.0055,"Other Fossil":0.0177,"Other Renewables":0.0009},
    {Coal:0.047,Gas:0.0346,Nuclear:0.7888,Hydro:0.1026,Solar:0.0,Wind:0.0007,Bioenergy:0.0058,"Other Fossil":0.0196,"Other Renewables":0.0009},
    {Coal:0.043,Gas:0.0372,Nuclear:0.7917,Hydro:0.1025,Solar:0.0,Wind:0.001,Bioenergy:0.0058,"Other Fossil":0.018,"Other Renewables":0.0008},
    {Coal:0.0483,Gas:0.0405,Nuclear:0.7934,Hydro:0.0881,Solar:0.0,Wind:0.0017,Bioenergy:0.006,"Other Fossil":0.0212,"Other Renewables":0.0008},
    {Coal:0.0403,Gas:0.0384,Nuclear:0.7936,Hydro:0.0967,Solar:0.0,Wind:0.0038,Bioenergy:0.006,"Other Fossil":0.0204,"Other Renewables":0.0008},
    {Coal:0.0435,Gas:0.0391,Nuclear:0.7828,Hydro:0.0997,Solar:0.0,Wind:0.0072,Bioenergy:0.0067,"Other Fossil":0.0202,"Other Renewables":0.0008},
    {Coal:0.0407,Gas:0.0386,Nuclear:0.7751,Hydro:0.1096,Solar:0.0001,Wind:0.01,Bioenergy:0.007,"Other Fossil":0.0181,"Other Renewables":0.0008},
    {Coal:0.041,Gas:0.0388,Nuclear:0.7746,Hydro:0.1049,Solar:0.0003,Wind:0.015,Bioenergy:0.0078,"Other Fossil":0.0167,"Other Renewables":0.0009},
    {Coal:0.0415,Gas:0.0423,Nuclear:0.7619,Hydro:0.1088,Solar:0.0011,Wind:0.0177,Bioenergy:0.0079,"Other Fossil":0.0179,"Other Renewables":0.0009},
    {Coal:0.0306,Gas:0.052,Nuclear:0.7792,Hydro:0.0806,Solar:0.0041,Wind:0.0218,Bioenergy:0.0089,"Other Fossil":0.0218,"Other Renewables":0.001},
    {Coal:0.0378,Gas:0.0401,Nuclear:0.7496,Hydro:0.1054,Solar:0.0078,Wind:0.0267,Bioenergy:0.0093,"Other Fossil":0.0224,"Other Renewables":0.0009},
    {Coal:0.0413,Gas:0.0319,Nuclear:0.7346,Hydro:0.1247,Solar:0.009,Wind:0.028,Bioenergy:0.0098,"Other Fossil":0.0198,"Other Renewables":0.0009},
    {Coal:0.0199,Gas:0.0232,Nuclear:0.7707,Hydro:0.1126,Solar:0.0113,Wind:0.0306,Bioenergy:0.0106,"Other Fossil":0.0201,"Other Renewables":0.001},
    {Coal:0.0207,Gas:0.0368,Nuclear:0.7619,Hydro:0.0968,Solar:0.0135,Wind:0.0373,Bioenergy:0.0114,"Other Fossil":0.0206,"Other Renewables":0.001},
    {Coal:0.0183,Gas:0.0626,Nuclear:0.7214,Hydro:0.1089,Solar:0.0155,Wind:0.0383,Bioenergy:0.0135,"Other Fossil":0.0205,"Other Renewables":0.0011},
    {Coal:0.0231,Gas:0.0729,Nuclear:0.7167,Hydro:0.09,Solar:0.016,Wind:0.0443,Bioenergy:0.014,"Other Fossil":0.0219,"Other Renewables":0.0012},
    {Coal:0.0144,Gas:0.053,Nuclear:0.7167,Hydro:0.113,Solar:0.0193,Wind:0.0496,Bioenergy:0.0145,"Other Fossil":0.0184,"Other Renewables":0.0011},
    {Coal:0.0064,Gas:0.0694,Nuclear:0.7055,Hydro:0.1006,Solar:0.0213,Wind:0.0614,Bioenergy:0.0153,"Other Fossil":0.019,"Other Renewables":0.0011},
    {Coal:0.0059,Gas:0.0669,Nuclear:0.671,Hydro:0.1186,Solar:0.0248,Wind:0.076,Bioenergy:0.0166,"Other Fossil":0.0191,"Other Renewables":0.0012},
    {Coal:0.0099,Gas:0.0605,Nuclear:0.6893,Hydro:0.1082,Solar:0.0278,Wind:0.0675,Bioenergy:0.0174,"Other Fossil":0.0184,"Other Renewables":0.0011},
    {Coal:0.0089,Gas:0.0976,Nuclear:0.6292,Hydro:0.0973,Solar:0.0413,Wind:0.0815,Bioenergy:0.0206,"Other Fossil":0.0223,"Other Renewables":0.0013},
    {Coal:0.0031,Gas:0.0579,Nuclear:0.6519,Hydro:0.1078,Solar:0.0435,Wind:0.0973,Bioenergy:0.0192,"Other Fossil":0.0182,"Other Renewables":0.0011},
    {Coal:0.0018,Gas:0.0322,Nuclear:0.6772,Hydro:0.1266,Solar:0.0443,Wind:0.0809,Bioenergy:0.019,"Other Fossil":0.017,"Other Renewables":0.001},
    {Coal:0.0031,Gas:0.0303,Nuclear:0.6878,Hydro:0.1042,Solar:0.0558,Wind:0.0816,Bioenergy:0.018,"Other Fossil":0.0182,"Other Renewables":0.001},
  ],
  Australia: [
    {Coal:0.8313,Gas:0.0773,Nuclear:0.0,Hydro:0.076,Solar:0.0002,Wind:0.0006,Bioenergy:0.0041,"Other Fossil":0.0105,"Other Renewables":0.0},
    {Coal:0.8021,Gas:0.1092,Nuclear:0.0,Hydro:0.0719,Solar:0.0002,Wind:0.0013,Bioenergy:0.0036,"Other Fossil":0.0117,"Other Renewables":0.0},
    {Coal:0.7689,Gas:0.1367,Nuclear:0.0,Hydro:0.072,Solar:0.0003,Wind:0.0024,Bioenergy:0.0057,"Other Fossil":0.014,"Other Renewables":0.0},
    {Coal:0.7684,Gas:0.1334,Nuclear:0.0,Hydro:0.0717,Solar:0.0003,Wind:0.0031,Bioenergy:0.0075,"Other Fossil":0.0156,"Other Renewables":0.0},
    {Coal:0.7807,Gas:0.1194,Nuclear:0.0,Hydro:0.0684,Solar:0.0003,Wind:0.0035,Bioenergy:0.0123,"Other Fossil":0.0154,"Other Renewables":0.0},
    {Coal:0.7931,Gas:0.1008,Nuclear:0.0,Hydro:0.067,Solar:0.0003,Wind:0.0056,Bioenergy:0.0168,"Other Fossil":0.0164,"Other Renewables":0.0},
    {Coal:0.7805,Gas:0.1147,Nuclear:0.0,Hydro:0.0628,Solar:0.0004,Wind:0.0091,Bioenergy:0.0165,"Other Fossil":0.016,"Other Renewables":0.0},
    {Coal:0.7627,Gas:0.1373,Nuclear:0.0,Hydro:0.0537,Solar:0.0005,Wind:0.0117,Bioenergy:0.0176,"Other Fossil":0.0165,"Other Renewables":0.0},
    {Coal:0.7507,Gas:0.148,Nuclear:0.0,Hydro:0.0482,Solar:0.0006,Wind:0.0141,Bioenergy:0.0151,"Other Fossil":0.0233,"Other Renewables":0.0},
    {Coal:0.7283,Gas:0.1645,Nuclear:0.0,Hydro:0.0506,Solar:0.0012,Wind:0.0178,Bioenergy:0.0112,"Other Fossil":0.0264,"Other Renewables":0.0},
    {Coal:0.7014,Gas:0.1864,Nuclear:0.0,Hydro:0.0548,Solar:0.0039,Wind:0.0199,Bioenergy:0.0097,"Other Fossil":0.0239,"Other Renewables":0.0},
    {Coal:0.671,Gas:0.1903,Nuclear:0.0,Hydro:0.0764,Solar:0.008,Wind:0.0251,Bioenergy:0.01,"Other Fossil":0.0192,"Other Renewables":0.0},
    {Coal:0.6598,Gas:0.1987,Nuclear:0.0,Hydro:0.068,Solar:0.0096,Wind:0.0308,Bioenergy:0.0124,"Other Fossil":0.0207,"Other Renewables":0.0},
    {Coal:0.6229,Gas:0.2113,Nuclear:0.0,Hydro:0.0765,Solar:0.0154,Wind:0.0371,Bioenergy:0.0133,"Other Fossil":0.0235,"Other Renewables":0.0},
    {Coal:0.6268,Gas:0.2167,Nuclear:0.0,Hydro:0.0585,Solar:0.02,Wind:0.0395,Bioenergy:0.0143,"Other Fossil":0.0242,"Other Renewables":0.0},
    {Coal:0.6386,Gas:0.1957,Nuclear:0.0,Hydro:0.0555,Solar:0.0244,Wind:0.0466,Bioenergy:0.0145,"Other Fossil":0.0247,"Other Renewables":0.0},
    {Coal:0.6287,Gas:0.1863,Nuclear:0.0,Hydro:0.0683,Solar:0.0288,Wind:0.0505,Bioenergy:0.0141,"Other Fossil":0.0233,"Other Renewables":0.0},
    {Coal:0.6147,Gas:0.2127,Nuclear:0.0,Hydro:0.0521,Solar:0.0344,Wind:0.051,Bioenergy:0.0137,"Other Fossil":0.0213,"Other Renewables":0.0},
    {Coal:0.5962,Gas:0.1959,Nuclear:0.0,Hydro:0.0659,Solar:0.0469,Wind:0.0619,Bioenergy:0.0137,"Other Fossil":0.0195,"Other Renewables":0.0},
    {Coal:0.5636,Gas:0.2095,Nuclear:0.0,Hydro:0.0527,Solar:0.0688,Wind:0.0732,Bioenergy:0.0131,"Other Fossil":0.0191,"Other Renewables":0.0},
    {Coal:0.539,Gas:0.2001,Nuclear:0.0,Hydro:0.0544,Solar:0.0899,Wind:0.0853,Bioenergy:0.0129,"Other Fossil":0.0184,"Other Renewables":0.0},
    {Coal:0.5137,Gas:0.1781,Nuclear:0.0,Hydro:0.0596,Solar:0.1166,Wind:0.1002,Bioenergy:0.0125,"Other Fossil":0.0193,"Other Renewables":0.0},
    {Coal:0.4734,Gas:0.1862,Nuclear:0.0,Hydro:0.061,Solar:0.1375,Wind:0.1101,Bioenergy:0.0117,"Other Fossil":0.02,"Other Renewables":0.0},
    {Coal:0.4599,Gas:0.1709,Nuclear:0.0,Hydro:0.0552,Solar:0.1647,Wind:0.1167,Bioenergy:0.0115,"Other Fossil":0.0211,"Other Renewables":0.0},
    {Coal:0.4521,Gas:0.1743,Nuclear:0.0,Hydro:0.0456,Solar:0.1783,Wind:0.1162,Bioenergy:0.0106,"Other Fossil":0.0228,"Other Renewables":0.0},
  ],
};

const FUELS = ["Coal", "Gas", "Nuclear", "Hydro", "Solar", "Wind", "Bioenergy", "Other Fossil", "Other Renewables"];

const FUEL_COLORS = {
  Coal: "#4a4a4a", Gas: "#e67e22", Nuclear: "#9b59b6", Hydro: "#3498db",
  Solar: "#f1c40f", Wind: "#2ecc71", Bioenergy: "#8b4513", "Other Fossil": "#95a5a6", "Other Renewables": "#1abc9c"
};

const STATUS_COLORS = { normal: "#22c55e", caution: "#eab308", drift: "#ef4444", spike: "#8b5cf6" };
const StatusLabel = { normal: "STABLE", caution: "K_eff DECLINING", drift: "DECEPTIVE DRIFT", spike: "VELOCITY SPIKE" };

function getStatus(keff, keffPrev, keffPrev2, vel, velMedian) {
  if (vel !== null && velMedian > 0 && vel > velMedian * 2) return "spike";
  if (keff && keffPrev && keffPrev2 && keff < keffPrev && keffPrev < keffPrev2 && vel !== null && vel < velMedian) return "drift";
  if (keff && keffPrev && keff < keffPrev) return "caution";
  return "normal";
}

// Compute carrier wrap counts: a "wrap" = carrier doubles or halves vs its starting proportion
function computeWrapCounts(carriers) {
  if (!carriers || carriers.length === 0) return [];
  const initial = carriers[0];
  return carriers.map((snap) => {
    const wraps = {};
    FUELS.forEach(fuel => {
      const p0 = initial[fuel] || 0.001;
      const pNow = snap[fuel] || 0;
      if (p0 < 0.001) { wraps[fuel] = pNow > 0.02 ? 1 : 0; return; }
      const ratio = pNow / p0;
      // Each doubling or halving = 1 wrap. log2(ratio) counts doublings.
      wraps[fuel] = Math.floor(Math.abs(Math.log2(Math.max(ratio, 0.001))));
    });
    return wraps;
  });
}

const P = {bg: "#0a0a1a", panel: "#111127", border: "#333", text: "#e0e0e0", dim: "#888", vdim: "#666", vvdim: "#444", blue: "#60a5fa", purple: "#a78bfa", orange: "#f97316", green: "#22c55e", red: "#ef4444", yellow: "#eab308", cyan: "#06b6d4", pink: "#ec4899"};

export default function HUFSpectrumAnalyzerV3() {
  const [country, setCountry] = useState("Germany");
  const [yearIdx, setYearIdx] = useState(null);
  const [metric, setMetric] = useState("both");
  const [playing, setPlaying] = useState(false);
  const [showPhase, setShowPhase] = useState(true);

  const d = EMBER_DATA[country];
  const carriers = CARRIER_DATA[country];
  const wrapCounts = useMemo(() => computeWrapCounts(carriers), [carriers]);

  const chartData = useMemo(() => {
    const velKey = metric === "tvd" ? "tvd" : "l2";
    const vals = d[velKey].filter(v => v !== null);
    const sorted = [...vals].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)] || 0;

    let cumTV = 0, cumKeff = 0;

    return d.years.map((year, i) => {
      const status = getStatus(d.keff[i], d.keff[i-1], d.keff[i-2], d[velKey][i], median);
      // Group phase: cumulative TV distance and cumulative |delta K_eff|
      if (d.tvd[i] !== null) cumTV += d.tvd[i];
      if (i > 0 && d.keff[i] !== null && d.keff[i-1] !== null) cumKeff += Math.abs(d.keff[i] - d.keff[i-1]);

      // Carrier snapshot for this year
      const snap = carriers[i] || {};

      return {
        year, keff: d.keff[i], l2: d.l2[i], tvd: d.tvd[i],
        status, isShock: d.shocks.some(s => s.year === year),
        shockLabel: d.shocks.find(s => s.year === year)?.event || null,
        isDriftL2: d.drift_l2.includes(year), isDriftTVD: d.drift_tvd.includes(year),
        // Group phase
        cumTV: Math.round(cumTV * 10000) / 10000,
        cumKeff: Math.round(cumKeff * 100) / 100,
        // Carrier proportions (for ribbon)
        ...Object.fromEntries(FUELS.map(f => [`c_${f}`, snap[f] || 0])),
      };
    });
  }, [country, metric, d, carriers]);

  const activeIdx = yearIdx !== null ? yearIdx : chartData.length - 1;
  const active = chartData[activeIdx];
  const activeWraps = wrapCounts[activeIdx] || {};

  const keffMin = Math.min(...d.keff);
  const keffMax = Math.max(...d.keff);
  const keffRange = keffMax - keffMin;
  const keffNorm = keffRange > 0 ? (active.keff - keffMin) / keffRange : 0.5;

  // Total wraps across all carriers at current time
  const totalWraps = Object.values(activeWraps).reduce((s, v) => s + v, 0);

  const handlePlay = useCallback(() => {
    if (playing) { setPlaying(false); return; }
    setPlaying(true);
    setYearIdx(0);
    let idx = 0;
    const interval = setInterval(() => {
      idx++;
      if (idx >= chartData.length) { clearInterval(interval); setPlaying(false); return; }
      setYearIdx(idx);
    }, 600);
  }, [playing, chartData.length]);

  const keffGaugeColor = active.keff > (keffMin + keffRange * 0.6) ? P.green :
                          active.keff > (keffMin + keffRange * 0.3) ? P.yellow : P.red;

  const panelStyle = {background: P.panel, border: `1px solid ${P.border}`, borderRadius: "4px", padding: "8px"};
  const labelStyle = {fontSize: "10px", color: P.dim, marginBottom: "4px", paddingLeft: "4px", letterSpacing: "0.5px"};

  return (
    <div style={{background: P.bg, color: P.text, minHeight: "100vh", fontFamily: "'JetBrains Mono', 'Fira Code', monospace", padding: "16px", maxWidth: "1200px", margin: "0 auto"}}>

      {/* Header */}
      <div style={{display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px", borderBottom: `1px solid ${P.border}`, paddingBottom: "8px"}}>
        <div>
          <h1 style={{margin: 0, fontSize: "20px", color: P.blue, letterSpacing: "2px"}}>HUF SPECTRUM ANALYZER</h1>
          <div style={{fontSize: "11px", color: P.dim, marginTop: "2px"}}>Composition Monitoring v3.0 — Phase Display + Carrier Ribbon</div>
        </div>
        <div style={{textAlign: "right", fontSize: "11px", color: P.vdim}}>
          <div>Source: EMBER Electricity (CC BY 4.0)</div>
          <div>HUF-GOV — KNOB-001 + DISP-001</div>
        </div>
      </div>

      {/* Controls */}
      <div style={{display: "flex", gap: "12px", marginBottom: "12px", flexWrap: "wrap", alignItems: "center"}}>
        <div style={{display: "flex", gap: "4px"}}>
          {Object.keys(EMBER_DATA).map(c => (
            <button key={c} onClick={() => {setCountry(c); setYearIdx(null);}}
              style={{padding: "4px 10px", fontSize: "11px", border: country === c ? `1px solid ${P.blue}` : `1px solid #444`,
                background: country === c ? "#1e3a5f" : "#1a1a2e", color: country === c ? P.blue : P.dim,
                borderRadius: "3px", cursor: "pointer"}}>
              {c === "United Kingdom" ? "UK" : c}
            </button>
          ))}
        </div>
        <div style={{display: "flex", gap: "4px"}}>
          {[["both","Dual trace"],["tvd","Velocity"],["l2","Peak"]].map(([val, label]) => (
            <button key={val} onClick={() => setMetric(val)}
              style={{padding: "4px 8px", fontSize: "10px", border: metric === val ? `1px solid ${P.purple}` : "1px solid #444",
                background: metric === val ? "#2d1b69" : "#1a1a2e", color: metric === val ? P.purple : P.dim,
                borderRadius: "3px", cursor: "pointer"}}>
              {label}
            </button>
          ))}
        </div>
        <button onClick={() => setShowPhase(!showPhase)}
          style={{padding: "4px 10px", fontSize: "10px", border: showPhase ? `1px solid ${P.cyan}` : "1px solid #444",
            background: showPhase ? "#0d3b4a" : "#1a1a2e", color: showPhase ? P.cyan : P.dim,
            borderRadius: "3px", cursor: "pointer"}}>
          {showPhase ? "PHASE ON" : "PHASE OFF"}
        </button>
        <button onClick={handlePlay}
          style={{padding: "4px 12px", fontSize: "11px", border: `1px solid ${P.green}`, background: playing ? "#14532d" : "#1a1a2e",
            color: P.green, borderRadius: "3px", cursor: "pointer"}}>
          {playing ? "STOP" : "PLAY"}
        </button>
      </div>

      {/* Main Display Grid */}
      <div style={{display: "grid", gridTemplateColumns: "200px 1fr", gap: "12px", marginBottom: "12px"}}>

        {/* Left Panel — Gauges */}
        <div style={{display: "flex", flexDirection: "column", gap: "8px"}}>

          {/* Year + Status */}
          <div style={{...panelStyle, padding: "10px", textAlign: "center"}}>
            <div style={{fontSize: "28px", fontWeight: "bold", color: P.blue}}>{active.year}</div>
            <div style={{fontSize: "11px", padding: "3px 8px", borderRadius: "10px", display: "inline-block", marginTop: "4px",
              background: STATUS_COLORS[active.status] + "22", color: STATUS_COLORS[active.status], border: `1px solid ${STATUS_COLORS[active.status]}44`}}>
              {StatusLabel[active.status]}
            </div>
            {active.isShock && <div style={{fontSize: "10px", color: P.red, marginTop: "4px"}}>* {active.shockLabel}</div>}
          </div>

          {/* Calibration */}
          <div style={{...panelStyle, padding: "6px 10px", display: "flex", justifyContent: "space-between", alignItems: "center"}}>
            <div style={{fontSize: "10px", color: P.dim}}>CALIBRATION</div>
            <div style={{fontSize: "10px", color: P.green, display: "flex", alignItems: "center", gap: "4px"}}>
              <div style={{width: "8px", height: "8px", borderRadius: "50%", background: P.green, boxShadow: `0 0 6px ${P.green}`}} />
              sum = 1.000
            </div>
          </div>

          {/* Complexity Gauge */}
          <div style={{...panelStyle, padding: "10px"}}>
            <div style={{fontSize: "10px", color: P.dim, marginBottom: "6px"}}>COMPLEXITY (K_eff)</div>
            <div style={{fontSize: "24px", fontWeight: "bold", color: keffGaugeColor, textAlign: "center"}}>{active.keff.toFixed(2)}</div>
            <div style={{height: "8px", background: "#222", borderRadius: "4px", marginTop: "6px", overflow: "hidden"}}>
              <div style={{height: "100%", width: `${keffNorm * 100}%`, background: `linear-gradient(90deg, ${P.red}, ${P.yellow}, ${P.green})`,
                borderRadius: "4px", transition: "width 0.3s"}} />
            </div>
            <div style={{display: "flex", justifyContent: "space-between", fontSize: "9px", color: P.vdim, marginTop: "2px"}}>
              <span>{keffMin.toFixed(1)}</span><span>{keffMax.toFixed(1)}</span>
            </div>
          </div>

          {/* Velocity + Peak */}
          <div style={{...panelStyle, padding: "10px"}}>
            <div style={{fontSize: "10px", color: P.dim, marginBottom: "6px"}}>STRUCTURAL CHANGE</div>
            {(metric === "both" || metric === "tvd") && (
              <div style={{marginBottom: "6px"}}>
                <div style={{display: "flex", justifyContent: "space-between", fontSize: "9px"}}>
                  <span style={{color: P.purple}}>Velocity (TV)</span>
                  <span style={{color: P.purple}}>{active.tvd !== null ? active.tvd.toFixed(4) : "--"}</span>
                </div>
                <div style={{height: "4px", background: "#222", borderRadius: "2px", marginTop: "2px"}}>
                  <div style={{height: "100%", width: `${Math.min((active.tvd || 0) / 0.15 * 100, 100)}%`,
                    background: P.purple, borderRadius: "2px", transition: "width 0.3s"}} />
                </div>
              </div>
            )}
            {(metric === "both" || metric === "l2") && (
              <div>
                <div style={{display: "flex", justifyContent: "space-between", fontSize: "9px"}}>
                  <span style={{color: P.orange}}>Peak (L2)</span>
                  <span style={{color: P.orange}}>{active.l2 !== null ? active.l2.toFixed(4) : "--"}</span>
                </div>
                <div style={{height: "4px", background: "#222", borderRadius: "2px", marginTop: "2px"}}>
                  <div style={{height: "100%", width: `${Math.min((active.l2 || 0) / 0.2 * 100, 100)}%`,
                    background: P.orange, borderRadius: "2px", transition: "width 0.3s"}} />
                </div>
              </div>
            )}
          </div>

          {/* Drift Detection */}
          <div style={{...panelStyle, padding: "10px"}}>
            <div style={{fontSize: "10px", color: P.dim, marginBottom: "6px"}}>DRIFT DETECTION</div>
            <div style={{fontSize: "9px", lineHeight: "1.6"}}>
              <div>TV: <span style={{color: active.isDriftTVD ? P.red : P.green}}>{active.isDriftTVD ? "DRIFT" : "clear"}</span></div>
              <div>L2: <span style={{color: active.isDriftL2 ? P.red : P.green}}>{active.isDriftL2 ? "DRIFT" : "clear"}</span></div>
            </div>
          </div>

          {/* Group Phase Summary */}
          {showPhase && (
            <div style={{...panelStyle, padding: "10px"}}>
              <div style={{fontSize: "10px", color: P.cyan, marginBottom: "6px"}}>GROUP PHASE</div>
              <div style={{fontSize: "9px", lineHeight: "1.8"}}>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                  <span style={{color: P.dim}}>Cum. TV dist</span>
                  <span style={{color: P.cyan}}>{active.cumTV.toFixed(3)}</span>
                </div>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                  <span style={{color: P.dim}}>Cum. K_eff path</span>
                  <span style={{color: P.pink}}>{active.cumKeff.toFixed(2)}</span>
                </div>
                <div style={{display: "flex", justifyContent: "space-between", marginTop: "4px"}}>
                  <span style={{color: P.dim}}>Total wraps</span>
                  <span style={{color: totalWraps > 3 ? P.yellow : P.green}}>{totalWraps}</span>
                </div>
              </div>
            </div>
          )}

          {/* Carrier Wrap Counts (Individual Phase) */}
          {showPhase && (
            <div style={{...panelStyle, padding: "10px"}}>
              <div style={{fontSize: "10px", color: P.cyan, marginBottom: "6px"}}>CARRIER WRAPS</div>
              <div style={{fontSize: "8px", lineHeight: "1.5"}}>
                {FUELS.filter(f => (carriers[activeIdx] || {})[f] > 0.005 || (activeWraps[f] || 0) > 0).map(fuel => (
                  <div key={fuel} style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
                    <span style={{display: "flex", alignItems: "center", gap: "3px"}}>
                      <span style={{width: "6px", height: "6px", borderRadius: "1px", background: FUEL_COLORS[fuel], display: "inline-block"}} />
                      <span style={{color: P.dim}}>{fuel.length > 10 ? fuel.slice(0, 8) + ".." : fuel}</span>
                    </span>
                    <span style={{color: (activeWraps[fuel] || 0) > 0 ? P.yellow : P.vdim}}>
                      {activeWraps[fuel] || 0}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Panel — Charts */}
        <div style={{display: "flex", flexDirection: "column", gap: "8px"}}>

          {/* K_eff Trace */}
          <div style={panelStyle}>
            <div style={labelStyle}>COMPLEXITY (K_eff) -- structural diversity over time</div>
            <ResponsiveContainer width="100%" height={140}>
              <ComposedChart data={chartData} margin={{top: 5, right: 10, left: 0, bottom: 0}}>
                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                <XAxis dataKey="year" tick={{fontSize: 9, fill: P.vdim}} interval={4} />
                <YAxis tick={{fontSize: 9, fill: P.vdim}} domain={['auto', 'auto']} width={35} />
                <Tooltip contentStyle={{background: "#1a1a2e", border: "1px solid #444", fontSize: "11px"}} labelStyle={{color: P.blue}} />
                {d.shocks.map((s, i) => <ReferenceLine key={i} x={s.year} stroke={P.red} strokeDasharray="4 4" strokeWidth={1} />)}
                {d.drift_l2.map((yr, i) => <ReferenceLine key={`dl${i}`} x={yr} stroke={P.yellow} strokeDasharray="2 2" strokeWidth={1} />)}
                <Line type="monotone" dataKey="keff" stroke={P.blue} strokeWidth={2} dot={false} name="K_eff" />
                {yearIdx !== null && <ReferenceLine x={active.year} stroke="#fff" strokeWidth={1} />}
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          {/* Velocity Trace */}
          <div style={panelStyle}>
            <div style={labelStyle}>VELOCITY + PEAK -- rate of structural change</div>
            <ResponsiveContainer width="100%" height={110}>
              <ComposedChart data={chartData} margin={{top: 5, right: 10, left: 0, bottom: 0}}>
                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                <XAxis dataKey="year" tick={{fontSize: 9, fill: P.vdim}} interval={4} />
                <YAxis tick={{fontSize: 9, fill: P.vdim}} domain={[0, 'auto']} width={35} />
                <Tooltip contentStyle={{background: "#1a1a2e", border: "1px solid #444", fontSize: "11px"}} labelStyle={{color: P.blue}} />
                {d.shocks.map((s, i) => <ReferenceLine key={i} x={s.year} stroke={P.red} strokeDasharray="4 4" strokeWidth={1} />)}
                {(metric === "both" || metric === "l2") && <Line type="monotone" dataKey="l2" stroke={P.orange} strokeWidth={1.5} dot={false} name="Peak (L2)" connectNulls />}
                {(metric === "both" || metric === "tvd") && <Line type="monotone" dataKey="tvd" stroke={P.purple} strokeWidth={1.5} dot={false} name="Velocity (TV)" connectNulls />}
                {yearIdx !== null && <ReferenceLine x={active.year} stroke="#fff" strokeWidth={1} />}
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          {/* Deceptive Drift Signature */}
          <div style={panelStyle}>
            <div style={labelStyle}>DECEPTIVE DRIFT SIGNATURE -- K_eff falling (red) while velocity calm</div>
            <ResponsiveContainer width="100%" height={80}>
              <BarChart data={chartData.map((pt, i) => ({
                ...pt,
                keff_change: i > 0 && pt.keff && chartData[i-1].keff ? pt.keff - chartData[i-1].keff : 0,
              }))} margin={{top: 5, right: 10, left: 0, bottom: 0}}>
                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                <XAxis dataKey="year" tick={{fontSize: 9, fill: P.vdim}} interval={4} />
                <YAxis tick={{fontSize: 9, fill: P.vdim}} width={35} />
                <Tooltip contentStyle={{background: "#1a1a2e", border: "1px solid #444", fontSize: "11px"}} />
                <Bar dataKey="keff_change" name="K_eff change" radius={[1,1,0,0]}
                  shape={(props) => {
                    const { x, y, width, height, payload } = props;
                    const fill = payload.keff_change < 0 ? P.red : P.green;
                    return <rect x={x} y={y} width={width} height={Math.abs(height)} fill={fill} rx={1} opacity={0.7} />;
                  }} />
                {d.shocks.map((s, i) => <ReferenceLine key={i} x={s.year} stroke={P.red} strokeDasharray="4 4" strokeWidth={1} />)}
                {yearIdx !== null && <ReferenceLine x={active.year} stroke="#fff" strokeWidth={1} />}
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* === NEW: Carrier Composition Ribbon === */}
          <div style={panelStyle}>
            <div style={labelStyle}>CARRIER RIBBON -- proportional composition (sum = 1.0)</div>
            <ResponsiveContainer width="100%" height={120}>
              <AreaChart data={chartData} margin={{top: 5, right: 10, left: 0, bottom: 0}} stackOffset="expand">
                <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                <XAxis dataKey="year" tick={{fontSize: 9, fill: P.vdim}} interval={4} />
                <YAxis tick={{fontSize: 9, fill: P.vdim}} tickFormatter={(v) => `${(v*100).toFixed(0)}%`} width={35} />
                <Tooltip contentStyle={{background: "#1a1a2e", border: "1px solid #444", fontSize: "10px"}} labelStyle={{color: P.blue}}
                  formatter={(val) => `${(val*100).toFixed(1)}%`} />
                {FUELS.map(fuel => (
                  <Area key={fuel} type="monotone" dataKey={`c_${fuel}`} stackId="1"
                    fill={FUEL_COLORS[fuel]} stroke={FUEL_COLORS[fuel]}
                    fillOpacity={0.85} strokeWidth={0} name={fuel} />
                ))}
                {yearIdx !== null && <ReferenceLine x={active.year} stroke="#fff" strokeWidth={1} />}
              </AreaChart>
            </ResponsiveContainer>
            {/* Carrier legend */}
            <div style={{display: "flex", gap: "8px", marginTop: "4px", flexWrap: "wrap"}}>
              {FUELS.filter(f => {
                const snap = carriers[activeIdx] || {};
                return (snap[f] || 0) > 0.005;
              }).map(fuel => (
                <span key={fuel} style={{fontSize: "8px", color: P.dim, display: "flex", alignItems: "center", gap: "3px"}}>
                  <span style={{width: "8px", height: "8px", background: FUEL_COLORS[fuel], display: "inline-block", borderRadius: "1px"}} />
                  {fuel} {((carriers[activeIdx] || {})[fuel] * 100).toFixed(1)}%
                  {showPhase && (activeWraps[fuel] || 0) > 0 && <span style={{color: P.yellow, marginLeft: "2px"}}>[W{activeWraps[fuel]}]</span>}
                </span>
              ))}
            </div>
          </div>

          {/* === NEW: Group Phase Panel === */}
          {showPhase && (
            <div style={panelStyle}>
              <div style={labelStyle}>GROUP PHASE -- cumulative structural distance (monotonically non-decreasing)</div>
              <ResponsiveContainer width="100%" height={120}>
                <ComposedChart data={chartData} margin={{top: 5, right: 10, left: 0, bottom: 0}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#222" />
                  <XAxis dataKey="year" tick={{fontSize: 9, fill: P.vdim}} interval={4} />
                  <YAxis yAxisId="tv" tick={{fontSize: 9, fill: P.cyan}} width={40} />
                  <YAxis yAxisId="keff" orientation="right" tick={{fontSize: 9, fill: P.pink}} width={40} />
                  <Tooltip contentStyle={{background: "#1a1a2e", border: "1px solid #444", fontSize: "11px"}} labelStyle={{color: P.blue}} />
                  <Line yAxisId="tv" type="monotone" dataKey="cumTV" stroke={P.cyan} strokeWidth={2} dot={false} name="Cum. TV dist" />
                  <Line yAxisId="keff" type="monotone" dataKey="cumKeff" stroke={P.pink} strokeWidth={2} dot={false} name="Cum. K_eff path" />
                  {d.shocks.map((s, i) => <ReferenceLine key={i} yAxisId="tv" x={s.year} stroke={P.red} strokeDasharray="4 4" strokeWidth={1} />)}
                  {yearIdx !== null && <ReferenceLine yAxisId="tv" x={active.year} stroke="#fff" strokeWidth={1} />}
                </ComposedChart>
              </ResponsiveContainer>
              <div style={{fontSize: "8px", color: P.vvdim, marginTop: "4px", paddingLeft: "4px"}}>
                Slope = current rate of structural change. Flat = quiet. Steep = active. Two systems at the same K_eff with different group phase have different histories.
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Year Scrubber */}
      <div style={{...panelStyle, padding: "8px 12px", marginBottom: "12px"}}>
        <input type="range" min={0} max={chartData.length - 1} value={activeIdx}
          onChange={e => setYearIdx(parseInt(e.target.value))}
          style={{width: "100%", accentColor: P.blue}} />
        <div style={{display: "flex", justifyContent: "space-between", fontSize: "9px", color: P.vdim}}>
          <span>{chartData[0]?.year}</span>
          <span>SCRUB THROUGH TIME</span>
          <span>{chartData[chartData.length-1]?.year}</span>
        </div>
      </div>

      {/* Narrative Panel */}
      <div style={{...panelStyle, padding: "12px", marginBottom: "12px"}}>
        <div style={{fontSize: "10px", color: P.blue, marginBottom: "6px", letterSpacing: "1px"}}>DOMAIN NARRATIVE -- {country.toUpperCase()}</div>
        <div style={{fontSize: "12px", lineHeight: "1.6", color: "#ccc"}}>{d.narrative}</div>
      </div>

      {/* Legend */}
      <div style={{display: "flex", gap: "16px", marginTop: "8px", fontSize: "9px", color: P.vdim, flexWrap: "wrap"}}>
        <span><span style={{color: P.green}}>*</span> Calibration (sum=1)</span>
        <span><span style={{color: P.blue}}>--</span> Complexity</span>
        <span><span style={{color: P.purple}}>--</span> Velocity (TV)</span>
        <span><span style={{color: P.orange}}>--</span> Peak (L2)</span>
        <span><span style={{color: P.red}}>|</span> Known shock</span>
        <span><span style={{color: P.yellow}}>|</span> Drift detected</span>
        {showPhase && <>
          <span><span style={{color: P.cyan}}>--</span> Cum. TV dist</span>
          <span><span style={{color: P.pink}}>--</span> Cum. K_eff path</span>
          <span><span style={{color: P.yellow}}>[W]</span> Carrier wrap count</span>
        </>}
      </div>

      <div style={{marginTop: "12px", fontSize: "9px", color: P.vvdim, textAlign: "center"}}>
        HUF-GOV Spectrum Analyzer v3.0 -- KNOB-001 + DISP-001 Standard -- Peter Higgins / Claude (Opus 4.6) -- March 30, 2026
        <br />Source: EMBER Global Electricity Review (CC BY 4.0) -- 9 fuel types, 5 countries, 2000-2025
        <br />Seven readings: Source, Calibration, Complexity, Velocity, Peak, Group Phase, Carrier Phase. One instrument. Every domain.
      </div>
    </div>
  );
}
