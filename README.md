# Resilient Routing: Disaster-Proof Hospital Access System

| Name | NRP | Class |
| ---  | --- | --- |
| Bismantaka Revano Dirgantara | 5025241075 | IUP |
| Naufal Bintang Brillian | 5025241168 | IUP |
| Stephanie Gabriella Adiseputra | 5025241081 | IUP |

This document explains the Python implementation of a Decision Support System that models a city road network as a graph. It utilizes Dijkstra and BFS to calculate evacuation routes to the nearest hospital.
Unlike static railway maps, this system is dynamic: it simulates real-time disaster updates (Floods/Landslides) that alter travel times or block roads entirely.

**1. Dataset Overview**
<br>

**1.1 Hospital List (nodes / hospitals)**
All algorithms (Dijkstra, BFS) use the same 25 major hospitals in Surabaya (they are abbreaviated in order to simplify):
```
nodes = [
    "DST", "SIL", "MYP", "PRS", "NHS",
    "BHY", "UNA", "HSU", "RSL", "MRN",
    "AUS", "RKZ", "BDH", "ONK", "ADH",
    "MTK", "RYL", "JMR", "ALR", "PHC",
    "SMS", "SBI", "GTR", "WYS", "SEM"
]
```

<br>

**Hospital Code Explanation**

Below is the full meaning of each code, sorted descending by quality (from highest-tier to lower-tier hospitals). We sorted these because this ordering is ideal for routing priority in disaster scenarios.


**Top-Tier Hospitals**

These hospitals have the highest capacity, strongest emergency departments, and the most complete medical services.

- **DST - Dr. Soetomo General Hospital (RSUD Dr. Soetomo)** <br>
National referral hospital; the largest and most complete medical center in East Java.
- **SIL - Siloam Hospitals Surabaya** <br>
Premium private hospital with strong emergency care and modern facilities.
- **MYP - Mayapada Hospital Surabaya** <br>
High-end private hospital known for advanced diagnostics and comprehensive services.
- **PRS - Premier Surabaya Hospital** <br>
Excellent for cardiac care, surgery, ICU, trauma services, and emergency response.
- **NHS - National Hospital Surabaya** <br>
Modern mid-to-upper class general hospital with high-tech facilities and 24/7 ER.


**Upper-Tier Hospitals**

High-quality hospitals with strong general services, specialty clinics, and emergency capabilities.

- **BHY - Bhayangkara Hospital Surabaya** <br>
Police-operated hospital; strong trauma and emergency handling.
- **UNA - Airlangga University Hospital (RS UNAIR)** <br>
Teaching hospital with a wide range of specialty services.
- **HSU - Husada Utama Hospital** <br>
Well-known for full diagnostic facilities (MRI, CT, advanced labs).
- **RSL - Naval Hospital Dr. Ramelan** <br>
Major military hospital with extensive medical capabilities.
- **MRN - Marine Corps Hospital Gunungsari** <br>
Military hospital providing general and emergency services.
- **AUS - Air Force Hospital dr. Soemitro** <br>
Air Force medical facility with standard trauma services.
- **RKZ - St. Vincentius a Paulo Catholic Hospital (RKZ)** <br>
Long-standing nonprofit hospital with comprehensive care.
- **BDH - Bhakti Dharma Husada Hospital** <br>
Municipal hospital with full general services and 24/7 ER.
- **ONK - Surabaya Oncology Hospital** <br>
Specialized cancer center; top-tier for oncology but not a general hospital.



Middle-Tier Hospitals

Reliable general hospitals with decent facilities but not at the premium tier.

ADH – Adi Husada Undaan Hospital
Long-established private general hospital with solid service standards.

MTK – Mitra Keluarga Surabaya Hospital
Well-known family hospital chain with stable service quality.

RYL – Royal Hospital Surabaya
General hospital with regular specialty services.

JMR – Jemursari Islamic Hospital
Popular mid-tier general hospital.

ALR – Al-Irsyad Hospital Surabaya
Islamic hospital with adequate general facilities.

PHC – PHC Hospital Surabaya
Corporate-managed hospital with 24/7 emergency services.



Lower Middle-Tier Hospitals

Hospitals that are operational but not in the premium or upper tiers.

SMS – Surabaya Medical Service Hospital
Mid-range private general hospital.

SBI – Surabaya International Hospital
General hospital with moderate service quality.

GTR – Gotong Royong Hospital
Mid-tier hospital with basic general service.

WYS – Wiyung Sejahtera Hospital
Standard regional general hospital.

SEM – Sejahtera Medical Hospital
Lower-tier general hospital; lowest benchmark in the dataset.
