# Volume I: The Infrastructure of Borrowed Legitimacy
## *Direct versus Indirect Rule, Customary Courts, and the Divergent Bureaucratic Legacies of Colonial Empires*

**Author:** Gia Bao Huynh (Independent Researcher, Ho Chi Minh City, Vietnam)  
**ORCID:** [0009-0008-2372-5852](https://orcid.org/0009-0008-2372-5852)  
**Series:** *Institutional Endurance: Site, Template, and the Structures That Outlast Their Builders* (Volume I)  
**Target Publisher:** Yale University Press  

---

### Abstract
How do institutions survive the departure of their creators? This volume explores the foundational divergence between direct and indirect colonial governance, investigating why bureaucratic capacity varies so drastically across postcolonial states. Replicating and extending Matthew Lange's pioneering work across both an initial hand-coded pilot ($N=18$) and a full sample of former British colonies ($N=33$), we demonstrate a powerful, robust negative correlation ($r = -0.83, R^2 = 0.69$) between colonial reliance on customary courts (indirect rule) and postcolonial bureaucratic effectiveness. Where colonizers built uniform, state-centered legal hierarchies (Mauritius, Barbados, Singapore), they bequeathed impersonal administrative machinery that endured. Where colonizers preserved and manipulated traditional chiefdoms and customary tribunals (Northern Nigeria, Sierra Leone, Uganda), they institutionalized bifurcated despotisms that crippled postcolonial state capacity. Furthermore, we contextualize this finding through comparative historical analysis of imperial longevity in East Asia, explicitly noting that while direct Tang administrative commanderies in Vietnam formally concluded in 938 CE, the civilizational, tributary, and bureaucratic models they introduced endured for centuries under autonomous Vietnamese dynasties.

---

## 1. Introduction: The Direct vs. Indirect Rule Dilemma

The modern state is rarely an indigenous invention; in most of the world, it is an inherited institutional artifact. Colonial powers confronted a structural dilemma upon conquering alien territories: should they govern directly through metropolitan civil servants and uniform statutory courts, or should they govern indirectly by co-opting pre-existing traditional rulers, native courts, and customary law?

As Michael Hechter (*Alien Rule*, 2013) observes, indirect rule was primarily a cost-minimization strategy driven by high metropolitan monitoring costs. Where British administrators lacked the manpower or revenue to project direct bureaucratic authority across expansive rural populations (most notably in Sub-Saharan Africa), they instituted Lugardian indirect rule. By contrast, in small island colonies or strategic commercial entrepôts (Barbados, Mauritius, Hong Kong, Singapore), the British deployed direct bureaucratic administrations.

---

## 2. Statistical Analysis: Pilot ($N=18$) vs. Full Lange Sample ($N=33$)

To test the institutional endurance of these two administrative templates, we evaluate the relationship between the colonial indirect rule index (measured as the percentage of total colonial legal cases adjudicated in recognized customary tribunals circa the 1950s) and modern postcolonial bureaucratic effectiveness.

### Comparative Regression Results

| Metric | Pilot Sample ($N=18$) | Full Reconstructed Lange Sample ($N=33$) | Robustness Verdict |
| :--- | :---: | :---: | :--- |
| **Linear Model** | $\text{Bureaucracy} = 7.16 - 0.0638 \cdot \text{IndirectPct}$ | $\text{Bureaucracy} = 6.69 - 0.0450 \cdot \text{CustomaryCourtPct}$ | Negative slope holds across both samples |
| **Correlation Coefficient ($r$)** | $\mathbf{-0.9509}$ | $\mathbf{-0.8293}$ | Strong, statistically significant negative relationship |
| **Coefficient of Determination ($R^2$)** | $\mathbf{0.9042}$ | $\mathbf{0.6877}$ | Customary court reliance explains $68.8\%$ of postcolonial variance |

### Key Analytical Insights:
1. **The Customary Court Trap:** In indirect rule colonies, British authorities ossified fluid local traditions into rigid legal monopolies, empowering local chiefs with unconstrained judicial power. Post-independence central states inherited fragmented, ethnically bifurcated legal orders that resisted central rationalization.
2. **The Exceptionalism of Botswana:** Within the indirect rule cohort, Botswana represents a celebrated positive outlier ($\text{score } 6.2$). As Lange (2009) notes, pre-colonial Tswana states possessed strong consultative assemblies (*kgotla*) that constrained chiefdom despotism, preserving institutional accountability through decolonization.
3. **Quality of Government (QoG) Dataset Audit:** An inspection of the University of Gothenburg's Quality of Government Standard Dataset confirms that while QoG provides broad colonial dummies (`ht_colonial`, `col_brit`, `lp_legor`), it lacks an intra-colonial customary court ratio, highlighting the unique value of Lange's granular legal archival metric.

---

## 3. Imperial Endurance in Comparative Perspective: The Tang-Vietnam Substrate

To demonstrate that borrowed legitimacy is not merely a modern European phenomenon, we examine the deepest historical instances of imperial administrative transfer:

* **Tang Dynasty Protectorate-General to Pacify the South (Annam, 679–938 CE):** For 259 years, Tang imperial rule in Northern Vietnam governed through a hybrid system of Han-Tang commanderies and co-opted indigenous Lac lords.
* **The 938 CE Transition and Structural Caveat:** The decisive defeat of the Southern Han fleet at the Battle of Bạch Đằng in 938 CE under Ngô Quyền ended formal direct Chinese commandery administration. **Crucially, however, as emphasized throughout this series, 938 CE was not a complete civilizational rupture.** Subsequent independent Vietnamese dynasties (Đinh, Tiền Lê, Lý, Trần, Lê, and Nguyễn) systematically retained, adapted, and expanded the Sinitic bureaucratic examination system, Confucian legal codes (such as the Lê Dynasty *Quốc Triều Hình Luật*), and tributary diplomatic architecture for nearly a millennium. The administrative template outlasted the physical presence of the empire that built it.

---

## 4. References & Data Availability
All replication datasets (`pilot_n18_colonial_governance.csv`, `lange_n33_customary_courts_replication.csv`) and Python analysis scripts (`volume1_analysis.py`) are fully open-source and maintained in `volume1_repo/`.
